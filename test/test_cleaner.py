import sys
from pathlib import Path

# Tambahkan root project ke path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.sentimen_analisis.cleaner import clean

contoh = [
    "pak X ngajarnya enak bgt, gampang dipahami",
    "bu X galak bgt, sering marah2 ga jelas",
    "bagusssss banget ngajarnya",
    "gak ngerti sama sekali cara ngajarnya",
    "biasa aja sih",
    "telat mulu tiap masuk kelas",
]

for komentar in contoh:
    print(f"ASLI  : {komentar}")
    print(f"BERSIH: {clean(komentar)}")
    print()