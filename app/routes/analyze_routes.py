from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.analyze_schema import (
    GuruAnalyzeParams,
    GuruMapelAnalyzeParams,
    MapelAnalyzeParams,
    PeriodeAnalyzeParams,
    PeriodeMapelAnalyzeParams,
)
from app.services.analyze_service import (
    analyze_guru,
    analyze_guru_mapel,
    analyze_mapel,
    analyze_periode,
    analyze_periode_mapel,
)
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/analyze", tags=["Analyze"])


@router.get("/guru")
def route_analyze_guru(params: GuruAnalyzeParams = Depends()):
    """Analisis performa satu guru — semua mapel, semua waktu."""
    try:
        result = analyze_guru(nama_guru=params.nama_guru)
        return success_response("Analisis guru berhasil", data=result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=error_response(str(e)))


@router.get("/guru-mapel")
def route_analyze_guru_mapel(params: GuruMapelAnalyzeParams = Depends()):
    """Analisis performa satu guru di satu mata pelajaran spesifik."""
    try:
        result = analyze_guru_mapel(
            nama_guru=params.nama_guru,
            nama_mapel=params.nama_mapel,
        )
        return success_response("Analisis guru per mapel berhasil", data=result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=error_response(str(e)))


@router.get("/mapel")
def route_analyze_mapel(params: MapelAnalyzeParams = Depends()):
    """Perbandingan semua guru dalam satu mata pelajaran."""
    try:
        result = analyze_mapel(nama_mapel=params.nama_mapel)
        return success_response("Analisis per mapel berhasil", data=result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=error_response(str(e)))


@router.get("/periode")
def route_analyze_periode(params: PeriodeAnalyzeParams = Depends()):
    """Perbandingan semua guru dalam rentang waktu tertentu."""
    try:
        result = analyze_periode(
            tanggal_mulai=params.tanggal_mulai,
            tanggal_selesai=params.tanggal_selesai,
        )
        return success_response("Analisis per periode berhasil", data=result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=error_response(str(e)))


@router.get("/periode-mapel")
def route_analyze_periode_mapel(params: PeriodeMapelAnalyzeParams = Depends()):
    """Perbandingan semua guru, difilter by waktu + mata pelajaran."""
    try:
        result = analyze_periode_mapel(
            nama_mapel=params.nama_mapel,
            tanggal_mulai=params.tanggal_mulai,
            tanggal_selesai=params.tanggal_selesai,
        )
        return success_response("Analisis per periode dan mapel berhasil", data=result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=error_response(str(e)))