# Novel Translator - How to Use

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Test the Translation

Run the test script to see both translators in action:

```bash
# Test Google Translate only (no API key needed)
python test_translation.py

# Test both Google Translate AND DeepL
export DEEPL_API_KEY="your-deepl-api-key-here"
python test_translation.py
```

### 3. Translate a Real Novel

#### Option A: Using Google Translate (Free, Basic Quality)

```bash
python novel_translator.py <NOVEL_URL> -o output.epub -s 1 -e 5
```

#### Option B: Using DeepL (Better Quality, Free Tier: 500K chars/month)

```bash
# First, get your FREE DeepL API key from: https://www.deepl.com/pro-api
# Then run:

python novel_translator.py <NOVEL_URL> \
  --translator deepl \
  --deepl-api-key "your-api-key" \
  -o output.epub \
  -s 1 -e 5
```

Or set the API key as an environment variable:

```bash
export DEEPL_API_KEY="your-api-key"
python novel_translator.py <NOVEL_URL> --translator deepl -o output.epub -s 1 -e 5
```

## Where Does the Code Go?

**You don't need to add code anywhere!** Everything is already set up:

```
Translatednovelspublic/
├── novel_translator.py      ← Main CLI tool (UPDATED with DeepL support)
├── test_translation.py      ← NEW: Simple test script
├── requirements.txt         ← Dependencies (UPDATED with deepl)
└── src/
    ├── scraper.py          ← Web scraping logic
    ├── translator.py       ← Translation logic (UPDATED with DeepL classes)
    └── epub_generator.py   ← ePub generation
```

## Testing Options

### 1. Quick Translation Test (No URL needed)
```bash
python test_translation.py
```
This tests the translators with sample Chinese text.

### 2. Test with a Real Novel URL

Give me a URL and I can test it for you! For example:
- Qidian novels
- Zongheng novels
- Any Chinese web novel site

```bash
python novel_translator.py <YOUR_URL> -s 1 -e 3 --translator deepl
```

### 3. Just Check Metadata (No translation)
```bash
python novel_translator.py <YOUR_URL> --no-translate
```

## Getting a DeepL API Key

1. Go to https://www.deepl.com/pro-api
2. Sign up for the FREE plan (500,000 characters/month)
3. Copy your API key
4. Use it with `--deepl-api-key` or set `DEEPL_API_KEY` environment variable

## CLI Options

```
Options:
  -o, --output TEXT              Output file path (default: output.epub)
  -s, --start INTEGER           Starting chapter (default: 1)
  -e, --end INTEGER             Ending chapter (default: all)
  --translator [google|deepl]   Choose translator (default: google)
  --deepl-api-key TEXT          DeepL API key (or set DEEPL_API_KEY env var)
  --no-translate                Skip translation, create ePub in Chinese
  --scrape-delay FLOAT          Delay between scrapes (default: 1.0s)
  --translate-delay FLOAT       Delay between translations (default: 0.5s)
```

## Examples

### Example 1: Quick test
```bash
python test_translation.py
```

### Example 2: Translate 10 chapters with Google
```bash
python novel_translator.py https://example.com/novel -s 1 -e 10 -o mynovel.epub
```

### Example 3: Translate 5 chapters with DeepL
```bash
export DEEPL_API_KEY="your-key"
python novel_translator.py https://example.com/novel -s 1 -e 5 --translator deepl
```

### Example 4: Just scrape, no translation
```bash
python novel_translator.py https://example.com/novel --no-translate -o chinese.epub
```

## Translation Quality Comparison

| Translator | Cost | Quality | Speed | Best For |
|------------|------|---------|-------|----------|
| Google Translate | FREE | ⭐⭐⭐ | Fast | Quick testing |
| DeepL | FREE tier (500K/month) | ⭐⭐⭐⭐⭐ | Fast | Literary content |

**Recommendation:** Use DeepL for better quality translations, especially for novels where style and tone matter!
