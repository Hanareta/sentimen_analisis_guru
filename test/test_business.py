import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from src.sentimen_analisis.aggregator import Aggregator
from src.sentimen_analisis.risk_scoring import RiskScorer
from src.sentimen_analisis.action_recomender import ActionRecommender

# Simulasi data review
data = [
    {"nama_guru": "Bu Sari",  "rating": 5, "komentar": "ngajarnya enak bgt gampang dipahami"},
    {"nama_guru": "Bu Sari",  "rating": 4, "komentar": "sabar dan jelas dalam menjelaskan"},
    {"nama_guru": "Bu Sari",  "rating": 2, "komentar": "kadang terlalu cepat ngajarnya"},
    {"nama_guru": "Bu Sari",  "rating": 5, "komentar": "bagus banget cara mengajarnya"},
    {"nama_guru": "Pak Budi", "rating": 1, "komentar": "sering telat masuk kelas"},
    {"nama_guru": "Pak Budi", "rating": 2, "komentar": "galak dan sering marah ga jelas"},
    {"nama_guru": "Pak Budi", "rating": 1, "komentar": "cara ngajarnya susah dipahami"},
    {"nama_guru": "Pak Budi", "rating": 2, "komentar": "tidak perhatian sama murid"},
]

df = pd.DataFrame(data)

# Jalankan pipeline lengkap
aggregator = Aggregator()
risk_scorer = RiskScorer()
action_recommender = ActionRecommender()

_, summary_df = aggregator.run(df)
risk_df = risk_scorer.transform(summary_df)
action_df = action_recommender.transform(risk_df)

print("=" * 60)
print("HASIL BUSINESS LAYER")
print("=" * 60)
for _, row in action_df.iterrows():
    print(f"Guru              : {row['nama_guru']}")
    print(f"Sentimen akhir    : {row['sentimen_akhir']}")
    print(f"Risk score        : {row['risk_score']}")
    print(f"Urgency level     : {row['urgency_level']}")
    print(f"Rekomendasi       : {row['recommended_action']}")
    print(f"Follow up (hari)  : {row['follow_up_days']}")
    print(f"Prioritas         : {row['action_priority']}")
    print()