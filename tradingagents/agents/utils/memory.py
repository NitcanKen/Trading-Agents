import chromadb
from chromadb.config import Settings
from openai import OpenAI
import numpy as np
import logging
import os
import tempfile
import shutil
import atexit
import gc


# Global list to track temp directories for cleanup at exit
_temp_dirs_to_cleanup = []

def _cleanup_at_exit():
    """Cleanup function to run at program exit"""
    for temp_dir in _temp_dirs_to_cleanup:
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass  # Ignore cleanup errors at exit

# Register the cleanup function
atexit.register(_cleanup_at_exit)


class FinancialSituationMemory:
    def __init__(self, name):
        self.client = OpenAI()
        self.collection_name = name
        self.chroma_client = None
        self.situation_collection = None
        self.temp_dir = None
        self._use_in_memory = True  # Try in-memory first
        self._initialize_chroma()

    def _initialize_chroma(self):
        """Initialize or reinitialize ChromaDB client and collection"""
        try:
            if self._use_in_memory:
                # Try in-memory first (fastest and no cleanup needed)
                settings = Settings(
                    allow_reset=True,
                    is_persistent=False
                )
                self.chroma_client = chromadb.Client(settings)
            else:
                # Fall back to temporary directory
                if self.temp_dir is None:
                    self.temp_dir = tempfile.mkdtemp(prefix=f"chroma_{self.collection_name}_")
                    _temp_dirs_to_cleanup.append(self.temp_dir)
                
                settings = Settings(
                    allow_reset=True,
                    persist_directory=self.temp_dir,
                    is_persistent=True
                )
                self.chroma_client = chromadb.Client(settings)
            
            # Try to get existing collection or create new one
            try:
                self.situation_collection = self.chroma_client.get_collection(name=self.collection_name)
            except Exception:
                # Collection doesn't exist, create it
                self.situation_collection = self.chroma_client.create_collection(name=self.collection_name)
                
        except Exception as e:
            logging.warning(f"ChromaDB initialization warning for {self.collection_name}: {e}")
            # If in-memory failed, try persistent storage
            if self._use_in_memory:
                self._use_in_memory = False
                self._initialize_chroma()
            else:
                # Last resort: try to reset and recreate
                try:
                    self._cleanup_temp_dir()
                    self._initialize_chroma()
                except Exception as reset_error:
                    logging.error(f"Failed to reset ChromaDB for {self.collection_name}: {reset_error}")
                    raise reset_error

    def _cleanup_temp_dir(self):
        """Clean up temporary directory with Windows-friendly approach"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                # Force garbage collection to release any file handles
                gc.collect()
                
                # Try immediate cleanup
                shutil.rmtree(self.temp_dir)
                if self.temp_dir in _temp_dirs_to_cleanup:
                    _temp_dirs_to_cleanup.remove(self.temp_dir)
                self.temp_dir = None
            except Exception as e:
                # On Windows, files might be locked, so we'll leave it for exit cleanup
                logging.warning(f"Delayed cleanup scheduled for temp directory: {self.temp_dir}")

    def reset(self):
        """Reset the ChromaDB client and collection"""
        try:
            # Close existing client if it exists
            if self.chroma_client:
                try:
                    self.chroma_client.reset()
                except:
                    pass  # Continue with cleanup even if reset fails
            
            # Force garbage collection to release file handles
            gc.collect()
            
            # Clean up temporary directory if using persistent storage
            if not self._use_in_memory:
                self._cleanup_temp_dir()
            
            # Clear references
            self.chroma_client = None
            self.situation_collection = None
            
            # Reset to try in-memory first
            self._use_in_memory = True
            
            # Reinitialize everything
            self._initialize_chroma()
            
        except Exception as e:
            logging.warning(f"Error during reset of {self.collection_name}: {e}")
            # Force complete reinitialization
            if not self._use_in_memory:
                self._cleanup_temp_dir()
            self.chroma_client = None
            self.situation_collection = None
            self._use_in_memory = True
            self._initialize_chroma()

    def __del__(self):
        """Cleanup when object is destroyed"""
        if not self._use_in_memory:
            self._cleanup_temp_dir()

    def get_embedding(self, text):
        """Get OpenAI embedding for a text"""
        response = self.client.embeddings.create(
            model="text-embedding-ada-002", input=text
        )
        return response.data[0].embedding

    def add_situations(self, situations_and_advice):
        """Add financial situations and their corresponding advice. Parameter is a list of tuples (situation, rec)"""
        if not self.situation_collection:
            self._initialize_chroma()

        situations = []
        advice = []
        ids = []
        embeddings = []

        offset = self.situation_collection.count()

        for i, (situation, recommendation) in enumerate(situations_and_advice):
            situations.append(situation)
            advice.append(recommendation)
            ids.append(str(offset + i))
            embeddings.append(self.get_embedding(situation))

        self.situation_collection.add(
            documents=situations,
            metadatas=[{"recommendation": rec} for rec in advice],
            embeddings=embeddings,
            ids=ids,
        )

    def get_memories(self, current_situation, n_matches=1):
        """Find matching recommendations using OpenAI embeddings"""
        if not self.situation_collection:
            self._initialize_chroma()
            
        query_embedding = self.get_embedding(current_situation)

        results = self.situation_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_matches,
            include=["metadatas", "documents", "distances"],
        )

        matched_results = []
        for i in range(len(results["documents"][0])):
            matched_results.append(
                {
                    "matched_situation": results["documents"][0][i],
                    "recommendation": results["metadatas"][0][i]["recommendation"],
                    "similarity_score": 1 - results["distances"][0][i],
                }
            )

        return matched_results


# Global cleanup function for cleaning up persistent ChromaDB files
def cleanup_persistent_chromadb():
    """Clean up any persistent ChromaDB files in the project directory"""
    try:
        # Force garbage collection first
        gc.collect()
        
        chroma_db_path = os.path.join(os.getcwd(), "chroma_db")
        if os.path.exists(chroma_db_path):
            try:
                shutil.rmtree(chroma_db_path)
                print(f"✅ Cleaned up persistent ChromaDB directory: {chroma_db_path}")
            except Exception as e:
                print(f"⚠️  ChromaDB directory cleanup scheduled for later: {chroma_db_path}")
        
        # Also clean up any .chroma files in current directory
        cleaned_files = []
        for file in os.listdir(os.getcwd()):
            if file.endswith('.sqlite3') and 'chroma' in file.lower():
                try:
                    os.remove(file)
                    cleaned_files.append(file)
                except:
                    pass
        
        if cleaned_files:
            print(f"✅ Cleaned up ChromaDB files: {', '.join(cleaned_files)}")
                    
    except Exception as e:
        logging.warning(f"Failed to cleanup persistent ChromaDB files: {e}")


if __name__ == "__main__":
    # Example usage
    matcher = FinancialSituationMemory("test_memory")

    # Example data
    example_data = [
        (
            "High inflation rate with rising interest rates and declining consumer spending",
            "Consider defensive sectors like consumer staples and utilities. Review fixed-income portfolio duration.",
        ),
        (
            "Tech sector showing high volatility with increasing institutional selling pressure",
            "Reduce exposure to high-growth tech stocks. Look for value opportunities in established tech companies with strong cash flows.",
        ),
        (
            "Strong dollar affecting emerging markets with increasing forex volatility",
            "Hedge currency exposure in international positions. Consider reducing allocation to emerging market debt.",
        ),
        (
            "Market showing signs of sector rotation with rising yields",
            "Rebalance portfolio to maintain target allocations. Consider increasing exposure to sectors benefiting from higher rates.",
        ),
    ]

    # Add the example situations and recommendations
    matcher.add_situations(example_data)

    # Example query
    current_situation = """
    Market showing increased volatility in tech sector, with institutional investors 
    reducing positions and rising interest rates affecting growth stock valuations
    """

    try:
        recommendations = matcher.get_memories(current_situation, n_matches=2)

        for i, rec in enumerate(recommendations, 1):
            print(f"\nMatch {i}:")
            print(f"Similarity Score: {rec['similarity_score']:.2f}")
            print(f"Matched Situation: {rec['matched_situation']}")
            print(f"Recommendation: {rec['recommendation']}")

    except Exception as e:
        print(f"Error during recommendation: {str(e)}")
