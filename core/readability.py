"""
Readability & Keyword Density Auditor (Semrush SEO Writing Assistant Engine).
Calculates Flesch Reading Ease Score, Grade Level, sentence length variance, and keyword density metrics.
"""

import re
import math
from typing import Dict, Any, List


class ReadabilityAuditor:
    """Calculates Flesch Reading Ease score, grade level, and keyword density."""

    @staticmethod
    def count_syllables(word: str) -> int:
        """Estimates syllable count for a given word."""
        word = word.lower().strip()
        if not word:
            return 0
        if len(word) <= 3:
            return 1
        word = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', word)
        word = re.sub(r'^y', '', word)
        syllables = len(re.findall(r'[aeiouy]{1,2}', word))
        return max(1, syllables)

    @classmethod
    def calculate_flesch_reading_ease(cls, text: str) -> Dict[str, Any]:
        """
        Calculates Flesch Reading Ease Score (0 - 100) and Flesch-Kincaid Grade Level.
        Formula: 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        """
        # Clean HTML tags if present
        clean_text = re.sub(r'<[^>]+>', ' ', text)
        sentences = [s.strip() for s in re.split(r'[.!?]+', clean_text) if s.strip()]
        words = re.findall(r'\b[a-zA-Z0-9]+\b', clean_text)

        num_sentences = max(1, len(sentences))
        num_words = max(1, len(words))
        num_syllables = sum(cls.count_syllables(w) for w in words)

        asl = num_words / num_sentences  # Average Sentence Length
        asw = num_syllables / num_words  # Average Syllables per Word

        flesch_score = 206.835 - (1.015 * asl) - (84.6 * asw)
        flesch_score = max(0.0, min(100.0, flesch_score))

        # Grade level formula: 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
        grade_level = (0.39 * asl) + (11.8 * asw) - 15.59
        grade_level = max(1.0, grade_level)

        if flesch_score >= 80:
            reading_ease = "Easy (6th Grade)"
        elif flesch_score >= 60:
            reading_ease = "Standard / Conversational (8th-9th Grade)"
        elif flesch_score >= 40:
            reading_ease = "Fairly Difficult (High School)"
        else:
            reading_ease = "Difficult / Academic (College)"

        return {
            "flesch_score": round(flesch_score, 1),
            "grade_level": round(grade_level, 1),
            "reading_ease": reading_ease,
            "word_count": num_words,
            "sentence_count": num_sentences,
            "avg_words_per_sentence": round(asl, 1)
        }

    @staticmethod
    def calculate_keyword_density(text: str, primary_keyword: str, secondary_keywords: List[str] = None) -> Dict[str, Any]:
        """Calculates keyword density percentages and flags over-stuffing or under-optimization."""
        clean_text = re.sub(r'<[^>]+>', ' ', text).lower()
        words = re.findall(r'\b[a-zA-Z0-9]+\b', clean_text)
        total_words = max(1, len(words))

        pk = primary_keyword.lower().strip()
        pk_count = clean_text.count(pk) if pk else 0
        pk_density = (pk_count * len(pk.split()) / total_words) * 100 if pk else 0.0

        if pk_density < 0.5:
            pk_status = "⚠️ Under-optimized (<0.5%)"
        elif pk_density <= 2.5:
            pk_status = "🟢 Optimal (0.5% - 2.5%)"
        else:
            pk_status = "🔴 Over-stuffed (>2.5%)"

        sk_metrics = {}
        if secondary_keywords:
            for sk in secondary_keywords:
                sk_clean = sk.lower().strip()
                if sk_clean:
                    cnt = clean_text.count(sk_clean)
                    dens = (cnt * len(sk_clean.split()) / total_words) * 100
                    sk_metrics[sk] = {
                        "count": cnt,
                        "density_pct": round(dens, 2)
                    }

        return {
            "primary_keyword": primary_keyword,
            "primary_count": pk_count,
            "primary_density_pct": round(pk_density, 2),
            "primary_status": pk_status,
            "secondary_metrics": sk_metrics
        }
