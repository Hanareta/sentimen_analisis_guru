# Business Layer — Dokumentasi Teknis

Business layer menginterpretasi hasil analisis sentimen menjadi keputusan bisnis — seberapa berisiko seorang guru dan tindakan apa yang perlu diambil.

Terdiri dari dua komponen:

```
Input (summary_df dari Core Engine)
    ↓
RiskScorer          → hitung risk score per guru
    ↓
ActionRecommender   → susun rekomendasi tindakan
    ↓
Output (action_df dengan risk_score, urgency_level, recommended_action)
```

---

## Konfigurasi

**File:** `src/sentimen_analisis/business_config.py`

Semua threshold, bobot, dan mapping aksi ada di sini. Ubah file ini untuk menyesuaikan kebijakan sekolah — tanpa menyentuh logika utama.

### Bobot Risk Score

```python
RISK_WEIGHTS = {
    "persentase_negatif": 0.5,  # 50% dari persentase komentar negatif
    "rata_rata_skor": 0.3,       # 30% dari rata-rata sentiment score
    "rata_rata_rating": 0.2,     # 20% dari rata-rata rating
}
```

Total bobot harus selalu = 1.0

### Threshold Urgency

```python
URGENCY_THRESHOLDS = {
    "critical": 0.8,   # risk_score >= 0.8
    "high":     0.6,   # risk_score >= 0.6
    "medium":   0.3,   # risk_score >= 0.3
    "low":      0.0,   # risk_score < 0.3
}
```

### Bobot Issue

Issue tertentu menaikkan risk score jika terdeteksi:

```python
ISSUE_WEIGHTS = {
    "kedisiplinan":       0.2,
    "cara_mengajar":      0.15,
    "sikap":              0.2,
    "penguasaan_materi":  0.1,
    "komunikasi":         0.1,
}
```

### Action Map

```python
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
```

### Issue Action Notes

Catatan tambahan per issue dominan — hanya ditampilkan untuk urgency `medium` ke atas:

```python
ISSUE_ACTION_NOTES = {
    "kedisiplinan":      "Fokus pada perbaikan kehadiran dan ketepatan waktu.",
    "cara_mengajar":     "Pertimbangkan pelatihan metode pengajaran.",
    "sikap":             "Perlu konseling terkait hubungan guru-siswa.",
    "penguasaan_materi": "Evaluasi kompetensi materi dan berikan pelatihan.",
    "komunikasi":        "Tingkatkan aksesibilitas guru di luar jam mengajar.",
}
```

---

## Risk Scorer

**File:** `src/sentimen_analisis/risk_scoring.py`

**Tujuan:** Menghitung risk score per guru dari summary DataFrame.

### Formula

```
risk_score = (persentase_negatif/100 × bobot_negatif)
           + ((1 - rata_rata_skor) / 2 × bobot_skor)
           + ((5 - rata_rata_rating) / 4 × bobot_rating)
           + (issue_bonus)

issue_bonus = issue_weight[issue_dominan] × (persentase_negatif/100)

final_score = min(1.0, risk_score)  ← clamp maksimal 1.0
```

### Contoh Perhitungan

Pak Budi:
```
persentase_negatif = 75%
rata_rata_skor     = -1.0
rata_rata_rating   = 1.5
issue_dominan      = "sikap"

negatif_component  = 0.75 × 0.5 = 0.375
skor_component     = ((1 - (-1.0)) / 2) × 0.3 = 1.0 × 0.3 = 0.3
rating_component   = ((5 - 1.5) / 4) × 0.2 = 0.875 × 0.2 = 0.175
base_score         = 0.375 + 0.3 + 0.175 = 0.85

issue_bonus        = 0.2 × 0.75 = 0.15
final_score        = min(1.0, 0.85 + 0.15) = 1.0
urgency_level      = "critical"
```

### Output Kolom Baru

| Kolom | Type | Deskripsi |
|-------|------|-----------|
| `risk_score` | float (0-1) | Skor risiko guru |
| `urgency_level` | string | "low", "medium", "high", "critical" |

---

## Action Recommender

**File:** `src/sentimen_analisis/action_recomender.py`

**Tujuan:** Menyusun rekomendasi tindakan berdasarkan urgency level dan issue dominan.

### Logika

```
1. Ambil urgency_level dari risk_df
2. Lookup ACTION_MAP[urgency_level] → dapat action, follow_up_days, priority
3. Jika urgency medium ke atas:
   - Ambil issue_dominan
   - Lookup ISSUE_ACTION_NOTES[issue_dominan]
   - Gabungkan ke action string
4. Return rekomendasi lengkap
```

### Contoh Output

Pak Budi (urgency: critical, issue: cara_mengajar):
```
recommended_action = "Panggil guru untuk evaluasi mendesak.
                      Pertimbangkan pelatihan metode pengajaran."
follow_up_days     = 7
action_priority    = 1
```

Bu Sari (urgency: low):
```
recommended_action = "Tidak ada tindakan khusus diperlukan"
follow_up_days     = 90
action_priority    = 4
```

### Output Kolom Baru

| Kolom | Type | Deskripsi |
|-------|------|-----------|
| `recommended_action` | string | Tindakan yang direkomendasikan |
| `follow_up_days` | int | Kapan follow-up berikutnya (hari) |
| `action_priority` | int | Prioritas tindakan (1=paling mendesak) |

---

## Testing

```bash
uv run python test/test_business.py
```

Contoh output yang diharapkan:

```
Guru              : Pak Budi
Sentimen akhir    : negatif
Risk score        : 1.0
Urgency level     : critical
Rekomendasi       : Panggil guru untuk evaluasi mendesak. ...
Follow up (hari)  : 7
Prioritas         : 1

Guru              : Bu Sari
Sentimen akhir    : positif
Risk score        : 0.242
Urgency level     : low
Rekomendasi       : Tidak ada tindakan khusus diperlukan
Follow up (hari)  : 90
Prioritas         : 4
```

---

## Cara Kustomisasi

### Ubah threshold urgency

Edit `URGENCY_THRESHOLDS` di `business_config.py`:

```python
# Contoh: lebih agresif dalam mendeteksi masalah
URGENCY_THRESHOLDS = {
    "critical": 0.7,   # diturunkan dari 0.8
    "high":     0.5,   # diturunkan dari 0.6
    "medium":   0.2,   # diturunkan dari 0.3
    "low":      0.0,
}
```

### Ubah bobot faktor

Edit `RISK_WEIGHTS` — pastikan total tetap 1.0:

```python
# Contoh: lebih menekankan rating dari siswa
RISK_WEIGHTS = {
    "persentase_negatif": 0.4,
    "rata_rata_skor": 0.2,
    "rata_rata_rating": 0.4,  # dinaikkan
}
```

### Ubah teks rekomendasi

Edit `ACTION_MAP` dan `ISSUE_ACTION_NOTES` sesuai kebijakan sekolah.
