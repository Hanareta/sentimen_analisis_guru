from __future__ import annotations

import re
from src.sentimen_analisis.data.slang import SLANG_MAP


def to_lowercase(text: str) -> str:
    return text.lower().strip()


def remove_repeated_chars(text: str) -> str:
    """
    Hapus karakter yang berulang lebih dari 2 kali.
    'bagusssss' → 'bagus'
    'marahhhh'  → 'marah'
    """
    return re.sub(r"(.)\1{2,}", r"\1", text)


def remove_noise(text: str) -> str:
    """
    Hapus karakter yang tidak relevan.
    - URL
    - Angka berdiri sendiri
    - Karakter selain huruf dan spasi
    """
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\b\d+\b", "", text)
    text = re.sub(r"[^\w\s]", " ", text)
    return text


def normalize_slang(text: str) -> str:
    """
    Ganti slang dan singkatan dengan kata formal.
    Hanya ganti kata utuh — bukan substring.
    'ga' diganti 'tidak', tapi 'gaga' tidak diganti.
    """
    words = text.split()
    normalized = [SLANG_MAP.get(word, word) for word in words]
    return " ".join(normalized)


def normalize_whitespace(text: str) -> str:
    """Hapus spasi berlebih."""
    return re.sub(r"\s+", " ", text).strip()


def clean(text: str) -> str:
    """
    Pipeline utama cleaner.
    Panggil fungsi ini dari luar — bukan fungsi individual.
    """
    text = to_lowercase(text)
    text = remove_repeated_chars(text)
    text = remove_noise(text)
    text = normalize_slang(text)
    text = normalize_whitespace(text)
    return text