"""Web scraper for Chinese novel websites."""

import re
import time
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class Chapter:
    """Represents a novel chapter."""

    def __init__(self, title: str, content: str, url: str, number: int):
        self.title = title
        self.content = content
        self.url = url
        self.number = number


class NovelMetadata:
    """Represents novel metadata."""

    def __init__(self, title: str, author: str, description: str = "", cover_url: str = ""):
        self.title = title
        self.author = author
        self.description = description
        self.cover_url = cover_url


class NovelScraper:
    """Generic scraper for Chinese novel websites."""

    def __init__(self, delay: float = 1.0):
        """
        Initialize the scraper.

        Args:
            delay: Delay between requests in seconds
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def _get_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a webpage.

        Args:
            url: URL to fetch

        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            # Try to detect encoding
            response.encoding = response.apparent_encoding or 'utf-8'

            return BeautifulSoup(response.text, 'lxml')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def get_metadata(self, url: str) -> Optional[NovelMetadata]:
        """
        Extract novel metadata from the main page.

        Args:
            url: Novel main page URL

        Returns:
            NovelMetadata or None if failed
        """
        soup = self._get_page(url)
        if not soup:
            return None

        # Try common patterns for novel metadata
        title = self._extract_title(soup)
        author = self._extract_author(soup)
        description = self._extract_description(soup)
        cover_url = self._extract_cover(soup, url)

        return NovelMetadata(title, author, description, cover_url)

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract novel title from page."""
        # Try common title selectors
        for selector in ['h1', '.book-title', '.novel-title', '#book-title', 'meta[property="og:title"]']:
            element = soup.select_one(selector)
            if element:
                if selector.startswith('meta'):
                    return element.get('content', 'Unknown Title')
                text = element.get_text(strip=True)
                if text:
                    return text
        return "Unknown Title"

    def _extract_author(self, soup: BeautifulSoup) -> str:
        """Extract author from page."""
        for selector in ['.author', '.book-author', '#author', 'meta[name="author"]']:
            element = soup.select_one(selector)
            if element:
                if selector.startswith('meta'):
                    return element.get('content', 'Unknown Author')
                text = element.get_text(strip=True)
                # Remove "作者:" or similar prefixes
                text = re.sub(r'^(作者|Author)[：:]\s*', '', text)
                if text:
                    return text
        return "Unknown Author"

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract description from page."""
        for selector in ['.description', '.intro', '.summary', '#intro', 'meta[property="og:description"]']:
            element = soup.select_one(selector)
            if element:
                if selector.startswith('meta'):
                    return element.get('content', '')
                text = element.get_text(strip=True)
                if text and len(text) > 20:
                    return text
        return ""

    def _extract_cover(self, soup: BeautifulSoup, base_url: str) -> str:
        """Extract cover image URL from page."""
        for selector in ['.book-cover img', '.cover img', '#cover img', 'meta[property="og:image"]']:
            element = soup.select_one(selector)
            if element:
                if selector.startswith('meta'):
                    url = element.get('content', '')
                else:
                    url = element.get('src', '')
                if url:
                    return urljoin(base_url, url)
        return ""

    def get_chapter_list(self, url: str) -> List[str]:
        """
        Extract chapter URLs from the table of contents.

        Args:
            url: Table of contents URL

        Returns:
            List of chapter URLs
        """
        soup = self._get_page(url)
        if not soup:
            return []

        chapter_urls = []

        # Try to find chapter list container
        containers = soup.select('.chapter-list, #chapter-list, .volume-list, #list')

        if not containers:
            # Fallback: find all links that look like chapters
            containers = [soup]

        for container in containers:
            links = container.find_all('a', href=True)
            for link in links:
                href = link.get('href')
                # Filter out non-chapter links
                if href and not any(x in href.lower() for x in ['javascript:', '#', 'mailto:']):
                    full_url = urljoin(url, href)
                    if full_url not in chapter_urls:
                        chapter_urls.append(full_url)

        return chapter_urls

    def get_chapter(self, url: str, number: int) -> Optional[Chapter]:
        """
        Scrape a single chapter.

        Args:
            url: Chapter URL
            number: Chapter number

        Returns:
            Chapter object or None if failed
        """
        soup = self._get_page(url)
        if not soup:
            return None

        time.sleep(self.delay)  # Rate limiting

        # Extract chapter title
        title = self._extract_chapter_title(soup)

        # Extract chapter content
        content = self._extract_chapter_content(soup)

        if not content:
            print(f"Warning: No content found for {url}")
            return None

        return Chapter(title, content, url, number)

    def _extract_chapter_title(self, soup: BeautifulSoup) -> str:
        """Extract chapter title."""
        for selector in ['h1', '.chapter-title', '#chapter-title', '.title']:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text:
                    return text
        return "Untitled Chapter"

    def _extract_chapter_content(self, soup: BeautifulSoup) -> str:
        """Extract chapter content."""
        # Try common content selectors
        for selector in ['#content', '.content', '#chapter-content', '.chapter-content',
                        '.chapter', '#chapter', '.text', '#text']:
            element = soup.select_one(selector)
            if element:
                # Remove script and style elements
                for tag in element.find_all(['script', 'style', 'nav', 'header', 'footer']):
                    tag.decompose()

                # Get text with paragraph breaks
                paragraphs = []
                for p in element.find_all(['p', 'div']):
                    text = p.get_text(strip=True)
                    if text and len(text) > 10:  # Filter out short non-content text
                        paragraphs.append(text)

                if paragraphs:
                    return '\n\n'.join(paragraphs)

                # Fallback: get all text
                text = element.get_text(strip=True)
                if text and len(text) > 100:
                    return text

        return ""

    def scrape_novel(self, url: str, start_chapter: int = 1, end_chapter: Optional[int] = None) -> tuple:
        """
        Scrape an entire novel or a range of chapters.

        Args:
            url: Novel main page or table of contents URL
            start_chapter: First chapter to scrape (1-indexed)
            end_chapter: Last chapter to scrape (None for all)

        Returns:
            Tuple of (metadata, chapters)
        """
        print(f"Fetching metadata from {url}")
        metadata = self.get_metadata(url)

        print("Fetching chapter list...")
        chapter_urls = self.get_chapter_list(url)

        if not chapter_urls:
            print("No chapters found. Please check the URL.")
            return metadata, []

        print(f"Found {len(chapter_urls)} chapters")

        # Apply chapter range
        start_idx = max(0, start_chapter - 1)
        end_idx = end_chapter if end_chapter else len(chapter_urls)
        chapter_urls = chapter_urls[start_idx:end_idx]

        print(f"Scraping chapters {start_chapter} to {start_chapter + len(chapter_urls) - 1}...")

        chapters = []
        for i, chapter_url in enumerate(chapter_urls, start=start_chapter):
            print(f"  Scraping chapter {i}/{start_chapter + len(chapter_urls) - 1}...", end='\r')
            chapter = self.get_chapter(chapter_url, i)
            if chapter:
                chapters.append(chapter)

        print(f"\nSuccessfully scraped {len(chapters)} chapters")

        return metadata, chapters
