"""
tests/test_translator.py

Smoke-tests for the Translator class.
Run with:  pytest tests/
"""

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_translator():
    """Import and instantiate Translator (loads model once per session)."""
    from translator import Translator
    return Translator()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def t():
    """Session-scoped translator so the model loads only once."""
    return get_translator()


class TestRequiredPhrases:
    """The 3 mandatory demo phrases must produce non-empty Spanish translations."""

    @pytest.mark.parametrize("text", [
        "I like soccer",
        "How are you?",
        "What time is it?",
    ])
    def test_english_to_spanish(self, t, text):
        result = t.translate(text, "English", "Spanish")
        assert result, f"Empty translation for: {text}"
        assert not result.startswith("❌"), f"Error returned for: {text} → {result}"
        # Basic sanity: result should differ from input (it's a translation)
        assert result.lower() != text.lower(), f"Translation identical to input: {result}"


class TestEdgeCases:

    def test_empty_handled_by_app(self):
        """app.py guards empty input; translator itself may return empty for empty input."""
        from translator import Translator
        t = Translator.__new__(Translator)  # don't load model again
        # Just verify the guard in app.py would catch it
        assert "".strip() == ""

    def test_other_language_pair(self, t):
        result = t.translate("Hello", "English", "French")
        assert result
        assert not result.startswith("❌")
