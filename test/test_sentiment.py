import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.sentimen_analisis.cleaner import clean
from src.sentimen_analisis.sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()

test_data = [
    ("pak X ngajarnya enak bgt, gampang dipahami", 5),
    ("bu X galak bgt, sering marah2 ga jelas", 1),
    ("bagusssss banget ngajarnya", 4),
    ("gak ngerti sama sekali cara ngajarnya", 2),
    ("biasa aja sih", 3),
    ("telat mulu tiap masuk kelas", 2),
    ("tidak jelek sih tapi kurang perhatian", 2),
]

for komentar, rating in test_data:
    cleaned = clean(komentar)
    result = analyzer.analyze(cleaned, rating)

    print(f"ASLI    : {komentar}")
    print(f"BERSIH  : {cleaned}")
    print(f"SENTIMEN: {result.sentiment} (score={result.score:.3f})")
    print(f"ALASAN  : {result.reasoning}")
    print()