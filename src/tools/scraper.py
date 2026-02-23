"""Web scraping and content extraction"""
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
import logging
import asyncio
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def _sync_scrape(self, url: str) -> List[Document]:
        """Synchronous scrape — runs in thread pool to avoid blocking the event loop"""
        loader = WebBaseLoader(url)
        docs = loader.load()
        for doc in docs:
            soup = BeautifulSoup(doc.page_content, 'html.parser')
            doc.page_content = soup.get_text(separator='\n', strip=True)
            doc.metadata['source'] = url
        return self.splitter.split_documents(docs)

    async def scrape_url(self, url: str) -> List[Document]:
        """Scrape a single URL — offloads sync I/O to thread pool"""
        try:
            loop = asyncio.get_event_loop()
            chunks = await loop.run_in_executor(None, self._sync_scrape, url)
            logger.info(f"Scraped {url}: {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return []

    async def scrape_multiple(self, urls: List[str], max_workers: int = 3) -> List[Document]:
        """Scrape multiple URLs concurrently with asyncio.gather"""
        tasks = [self.scrape_url(url) for url in urls[:max_workers]]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        all_chunks = []
        for result in results:
            if isinstance(result, list):
                all_chunks.extend(result)
        logger.info(f"Total chunks from {len(urls)} URLs: {len(all_chunks)}")
        return all_chunks
