"""Cek kesiapan laptop peserta. Jalankan dari root repo:

    python setup_check.py            # cek lengkap (termasuk panggilan API & unduh model embedding)
    python setup_check.py --offline  # lewati cek yang butuh internet
"""
from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

OFFLINE = "--offline" in sys.argv
ROOT = Path(__file__).resolve().parent
ok_all = True


def check(name: str, fn, hint: str = "") -> None:
    global ok_all
    t0 = time.perf_counter()
    try:
        info = fn() or ""
        print(f"  [OK]   {name} {info} ({time.perf_counter() - t0:.1f}s)")
    except Exception as e:  # noqa: BLE001
        ok_all = False
        print(f"  [GAGAL] {name}: {type(e).__name__}: {str(e)[:200]}")
        if hint:
            print(f"          -> {hint}")


def warn(name: str, msg: str, hint: str = "") -> None:
    """Peringatan: tidak menggagalkan pemeriksaan, tetapi perlu dibaca (biasanya sisa latihan hari 1-2)."""
    print(f"  [PERINGATAN] {name}: {msg}")
    if hint:
        print(f"          -> {hint}")


RESET = "python scripts/reset_knowledge.py"

print("\n== 1. Python dan paket")


def _py():
    v = sys.version_info
    if v < (3, 10):
        raise RuntimeError(f"Python {v.major}.{v.minor} terlalu lama")
    return f"Python {v.major}.{v.minor}.{v.micro} di {sys.executable}"


check("Versi Python >= 3.10", _py, "Pasang Python 3.11 atau 3.12 (Unit 1 Langkah 1)")
for pkg in ["openai", "dotenv", "pydantic", "pandas", "matplotlib", "streamlit", "langchain_core", "langchain_openai",
            "langchain_community", "langchain_text_splitters", "langchain_chroma", "chromadb", "fastembed", "rank_bm25",
            "pypdf", "yaml", "common", "langchain", "langgraph", "langgraph.checkpoint.sqlite",
            "langchain_mcp_adapters", "migas_shared"]:
    check(f"import {pkg}", lambda p=pkg: getattr(importlib.import_module(p), "__version__", ""),
          "Aktifkan virtual environment, kemudian jalankan: pip install -r requirements.txt")

print("\n== 2. Konfigurasi .env")


def _env():
    if not (ROOT / ".env").exists():
        raise FileNotFoundError(".env belum ada")
    from common import config

    p = config.get_profile()
    if not p.api_key or "isi-dengan" in p.api_key:
        raise ValueError(f"{p.name.upper()}_API_KEY belum diisi")
    return f"profil={p.name}, model={p.model}, API key terisi"


check("File .env dan API key", _env, "Salin .env.example menjadi .env, kemudian isi API key (Unit 1 Langkah 5)")


def _env_hari34():
    from migas_shared import config as cfg

    cfg.ai_settings()
    return "ONLINE_* terisi, dipakai bersama hari 1-2"


check("Konfigurasi .env untuk hari 3-4", _env_hari34, "Isi ONLINE_API_KEY, ONLINE_BASE_URL, dan ONLINE_MODEL di .env")


def _data():
    need = ["data/raw/work_orders.csv", "data/raw/hse_incidents.csv", "data/docs/sop/SOP-HSE-001_rev3_H2S.md",
            "data/docs/manual/MAN-VSD-FD500.pdf", "data/eval/rag_golden_set.jsonl", "data/field/sumur.csv"]
    missing = [n for n in need if not (ROOT / n).exists()]
    if missing:
        raise FileNotFoundError(missing)
    return "data lengkap"


check("Data workshop", _data, "Lakukan clone ulang repository")

print("\n== 2b. Sisa latihan hari 1-2 yang memengaruhi hari 3-4")


