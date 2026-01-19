# Novel Translator

A powerful Python tool for scraping Chinese web novels, translating them to English (or other languages), and generating ePub files for easy reading on e-readers.

## Features

- **Web Scraping**: Automatically extracts novel content from Chinese web novel sites
- **Translation**: Translates Chinese text to English using Google Translate (free, no API key required)
- **ePub Generation**: Creates professional ePub files with proper formatting
- **Chapter Range**: Scrape specific chapter ranges or entire novels
- **Metadata Extraction**: Automatically extracts title, author, description, and cover images
- **Progress Tracking**: Real-time progress bars for scraping and translation
- **Caching**: Avoids re-translating duplicate text
- **Customizable**: Adjust delays, language codes, and more

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Translatednovelspublic
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

Basic usage - scrape, translate, and create ePub:
```bash
python novel_translator.py https://example.com/novel/123
```

This will:
1. Scrape all chapters from the URL
2. Translate from Chinese to English
3. Generate `output.epub`

## Usage Examples

### Specify output file name:
```bash
python novel_translator.py https://example.com/novel/123 -o my_novel.epub
```

### Scrape specific chapter range:
```bash
# Chapters 1-10
python novel_translator.py https://example.com/novel/123 -s 1 -e 10

# Chapters 50-100
python novel_translator.py https://example.com/novel/123 -s 50 -e 100
```

### Skip translation (create Chinese ePub):
```bash
python novel_translator.py https://example.com/novel/123 --no-translate
```

### Translate to different language:
```bash
# Translate to Spanish
python novel_translator.py https://example.com/novel/123 --target-lang es

# Translate Japanese to English
python novel_translator.py https://example.com/novel/123 --source-lang ja --target-lang en
```

### Adjust delays (for rate limiting):
```bash
# Slower scraping (2 seconds between requests)
python novel_translator.py https://example.com/novel/123 --scrape-delay 2.0

# Slower translation (1 second between requests)
python novel_translator.py https://example.com/novel/123 --translate-delay 1.0
```

## Command Line Options

```
Usage: novel_translator.py URL [OPTIONS]

Arguments:
  URL                      The URL of the novel's main page or table of contents

Options:
  -o, --output PATH        Output ePub file path (default: output.epub)
  -s, --start INTEGER      Starting chapter number (default: 1)
  -e, --end INTEGER        Ending chapter number (default: all chapters)
  --source-lang TEXT       Source language code (default: zh-CN)
  --target-lang TEXT       Target language code (default: en)
  --no-translate           Skip translation (create ePub from original)
  --scrape-delay FLOAT     Delay between scraping requests in seconds (default: 1.0)
  --translate-delay FLOAT  Delay between translation requests in seconds (default: 0.5)
  --help                   Show this message and exit
```

## Supported Language Codes

Common language codes for translation:
- `zh-CN` - Chinese (Simplified)
- `zh-TW` - Chinese (Traditional)
- `en` - English
- `ja` - Japanese
- `ko` - Korean
- `es` - Spanish
- `fr` - French
- `de` - German
- `ru` - Russian

For more language codes, see [Google Translate supported languages](https://cloud.google.com/translate/docs/languages).

## How It Works

1. **Scraping**: The tool visits the provided URL and attempts to extract:
   - Novel metadata (title, author, description, cover image)
   - List of chapter URLs from the table of contents
   - Chapter content from each chapter page

2. **Translation**: Each chapter's title and content are translated using Google Translate API (via deep-translator library). The translation includes:
   - Smart chunking for long chapters
   - Automatic retry on failures
   - Caching to avoid duplicate translations

3. **ePub Generation**: Creates a properly formatted ePub file with:
   - Table of contents
   - Chapter navigation
   - Cover image (if available)
   - CSS styling for readability
   - Proper metadata

## Tips for Best Results

1. **Find the Table of Contents**: The tool works best when you provide the URL to the novel's table of contents page (the page listing all chapters).

2. **Start with a Few Chapters**: Test with a small range first (e.g., `-s 1 -e 5`) to ensure the scraping works correctly for your specific website.

3. **Be Patient**: Translation can take time, especially for long novels. A typical chapter might take 10-30 seconds to translate depending on length.

4. **Respect Websites**: The default delays are set to be respectful to web servers. Avoid reducing delays too much.

5. **Check the Output**: After generation, open the ePub file in an e-reader app (Calibre, Apple Books, etc.) to verify the formatting.

## Supported Websites

The scraper uses generic selectors that work with many Chinese novel websites. It has been designed to work with common patterns found on sites like:
- Qidian (起点中文网)
- JJWXC (晋江文学城)
- And many others with similar HTML structures

However, each website is different. If a site doesn't work, you may need to adjust the scraper's selectors in `src/scraper.py`.

## Troubleshooting

### No chapters found
- Verify the URL is correct and points to a table of contents page
- Try viewing the page source to see if chapters are loaded dynamically (JavaScript)
- Some sites may require authentication or cookies

### Translation fails
- Check your internet connection
- Google Translate may rate-limit excessive requests - increase `--translate-delay`
- Try translating fewer chapters at once

### ePub file is empty or corrupted
- Verify that chapters were actually scraped (check console output)
- Ensure the scraping found content (not just empty pages)
- Try opening the ePub in different readers (some readers are more forgiving)

### Rate limiting / IP blocked
- Increase `--scrape-delay` to make requests slower
- Some sites may block automated scraping
- Consider using a VPN or waiting before retrying

## Project Structure

```
Translatednovelspublic/
├── novel_translator.py      # Main CLI application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
└── src/
    ├── __init__.py          # Package initialization
    ├── scraper.py           # Web scraping module
    ├── translator.py        # Translation module
    └── epub_generator.py    # ePub generation module
```

## Requirements

- Python 3.8 or higher
- Internet connection (for scraping and translation)
- Dependencies listed in `requirements.txt`

## Legal Notice

This tool is for personal use only. Please respect copyright laws and the terms of service of websites you scrape. Only use this tool for:
- Novels that are freely available online
- Personal reading purposes
- Content you have permission to access

Do not distribute translated content without proper authorization from the original authors.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Share website-specific scraper configurations

## License

This project is provided as-is for educational and personal use.

## Acknowledgments

- **deep-translator**: For providing free translation services
- **ebooklib**: For ePub generation capabilities
- **BeautifulSoup**: For HTML parsing
- All the authors who share their works online

---

Enjoy reading your translated novels!
