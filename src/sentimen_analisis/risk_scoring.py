from __future__ import annotations

import pandas as pd
from src.sentimen_analisis.business_config import (
    RISK_WEIGHTS,
    URGENCY_THRESHOLDS,
    ISSUE_WEIGHTS,
)


class RiskScorer:
    """
    Menghitung risk score per guru berdasarkan hasil agregasi.
    Semua threshold dan bobot ada di business_config.py
    """

    def __init__(self):
        self.weights = RISK_WEIGHTS
        self.thresholds = URGENCY_THRESHOLDS
        self.issue_weights = ISSUE_WEIGHTS

    def _calculate_risk_score(self, row: pd.Series) -> float:
        """
        Hitung risk score dari satu baris summary guru.
        Range: 0.0 (tidak berisiko) sampai 1.0 (sangat berisiko)
        """

        # Komponen 1 — persentase negatif (0 sampai 1)
        negatif_component = (row["persentase_negatif"] / 100) * self.weights["persentase_negatif"]

        # Komponen 2 — rata-rata skor sentimen
        # skor range -1 sampai 1, kita flip jadi 0 sampai 1
        # skor -1 (sangat negatif) → 1.0
        # skor  1 (sangat positif) → 0.0
        skor_flipped = (1 - row["rata_rata_skor"]) / 2
        skor_component = skor_flipped * self.weights["rata_rata_skor"]

        # Komponen 3 — rata-rata rating
        # rating range 1 sampai 5, kita balik jadi 0 sampai 1
        # rating 1 (buruk) → 1.0
        # rating 5 (bagus) → 0.0
        rating_flipped = (5 - row["rata_rata_rating"]) / 4
        rating_component = rating_flipped * self.weights["rata_rata_rating"]

        base_score = negatif_component + skor_component + rating_component

        # Bonus risk dari issue dominan
        issue_bonus = 0.0
        issue_dominan = row.get("issue_dominan")
        if issue_dominan and issue_dominan in self.issue_weights:
            issue_bonus = self.issue_weights[issue_dominan] * (row["persentase_negatif"] / 100)

        # Clamp antara 0 dan 1
        final_score = min(1.0, base_score + issue_bonus)
        return round(final_score, 3)

    def _determine_urgency(self, risk_score: float) -> str:
        """Tentukan urgency level dari risk score."""
        if risk_score >= self.thresholds["critical"]:
            return "critical"
        elif risk_score >= self.thresholds["high"]:
            return "high"
        elif risk_score >= self.thresholds["medium"]:
            return "medium"
        else:
            return "low"

    def transform(self, summary_df: pd.DataFrame) -> pd.DataFrame:
        """
        Tambahkan kolom risk_score dan urgency_level ke summary DataFrame.
        """
        df = summary_df.copy()

        df["risk_score"] = df.apply(self._calculate_risk_score, axis=1)
        df["urgency_level"] = df["risk_score"].apply(self._determine_urgency)

        # Urutkan dari risk tertinggi
        df = df.sort_values(by="risk_score", ascending=False).reset_index(drop=True)

        return df