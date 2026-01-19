#!/usr/bin/env python3
"""
Novel Translator - Scrape, translate, and generate ePub files from Chinese web novels.

Usage:
    python novel_translator.py <url> [options]
"""

import os
import sys
from pathlib import Path

import click

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.scraper import NovelScraper
from src.translator import CachedTranslator
from src.epub_generator import EpubGenerator


@click.command()
@click.argument('url')
@click.option('--output', '-o', default='output.epub',
              help='Output ePub file path (default: output.epub)')
@click.option('--start', '-s', default=1, type=int,
              help='Starting chapter number (default: 1)')
@click.option('--end', '-e', default=None, type=int,
              help='Ending chapter number (default: all chapters)')
@click.option('--source-lang', default='zh-CN',
              help='Source language code (default: zh-CN)')
@click.option('--target-lang', default='en',
              help='Target language code (default: en)')
@click.option('--no-translate', is_flag=True,
              help='Skip translation (create ePub from original Chinese)')
@click.option('--scrape-delay', default=1.0, type=float,
              help='Delay between scraping requests in seconds (default: 1.0)')
@click.option('--translate-delay', default=0.5, type=float,
              help='Delay between translation requests in seconds (default: 0.5)')
def main(url, output, start, end, source_lang, target_lang, no_translate,
         scrape_delay, translate_delay):
    """
    Scrape a Chinese web novel, translate it, and generate an ePub file.

    URL: The URL of the novel's main page or table of contents

    Examples:
        python novel_translator.py https://example.com/novel/123
        python novel_translator.py https://example.com/novel/123 -o mynovel.epub
        python novel_translator.py https://example.com/novel/123 -s 1 -e 10
    """
    click.echo("=" * 60)
    click.echo("Novel Translator - Chinese Web Novel to ePub")
    click.echo("=" * 60)
    click.echo()

    # Create output directory if needed
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Step 1: Scrape the novel
        click.echo("[1/3] Scraping novel...")
        click.echo(f"URL: {url}")
        click.echo(f"Chapter range: {start} to {end if end else 'end'}")
        click.echo()

        scraper = NovelScraper(delay=scrape_delay)
        metadata, chapters = scraper.scrape_novel(url, start, end)

        if not chapters:
            click.echo("Error: No chapters were scraped. Please check the URL.", err=True)
            sys.exit(1)

        click.echo()
        click.echo(f"✓ Successfully scraped {len(chapters)} chapters")
        click.echo(f"  Title: {metadata.title}")
        click.echo(f"  Author: {metadata.author}")
        click.echo()

        # Step 2: Translate (optional)
        if not no_translate:
            click.echo(f"[2/3] Translating from {source_lang} to {target_lang}...")
            click.echo("This may take a while depending on the number of chapters.")
            click.echo()

            translator = CachedTranslator(
                source_lang=source_lang,
                target_lang=target_lang,
                delay=translate_delay
            )

            # Translate metadata
            translator.translate_metadata(metadata)

            # Translate chapters
            translator.translate_chapters(chapters, show_progress=True)

            click.echo()
            click.echo(f"✓ Translation complete ({translator.cache_size()} items cached)")
            click.echo()
        else:
            click.echo("[2/3] Skipping translation (--no-translate flag set)")
            click.echo()

        # Step 3: Generate ePub
        click.echo("[3/3] Generating ePub file...")

        generator = EpubGenerator()
        output_file = generator.create_epub(metadata, chapters, str(output_path))

        click.echo()
        click.echo("=" * 60)
        click.echo("✓ SUCCESS!")
        click.echo("=" * 60)
        click.echo(f"ePub file created: {output_file}")
        click.echo(f"File size: {os.path.getsize(output_file) / 1024:.2f} KB")
        click.echo(f"Chapters: {len(chapters)}")
        click.echo()

    except KeyboardInterrupt:
        click.echo("\n\nOperation cancelled by user.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"\nError: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


@click.group()
def cli():
    """Novel Translator CLI"""
    pass


@cli.command()
@click.argument('url')
def metadata(url):
    """Extract and display novel metadata from URL."""
    click.echo("Fetching metadata...")
    scraper = NovelScraper()
    meta = scraper.get_metadata(url)

    if meta:
        click.echo()
        click.echo(f"Title: {meta.title}")
        click.echo(f"Author: {meta.author}")
        click.echo(f"Description: {meta.description[:200]}..." if len(meta.description) > 200 else f"Description: {meta.description}")
        click.echo(f"Cover URL: {meta.cover_url}")
    else:
        click.echo("Failed to extract metadata.", err=True)


@cli.command()
@click.argument('url')
def chapters(url):
    """List all chapter URLs from the table of contents."""
    click.echo("Fetching chapter list...")
    scraper = NovelScraper()
    chapter_urls = scraper.get_chapter_list(url)

    if chapter_urls:
        click.echo(f"\nFound {len(chapter_urls)} chapters:\n")
        for i, chapter_url in enumerate(chapter_urls[:20], 1):  # Show first 20
            click.echo(f"{i}. {chapter_url}")

        if len(chapter_urls) > 20:
            click.echo(f"\n... and {len(chapter_urls) - 20} more chapters")
    else:
        click.echo("No chapters found.", err=True)


if __name__ == '__main__':
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        main(['--help'])
    else:
        main()
