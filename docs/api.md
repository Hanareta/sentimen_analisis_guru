# API Endpoints

Semua endpoint menggunakan metode **GET** dengan query parameters.

Base URL: `http://localhost:8000/api`

Interactive docs: `http://localhost:8000/docs`

---

## Daftar Endpoint

| Endpoint | Deskripsi |
|----------|-----------|
| `GET /analyze/guru` | Analisis satu guru |
| `GET /analyze/guru-mapel` | Analisis satu guru di satu mata pelajaran |
| `GET /analyze/mapel` | Perbandingan semua guru dalam satu mata pelajaran |
| `GET /analyze/periode` | Perbandingan semua guru dalam rentang waktu |
| `GET /analyze/periode-mapel` | Perbandingan semua guru, filter waktu + mapel |

---

## 1. GET /analyze/guru

Analisis performa satu guru — semua mata pelajaran, semua waktu.

**Query Parameters:**

| Parameter | Tipe | Wajib | Deskripsi |
|-----------|------|-------|-----------|
| `nama_guru` | string | ✅ | Nama guru |

**Contoh Request:**
```bash
GET /api/analyze/guru?nama_guru=Bu%20Sari
```

**Contoh Response:**
```json
{
  "success": true,
  "message": "Analisis guru berhasil",
  "data": {
    "nama_guru": "Bu Sari",
    "summary": {
      "nama_guru": "Bu Sari",
      "total_komentar": 6,
      "jumlah_positif": 4,
      "jumlah_negatif": 1,
      "jumlah_netral": 1,
      "persentase_positif": 66.67,
      "persentase_negatif": 16.67,
      "persentase_netral": 16.67,
      "rata_rata_skor": 0.5,
      "rata_rata_rating": 3.83,
      "sentimen_akhir": "positif",
      "issue_dominan": "cara_mengajar",
      "risk_score": 0.242,
      "urgency_level": "low",
      "recommended_action": "Tidak ada tindakan khusus diperlukan",
      "follow_up_days": 90,
      "action_priority": 4
    },
    "detail_reviews": [
      {
        "nama_guru": "Bu Sari",
        "rating": 5,
        "komentar_asli": "ngajarnya enak bgt",
        "komentar_bersih": "ngajarnya enak banget",
        "sentimen": "positif",
        "skor": 1.0,
        "kata_kunci": ["enak"],
        "issues": [],
        "issue_dominan": null
      }
    ]
  }
}
```

---

## 2. GET /analyze/guru-mapel

Analisis performa satu guru di satu mata pelajaran spesifik.

**Query Parameters:**

| Parameter | Tipe | Wajib | Deskripsi |
|-----------|------|-------|-----------|
| `nama_guru` | string | ✅ | Nama guru |
| `nama_mapel` | string | ✅ | Nama mata pelajaran |

**Contoh Request:**
```bash
GET /api/analyze/guru-mapel?nama_guru=Bu%20Sari&nama_mapel=Matematika
```

---

## 3. GET /analyze/mapel

Perbandingan semua guru dalam satu mata pelajaran. Output diurutkan dari skor tertinggi.

**Query Parameters:**

| Parameter | Tipe | Wajib | Deskripsi |
|-----------|------|-------|-----------|
| `nama_mapel` | string | ✅ | Nama mata pelajaran |

**Contoh Request:**
```bash
GET /api/analyze/mapel?nama_mapel=Matematika
```

**Contoh Response:**
```json
{
  "success": true,
  "message": "Analisis per mapel berhasil",
  "data": {
    "nama_mapel": "Matematika",
    "total_guru": 2,
    "hasil": [
      {
        "summary": {
          "nama_guru": "Bu Sari",
          "sentimen_akhir": "positif",
          "risk_score": 0.242,
          "urgency_level": "low",
          ...
        },
        "detail_reviews": [...]
      },
      {
        "summary": {
          "nama_guru": "Pak Budi",
          "sentimen_akhir": "negatif",
          "risk_score": 1.0,
          "urgency_level": "critical",
          ...
        },
        "detail_reviews": [...]
      }
    ]
  }
}
```

---

## 4. GET /analyze/periode

Perbandingan semua guru dalam rentang waktu tertentu.

**Query Parameters:**

| Parameter | Tipe | Wajib | Deskripsi |
|-----------|------|-------|-----------|
| `tanggal_mulai` | date (YYYY-MM-DD) | ✅ | Awal periode |
| `tanggal_selesai` | date (YYYY-MM-DD) | ✅ | Akhir periode |

**Validasi:** `tanggal_mulai` tidak boleh lebih besar dari `tanggal_selesai`

