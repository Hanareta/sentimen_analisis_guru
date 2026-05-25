from __future__ import annotations

from datetime import date
from typing import Any, Optional

import pandas as pd

from src.sentimen_analisis.fetch_data import fetch_reviews
from src.sentimen_analisis.aggregator import Aggregator
from src.sentimen_analisis.risk_scoring import RiskScorer
from src.sentimen_analisis.action_recomender import ActionRecommender

# Inisialisasi sekali — bukan per-request
_aggregator = Aggregator()
_risk_scorer = RiskScorer()
_action_recommender = ActionRecommender()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _run_pipeline(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    analyzed_df, summary_df = _aggregator.run(df)
    risk_df = _risk_scorer.transform(summary_df)
    action_df = _action_recommender.transform(risk_df)

    # Ganti NaN dan Infinity dengan None agar JSON compliant
    analyzed_df = analyzed_df.replace({float("nan"): None, float("inf"): None, float("-inf"): None})
    action_df = action_df.replace({float("nan"): None, float("inf"): None, float("-inf"): None})

    return analyzed_df, action_df


def _raise_if_empty(df: pd.DataFrame, context: str) -> None:
    if df.empty:
        raise ValueError(f"Tidak ada data review untuk {context}")


def _format_single_guru(
    action_df: pd.DataFrame,
    analyzed_df: pd.DataFrame,
) -> dict[str, Any]:
    guru_row = action_df.iloc[0]
    detail = analyzed_df.to_dict(orient="records")
    return {
        "summary": guru_row.to_dict(),
        "detail_reviews": detail,
    }


def _format_multi_guru(
    action_df: pd.DataFrame,
    analyzed_df: pd.DataFrame,
) -> list[dict[str, Any]]:
    results = []
    for _, row in action_df.iterrows():
        nama_guru = row["nama_guru"]
        detail = analyzed_df[
            analyzed_df["nama_guru"] == nama_guru
        ].to_dict(orient="records")
        results.append({
            "summary": row.to_dict(),
            "detail_reviews": detail,
        })
    return results


# ---------------------------------------------------------------------------
# Service functions
# ---------------------------------------------------------------------------

def analyze_guru(nama_guru: str) -> dict[str, Any]:
    df = fetch_reviews(nama_guru=nama_guru)
    _raise_if_empty(df, f"guru '{nama_guru}'")

    analyzed_df, action_df = _run_pipeline(df)

    return {
        "nama_guru": nama_guru,
        **_format_single_guru(action_df, analyzed_df),
    }


def analyze_guru_mapel(nama_guru: str, nama_mapel: str) -> dict[str, Any]:
    df = fetch_reviews(nama_guru=nama_guru, nama_mapel=nama_mapel)
    _raise_if_empty(df, f"guru '{nama_guru}' mapel '{nama_mapel}'")

    analyzed_df, action_df = _run_pipeline(df)

    return {
        "nama_guru": nama_guru,
        "nama_mapel": nama_mapel,
        **_format_single_guru(action_df, analyzed_df),
    }


def analyze_mapel(nama_mapel: str) -> dict[str, Any]:
    df = fetch_reviews(nama_mapel=nama_mapel)
    _raise_if_empty(df, f"mapel '{nama_mapel}'")

    analyzed_df, action_df = _run_pipeline(df)

    return {
        "nama_mapel": nama_mapel,
        "total_guru": len(action_df),
        "hasil": _format_multi_guru(action_df, analyzed_df),
    }


def analyze_periode(tanggal_mulai: date, tanggal_selesai: date) -> dict[str, Any]:
    df = fetch_reviews(tanggal_mulai=tanggal_mulai, tanggal_selesai=tanggal_selesai)
    _raise_if_empty(df, f"periode {tanggal_mulai} s/d {tanggal_selesai}")

    analyzed_df, action_df = _run_pipeline(df)

    return {
        "tanggal_mulai": tanggal_mulai.isoformat(),
        "tanggal_selesai": tanggal_selesai.isoformat(),
        "total_guru": len(action_df),
        "hasil": _format_multi_guru(action_df, analyzed_df),
    }


def analyze_periode_mapel(
    nama_mapel: str,
    tanggal_mulai: date,
    tanggal_selesai: date,
) -> dict[str, Any]:
    df = fetch_reviews(
        nama_mapel=nama_mapel,
        tanggal_mulai=tanggal_mulai,
        tanggal_selesai=tanggal_selesai,
    )
    _raise_if_empty(df, f"mapel '{nama_mapel}' periode {tanggal_mulai} s/d {tanggal_selesai}")

    analyzed_df, action_df = _run_pipeline(df)

    return {
        "nama_mapel": nama_mapel,
        "tanggal_mulai": tanggal_mulai.isoformat(),
        "tanggal_selesai": tanggal_selesai.isoformat(),
        "total_guru": len(action_df),
        "hasil": _format_multi_guru(action_df, analyzed_df),
    }