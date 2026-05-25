from __future__ import annotations

from src.sentimen_analisis.data.issue_lexicon import ISSUE_KEYWORDS


class IssueResult:
    """Container hasil klasifikasi issue satu komentar."""

    def __init__(
        self,
        detected_issues: list[str],
        dominant_issue: str | None,
        issue_scores: dict[str, int],
        reasoning: str,
    ):
        self.detected_issues = detected_issues
        self.dominant_issue = dominant_issue
        self.issue_scores = issue_scores
        self.reasoning = reasoning

    def to_dict(self) -> dict:
        return {
            "detected_issues": self.detected_issues,
            "dominant_issue": self.dominant_issue,
            "issue_scores": self.issue_scores,
            "reasoning": self.reasoning,
        }


class IssueClassifier:
    """
    Mendeteksi kategori masalah dari komentar negatif.
    Satu komentar bisa punya lebih dari satu issue.
    """

    def __init__(self):
        self.issue_keywords = ISSUE_KEYWORDS

    def classify(self, text: str) -> IssueResult:
        """
        Deteksi issue dari teks komentar.

        Args:
            text: teks yang sudah dibersihkan (output dari cleaner)

        Returns:
            IssueResult object
        """
        issue_scores: dict[str, int] = {}

        # Hitung berapa kata kunci tiap kategori yang ditemukan
        for issue_name, keywords in self.issue_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    score += 1
            if score > 0:
                issue_scores[issue_name] = score

        # Issue yang terdeteksi (score > 0)
        detected_issues = list(issue_scores.keys())

        # Issue dominan = yang punya skor tertinggi
        dominant_issue = None
        if issue_scores:
            dominant_issue = max(issue_scores, key=issue_scores.get)

        reasoning = self._build_reasoning(detected_issues, issue_scores, dominant_issue)

        return IssueResult(
            detected_issues=detected_issues,
            dominant_issue=dominant_issue,
            issue_scores=issue_scores,
            reasoning=reasoning,
        )

    def _build_reasoning(
        self,
        detected_issues: list[str],
        issue_scores: dict[str, int],
        dominant_issue: str | None,
    ) -> str:
        if not detected_issues:
            return "tidak ada issue terdeteksi"

        scores_str = ", ".join(
            f"{issue}={score}"
            for issue, score in issue_scores.items()
        )
        return f"issues=[{scores_str}], dominant={dominant_issue or '-'}"