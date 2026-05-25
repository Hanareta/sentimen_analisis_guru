from __future__ import annotations

import pandas as pd
from src.sentimen_analisis.cleaner import clean
from src.sentimen_analisis.sentiment_analyzer import SentimentAnalyzer
from src.sentimen_analisis.issue_classifier import IssueClassifier


class Aggregator:
    """
    Menggabungkan hasil analisis per komentar
    menjadi summary per guru.
    """

    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.issue_classifier = IssueClassifier()

    # -----------------------------------------------------------------------
    # Step 1 — Analisis tiap komentar
    # -----------------------------------------------------------------------

    def analyze_comments(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analisis sentimen dan issue tiap komentar.

        Input DataFrame wajib punya kolom:
        - nama_guru
        - rating
        - komentar
        """
        results = []

        for _, row in df.iterrows():
            komentar_asli = str(row["komentar"])
            komentar_bersih = clean(komentar_asli)
            rating = int(row["rating"])

            # Analisis sentimen
            sentiment_result = self.sentiment_analyzer.analyze(
                text=komentar_bersih,
                rating=rating,
            )

            # Klasifikasi issue — hanya untuk komentar negatif
            if sentiment_result.sentiment == "negatif":
                issue_result = self.issue_classifier.classify(komentar_bersih)
            else:
                issue_result = None

            results.append({
                "nama_guru": row["nama_guru"],
                "rating": rating,
                "komentar_asli": komentar_asli,
                "komentar_bersih": komentar_bersih,
                "sentimen": sentiment_result.sentiment,
                "skor": sentiment_result.score,
                "kata_kunci": sentiment_result.detected_words,
                "alasan_sentimen": sentiment_result.reasoning,
                "issues": issue_result.detected_issues if issue_result else [],
                "issue_dominan": issue_result.dominant_issue if issue_result else None,
                "alasan_issue": issue_result.reasoning if issue_result else "-",
            })

        return pd.DataFrame(results)

    # -----------------------------------------------------------------------
    # Step 2 — Agregasi per guru
    # -----------------------------------------------------------------------

    def aggregate_per_guru(self, analyzed_df: pd.DataFrame) -> pd.DataFrame:
        """
        Dari hasil analisis tiap komentar, buat summary per guru.
        """
        results = []

        for nama_guru, group in analyzed_df.groupby("nama_guru"):
            total = len(group)

            jumlah_positif = int((group["sentimen"] == "positif").sum())
            jumlah_negatif = int((group["sentimen"] == "negatif").sum())
            jumlah_netral = int((group["sentimen"] == "netral").sum())

            rata_rata_skor = float(group["skor"].mean())
            rata_rata_rating = float(group["rating"].mean())

            sentimen_akhir = self._determine_final_sentiment(
                rata_rata_skor=rata_rata_skor,
                jumlah_positif=jumlah_positif,
                jumlah_negatif=jumlah_negatif,
                total=total,
            )

            issue_dominan = self._get_dominant_issue(group)

            results.append({
                "nama_guru": nama_guru,
                "total_komentar": total,
                "jumlah_positif": jumlah_positif,
                "jumlah_negatif": jumlah_negatif,
                "jumlah_netral": jumlah_netral,
                "persentase_positif": round(jumlah_positif / total * 100, 2),
                "persentase_negatif": round(jumlah_negatif / total * 100, 2),
                "persentase_netral": round(jumlah_netral / total * 100, 2),
                "rata_rata_skor": round(rata_rata_skor, 3),
                "rata_rata_rating": round(rata_rata_rating, 2),
                "sentimen_akhir": sentimen_akhir,
                "issue_dominan": issue_dominan,
            })

        result_df = pd.DataFrame(results)

        # Urutkan dari skor tertinggi ke terendah
        if not result_df.empty:
            result_df = result_df.sort_values(
                by="rata_rata_skor",
                ascending=False,
            ).reset_index(drop=True)

        return result_df

    # -----------------------------------------------------------------------
    # Internal helpers
    # -----------------------------------------------------------------------

    def _determine_final_sentiment(
        self,
        rata_rata_skor: float,
        jumlah_positif: int,
        jumlah_negatif: int,
        total: int,
    ) -> str:
        """
        Tentukan sentimen akhir guru dari semua komentarnya.
        Berdasarkan rata-rata skor dan rasio positif/negatif.
        """
        rasio_positif = jumlah_positif / total
        rasio_negatif = jumlah_negatif / total

        if rata_rata_skor >= 0.3 and rasio_positif >= 0.5:
            return "positif"
        elif rata_rata_skor <= -0.3 and rasio_negatif >= 0.4:
            return "negatif"
        else:
            return "netral"

    def _get_dominant_issue(self, group: pd.DataFrame) -> str | None:
        """
        Cari issue yang paling sering muncul dari semua komentar negatif guru ini.
        """
        issue_counts: dict[str, int] = {}

        for issues in group["issues"]:
            for issue in issues:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1

        if not issue_counts:
            return None

        return max(issue_counts, key=issue_counts.get)

    # -----------------------------------------------------------------------
    # Entry point
    # -----------------------------------------------------------------------

    def run(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Jalankan full pipeline dari DataFrame mentah.

        Returns:
        - analyzed_df  : hasil analisis tiap komentar
        - summary_df   : ringkasan per guru
        """
        analyzed_df = self.analyze_comments(df)
        summary_df = self.aggregate_per_guru(analyzed_df)
        return analyzed_df, summary_df