def _sisa_latihan():
    """Hari 3-4 memakai knowledge base dan .env yang sama dengan hari 1-2. Cek sisa perubahan yang membuat hasil berbeda."""
    import os

    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
    ada = False
    uploads = ROOT / "data" / "docs" / "uploads"
    berkas = [f for f in uploads.rglob("*") if f.is_file()] if uploads.exists() else []
    if berkas:
        ada = True
        override = " (termasuk _status_overrides.json: revisi lama ditandai superseded)" if any(
            f.name == "_status_overrides.json" for f in berkas) else ""
        warn("Dokumen hasil upload", f"{len(berkas)} file di data/docs/uploads/{override}. "
             "Jawaban bab RAG akan berbeda dari materi.", RESET)
    effort = os.getenv("LLM_REASONING_EFFORT", "none").strip().lower()
    if effort not in ("", "none"):
        ada = True
        warn("LLM_REASONING_EFFORT", f"bernilai '{effort}'. Hari 3-4 membaca nilai ini juga, sehingga jawaban lebih lambat dan "
             "demo max_tokens di bab 1 berbeda.", "Kembalikan ke none di .env (kecuali memang ingin bereksperimen)")
    if not ada:
        return "tidak ada upload dan mode reasoning bawaan (none)"
    return "ada peringatan di atas (tidak menggagalkan pemeriksaan)"


check("Kondisi knowledge base dan .env", _sisa_latihan)

if not OFFLINE:
    print("\n== 3. Koneksi (memerlukan internet)")

    def _llm():
        from common.llm import chat

        out = chat("Balas hanya dengan kata: SIAP", max_tokens=5, use_cache=False)
        return f"jawaban model: {out.strip()!r}"

    check("Pemanggilan LLM", _llm, "Periksa API key dan koneksi internet (Lampiran A pada labsheet)")

    def _llm_hari34():
        from migas_shared.llm import chat

        out = chat("Balas hanya dengan kata: SIAP")
        return f"jawaban model (LangChain): {out.strip()!r}"

    check("Pemanggilan LLM lewat LangChain (hari 3-4)", _llm_hari34,
          "Periksa ONLINE_BASE_URL, ONLINE_API_KEY, dan ONLINE_MODEL di .env")

    def _emb():
        from common.embeddings import get_embeddings

        v = get_embeddings().embed_query("uji embedding")
        return f"dimensi {len(v)}"

    check("Model embedding (unduhan pertama sekitar 220 MB)", _emb,
          "Salin folder models/ dari instruktur ke folder repository (Lampiran A pada labsheet)")

    def _emb_hari34():
        from migas_shared.embeddings import get_embeddings

        return f"dimensi {len(get_embeddings().embed_query('alarm H2S'))}"

    check("Model embedding lewat migas_shared (hari 3-4)", _emb_hari34, "Sama dengan pemeriksaan embedding di atas")

    def _index_cocok():
        """Index Chroma lama (dari hari 2) harus berasal dari model embedding yang sama dengan model saat ini."""
        chroma = ROOT / "chroma_db"
        if not chroma.exists():
            return "belum ada index (dibangun otomatis saat pertama dipakai)"
        import chromadb
        from migas_shared.embeddings import get_embeddings

        sekarang = len(get_embeddings().embed_query("alarm H2S"))
        client = chromadb.PersistentClient(path=str(chroma))
        for nama in [c if isinstance(c, str) else c.name for c in client.list_collections()]:
            vektor = client.get_collection(nama).peek(1).get("embeddings")
            if vektor is None or len(vektor) == 0:
                continue
            if len(vektor[0]) != sekarang:
                warn("Index Chroma", f"koleksi '{nama}' berdimensi {len(vektor[0])}, model embedding sekarang "
                     f"{sekarang}. Model embedding diganti setelah index dibuat.", RESET)
                return "dimensi tidak cocok (tidak menggagalkan pemeriksaan)"
        return f"dimensi index sama dengan model embedding ({sekarang})"

    check("Index Chroma cocok dengan model embedding", _index_cocok, RESET)

print("\n" + ("Seluruh pemeriksaan berhasil. Environment siap digunakan." if ok_all
               else "Terdapat pemeriksaan yang GAGAL. Ikuti petunjuk pada baris tersebut atau lihat Lampiran A pada labsheet."))
sys.exit(0 if ok_all else 1)
