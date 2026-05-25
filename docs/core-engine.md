# Core Engine — Dokumentasi Teknis

Core engine adalah bagian yang menganalisis teks komentar siswa.
Terdiri dari 4 layer sequential yang dikelola oleh `Aggregator`.

```
Input (DataFrame mentah)
    ↓
Layer 1: Cleaner          → normalisasi teks
    ↓
Layer 2: Sentiment Analyzer → deteksi sentimen
    ↓
Layer 3: Issue Classifier  → deteksi kategori masalah
    ↓
Layer 4: Aggregator        → ringkasan per guru
    ↓
Output (analyzed_df, summary_df)
```

---

## Layer 1 — Cleaner

**File:** `src/sentimen_analisis/cleaner.py`

**Tujuan:** Normalisasi teks mentah ke bentuk konsisten sebelum dianalisis.

### Urutan Proses

```
"Bu Sari gk jelas bgt ngajarnya galakkkk"
    ↓ lowercase
"bu sari gk jelas bgt ngajarnya galakkkk"
    ↓ hapus karakter berulang
"bu sari gk jelas bgt ngajarnya galak"
    ↓ hapus noise (URL, angka, karakter aneh)
"bu sari gk jelas bgt ngajarnya galak"
    ↓ normalisasi slang
"ibu sari tidak jelas banget ngajarnya galak"
    ↓ normalisasi spasi
"ibu sari tidak jelas banget ngajarnya galak"
```

### Fungsi

| Fungsi | Deskripsi |
|--------|-----------|
| `to_lowercase` | Ubah ke lowercase |
| `remove_repeated_chars` | "bagusssss" → "bagus" |
| `remove_noise` | Hapus URL, angka, karakter aneh |
| `normalize_slang` | "gk" → "tidak", "bgt" → "banget" |
| `normalize_whitespace` | Hapus spasi berlebih |
| `clean` | Entry point — panggil semua fungsi di atas |

### Konfigurasi

Kamus slang ada di `src/sentimen_analisis/data/slang.py`:

```python
SLANG_MAP = {
    "gk": "tidak",
    "bgt": "banget",
    "ngajar": "mengajar",
    ...
}
```

**Cara tambah slang:** Edit `slang.py`, tambah key-value, test dengan `test/test_cleaner.py`

---

## Layer 2 — Sentiment Analyzer

**File:** `src/sentimen_analisis/sentiment_analyzer.py`

**Tujuan:** Analisis sentimen satu komentar — positif, negatif, atau netral.

### Cara Kerja

```
1. Split teks jadi kata-kata
2. Loop tiap kata:
   - Ada di POSITIVE_WORDS? → tambah positive_score
   - Ada di NEGATIVE_WORDS? → tambah negative_score
   - Ada negasi sebelumnya? → flip score
   - Ada intensifier sesudahnya? → kali score dengan multiplier
3. Hitung skor akhir: (pos - neg) / total → range -1 sampai 1
4. Pertimbangkan rating (30% weight)
5. Tentukan sentimen:
   - score >= 0.3  → positif
   - score <= -0.3 → negatif
   - di antara     → netral
```

### Contoh — Negasi

```
Komentar: "tidak jelek"
words = ["tidak", "jelek"]

i=1: "jelek" → NEGATIVE (skor -3)
     cek 2 kata sebelumnya → ada "tidak"
     flip skor → +3

Hasil: positif
```

### Contoh — Intensifier

```
Komentar: "bagus banget"
words = ["bagus", "banget"]

i=0: "bagus" → POSITIVE (skor +3)
     cek kata sesudahnya → ada "banget" (multiplier 1.5)
     skor akhir: 3 × 1.5 = 4.5

Hasil: positif (lebih kuat)
```

### Konfigurasi

File: `src/sentimen_analisis/data/sentiment_lexicon.py`

```python
POSITIVE_WORDS = {
    "bagus": 3,
    "jelas": 2,
    "sabar": 2,
    ...
}

NEGATIVE_WORDS = {
    "galak": -2,
    "terlambat": -2,
    "susah dipahami": -2,
    ...
}

NEGATION_WORDS = {"tidak", "gak", "ga", "kurang", ...}

INTENSIFIER_WORDS = {
    "banget": 1.5,
    "sangat": 1.5,
    ...
}
```

---

## Layer 3 — Issue Classifier

