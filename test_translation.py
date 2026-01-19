#!/usr/bin/env python3
"""
Simple test script to compare Google Translate vs DeepL translation quality.
"""

import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.translator import CachedTranslator, CachedDeepLTranslator
from src.scraper import NovelMetadata, Chapter


def test_google_translate():
    """Test Google Translate."""
    print("=" * 60)
    print("Testing Google Translate (FREE)")
    print("=" * 60)
    print()

    translator = CachedTranslator(source_lang='zh-CN', target_lang='en')

    # Test texts
    test_texts = [
        "第一章：修炼之路",
        "在这个世界上，修炼者无数，但能真正达到巅峰的却寥寥无几。",
        "他看着远方的山峰，心中升起一股豪情。",
    ]

    for i, text in enumerate(test_texts, 1):
        translated = translator.translate_text(text)
        print(f"Test {i}:")
        print(f"  Original:   {text}")
        print(f"  Translated: {translated}")
        print()

    print(f"✓ Google Translate test complete!")
    print()


def test_deepl_translate(api_key):
    """Test DeepL translation."""
    print("=" * 60)
    print("Testing DeepL (FREE: 500K chars/month)")
    print("=" * 60)
    print()

    try:
        translator = CachedDeepLTranslator(
            api_key=api_key,
            source_lang='ZH',
            target_lang='EN-US'
        )

        # Test texts
        test_texts = [
            "第一章：修炼之路",
            "在这个世界上，修炼者无数，但能真正达到巅峰的却寥寥无几。",
            "他看着远方的山峰，心中升起一股豪情。",
        ]

        for i, text in enumerate(test_texts, 1):
            translated = translator.translate_text(text)
            print(f"Test {i}:")
            print(f"  Original:   {text}")
            print(f"  Translated: {translated}")
            print()

        print(f"✓ DeepL test complete!")
        print()

    except Exception as e:
        print(f"❌ DeepL test failed: {e}")
        print()
        print("Make sure you:")
        print("1. Have a DeepL API key from https://www.deepl.com/pro-api")
        print("2. Installed the library: pip install deepl")
        print()


def test_chapter_translation(api_key=None):
    """Test translating a full chapter object."""
    print("=" * 60)
    print("Testing Chapter Translation")
    print("=" * 60)
    print()

    # Create a sample chapter
    chapter = Chapter(
        title="第一章：开端",
        content="这是一个关于修炼的故事。\n\n主角叫做林风，是一个普通的少年。\n\n但命运即将改变他的人生。",
        url="https://example.com/chapter1",
        number=1
    )

    print("Original Chapter:")
    print(f"  Title: {chapter.title}")
    print(f"  Content: {chapter.content[:100]}...")
    print()

    # Test with Google Translate
    print("Translating with Google Translate...")
    google_translator = CachedTranslator(source_lang='zh-CN', target_lang='en')
    google_translator.translate_chapter(chapter)

    print("Translated Chapter (Google):")
    print(f"  Title: {chapter.title}")
    print(f"  Content: {chapter.content}")
    print()

    # Test with DeepL if API key provided
    if api_key:
        # Reset chapter
        chapter = Chapter(
            title="第一章：开端",
            content="这是一个关于修炼的故事。\n\n主角叫做林风，是一个普通的少年。\n\n但命运即将改变他的人生。",
            url="https://example.com/chapter1",
            number=1
        )

        print("Translating with DeepL...")
        deepl_translator = CachedDeepLTranslator(
            api_key=api_key,
            source_lang='ZH',
            target_lang='EN-US'
        )
        deepl_translator.translate_chapter(chapter)

        print("Translated Chapter (DeepL):")
        print(f"  Title: {chapter.title}")
        print(f"  Content: {chapter.content}")
        print()


def main():
    """Main test function."""
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         Novel Translator - Translation Test               ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

    # Check for DeepL API key
    deepl_api_key = os.environ.get('DEEPL_API_KEY')

    if not deepl_api_key:
        print("⚠️  DeepL API key not found in environment variables.")
        print()
        print("To test DeepL:")
        print("  1. Get a FREE API key at: https://www.deepl.com/pro-api")
        print("  2. Set it as an environment variable:")
        print("     export DEEPL_API_KEY='your-key-here'")
        print("  3. Or run: DEEPL_API_KEY='your-key' python test_translation.py")
        print()
        print("For now, we'll only test Google Translate.")
        print()

    # Run tests
    test_google_translate()

    if deepl_api_key:
        test_deepl_translate(deepl_api_key)
        test_chapter_translation(deepl_api_key)
    else:
        test_chapter_translation()

    print("=" * 60)
    print("✓ All tests complete!")
    print("=" * 60)
    print()
    print("To translate a real novel, use:")
    print("  python novel_translator.py <URL> --translator deepl --deepl-api-key YOUR_KEY")
    print()


if __name__ == '__main__':
    main()
