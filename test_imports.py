#!/usr/bin/env python3
"""
Simple test to verify all modules can be imported correctly.
"""

def test_imports():
    """Test that all modules import without errors."""

    print("Testing imports...")

    try:
        print("  Importing scraper...", end=" ")
        from src.scraper import NovelScraper, Chapter, NovelMetadata
        print("✓")

        print("  Importing translator...", end=" ")
        from src.translator import Translator, CachedTranslator
        print("✓")

        print("  Importing epub_generator...", end=" ")
        from src.epub_generator import EpubGenerator
        print("✓")

        print("\nAll imports successful!")

        # Test basic instantiation
        print("\nTesting basic instantiation...")
        print("  Creating NovelScraper...", end=" ")
        scraper = NovelScraper()
        print("✓")

        print("  Creating CachedTranslator...", end=" ")
        translator = CachedTranslator()
        print("✓")

        print("  Creating EpubGenerator...", end=" ")
        generator = EpubGenerator()
        print("✓")

        print("\nAll tests passed! The Novel Translator is ready to use.")
        print("\nUsage:")
        print("  python novel_translator.py <url>")
        print("\nFor help:")
        print("  python novel_translator.py --help")

        return True

    except ImportError as e:
        print(f"✗\n\nError: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"✗\n\nUnexpected error: {e}")
        return False


if __name__ == '__main__':
    success = test_imports()
    exit(0 if success else 1)
