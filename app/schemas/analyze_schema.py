from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, model_validator


class GuruAnalyzeParams(BaseModel):
    """Analisis performa satu guru — semua mapel, semua waktu."""
    nama_guru: str = Field(..., min_length=1)


class GuruMapelAnalyzeParams(BaseModel):
    """Analisis performa satu guru di satu mata pelajaran spesifik."""
    nama_guru: str = Field(..., min_length=1)
    nama_mapel: str = Field(..., min_length=1)


class MapelAnalyzeParams(BaseModel):
    """Perbandingan semua guru dalam satu mata pelajaran."""
    nama_mapel: str = Field(..., min_length=1)


class PeriodeAnalyzeParams(BaseModel):
    """Perbandingan semua guru dalam rentang waktu tertentu."""
    tanggal_mulai: date
    tanggal_selesai: date

    @model_validator(mode="after")
    def validate_periode(self) -> "PeriodeAnalyzeParams":
        if self.tanggal_mulai > self.tanggal_selesai:
            raise ValueError("tanggal_mulai tidak boleh lebih besar dari tanggal_selesai")
        return self


class PeriodeMapelAnalyzeParams(BaseModel):
    """Perbandingan semua guru, difilter by waktu + mata pelajaran."""
    nama_mapel: str = Field(..., min_length=1)
    tanggal_mulai: date
    tanggal_selesai: date

    @model_validator(mode="after")
    def validate_periode(self) -> "PeriodeMapelAnalyzeParams":
        if self.tanggal_mulai > self.tanggal_selesai:
            raise ValueError("tanggal_mulai tidak boleh lebih besar dari tanggal_selesai")
        return self