from __future__ import annotations

from src.sentimen_analisis.data.sentiment_lexicon import (
    POSITIVE_WORDS,
    NEGATIVE_WORDS,
    NEGATION_WORDS,
    INTENSIFIER_WORDS,
)


class SentimentResult:
    """Container hasil analisis satu komentar."""

    def __init__(
        self,
        sentiment: str,
        score: float,
        positive_score: float,
        negative_score: float,
        detected_words: list[str],
        reasoning: str,
    ):
        self.sentiment = sentiment
        self.score = score
        self.positive_score = positive_score
        self.negative_score = negative_score
        self.detected_words = detected_words
        self.reasoning = reasoning

    def to_dict(self) -> dict:
        return {
            "sentiment": self.sentiment,
            "score": round(self.score, 3),
            "positive_score": round(self.positive_score, 3),
            "negative_score": round(self.negative_score, 3),
            "detected_words": self.detected_words,
            "reasoning": self.reasoning,
        }


class SentimentAnalyzer:
    """Rule-based sentiment analyzer untuk Bahasa Indonesia."""

    def __init__(self):
        self.positive_words = POSITIVE_WORDS
        self.negative_words = NEGATIVE_WORDS
        self.negation_words = NEGATION_WORDS
        self.intensifier_words = INTENSIFIER_WORDS

    def _check_negation(self, words: list[str], word_index: int) -> bool:
        """Cek apakah kata di sebelum index ada negasi."""
        if word_index == 0:
            return False
        # Cek 1-2 kata sebelumnya
        for i in range(max(0, word_index - 2), word_index):
            if words[i] in self.negation_words:
                return True
        return False

    def _get_intensifier_multiplier(self, words: list[str], word_index: int) -> float:
        """Cek apakah ada intensifier (banget, sangat) setelah kata."""
        multiplier = 1.0
        if word_index < len(words) - 1:
            next_word = words[word_index + 1]
            if next_word in self.intensifier_words:
                multiplier = self.intensifier_words[next_word]
        return multiplier

    def analyze(self, text: str, rating: int = None) -> SentimentResult:
        """
        Analisis sentimen dari teks komentar.

        Args:
            text: teks yang sudah dibersihkan (output dari cleaner)
            rating: rating siswa (1-5), optional untuk bobot tambahan

        Returns:
            SentimentResult object
        """
        words = text.split()
        positive_score = 0.0
        negative_score = 0.0
        detected_words = []

        # Hitung skor positif dan negatif
        for i, word in enumerate(words):
            if word in self.positive_words:
                has_negation = self._check_negation(words, i)
                multiplier = self._get_intensifier_multiplier(words, i)
                word_score = self.positive_words[word] * multiplier

                if has_negation:
                    negative_score += word_score
                    detected_words.append(f"tidak {word}")
                else:
                    positive_score += word_score
                    detected_words.append(word)

            elif word in self.negative_words:
                has_negation = self._check_negation(words, i)
                multiplier = self._get_intensifier_multiplier(words, i)
                word_score = self.negative_words[word] * multiplier

                if has_negation:
                    positive_score += abs(word_score)
                    detected_words.append(f"tidak {word}")
                else:
                    negative_score += abs(word_score)
                    detected_words.append(word)

        # Hitung skor akhir (-1 sampai 1)
        total = positive_score + negative_score
        if total == 0:
            final_score = 0.0
        else:
            final_score = (positive_score - negative_score) / total

        # Tentukan sentimen berdasarkan skor dan rating
        sentiment = self._determine_sentiment(final_score, rating)
        reasoning = self._build_reasoning(
            positive_score, negative_score, detected_words, final_score, rating
        )

        return SentimentResult(
            sentiment=sentiment,
            score=final_score,
            positive_score=positive_score,
            negative_score=negative_score,
            detected_words=detected_words,
            reasoning=reasoning,
        )

    def _determine_sentiment(self, score: float, rating: int = None) -> str:
        """Tentukan sentimen berdasarkan skor dan rating."""
        # Rating memiliki weight 30%, skor text 70%
        if rating:
            rating_sentiment_score = (rating - 1) / 4  # normalize 1-5 to -1 to 1
            combined_score = (score * 0.7) + (rating_sentiment_score * 0.3)
        else:
            combined_score = score

        if combined_score >= 0.3:
            return "positif"
        elif combined_score <= -0.3:
            return "negatif"
        else:
            return "netral"

    def _build_reasoning(
        self,
        pos_score: float,
        neg_score: float,
        detected_words: list,
        final_score: float,
        rating: int = None,
    ) -> str:
        """Buat penjelasan mengapa sentimen ini."""
        words_str = ", ".join(detected_words) if detected_words else "tidak ada kata kunci"
        rating_str = f", rating={rating}" if rating else ""
        return (
            f"pos={pos_score:.2f}, neg={neg_score:.2f}, "
            f"score={final_score:.3f}{rating_str}, kata_kunci=[{words_str}]"
        )