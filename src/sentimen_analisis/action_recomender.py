from __future__ import annotations

import pandas as pd
from src.sentimen_analisis.business_config import (
    ACTION_MAP,
    ISSUE_ACTION_NOTES,
)


class ActionRecommender:
    """
    Menyusun rekomendasi tindakan per guru berdasarkan urgency level.
    Semua mapping aksi ada di business_config.py
    """

    def __init__(self):
        self.action_map = ACTION_MAP
        self.issue_notes = ISSUE_ACTION_NOTES

    def _build_recommendation(self, row: pd.Series) -> dict:
        urgency = row["urgency_level"]
        action_config = self.action_map[urgency]

        # Issue note hanya untuk medium ke atas
        issue_note = ""
        if urgency in ("medium", "high", "critical"):
            issue_dominan = row.get("issue_dominan")
            issue_note = self.issue_notes.get(issue_dominan, "") if issue_dominan else ""

        full_action = action_config["action"]
        if issue_note:
            full_action = f"{full_action} {issue_note}"

        return {
            "recommended_action": full_action,
            "follow_up_days": action_config["follow_up_days"],
            "action_priority": action_config["priority"],
        }

    def transform(self, risk_df: pd.DataFrame) -> pd.DataFrame:
        """
        Tambahkan kolom rekomendasi ke risk DataFrame.
        """
        df = risk_df.copy()

        recommendations = df.apply(self._build_recommendation, axis=1)
        recommendations_df = pd.DataFrame(recommendations.tolist())

        df["recommended_action"] = recommendations_df["recommended_action"].values
        df["follow_up_days"] = recommendations_df["follow_up_days"].values
        df["action_priority"] = recommendations_df["action_priority"].values

        return df