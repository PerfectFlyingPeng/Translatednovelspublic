#!/usr/bin/env python3
"""
Test the scraper with a real URL to see what content it extracts.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.scraper import NovelScraper

def test_metadata(url):
    """Test metadata extraction."""
    print("=" * 80)
    print("TESTING METADATA EXTRACTION")
    print("=" * 80)
    print()

    scraper = NovelScraper()
    metadata = scraper.get_metadata(url)

    if metadata:
        print(f"Title: {metadata.title}")
        print(f"Author: {metadata.author}")
        print(f"Description: {metadata.description[:300] if metadata.description else 'None'}...")
        print(f"Cover URL: {metadata.cover_url}")
    else:
        print("Failed to extract metadata")

    print()


def test_chapter_list(url):
    """Test chapter list extraction."""
    print("=" * 80)
    print("TESTING CHAPTER LIST EXTRACTION")
    print("=" * 80)
    print()

    scraper = NovelScraper()
    chapters = scraper.get_chapter_list(url)

    print(f"Found {len(chapters)} chapters")
    print()
    print("First 5 chapters:")
    for i, chapter_url in enumerate(chapters[:5], 1):
        print(f"  {i}. {chapter_url}")

    print()
    return chapters


def test_chapter_content(chapter_url, chapter_num=1):
    """Test single chapter extraction."""
    print("=" * 80)
    print(f"TESTING CHAPTER CONTENT EXTRACTION - Chapter {chapter_num}")
    print("=" * 80)
    print()
    print(f"URL: {chapter_url}")
    print()

    scraper = NovelScraper()
    chapter = scraper.get_chapter(chapter_url, chapter_num)

    if chapter:
        print(f"Title: {chapter.title}")
        print(f"Content length: {len(chapter.content)} characters")
        print()
        print("-" * 80)
        print("CONTENT PREVIEW (first 1000 chars):")
        print("-" * 80)
        print(chapter.content[:1000])
        print()
        print("-" * 80)
        print("CONTENT PREVIEW (last 500 chars):")
        print("-" * 80)
        print(chapter.content[-500:])
        print()

        # Check for common junk patterns
        print("=" * 80)
        print("JUNK DETECTION")
        print("=" * 80)
        junk_patterns = [
            ("上一章", "Previous chapter link"),
            ("下一章", "Next chapter link"),
            ("返回目录", "Back to contents"),
            ("加入书签", "Add bookmark"),
            ("本章说", "Chapter comments"),
            ("作者的话", "Author's note"),
            ("PS:", "Postscript"),
            ("http://", "URL in content"),
            ("www.", "URL in content"),
        ]

        found_junk = False
        for pattern, description in junk_patterns:
            if pattern in chapter.content:
                print(f"⚠️  Found: {description} ({pattern})")
                found_junk = True

        if not found_junk:
            print("✓ No obvious junk patterns detected")

        print()
    else:
        print("Failed to extract chapter content")


def main():
    url = "https://www.69shuba.com/book/51659/"

    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "SCRAPER TEST - 69shuba.com" + " " * 32 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    # Test 1: Metadata
    test_metadata(url)

    # Test 2: Chapter list
    chapters = test_chapter_list(url)

    # Test 3: First chapter content
    if chapters:
        test_chapter_content(chapters[0], 1)

        # Test a middle chapter too
        if len(chapters) > 10:
            print("\n" + "=" * 80)
            print("Testing a middle chapter (Chapter 10)...")
            print("=" * 80 + "\n")
            test_chapter_content(chapters[9], 10)

    print()
    print("=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
