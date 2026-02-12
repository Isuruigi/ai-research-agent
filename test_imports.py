"""Simple test to verify imports work"""
import sys
print("Python version:", sys.version)
print("Testing imports...")

try:
    from langchain_core.documents import Document
    print("✓ langchain_core.documents")
except Exception as e:
    print(f"✗ langchain_core.documents: {e}")

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    print("✓ langchain_text_splitters")
except Exception as e:
    print(f"✗ langchain_text_splitters: {e}")

try:
    from langchain_huggingface import HuggingFaceEmbeddings
    print("✓ langchain_huggingface")
except Exception as e:
    print(f"✗ langchain_huggingface: {e}")

try:
    from langchain_groq import ChatGroq
    print("✓ langchain_groq")
except Exception as e:
    print(f"✗ langchain_groq: {e}")

try:
    import chromadb
    print("✓ chromadb")
except Exception as e:
    print(f"✗ chromadb: {e}")

print("\nAll imports successful!")
