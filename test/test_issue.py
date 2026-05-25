import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.sentimen_analisis.cleaner import clean
from src.sentimen_analisis.issue_classifier import IssueClassifier

classifier = IssueClassifier()

test_data = [
    "pak X sering telat masuk kelas",
    "cara ngajarnya susah dipahami dan terlalu cepat",
    "galak banget sering marah tidak perhatian sama murid",
    "sepertinya tidak menguasai materi dengan baik",
    "susah dihubungi kalau mau tanya diluar kelas",
    "guru yang baik dan jelas dalam mengajar",       # positif, harusnya tidak ada issue
    "sering telat dan galak kalau ditanya",          # dua issue sekaligus
]

for komentar in test_data:
    cleaned = clean(komentar)
    result = classifier.classify(cleaned)

    print(f"ASLI    : {komentar}")
    print(f"BERSIH  : {cleaned}")
    print(f"ISSUES  : {result.detected_issues}")
    print(f"DOMINAN : {result.dominant_issue}")
    print(f"ALASAN  : {result.reasoning}")
    print()