# Arsitektur System

## Alur Request — Dari Client sampai Response

```
Client (Frontend / External System)
    │
    ├─ GET /api/analyze/guru?nama_guru=Bu+Sari
    │
    ↓
Routes Layer (app/routes/analyze_routes.py)
    ├─ Terima request
    ├─ Validasi query parameter via Pydantic schema
    └─ Panggil service function
    │
    ↓
Service Layer (app/services/analyze_service.py)
    ├─ Orkestrasi semua layer
    ├─ Panggil fetch_data untuk ambil data
    ├─ Panggil pipeline analisis
    └─ Format hasil untuk response
    │
    ↓
Fetch Data (src/sentimen_analisis/fetch_data.py)
    ├─ Saat ini: mock data hardcoded
    ├─ Nanti: query SIAKAD via api_client.py
    └─ Return DataFrame
    │
    ↓
Core Engine (src/sentimen_analisis/)
    ├─ Layer 1: Cleaner
    ├─ Layer 2: Sentiment Analyzer
    ├─ Layer 3: Issue Classifier
    └─ Layer 4: Aggregator → summary per guru
    │
    ↓
Business Layer (src/sentimen_analisis/)
    ├─ Risk Scorer → hitung risk score
    └─ Action Recommender → susun rekomendasi tindakan
    │
    ↓
Response
    └─ JSON: {"success": true, "data": {...}}
```

---

## Empat Layer Utama

### 1. HTTP Layer (app/)

**Tanggung jawab:**
- Terima HTTP request
- Validasi input
- Format response

**Tidak boleh:**
- Mengandung business logic
- Tahu soal pandas, NLP, atau data processing

**File:**
- `routes/` — endpoint definition
- `schemas/` — Pydantic model untuk validasi query params
- `services/` — orkestrasi semua layer
- `utils/` — helper functions

---

### 2. Core Engine (src/sentimen_analisis/)

**Tanggung jawab:** Analisis teks dan ekstrak informasi

```
Input (DataFrame mentah)
    ↓
1. Cleaner        → normalisasi teks
2. Sentiment      → deteksi positif/negatif/netral
3. Issue          → deteksi kategori masalah
4. Aggregator     → ringkasan per guru
    ↓
Output (analyzed_df + summary_df)
```

---

### 3. Business Layer (src/sentimen_analisis/)

**Tanggung jawab:** Interpretasi hasil analisis menjadi keputusan bisnis

```
Input (summary_df dari Core Engine)
    ↓
1. RiskScorer         → hitung risk score (0.0 - 1.0)
2. ActionRecommender  → susun rekomendasi tindakan
    ↓
Output (action_df dengan risk_score, urgency_level, recommended_action)
```

**Konfigurasi ada di `business_config.py`** — threshold dan bobot bisa diubah tanpa menyentuh logika.

---

### 4. Data Layer (fetch_data.py, api_client.py)

**Tanggung jawab:** Ambil data dari sumber, return DataFrame

**Status saat ini:** Mock data hardcoded di `fetch_data.py`

**Rencana:** Swap ke HTTP call ke SIAKAD via `api_client.py`

---

## Data Flow — Contoh Konkret

### Scenario: GET /api/analyze/guru?nama_guru=Bu Sari

```
1. REQUEST MASUK
   GET /api/analyze/guru?nama_guru=Bu%20Sari

2. ROUTES (analyze_routes.py)
   - FastAPI validasi params via Pydantic
   - Panggil service.analyze_guru("Bu Sari")

3. SERVICE (analyze_service.py)
   - fetch_reviews(nama_guru="Bu Sari")
   - _run_pipeline(df)
     - aggregator.run(df)
     - risk_scorer.transform(summary_df)
     - action_recommender.transform(risk_df)
   - Format response

4. FETCH DATA (fetch_data.py)
   - Filter mock data by nama_guru
   - Return DataFrame:
   ┌──────────┬────────┬──────────────────────┐
   │ nama_guru│ rating │ komentar             │
   ├──────────┼────────┼──────────────────────┤
   │ Bu Sari  │   5    │ ngajarnya enak bgt   │
   │ Bu Sari  │   4    │ sabar dan jelas      │
   │ Bu Sari  │   2    │ terlalu cepat        │
   └──────────┴────────┴──────────────────────┘

5. CORE ENGINE (aggregator.py)
   analyze_comments():
   ┌──────────┬─────────┬────────┬──────────────┐
   │ nama_guru│ sentimen│  skor  │ issues       │
   ├──────────┼─────────┼────────┼──────────────┤
   │ Bu Sari  │ positif │  1.000 │ []           │
   │ Bu Sari  │ positif │  1.000 │ []           │
   │ Bu Sari  │ negatif │ -1.000 │[cara_mengajar]│
   └──────────┴─────────┴────────┴──────────────┘

   aggregate_per_guru():
   ┌──────────┬───────┬─────────┬───────────────┐
   │ nama_guru│ total │ positif │ sentimen_akhir│
   ├──────────┼───────┼─────────┼───────────────┤
   │ Bu Sari  │   3   │  2(67%) │   positif     │
   └──────────┴───────┴─────────┴───────────────┘

6. BUSINESS LAYER
   risk_scorer.transform():
   - risk_score = 0.242
   - urgency_level = "low"

   action_recommender.transform():
   - recommended_action = "Tidak ada tindakan khusus"
   - follow_up_days = 90

7. RESPONSE
   {
     "success": true,
     "data": {
       "nama_guru": "Bu Sari",
       "summary": {
         "sentimen_akhir": "positif",
         "risk_score": 0.242,
         "urgency_level": "low",
         "recommended_action": "Tidak ada tindakan khusus"
       },
       "detail_reviews": [...]
     }
   }
```

---

## Inisialisasi Engine

Semua engine di-inisialisasi **sekali saat server start**, bukan per-request:

```python
# analyze_service.py — top level
_aggregator = Aggregator()
_risk_scorer = RiskScorer()
_action_recommender = ActionRecommender()
```

Lebih efisien karena tidak perlu buat object baru setiap request masuk.

---

## Error Handling

```
Core Engine raise ValueError (data kosong)
        ↓
Service layer propagate error
        ↓
Routes layer catch → HTTPException 404
        ↓
FastAPI return error response ke client:
{
  "success": false,
  "message": "Tidak ada data review untuk guru 'X'"
}
```

---

## Koneksi SIAKAD (Planned)

Saat koneksi SIAKAD siap, yang perlu diubah hanya `fetch_data.py`:

```python
# Sekarang (mock):
df = pd.DataFrame(MOCK_REVIEWS)

# Nanti (SIAKAD):
client = SiakadClient()
data = client.get_reviews(params)
df = pd.DataFrame(data)
```

Semua layer lain tidak perlu diubah.
