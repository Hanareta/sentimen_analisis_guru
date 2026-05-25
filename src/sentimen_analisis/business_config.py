# -----------------------------------------------------------------------
# Bobot untuk menghitung risk score
# Total bobot harus = 1.0
# -----------------------------------------------------------------------
RISK_WEIGHTS = {
    "persentase_negatif": 0.5,   # 50% dari skor negatif
    "rata_rata_skor": 0.3,        # 30% dari skor sentimen
    "rata_rata_rating": 0.2,      # 20% dari rating
}

# -----------------------------------------------------------------------
# Threshold urgency level
# -----------------------------------------------------------------------
URGENCY_THRESHOLDS = {
    "critical": 0.8,
    "high": 0.6,
    "medium": 0.3,
    "low": 0.0,
}

# -----------------------------------------------------------------------
# Bobot tambahan per issue
# Issue tertentu bisa menaikkan risk score
# -----------------------------------------------------------------------
ISSUE_WEIGHTS = {
    "kedisiplinan": 0.2,
    "cara_mengajar": 0.15,
    "sikap": 0.2,
    "penguasaan_materi": 0.1,
    "komunikasi": 0.1,
}

# -----------------------------------------------------------------------
# Rekomendasi tindakan per urgency level
# Bisa dikustomisasi per sekolah
# -----------------------------------------------------------------------
ACTION_MAP = {
    "critical": {
        "action": "Panggil guru untuk evaluasi mendesak",
        "follow_up_days": 7,
        "priority": 1,
    },
    "high": {
        "action": "Jadwalkan coaching dan monitoring ketat",
        "follow_up_days": 14,
        "priority": 2,
    },
    "medium": {
        "action": "Berikan feedback dan pantau perkembangan",
        "follow_up_days": 30,
        "priority": 3,
    },
    "low": {
        "action": "Tidak ada tindakan khusus diperlukan",
        "follow_up_days": 90,
        "priority": 4,
    },
}

# -----------------------------------------------------------------------
# Pesan tambahan per issue dominan
# Ditambahkan ke action recommendation
# -----------------------------------------------------------------------
ISSUE_ACTION_NOTES = {
    "kedisiplinan": "Fokus pada perbaikan kehadiran dan ketepatan waktu.",
    "cara_mengajar": "Pertimbangkan pelatihan metode pengajaran.",
    "sikap": "Perlu konseling terkait hubungan guru-siswa.",
    "penguasaan_materi": "Evaluasi kompetensi materi dan berikan pelatihan.",
    "komunikasi": "Tingkatkan aksesibilitas guru di luar jam mengajar.",
}