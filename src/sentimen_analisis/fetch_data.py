from __future__ import annotations

from datetime import date
from typing import Optional

import pandas as pd

# ---------------------------------------------------------------------------
# Mock data — mirip response dari SIAKAD API
# Nanti diganti dengan koneksi ke SIAKAD asli
# ---------------------------------------------------------------------------

MOCK_REVIEWS = [
    # Bu Sari — Matematika
    {"tanggal": "2024-01-10", "jam": "08:00", "nama_murid": "Andi",  "nama_guru": "Bu Sari",  "nama_mapel": "Matematika", "rating": 5, "komentar": "ngajarnya enak bgt gampang dipahami"},
    {"tanggal": "2024-01-11", "jam": "08:00", "nama_murid": "Budi",  "nama_guru": "Bu Sari",  "nama_mapel": "Matematika", "rating": 4, "komentar": "sabar dan jelas dalam menjelaskan"},
    {"tanggal": "2024-01-12", "jam": "08:00", "nama_murid": "Cici",  "nama_guru": "Bu Sari",  "nama_mapel": "Matematika", "rating": 2, "komentar": "kadang terlalu cepat ngajarnya"},
    {"tanggal": "2024-01-13", "jam": "08:00", "nama_murid": "Dedi",  "nama_guru": "Bu Sari",  "nama_mapel": "Matematika", "rating": 5, "komentar": "bagus banget cara mengajarnya"},
    # Bu Sari — Fisika
    {"tanggal": "2024-02-10", "jam": "10:00", "nama_murid": "Eka",   "nama_guru": "Bu Sari",  "nama_mapel": "Fisika",     "rating": 4, "komentar": "penjelasannya mudah dimengerti"},
    {"tanggal": "2024-02-11", "jam": "10:00", "nama_murid": "Fajar", "nama_guru": "Bu Sari",  "nama_mapel": "Fisika",     "rating": 3, "komentar": "biasa aja sih"},
    # Pak Budi — Matematika
    {"tanggal": "2024-01-10", "jam": "09:00", "nama_murid": "Gina",  "nama_guru": "Pak Budi", "nama_mapel": "Matematika", "rating": 1, "komentar": "sering telat masuk kelas"},
    {"tanggal": "2024-01-11", "jam": "09:00", "nama_murid": "Hana",  "nama_guru": "Pak Budi", "nama_mapel": "Matematika", "rating": 2, "komentar": "galak dan sering marah ga jelas"},
    {"tanggal": "2024-01-12", "jam": "09:00", "nama_murid": "Ivan",  "nama_guru": "Pak Budi", "nama_mapel": "Matematika", "rating": 1, "komentar": "cara ngajarnya susah dipahami"},
    {"tanggal": "2024-01-13", "jam": "09:00", "nama_murid": "Julia", "nama_guru": "Pak Budi", "nama_mapel": "Matematika", "rating": 2, "komentar": "tidak perhatian sama murid"},
    # Pak Budi — Fisika
    {"tanggal": "2024-02-10", "jam": "11:00", "nama_murid": "Kevin", "nama_guru": "Pak Budi", "nama_mapel": "Fisika",     "rating": 2, "komentar": "susah dipahami cara ngajarnya"},
    {"tanggal": "2024-02-11", "jam": "11:00", "nama_murid": "Lisa",  "nama_guru": "Pak Budi", "nama_mapel": "Fisika",     "rating": 1, "komentar": "jarang masuk kelas"},
    # Bu Rini — Fisika
    {"tanggal": "2024-01-15", "jam": "13:00", "nama_murid": "Miko",  "nama_guru": "Bu Rini",  "nama_mapel": "Fisika",     "rating": 5, "komentar": "sangat sabar dan perhatian sama murid"},
    {"tanggal": "2024-01-16", "jam": "13:00", "nama_murid": "Nana",  "nama_guru": "Bu Rini",  "nama_mapel": "Fisika",     "rating": 4, "komentar": "jelas banget ngajarnya enak"},
    {"tanggal": "2024-01-17", "jam": "13:00", "nama_murid": "Omar",  "nama_guru": "Bu Rini",  "nama_mapel": "Fisika",     "rating": 5, "komentar": "bagus cara mengajarnya mudah dipahami"},
]


def fetch_reviews(
    nama_guru: Optional[str] = None,
    nama_mapel: Optional[str] = None,
    tanggal_mulai: Optional[date] = None,
    tanggal_selesai: Optional[date] = None,
) -> pd.DataFrame:
    """
    Ambil data review berdasarkan filter.
    Saat ini menggunakan mock data — nanti diganti koneksi SIAKAD.
    """
    df = pd.DataFrame(MOCK_REVIEWS)
    df["tanggal"] = pd.to_datetime(df["tanggal"]).dt.date

    if nama_guru:
        df = df[df["nama_guru"].str.lower() == nama_guru.lower()]

    if nama_mapel:
        df = df[df["nama_mapel"].str.lower() == nama_mapel.lower()]

    if tanggal_mulai:
        df = df[df["tanggal"] >= tanggal_mulai]

    if tanggal_selesai:
        df = df[df["tanggal"] <= tanggal_selesai]

    return df.reset_index(drop=True)