**File:** `src/sentimen_analisis/issue_classifier.py`

**Tujuan:** Deteksi kategori masalah dari komentar negatif.

### Kategori Issue

| Issue | Contoh Keyword |
|-------|---------------|
| `kedisiplinan` | terlambat, jarang masuk, bolos |
| `cara_mengajar` | tidak jelas, susah dipahami, membosankan |
| `sikap` | galak, kasar, tidak perhatian |
| `penguasaan_materi` | tidak menguasai, salah menjelaskan |
| `komunikasi` | tidak responsif, susah dihubungi |

### Cara Kerja

```
Komentar: "sering terlambat dan galak"

Loop tiap kategori:
- kedisiplinan:  "terlambat" ditemukan → score=1
- cara_mengajar: tidak ada → score=0
- sikap:         "galak" ditemukan → score=1
- ...

detected_issues = ["kedisiplinan", "sikap"]
dominant_issue  = "kedisiplinan"  (score sama, ambil urutan pertama)
```

**Catatan:** Issue hanya diklasifikasi untuk komentar negatif.

### Konfigurasi

File: `src/sentimen_analisis/data/issue_lexicon.py`

```python
ISSUE_KEYWORDS = {
    "kedisiplinan": ["terlambat", "telat", "jarang masuk", ...],
    "cara_mengajar": ["tidak jelas", "susah dipahami", ...],
    ...
}
```

---

## Layer 4 — Aggregator

**File:** `src/sentimen_analisis/aggregator.py`

**Tujuan:** Gabungkan hasil analisis per komentar menjadi summary per guru.

### Dua Tahap

#### Tahap 1: analyze_comments()

Loop semua komentar, jalankan layer 1-3 untuk masing-masing.

```
Input:
┌──────────┬────────┬─────────────────┐
│ nama_guru│ rating │ komentar        │
├──────────┼────────┼─────────────────┤
│ Bu Sari  │   5    │ enak bgt        │
│ Bu Sari  │   2    │ terlalu cepat   │
│ Pak Budi │   1    │ galak dan marah │
└──────────┴────────┴─────────────────┘

Output:
┌──────────┬─────────┬────────┬──────────────┐
│ nama_guru│ sentimen│  skor  │ issues       │
├──────────┼─────────┼────────┼──────────────┤
│ Bu Sari  │ positif │  1.000 │ []           │
│ Bu Sari  │ negatif │ -1.000 │[cara_mengajar]│
│ Pak Budi │ negatif │ -1.000 │[sikap]       │
└──────────┴─────────┴────────┴──────────────┘
```

#### Tahap 2: aggregate_per_guru()

Groupby `nama_guru`, hitung statistik.

```
Output:
┌──────────┬───────┬──────────┬───────────────┬──────────────┐
│ nama_guru│ total │ positif  │ sentimen_akhir│ issue_dominan│
├──────────┼───────┼──────────┼───────────────┼──────────────┤
│ Bu Sari  │   2   │ 1 (50%)  │   netral      │ cara_mengajar│
│ Pak Budi │   1   │ 0 (0%)   │   negatif     │ sikap        │
└──────────┴───────┴──────────┴───────────────┴──────────────┘
```

### Logika Sentimen Akhir

```python
if rata_rata_skor >= 0.3 and rasio_positif >= 0.5:
    return "positif"
elif rata_rata_skor <= -0.3 and rasio_negatif >= 0.4:
    return "negatif"
else:
    return "netral"
```

### Entry Point

```python
def run(df) -> tuple[pd.DataFrame, pd.DataFrame]:
    analyzed_df = self.analyze_comments(df)
    summary_df  = self.aggregate_per_guru(analyzed_df)
    return analyzed_df, summary_df
```

---

## Testing

```bash
uv run python test/test_cleaner.py      # Layer 1
uv run python test/test_sentiment.py    # Layer 2
uv run python test/test_issue.py        # Layer 3
uv run python test/test_aggregator.py   # Layer 4
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Sentimen "tidak jelek" = negatif | Negasi tidak terdeteksi | Pastikan "tidak" ada di NEGATION_WORDS |
| "susah dipahami" = netral | Kata tidak ada di sentiment lexicon | Tambah ke NEGATIVE_WORDS |
| Issue tidak terdeteksi | Keyword tidak ada di issue lexicon | Tambah keyword ke ISSUE_KEYWORDS |
