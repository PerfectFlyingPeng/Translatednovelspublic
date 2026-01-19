"""ePub generation module for creating ePub files from novel chapters."""

import io
import re
from datetime import datetime
from typing import List, Optional

import requests
from ebooklib import epub
from PIL import Image


class EpubGenerator:
    """Generates ePub files from novel chapters."""

    def __init__(self):
        """Initialize ePub generator."""
        self.default_css = '''
        @namespace epub "http://www.idpf.org/2007/ops";
        body {
            font-family: Georgia, serif;
            line-height: 1.6;
            margin: 5%;
            text-align: justify;
        }
        h1 {
            text-align: center;
            margin-bottom: 2em;
            font-size: 2em;
        }
        h2 {
            text-align: center;
            margin-top: 2em;
            margin-bottom: 1em;
            font-size: 1.5em;
        }
        p {
            margin: 0;
            text-indent: 2em;
            margin-bottom: 1em;
        }
        .chapter {
            page-break-before: always;
        }
        '''

    def create_epub(self, metadata, chapters: List, output_path: str,
                   cover_image_path: Optional[str] = None) -> str:
        """
        Create an ePub file from chapters.

        Args:
            metadata: NovelMetadata object
            chapters: List of Chapter objects
            output_path: Path to save the ePub file
            cover_image_path: Optional path to cover image

        Returns:
            Path to the created ePub file
        """
        book = epub.EpubBook()

        # Set metadata
        book.set_identifier(self._generate_id(metadata.title))
        book.set_title(metadata.title)
        book.set_language('en')
        book.add_author(metadata.author)

        if metadata.description:
            book.add_metadata('DC', 'description', metadata.description)

        book.add_metadata('DC', 'date', datetime.now().strftime('%Y-%m-%d'))

        # Add CSS
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content=self.default_css
        )
        book.add_item(nav_css)

        # Add cover image if available
        if cover_image_path:
            self._add_cover_image(book, cover_image_path)
        elif metadata.cover_url:
            self._add_cover_from_url(book, metadata.cover_url)

        # Create chapters
        epub_chapters = []
        spine = ['nav']

        for chapter in chapters:
            epub_chapter = self._create_chapter(chapter)
            book.add_item(epub_chapter)
            epub_chapters.append(epub_chapter)
            spine.append(epub_chapter)

        # Define Table of Contents
        book.toc = tuple(epub_chapters)

        # Add navigation files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # Define spine
        book.spine = spine

        # Write ePub file
        epub.write_epub(output_path, book, {})

        return output_path

    def _generate_id(self, title: str) -> str:
        """Generate a unique identifier from title."""
        # Remove special characters and spaces
        clean_title = re.sub(r'[^a-zA-Z0-9]', '', title.lower())
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"{clean_title}_{timestamp}"

    def _create_chapter(self, chapter) -> epub.EpubHtml:
        """
        Create an ePub chapter from a Chapter object.

        Args:
            chapter: Chapter object

        Returns:
            EpubHtml chapter
        """
        # Create chapter
        epub_chapter = epub.EpubHtml(
            title=chapter.title,
            file_name=f'chapter_{chapter.number:04d}.xhtml',
            lang='en'
        )

        # Format content
        content = self._format_content(chapter.title, chapter.content)
        epub_chapter.content = content

        return epub_chapter

    def _format_content(self, title: str, content: str) -> str:
        """
        Format chapter content as HTML.

        Args:
            title: Chapter title
            content: Chapter content

        Returns:
            HTML formatted content
        """
        # Split content into paragraphs
        paragraphs = content.split('\n\n')

        # Create HTML
        html = f'<html><head></head><body><div class="chapter">'
        html += f'<h2>{self._escape_html(title)}</h2>'

        for para in paragraphs:
            para = para.strip()
            if para:
                html += f'<p>{self._escape_html(para)}</p>'

        html += '</div></body></html>'

        return html

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))

    def _add_cover_image(self, book: epub.EpubBook, image_path: str):
        """
        Add cover image from local file.

        Args:
            book: EpubBook object
            image_path: Path to cover image
        """
        try:
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()

            # Determine image type
            img_type = 'image/jpeg'
            if image_path.lower().endswith('.png'):
                img_type = 'image/png'

            book.set_cover('cover.jpg', img_data)
        except Exception as e:
            print(f"Warning: Could not add cover image: {e}")

    def _add_cover_from_url(self, book: epub.EpubBook, url: str):
        """
        Download and add cover image from URL.

        Args:
            book: EpubBook object
            url: Cover image URL
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Resize image if too large
            img = Image.open(io.BytesIO(response.content))

            # Resize to reasonable dimensions
            max_width = 800
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # Save to bytes
            img_bytes = io.BytesIO()
            img_format = 'JPEG' if img.mode == 'RGB' else 'PNG'
            img.save(img_bytes, format=img_format)
            img_data = img_bytes.getvalue()

            book.set_cover('cover.jpg', img_data)
        except Exception as e:
            print(f"Warning: Could not download/add cover image: {e}")

    def create_epub_simple(self, title: str, author: str, chapters: List[tuple],
                          output_path: str) -> str:
        """
        Simple ePub creation with minimal metadata.

        Args:
            title: Book title
            author: Author name
            chapters: List of (chapter_title, chapter_content) tuples
            output_path: Path to save the ePub file

        Returns:
            Path to the created ePub file
        """
        # Create simple metadata object
        class SimpleMetadata:
            def __init__(self, title, author):
                self.title = title
                self.author = author
                self.description = ""
                self.cover_url = ""

        # Create simple chapter objects
        class SimpleChapter:
            def __init__(self, title, content, number):
                self.title = title
                self.content = content
                self.number = number
                self.url = ""

        metadata = SimpleMetadata(title, author)
        chapter_objects = [
            SimpleChapter(title, content, i + 1)
            for i, (title, content) in enumerate(chapters)
        ]

        return self.create_epub(metadata, chapter_objects, output_path)
