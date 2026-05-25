# Sentiment Analysis API — Dokumentasi

API untuk analisis sentimen guru berdasarkan review siswa SMK.

## Fitur Utama

- **Sentiment Analysis** — deteksi apakah komentar positif, negatif, atau netral
- **Issue Classification** — identifikasi kategori masalah (kedisiplinan, cara mengajar, sikap, dsb)
- **Risk Scoring** — hitung tingkat risiko per guru
- **Action Recommendation** — rekomendasi tindakan berdasarkan risk score
- **Agregasi Per Guru** — ringkasan performa guru dari semua komentarnya
- **Multi-endpoint** — analisis per guru, per mata pelajaran, per periode waktu, atau kombinasinya

## Teknologi

- **FastAPI** — framework API
- **Pandas** — pengolahan data
- **Pydantic** — validasi input
- **httpx** — HTTP client ke SIAKAD
- **Rule-based NLP** — analisis sentimen berbasis leksikon Bahasa Indonesia

## Struktur Project

```
.
├── app/                              # Layer FastAPI
│   ├── main.py                       # App utama
│   ├── routes/
│   │   └── analyze_routes.py         # Endpoint definition
│   ├── schemas/
│   │   └── analyze_schema.py         # Query params schema
│   ├── services/
│   │   └── analyze_service.py        # Orkestrasi business logic
│   └── utils/
│       └── response.py               # Helper response formatting
├── src/
│   └── sentimen_analisis/            # Core engine & business layer
│       ├── cleaner.py                # Text cleaning
│       ├── sentiment_analyzer.py     # Sentiment detection
│       ├── issue_classifier.py       # Issue categorization
│       ├── aggregator.py             # Result aggregation
│       ├── risk_scoring.py           # Risk score calculation
│       ├── action_recomender.py      # Action recommendation
│       ├── business_config.py        # Konfigurasi threshold & bobot
│       ├── fetch_data.py             # Data fetching (mock / SIAKAD)
│       ├── api_client.py             # HTTP client ke SIAKAD
│       └── data/
│           ├── slang.py              # Slang normalization lexicon
│           ├── sentiment_lexicon.py  # Sentiment words lexicon
│           └── issue_lexicon.py      # Issue keywords lexicon
├── test/                             # Unit tests
├── docs/                             # Dokumentasi
├── main.py                           # Entry point
└── pyproject.toml                    # Project config
```

## Quick Start

### 1. Setup

```bash
git clone <repo>
cd sentiment-api
uv sync
```

### 2. Jalankan Server

```bash
uv run python main.py
```

Server akan berjalan di `http://localhost:8000`

### 3. Akses Documentation

Buka `http://localhost:8000/docs` untuk interactive API documentation (Swagger UI).

## Dokumentasi Lengkap

- **[Arsitektur](./arsitektur.md)** — alur system secara keseluruhan
- **[Core Engine](./core-engine.md)** — cleaner, sentiment analyzer, issue classifier, aggregator
- **[Business Layer](./business-layer.md)** — risk scoring, action recommendation, konfigurasi
- **[API Endpoints](./api.md)** — dokumentasi semua endpoint dan cara penggunaannya

## Development

### Running Tests

```bash
uv run python test/test_cleaner.py
uv run python test/test_sentiment.py
uv run python test/test_issue.py
uv run python test/test_aggregator.py
uv run python test/test_business.py
```

### Project Structure Philosophy

```
app/        → Urusan FastAPI — tidak boleh tahu soal business logic
src/        → Urusan business logic — tidak boleh tahu soal FastAPI
test/       → Testing semua layer
docs/       → Dokumentasi
```

## Status

- ✅ Core engine (cleaner, sentiment analyzer, issue classifier, aggregator)
- ✅ Business layer (risk scoring, action recommendation)
- ✅ API routes dan schemas (5 endpoint GET)
- ✅ Mock data untuk development
- ⏳ Koneksi ke SIAKAD (menunggu koordinasi endpoint)
- ⏳ Caching layer (Redis — planned)
- ⏳ Machine learning integration (future)