**Contoh Request:**
```bash
GET /api/analyze/periode?tanggal_mulai=2024-01-01&tanggal_selesai=2024-06-30
```

**Use case:** Lihat siapa guru terbaik dan terburuk dalam satu semester.

---

## 5. GET /analyze/periode-mapel

Perbandingan semua guru dalam satu mata pelajaran pada periode tertentu.

**Query Parameters:**

| Parameter | Tipe | Wajib | Deskripsi |
|-----------|------|-------|-----------|
| `nama_mapel` | string | ✅ | Nama mata pelajaran |
| `tanggal_mulai` | date (YYYY-MM-DD) | ✅ | Awal periode |
| `tanggal_selesai` | date (YYYY-MM-DD) | ✅ | Akhir periode |

**Contoh Request:**
```bash
GET /api/analyze/periode-mapel?nama_mapel=Matematika&tanggal_mulai=2024-01-01&tanggal_selesai=2024-06-30
```

**Use case:** "Siapa guru Matematika terbaik semester ini?"

---

## Response Format

Semua endpoint menggunakan struktur yang sama:

```json
{
  "success": true,
  "message": "string",
  "data": {...}
}
```

---

## Field Penjelasan

### Summary Object

| Field | Type | Deskripsi |
|-------|------|-----------|
| `nama_guru` | string | Nama guru |
| `total_komentar` | int | Total review |
| `jumlah_positif` | int | Jumlah review positif |
| `jumlah_negatif` | int | Jumlah review negatif |
| `jumlah_netral` | int | Jumlah review netral |
| `persentase_positif` | float | % review positif |
| `persentase_negatif` | float | % review negatif |
| `persentase_netral` | float | % review netral |
| `rata_rata_skor` | float | Rata-rata sentiment score (-1 sampai 1) |
| `rata_rata_rating` | float | Rata-rata rating (1 sampai 5) |
| `sentimen_akhir` | string | "positif", "negatif", "netral" |
| `issue_dominan` | string\|null | Kategori masalah paling sering |
| `risk_score` | float | Skor risiko (0.0 sampai 1.0) |
| `urgency_level` | string | "low", "medium", "high", "critical" |
| `recommended_action` | string | Rekomendasi tindakan |
| `follow_up_days` | int | Kapan follow-up berikutnya (hari) |
| `action_priority` | int | Prioritas tindakan (1 = paling mendesak) |

### Detail Review Object

| Field | Type | Deskripsi |
|-------|------|-----------|
| `komentar_asli` | string | Teks original dari siswa |
| `komentar_bersih` | string | Teks setelah cleaning |
| `sentimen` | string | "positif", "negatif", "netral" |
| `skor` | float | Sentiment score (-1 sampai 1) |
| `kata_kunci` | array | Kata yang mempengaruhi sentimen |
| `issues` | array | Kategori masalah yang terdeteksi |
| `issue_dominan` | string\|null | Masalah utama dari komentar ini |

---

## Error Codes

| Code | Deskripsi |
|------|-----------|
| 200 | OK — request berhasil |
| 404 | Data tidak ditemukan |
| 422 | Validation error — parameter salah |
| 500 | Server error |

### Contoh Error 404
```json
{
  "success": false,
  "message": "Tidak ada data review untuk guru 'Guru X'",
  "data": null
}
```

### Contoh Error 422
```json
{
  "detail": [
    {
      "loc": ["query", "tanggal_mulai"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Contoh Penggunaan

### cURL
```bash
curl "http://localhost:8000/api/analyze/guru?nama_guru=Bu%20Sari"
curl "http://localhost:8000/api/analyze/mapel?nama_mapel=Matematika"
curl "http://localhost:8000/api/analyze/periode?tanggal_mulai=2024-01-01&tanggal_selesai=2024-06-30"
```

### Python (httpx)
```python
import httpx

client = httpx.Client()

# Analisis satu guru
response = client.get(
    "http://localhost:8000/api/analyze/guru",
    params={"nama_guru": "Bu Sari"}
)
print(response.json())

# Analisis per periode
response = client.get(
    "http://localhost:8000/api/analyze/periode",
    params={
        "tanggal_mulai": "2024-01-01",
        "tanggal_selesai": "2024-06-30",
    }
)
print(response.json())
```

### JavaScript (fetch)
```javascript
// Analisis satu guru
const res = await fetch('/api/analyze/guru?nama_guru=Bu%20Sari');
const data = await res.json();

// Analisis per periode
const params = new URLSearchParams({
  tanggal_mulai: '2024-01-01',
  tanggal_selesai: '2024-06-30'
});
const res2 = await fetch(`/api/analyze/periode?${params}`);
const data2 = await res2.json();
```
