#!/usr/bin/env python3
"""
Example script showing how to use the Novel Translator programmatically.
"""

from src.scraper import NovelScraper
from src.translator import CachedTranslator
from src.epub_generator import EpubGenerator


def example_usage():
    """Example of using the library programmatically."""

    # Example URL (replace with actual novel URL)
    url = "https://example.com/novel/123"

    # Step 1: Scrape the novel
    print("Scraping novel...")
    scraper = NovelScraper(delay=1.0)
    metadata, chapters = scraper.scrape_novel(url, start_chapter=1, end_chapter=5)

    print(f"Title: {metadata.title}")
    print(f"Author: {metadata.author}")
    print(f"Scraped {len(chapters)} chapters")

    # Step 2: Translate
    print("\nTranslating...")
    translator = CachedTranslator(source_lang='zh-CN', target_lang='en')
    translator.translate_metadata(metadata)
    translator.translate_chapters(chapters)

    print(f"Translation complete")

    # Step 3: Generate ePub
    print("\nGenerating ePub...")
    generator = EpubGenerator()
    output_path = generator.create_epub(metadata, chapters, "my_novel.epub")

    print(f"ePub created: {output_path}")


def simple_example():
    """Simple example with minimal code."""

    # You can also use the simple interface
    generator = EpubGenerator()

    chapters = [
        ("Chapter 1: The Beginning", "This is the first chapter content..."),
        ("Chapter 2: The Journey", "This is the second chapter content..."),
        ("Chapter 3: The End", "This is the third chapter content..."),
    ]

    generator.create_epub_simple(
        title="My Novel",
        author="Author Name",
        chapters=chapters,
        output_path="simple_novel.epub"
    )

    print("Simple ePub created!")


if __name__ == '__main__':
    print("Novel Translator Examples")
    print("=" * 60)
    print()
    print("This is an example script showing how to use the library.")
    print("Uncomment the function you want to run:")
    print()
    print("1. example_usage() - Full scraping, translation, and ePub generation")
    print("2. simple_example() - Create ePub from predefined chapters")
    print()

    # Uncomment one of these to run:
    # example_usage()
    # simple_example()

    print("Edit this file and uncomment a function to run it.")
