"""Translation module for novel content."""

import time
from typing import List, Optional

from deep_translator import GoogleTranslator
from tqdm import tqdm


class Translator:
    """Handles translation of novel content."""

    def __init__(self, source_lang: str = 'zh-CN', target_lang: str = 'en', delay: float = 0.5):
        """
        Initialize translator.

        Args:
            source_lang: Source language code (default: zh-CN for Chinese)
            target_lang: Target language code (default: en for English)
            delay: Delay between translation requests in seconds
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.delay = delay
        self.translator = GoogleTranslator(source=source_lang, target=target_lang)

    def translate_text(self, text: str, max_retries: int = 3) -> str:
        """
        Translate a single piece of text.

        Args:
            text: Text to translate
            max_retries: Maximum number of retry attempts

        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text

        for attempt in range(max_retries):
            try:
                # Split text into chunks if too long (Google Translate has a 5000 char limit)
                if len(text) > 4500:
                    return self._translate_long_text(text)

                translated = self.translator.translate(text)
                time.sleep(self.delay)  # Rate limiting
                return translated

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"\nTranslation error (attempt {attempt + 1}/{max_retries}): {e}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"\nFailed to translate after {max_retries} attempts: {e}")
                    return text  # Return original text if translation fails

        return text

    def _translate_long_text(self, text: str) -> str:
        """
        Translate long text by splitting into chunks.

        Args:
            text: Long text to translate

        Returns:
            Translated text
        """
        # Split by paragraphs
        paragraphs = text.split('\n\n')
        translated_paragraphs = []

        for para in paragraphs:
            if len(para) > 4500:
                # Further split long paragraphs by sentences
                sentences = para.split('。')
                translated_sentences = []
                current_chunk = ""

                for sentence in sentences:
                    if len(current_chunk) + len(sentence) < 4500:
                        current_chunk += sentence + '。'
                    else:
                        if current_chunk:
                            translated_sentences.append(self.translate_text(current_chunk))
                        current_chunk = sentence + '。'

                if current_chunk:
                    translated_sentences.append(self.translate_text(current_chunk))

                translated_paragraphs.append(' '.join(translated_sentences))
            else:
                translated_paragraphs.append(self.translate_text(para))

        return '\n\n'.join(translated_paragraphs)

    def translate_chapter(self, chapter) -> None:
        """
        Translate a chapter in-place.

        Args:
            chapter: Chapter object to translate
        """
        # Translate title
        chapter.title = self.translate_text(chapter.title)

        # Translate content
        chapter.content = self.translate_text(chapter.content)

    def translate_chapters(self, chapters: List, show_progress: bool = True) -> List:
        """
        Translate multiple chapters.

        Args:
            chapters: List of Chapter objects
            show_progress: Show progress bar

        Returns:
            List of translated chapters
        """
        if show_progress:
            chapters_iter = tqdm(chapters, desc="Translating chapters", unit="chapter")
        else:
            chapters_iter = chapters

        for chapter in chapters_iter:
            self.translate_chapter(chapter)

        return chapters

    def translate_metadata(self, metadata) -> None:
        """
        Translate novel metadata in-place.

        Args:
            metadata: NovelMetadata object
        """
        if metadata.title:
            metadata.title = self.translate_text(metadata.title)

        if metadata.author:
            # Don't translate author name, just clean it
            pass

        if metadata.description:
            metadata.description = self.translate_text(metadata.description)


class CachedTranslator(Translator):
    """Translator with caching support to avoid re-translating."""

    def __init__(self, source_lang: str = 'zh-CN', target_lang: str = 'en', delay: float = 0.5):
        super().__init__(source_lang, target_lang, delay)
        self.cache = {}

    def translate_text(self, text: str, max_retries: int = 3) -> str:
        """
        Translate text with caching.

        Args:
            text: Text to translate
            max_retries: Maximum number of retry attempts

        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text

        # Check cache
        cache_key = hash(text)
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Translate
        translated = super().translate_text(text, max_retries)

        # Store in cache
        self.cache[cache_key] = translated

        return translated

    def clear_cache(self):
        """Clear translation cache."""
        self.cache.clear()

    def cache_size(self) -> int:
        """Get number of cached translations."""
        return len(self.cache)


class DeepLTranslator(Translator):
    """Translator using DeepL API (better quality than Google Translate)."""

    def __init__(self, api_key: str, source_lang: str = 'ZH', target_lang: str = 'EN-US', delay: float = 0.5):
        """
        Initialize DeepL translator.

        Args:
            api_key: DeepL API key (get from https://www.deepl.com/pro-api)
            source_lang: Source language code (ZH for Chinese)
            target_lang: Target language code (EN-US for US English, EN-GB for British)
            delay: Delay between translation requests in seconds
        """
        # Don't call super().__init__ since we're not using GoogleTranslator
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.delay = delay

        try:
            import deepl
            self.translator = deepl.Translator(api_key)
        except ImportError:
            raise ImportError("DeepL library not installed. Run: pip install deepl")

    def translate_text(self, text: str, max_retries: int = 3) -> str:
        """
        Translate text using DeepL API.

        Args:
            text: Text to translate
            max_retries: Maximum number of retry attempts

        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text

        for attempt in range(max_retries):
            try:
                result = self.translator.translate_text(
                    text,
                    source_lang=self.source_lang,
                    target_lang=self.target_lang
                )
                time.sleep(self.delay)
                return result.text

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"\nDeepL translation error (attempt {attempt + 1}/{max_retries}): {e}")
                    time.sleep(2 ** attempt)
                else:
                    print(f"\nFailed to translate with DeepL after {max_retries} attempts: {e}")
                    return text

        return text


class CachedDeepLTranslator(DeepLTranslator):
    """DeepL translator with caching support."""

    def __init__(self, api_key: str, source_lang: str = 'ZH', target_lang: str = 'EN-US', delay: float = 0.5):
        super().__init__(api_key, source_lang, target_lang, delay)
        self.cache = {}

    def translate_text(self, text: str, max_retries: int = 3) -> str:
        """
        Translate text with caching.

        Args:
            text: Text to translate
            max_retries: Maximum number of retry attempts

        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text

        # Check cache
        cache_key = hash(text)
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Translate
        translated = super().translate_text(text, max_retries)

        # Store in cache
        self.cache[cache_key] = translated

        return translated

    def clear_cache(self):
        """Clear translation cache."""
        self.cache.clear()

    def cache_size(self) -> int:
        """Get number of cached translations."""
        return len(self.cache)
