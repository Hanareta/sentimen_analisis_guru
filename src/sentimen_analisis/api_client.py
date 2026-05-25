from __future__ import annotations

from datetime import date
from typing import Optional

import httpx
import pandas as pd


# ---------------------------------------------------------------------------
# Konfigurasi — nanti pindah ke config.py / .env
# ---------------------------------------------------------------------------

BASE_URL = "https://siakadmu.smktekmuh.sch.id/api"
API_TOKEN = "your_token_here"

# Kolom yang diperlukan per endpoint
KOLOM_PER_ENDPOINT = {
    "guru":          ["nama_guru", "rating", "komentar"],
    "guru_mapel":    ["nama_guru", "nama_mapel", "rating", "komentar"],
    "mapel":         ["nama_guru", "nama_mapel", "rating", "komentar"],
    "periode":       ["nama_guru", "tanggal", "rating", "komentar"],
    "periode_mapel": ["nama_guru", "nama_mapel", "tanggal", "rating", "komentar"],
}


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class SiakadClient:

    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json",
        }

    def get_reviews(
        self,
        nama_guru: Optional[str] = None,
        nama_mapel: Optional[str] = None,
        tanggal_mulai: Optional[date] = None,
        tanggal_selesai: Optional[date] = None,
        endpoint: str = "guru",
    ) -> pd.DataFrame:

        # Susun query params
        params = {}
        if nama_guru:
            params["nama_guru"] = nama_guru
        if nama_mapel:
            params["nama_mapel"] = nama_mapel
        if tanggal_mulai:
            params["tanggal_mulai"] = tanggal_mulai.isoformat()
        if tanggal_selesai:
            params["tanggal_selesai"] = tanggal_selesai.isoformat()

        # Minta kolom tertentu saja ke SIAKAD
        kolom = KOLOM_PER_ENDPOINT.get(endpoint, ["nama_guru", "rating", "komentar"])
        params["fields"] = ",".join(kolom)

        # Hit SIAKAD
        with httpx.Client(timeout=30) as client:
            response = client.get(
                f"{self.base_url}/reviews",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            data = response.json()

        # Konversi ke DataFrame dan filter kolom
        df = pd.DataFrame(data)
        df = df[kolom]  # ← pastikan kolom sesuai meski SIAKAD return lebih

        return df.reset_index(drop=True)