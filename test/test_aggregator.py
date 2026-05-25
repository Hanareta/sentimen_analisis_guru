import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from src.sentimen_analisis.aggregator import Aggregator

# Simulasi data review dari SIAKAD
data = [
    {"nama_guru": "Bu Sari", "rating": 5, "komentar": "ngajarnya enak bgt gampang dipahami"},
    {"nama_guru": "Bu Sari", "rating": 4, "komentar": "sabar dan jelas dalam menjelaskan"},
    {"nama_guru": "Bu Sari", "rating": 2, "komentar": "kadang terlalu cepat ngajarnya"},
    {"nama_guru": "Bu Sari", "rating": 5, "komentar": "bagus banget cara mengajarnya"},
    {"nama_guru": "Pak Budi", "rating": 1, "komentar": "sering telat masuk kelas"},
    {"nama_guru": "Pak Budi", "rating": 2, "komentar": "galak dan sering marah ga jelas"},
    {"nama_guru": "Pak Budi", "rating": 1, "komentar": "cara ngajarnya susah dipahami"},
    {"nama_guru": "Pak Budi", "rating": 2, "komentar": "tidak perhatian sama murid"},
]

df = pd.DataFrame(data)
aggregator = Aggregator()

analyzed_df, summary_df = aggregator.run(df)

print("=" * 60)
print("HASIL ANALISIS TIAP KOMENTAR")
print("=" * 60)
for _, row in analyzed_df.iterrows():
    print(f"Guru    : {row['nama_guru']}")
    print(f"Komentar: {row['komentar_asli']}")
    print(f"Sentimen: {row['sentimen']} (skor={row['skor']:.3f})")
    print(f"Issues  : {row['issues']}")
    print()

print("=" * 60)
print("SUMMARY PER GURU")
print("=" * 60)
for _, row in summary_df.iterrows():
    print(f"Guru             : {row['nama_guru']}")
    print(f"Total komentar   : {row['total_komentar']}")
    print(f"Positif          : {row['jumlah_positif']} ({row['persentase_positif']}%)")
    print(f"Negatif          : {row['jumlah_negatif']} ({row['persentase_negatif']}%)")
    print(f"Rata-rata rating : {row['rata_rata_rating']}")
    print(f"Sentimen akhir   : {row['sentimen_akhir']}")
    print(f"Issue dominan    : {row['issue_dominan']}")
    print()