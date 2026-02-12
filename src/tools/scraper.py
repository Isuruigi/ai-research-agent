"""Web scraping and content extraction"""
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
import logging
from bs4 import BeautifulSoup
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
    async def scrape_url(self, url: str) -> List[Document]:
        """Scrape single URL and return chunked documents"""
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            
            # Clean content
            for doc in docs:
                soup = BeautifulSoup(doc.page_content, 'html.parser')
                doc.page_content = soup.get_text(separator='\n', strip=True)
                doc.metadata['source'] = url
            
            chunks = self.splitter.split_documents(docs)
            logger.info(f"Scraped {url}: {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return []
    
    async def scrape_multiple(self, urls: List[str], max_workers: int = 3) -> List[Document]:
        """Scrape multiple URLs concurrently"""
        all_chunks = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(executor, lambda u=url: asyncio.run(self.scrape_url(u)))
                for url in urls
            ]
            results = await asyncio.gather(*tasks)
            
        for chunks in results:
            all_chunks.extend(chunks)
            
        logger.info(f"Total chunks from {len(urls)} URLs: {len(all_chunks)}")
        return all_chunks
