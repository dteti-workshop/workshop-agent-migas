"""Alat data migas untuk agen contoh mini project.

Data berasal dari folder data/ (fiktif), sama dengan yang dipakai di hari 1 dan 2:

  work order  : data/raw/work_orders.csv + data/eval/work_orders_truth.csv  (kolom terstruktur hasil ekstraksi)
  insiden HSE : data/raw/hse_incidents.csv + data/eval/hse_incidents_truth.csv
  produksi    : data/eval/daily_gs_sr1_2026-07.csv  (laporan harian GS-SR1, Juli 2026)
  sumur       : data/field/sumur.csv  (196 sumur Seruni, Kenanga, Melati; status dan produksi per 2026-07-31)
                data/field/produksi_sumur_2026-07.csv  (produksi harian semua sumur; jumlah sumur Seruni sama dengan laporan harian GS-SR1)

Ini KATALOG komponen agen: tool untuk empat use case (Operasi, Perawatan, HSE, Engineering). Lihat KATALOG di
bagian bawah file, atau jalankan code/01_katalog_tool.py.

Tool BACA mengembalikan teks ringkas. Tool TULIS (nama-namanya di TULIS) hanya mencatat ke daftar CATATAN_TINDAKAN
di memori. Tidak ada sistem nyata yang diubah, sehingga aman dicoba. Agen yang memakai tool tulis sebaiknya dipasangi
persetujuan manusia (lihat solusi/agen_contoh/perawatan.py).
"""
import threading
from functools import lru_cache
from typing import Literal

import pandas as pd
from langchain.tools import tool

from migas_shared import rag_pipeline as rp
from migas_shared.config import DATA
from migas_shared.field_tools import hitung_water_cut, konversi_satuan

CATATAN_TINDAKAN: list[dict] = []

# Pilihan terbatas ditulis sebagai Literal, sehingga skema argumen tool memuat daftar nilai yang sah (enum) dan model
# tidak bisa mengarang nilai lain. Penjelajah menampilkannya sebagai dropdown.
TipeAlat = Literal["ESP", "SRP", "PCP", "Flowline", "Separator", "Steam Generator", "Gas Compressor", "Water Injection Pump"]
Tingkat = Literal["Rendah", "Sedang", "Tinggi"]
Bahaya = Literal["Hot Work/Fire", "Working at Height", "Vehicle/Driving", "Spill/Release", "Electrical", "Dropped Object",
                 "H2S/Gas", "Steam/Hot Surface", "Manual Handling", "Pinch Point"]
Prioritas = Literal["rendah", "sedang", "tinggi"]
AreaSumur = Literal["Seruni", "Kenanga", "Melati"]
PompaSumur = Literal["ESP", "SRP", "PCP"]
StatusSumur = Literal["Produksi", "Menunggu pulling", "Workover", "Shut-in"]
UrutSumur = Literal["minyak_tertinggi", "water_cut_tertinggi", "kode"]

# Tool pencarian dokumen: jenis dokumen (doc_type) yang boleh dikembalikan dan peran tetap yang dipakai untuk akses.
# Satu tempat untuk tool dan penjelajah (yang menampilkan dokumen mana yang terjangkau tool).
SUMBER_DOKUMEN: dict[str, tuple[set[str], str]] = {
    "cari_dokumen_sop": ({"SOP"}, "engineer"),
    "cari_dokumen_manual": ({"Manual"}, "engineer"),
    "cari_dokumen_laporan": ({"Laporan", "Lessons Learned"}, "engineer"),
    "cari_dokumen_investigasi": ({"Investigasi"}, "hse"),
}


# Korpus dokumen bab 11 = korpus bersama (data/docs, dipakai hari 2 sampai 4) + dokumen tambahan khusus bab ini (data/docs_bab11).
# Dokumen tambahan sengaja dipisah supaya jumlah chunk dan keluaran bab lain tidak berubah. Indeksnya koleksi Chroma tersendiri.
FOLDER_DOKUMEN = {"docs": DATA / "docs", "docs_bab11": DATA / "docs_bab11"}
NAMA_INDEKS = "bab11_markdown_800"


@lru_cache(maxsize=1)
def muat_dokumen() -> list:
    """Semua dokumen bab 11 (korpus bersama + tambahan); metadata `folder` menunjukkan asalnya."""
    hasil = []
    for folder, path in FOLDER_DOKUMEN.items():
        for d in rp.load_documents(path):
            d.metadata["folder"] = folder
            hasil.append(d)
    return hasil


_kunci_retriever = threading.Lock()
_retriever: rp.HybridRetriever | None = None


def retriever_bab11() -> rp.HybridRetriever:
    """Retriever hibrida atas korpus bab 11. Indeks dibangun pada panggilan pertama (beberapa detik) dan dipakai ulang.

    Dikunci karena beberapa sesi (aplikasi agen di thread kernel, aplikasi lain) bisa memanggilnya bersamaan, dan membuka
    koleksi Chroma yang sama dari dua thread sekaligus bisa gagal ("Could not connect to tenant").
    """
    global _retriever
    with _kunci_retriever:
        if _retriever is None:
            chunks = rp.chunk_documents(muat_dokumen(), "markdown", 800, chunk_overlap=100)
            store = rp._open_store(NAMA_INDEKS)
            if set(store.get(include=[])["ids"]) != {c.metadata["chunk_id"] for c in chunks}:
                store = rp.build_index(chunks, NAMA_INDEKS)
            _retriever = rp.HybridRetriever(store, chunks)
        return _retriever


@lru_cache(maxsize=1)
def _work_order() -> pd.DataFrame:
    mentah = pd.read_csv(DATA / "raw" / "work_orders.csv")
    terstruktur = pd.read_csv(DATA / "eval" / "work_orders_truth.csv")
    return mentah.merge(terstruktur, on="wo_id").sort_values("tanggal", ascending=False)


@lru_cache(maxsize=1)
def _insiden() -> pd.DataFrame:
    mentah = pd.read_csv(DATA / "raw" / "hse_incidents.csv")
    terstruktur = pd.read_csv(DATA / "eval" / "hse_incidents_truth.csv")
    return mentah.merge(terstruktur, on="incident_id").sort_values("tanggal", ascending=False)


@lru_cache(maxsize=1)
def _harian() -> pd.DataFrame:
    return pd.read_csv(DATA / "eval" / "daily_gs_sr1_2026-07.csv")


@lru_cache(maxsize=1)
def _sumur() -> pd.DataFrame:
    return pd.read_csv(DATA / "field" / "sumur.csv")


@lru_cache(maxsize=1)
def _produksi_sumur() -> pd.DataFrame:
    return pd.read_csv(DATA / "field" / "produksi_sumur_2026-07.csv")


# Tabel sumber yang dibaca tool, untuk ditampilkan penjelajah (pembacaan yang sama dengan yang dipakai tool).
def tabel_work_order() -> pd.DataFrame:
    return _work_order()


def tabel_insiden() -> pd.DataFrame:
    return _insiden()


def tabel_harian() -> pd.DataFrame:
    return _harian()


def tabel_sumur() -> pd.DataFrame:
    return _sumur()


def tabel_produksi_sumur() -> pd.DataFrame:
    return _produksi_sumur()


# ---------------------------------------------------------------------------
# Pencarian dokumen (satu tool per jenis dokumen)
# ---------------------------------------------------------------------------


def _cari_jenis(query: str, k: int, nama: str, tool: str) -> str:
    """Cari di dokumen aktif, lalu simpan hanya chunk dengan doc_type yang terdaftar untuk `tool` di SUMBER_DOKUMEN.

    Peran tetap per tool: hak akses ditentukan oleh tool yang dipasang, bukan oleh konteks yang dikirim program.
    Di sistem nyata, hak akses berasal dari login pengguna.
    """
    jenis, peran = SUMBER_DOKUMEN[tool]
    docs = retriever_bab11().search(query, k=40, mode="hybrid", role=peran, active_only=True)
    docs = [d for d in docs if d.metadata.get("doc_type") in jenis][: max(1, min(k, 10))]
    return rp.format_context(docs) if docs else f"Tidak ada {nama} yang relevan dengan pencarian tersebut."


@tool(parse_docstring=True)
def cari_dokumen_sop(query: str, k: int = 3) -> str:
    """Cari prosedur kerja (SOP) di dokumen aktif: batas alarm, langkah kerja, dan tindakan darurat.

    Hasil berupa blok <dokumen id=... revisi=... bagian=...> yang dapat dikutip sebagai [DOC_ID bagian].

    Args:
        query: Kalimat pencarian dengan istilah teknis, contoh "alarm H2S 10 ppm tindakan".
        k: Jumlah chunk yang dikembalikan (1 sampai 10).
    """
    return _cari_jenis(query, k, "SOP", "cari_dokumen_sop")


@tool(parse_docstring=True)
def cari_dokumen_manual(query: str, k: int = 3) -> str:
    """Cari manual perangkat di dokumen aktif, misalnya kode alarm dan cara operasi VSD FD-500.

    Hasil berupa blok <dokumen id=... revisi=... bagian=...> yang dapat dikutip sebagai [DOC_ID bagian].

    Args:
        query: Kalimat pencarian, contoh "kode alarm overcurrent VSD FD500".
        k: Jumlah chunk yang dikembalikan (1 sampai 10).
    """
    return _cari_jenis(query, k, "manual perangkat", "cari_dokumen_manual")


@tool(parse_docstring=True)
def cari_dokumen_laporan(query: str, k: int = 3) -> str:
    """Cari laporan bulanan dan lessons learned di dokumen aktif.

    Hasil berupa blok <dokumen id=... revisi=... bagian=...> yang dapat dikutip sebagai [DOC_ID bagian].

    Args:
        query: Kalimat pencarian, contoh "kebakaran kecil saat grinding".
        k: Jumlah chunk yang dikembalikan (1 sampai 10).
    """
    return _cari_jenis(query, k, "laporan", "cari_dokumen_laporan")


@tool(parse_docstring=True)
def cari_dokumen_investigasi(query: str, k: int = 3) -> str:
    """Cari laporan investigasi insiden HSE. Dokumen ini terbatas: hanya tool ini yang dapat membacanya.

    Hasil berupa blok <dokumen id=... revisi=... bagian=...> yang dapat dikutip sebagai [DOC_ID bagian].

    Args:
        query: Kalimat pencarian, contoh "penyebab paparan H2S di SR-027".
        k: Jumlah chunk yang dikembalikan (1 sampai 10).
    """
    return _cari_jenis(query, k, "laporan investigasi", "cari_dokumen_investigasi")


# ---------------------------------------------------------------------------
# Pemeliharaan
# ---------------------------------------------------------------------------


@tool(parse_docstring=True)
def riwayat_work_order(asset_id: str, maks: int = 5) -> str:
    """Tampilkan riwayat work order sebuah aset: tanggal, kategori kegagalan, komponen, tindakan, dan downtime.

    Args:
        asset_id: Kode aset, contoh "SR-020" atau "V-SR1-101".
        maks: Jumlah work order terbaru yang ditampilkan (1 sampai 10).
    """
    baris = _work_order()
    baris = baris[baris["asset_id"].str.upper() == asset_id.strip().upper()]
    if baris.empty:
        return f"Tidak ada work order untuk aset {asset_id}."
    tampil = baris.head(max(1, min(maks, 10)))
    teks = [f"{asset_id.upper()}: {len(baris)} work order, total downtime {baris['downtime_hours'].sum():.1f} jam. Terbaru:"]
    for _, r in tampil.iterrows():
        teks.append(f"- {r['wo_id']} ({r['tanggal']}): {r['failure_category']}, komponen {r['component']}, "
                    f"tindakan {r['action_category']}, downtime {r['downtime_hours']} jam")
    return "\n".join(teks)


@tool(parse_docstring=True)
def statistik_kegagalan(tipe_peralatan: TipeAlat | None = None) -> str:
    """Hitung jumlah work order dan total downtime per kategori kegagalan, untuk satu tipe peralatan atau semuanya.

    Args:
        tipe_peralatan: Tipe peralatan (pilihan terbatas). Kosongkan untuk semua tipe.
    """
    baris = _work_order()
    if tipe_peralatan:
        baris = baris[baris["equipment_type"].str.lower() == tipe_peralatan.strip().lower()]
        if baris.empty:
            return f"Tipe peralatan {tipe_peralatan} tidak ditemukan."
    ringkas = (baris.groupby("failure_category")["downtime_hours"].agg(["count", "sum"])
               .sort_values("sum", ascending=False))
    judul = tipe_peralatan or "semua peralatan"
    teks = [f"Kegagalan {judul}: {len(baris)} work order, total downtime {baris['downtime_hours'].sum():.0f} jam."]
    for kategori, r in ringkas.iterrows():
        teks.append(f"- {kategori}: {int(r['count'])} work order, {r['sum']:.0f} jam")
    return "\n".join(teks)


@tool(parse_docstring=True)
def buat_work_order(asset_id: str, uraian: str, prioritas: Prioritas) -> str:
    """Buat work order pemeliharaan baru.

    Args:
        asset_id: Kode aset, contoh "V-SR1-101".
        uraian: Uraian pekerjaan yang diminta.
        prioritas: Prioritas pekerjaan (pilihan terbatas): rendah, sedang, atau tinggi.
    """
    nomor = f"WO-UJI-{len(CATATAN_TINDAKAN) + 1:03d}"
    CATATAN_TINDAKAN.append({"nomor": nomor, "jenis": "work order", "asset_id": asset_id, "uraian": uraian, "prioritas": prioritas})
    return f"Work order {nomor} dibuat untuk {asset_id} (prioritas {prioritas})."


@tool(parse_docstring=True)
def aset_downtime_tertinggi(maks: int = 5) -> str:
    """Tampilkan aset dengan total downtime tertinggi dari seluruh work order, beserta jumlah work order dan tipe peralatannya.

    Args:
        maks: Jumlah aset teratas yang ditampilkan (1 sampai 10).
    """
    baris = _work_order()
    per_aset = (baris.groupby("asset_id").agg(jumlah=("wo_id", "count"), jam=("downtime_hours", "sum"),
                                              tipe=("equipment_type", "first"))
                .sort_values("jam", ascending=False).head(max(1, min(maks, 10))))
    teks = [f"{len(per_aset)} aset dengan downtime tertinggi:"]
    for aset, r in per_aset.iterrows():
        teks.append(f"- {aset} ({r['tipe']}): {r['jam']:.0f} jam dari {int(r['jumlah'])} work order")
    return "\n".join(teks)


@tool(parse_docstring=True)
def tutup_work_order(wo_id: str, catatan: str) -> str:
    """Tutup sebuah work order yang pekerjaannya selesai.

    Args:
        wo_id: Nomor work order yang ada di riwayat, contoh "WO-26-12115".
        catatan: Catatan penutupan, singkat dan faktual.
    """
    if _work_order()["wo_id"].str.upper().ne(wo_id.strip().upper()).all():
        return f"Work order {wo_id} tidak ditemukan, penutupan tidak dicatat."
    nomor = f"TUTUP-UJI-{len(CATATAN_TINDAKAN) + 1:03d}"
    CATATAN_TINDAKAN.append({"nomor": nomor, "jenis": "penutupan work order", "wo_id": wo_id.strip().upper(), "catatan": catatan})
    return f"Penutupan {wo_id.strip().upper()} dicatat sebagai {nomor}."


# ---------------------------------------------------------------------------
# HSE
# ---------------------------------------------------------------------------


@tool(parse_docstring=True)
def cari_insiden(lokasi: str | None = None, bahaya: Bahaya | None = None, tingkat: Tingkat | None = None, maks: int = 5) -> str:
    """Cari insiden HSE menurut lokasi, jenis bahaya, dan tingkat keparahan. Semua filter bersifat opsional.

    Args:
        lokasi: Sebagian nama lokasi, contoh "GS-SR1" atau "Workshop".
        bahaya: Jenis bahaya (pilihan terbatas).
        tingkat: Tingkat keparahan (pilihan terbatas).
        maks: Jumlah insiden terbaru yang ditampilkan (1 sampai 10).
    """
    baris = _insiden()
    if lokasi:
        baris = baris[baris["lokasi"].str.contains(lokasi.strip(), case=False, regex=False)]
    if bahaya:
        baris = baris[baris["hazard"].str.contains(bahaya.strip(), case=False, regex=False)]
    if tingkat:
        baris = baris[baris["severity"].str.lower() == tingkat.strip().lower()]
    if baris.empty:
        return "Tidak ada insiden yang cocok dengan filter tersebut."
    teks = [f"{len(baris)} insiden cocok. Terbaru:"]
    for _, r in baris.head(max(1, min(maks, 10))).iterrows():
        teks.append(f"- {r['incident_id']} ({r['tanggal']}, {r['lokasi']}): {r['incident_type']}, bahaya {r['hazard']}, "
                    f"tingkat {r['severity']}. {r['narasi'][:150]}")
    return "\n".join(teks)


@tool(parse_docstring=True)
def ringkasan_insiden() -> str:
    """Ringkas seluruh insiden HSE: jumlah per jenis bahaya, per tingkat keparahan, dan lokasi paling sering."""
    baris = _insiden()
    per_bahaya = baris["hazard"].value_counts()
    per_tingkat = baris["severity"].value_counts()
    lokasi = baris["lokasi"].value_counts().head(3)
    return (f"Total {len(baris)} insiden.\n"
            f"Per bahaya: " + ", ".join(f"{k} {v}" for k, v in per_bahaya.items()) + "\n"
            f"Per tingkat: " + ", ".join(f"{k} {v}" for k, v in per_tingkat.items()) + "\n"
            f"Lokasi terbanyak: " + ", ".join(f"{k} {v}" for k, v in lokasi.items()))


@tool(parse_docstring=True)
def usulkan_tindakan_korektif(incident_id: str, tindakan: str, penanggung_jawab: str) -> str:
    """Catat usulan tindakan korektif untuk sebuah insiden.

    Args:
        incident_id: Nomor insiden, contoh "HSE-26-0004".
        tindakan: Tindakan korektif yang diusulkan.
        penanggung_jawab: Jabatan penanggung jawab, contoh "Supervisor HSE".
    """
    nomor = f"CAPA-UJI-{len(CATATAN_TINDAKAN) + 1:03d}"
    CATATAN_TINDAKAN.append({"nomor": nomor, "jenis": "tindakan korektif", "incident_id": incident_id,
                             "tindakan": tindakan, "penanggung_jawab": penanggung_jawab})
    return f"Tindakan korektif {nomor} dicatat untuk {incident_id}, penanggung jawab {penanggung_jawab}."


@tool(parse_docstring=True)
def kirim_notifikasi_hse(penerima: str, pesan: str) -> str:
    """Kirim notifikasi HSE kepada seorang penerima atau satu kelompok.

    Args:
        penerima: Jabatan atau kelompok penerima, contoh "Supervisor HSE" atau "Seluruh crew GS-SR1".
        pesan: Isi notifikasi, singkat dan faktual.
    """
    nomor = f"NOTIF-UJI-{len(CATATAN_TINDAKAN) + 1:03d}"
    CATATAN_TINDAKAN.append({"nomor": nomor, "jenis": "notifikasi HSE", "penerima": penerima, "pesan": pesan})
    return f"Notifikasi {nomor} dikirim ke {penerima}."


# ---------------------------------------------------------------------------
# Operasi
# ---------------------------------------------------------------------------


@tool(parse_docstring=True)
def laporan_harian(tanggal: str) -> str:
    """Tampilkan laporan produksi harian GS-SR1: minyak, air, gas, jumlah sumur aktif, deferred (produksi tertunda akibat gangguan), dan kejadian.

    Args:
        tanggal: Tanggal format YYYY-MM-DD pada Juli 2026, contoh "2026-07-14".
    """
    baris = _harian()
    baris = baris[baris["tanggal"] == tanggal.strip()]
    if baris.empty:
        return f"Tidak ada laporan untuk tanggal {tanggal}. Data tersedia 2026-07-01 sampai 2026-07-31."
    r = baris.iloc[0]
    kejadian = r["event"] if isinstance(r["event"], str) else "tidak ada kejadian khusus"
    return (f"GS-SR1 {r['tanggal']}: minyak {r['oil_bopd']} bopd, air {r['water_bwpd']} bwpd, gas {r['gas_mmscfd']} MMscfd, "
            f"{r['wells_on']} sumur aktif, deferred {r['deferred_bbl']} bbl. Kejadian: {kejadian}.")


@tool(parse_docstring=True)
def ringkasan_produksi_bulanan() -> str:
    """Ringkas produksi GS-SR1 selama Juli 2026: rata-rata minyak dan air, water cut, total deferred (produksi tertunda), dan hari berkejadian."""
    d = _harian()
    minyak, air = d["oil_bopd"].mean(), d["water_bwpd"].mean()
    kejadian = d[d["event"].notna()]
    terendah = d.loc[d["oil_bopd"].idxmin()]
    return (f"GS-SR1 Juli 2026 ({len(d)} hari): rata-rata minyak {minyak:.0f} bopd, air {air:.0f} bwpd, "
            f"water cut {air / (minyak + air) * 100:.1f}%. Total deferred {d['deferred_bbl'].sum()} bbl. "
            f"{len(kejadian)} hari memiliki kejadian. Minyak terendah {terendah['oil_bopd']} bopd pada {terendah['tanggal']}.")


@tool(parse_docstring=True)
def catat_serah_terima(catatan: str) -> str:
    """Simpan catatan serah terima shift.

    Args:
        catatan: Isi catatan serah terima, singkat dan faktual.
    """
    nomor = f"SHIFT-UJI-{len(CATATAN_TINDAKAN) + 1:03d}"
    CATATAN_TINDAKAN.append({"nomor": nomor, "jenis": "serah terima", "catatan": catatan})
    return f"Catatan serah terima {nomor} disimpan."


@tool(parse_docstring=True)
def bandingkan_produksi(tanggal_a: str, tanggal_b: str) -> str:
    """Bandingkan laporan produksi harian GS-SR1 pada dua tanggal: selisih minyak, air, gas, dan deferred (produksi tertunda akibat gangguan), tanggal_b dikurangi tanggal_a.

    Args:
        tanggal_a: Tanggal pembanding format YYYY-MM-DD pada Juli 2026, contoh "2026-07-10".
        tanggal_b: Tanggal yang dibandingkan format YYYY-MM-DD pada Juli 2026, contoh "2026-07-14".
    """
    d = _harian().set_index("tanggal")
    hilang = [t for t in (tanggal_a.strip(), tanggal_b.strip()) if t not in d.index]
    if hilang:
        return f"Tidak ada laporan untuk tanggal {', '.join(hilang)}. Data tersedia 2026-07-01 sampai 2026-07-31."
    a, b = d.loc[tanggal_a.strip()], d.loc[tanggal_b.strip()]
    return (f"{tanggal_b.strip()} dibanding {tanggal_a.strip()}: minyak {b['oil_bopd'] - a['oil_bopd']:+.0f} bopd "
            f"({a['oil_bopd']} -> {b['oil_bopd']}), air {b['water_bwpd'] - a['water_bwpd']:+.0f} bwpd, "
            f"gas {b['gas_mmscfd'] - a['gas_mmscfd']:+.2f} MMscfd, deferred {b['deferred_bbl'] - a['deferred_bbl']:+.0f} bbl.")


@tool(parse_docstring=True)
def hari_berkejadian(maks: int = 10) -> str:
    """Daftar hari pada Juli 2026 yang punya kejadian khusus di laporan harian GS-SR1, beserta deferred (produksi tertunda) pada hari itu.

    Args:
        maks: Jumlah hari yang ditampilkan (1 sampai 15).
    """
    baris = _harian().dropna(subset=["event"])
    if baris.empty:
        return "Tidak ada hari berkejadian pada Juli 2026."
    teks = [f"{len(baris)} hari berkejadian. Ditampilkan {min(len(baris), max(1, min(maks, 15)))} pertama:"]
    for _, r in baris.head(max(1, min(maks, 15))).iterrows():
        teks.append(f"- {r['tanggal']}: {r['event'][:110]} (deferred {r['deferred_bbl']} bbl)")
    return "\n".join(teks)


def _cari_sumur(kode_sumur: str) -> pd.Series | None:
    baris = _sumur()[_sumur()["kode_sumur"] == kode_sumur.strip().upper()]
    return None if baris.empty else baris.iloc[0]


def _water_cut(minyak: float, air: float) -> float:
    return air / (minyak + air) * 100 if minyak + air else 0.0


@tool(parse_docstring=True)
def cek_status_sumur(kode_sumur: str) -> str:
    """Cek status operasi sebuah sumur: area, jenis pompa, status, produksi minyak dan air, frekuensi VSD (khusus ESP), serta catatan terakhir.

    Args:
        kode_sumur: Kode sumur, contoh "SR-020" atau "KN-033".
    """
    r = _cari_sumur(kode_sumur)
    if r is None:
        return (f"Sumur {kode_sumur} tidak ditemukan. Data memuat {len(_sumur())} sumur dengan kode berpola "
                f"SR-nnn (Seruni), KN-nnn (Kenanga), dan ML-nnn (Melati).")
    vsd = f", VSD {int(r['frekuensi_vsd_hz'])} Hz" if pd.notna(r["frekuensi_vsd_hz"]) else ""
    return (f"Sumur {r['kode_sumur']} ({r['area']}, {r['pompa']}, {r['stasiun']}): status {r['status']}, "
            f"minyak {r['minyak_bopd']} bopd, air {r['air_bwpd']} bwpd{vsd}. Catatan: {r['catatan']} (per {r['diperbarui']})")


@tool(parse_docstring=True)
def daftar_sumur(area: AreaSumur | None = None, pompa: PompaSumur | None = None, status: StatusSumur | None = None,
                 urutkan: UrutSumur = "minyak_tertinggi", maks: int = 10) -> str:
    """Daftar sumur menurut area, jenis pompa, dan status, beserta produksi dan water cut-nya. Semua filter bersifat opsional.

    Args:
        area: Area lapangan (pilihan terbatas).
        pompa: Jenis pompa (pilihan terbatas).
        status: Status sumur (pilihan terbatas).
        urutkan: Urutan hasil (pilihan terbatas): minyak_tertinggi, water_cut_tertinggi, atau kode.
        maks: Jumlah sumur yang ditampilkan (1 sampai 20).
    """
    baris = _sumur()
    if area:
        baris = baris[baris["area"] == area]
    if pompa:
        baris = baris[baris["pompa"] == pompa]
    if status:
        baris = baris[baris["status"] == status]
    if baris.empty:
        return "Tidak ada sumur yang cocok dengan filter tersebut."
    baris = baris.assign(wc=[_water_cut(m, a) for m, a in zip(baris["minyak_bopd"], baris["air_bwpd"])])
    if urutkan == "minyak_tertinggi":
        baris = baris.sort_values(["minyak_bopd", "kode_sumur"], ascending=[False, True])
    elif urutkan == "water_cut_tertinggi":
        baris = baris.sort_values(["wc", "kode_sumur"], ascending=[False, True])
    else:
        baris = baris.sort_values("kode_sumur")
    tampil = max(1, min(maks, 20))
    minyak, air = baris["minyak_bopd"].sum(), baris["air_bwpd"].sum()
    teks = [f"{len(baris)} sumur cocok, total minyak {minyak} bopd, air {air} bwpd, water cut {_water_cut(minyak, air):.1f}%. "
            f"Ditampilkan {min(len(baris), tampil)} pertama ({urutkan.replace('_', ' ')}):"]
    for _, r in baris.head(tampil).iterrows():
        teks.append(f"- {r['kode_sumur']} ({r['area']}, {r['pompa']}, {r['status']}): minyak {r['minyak_bopd']} bopd, "
                    f"air {r['air_bwpd']} bwpd, water cut {r['wc']:.1f}%")
    return "\n".join(teks)


@tool(parse_docstring=True)
def produksi_sumur(kode_sumur: str, dari: str = "2026-07-01", sampai: str = "2026-07-31") -> str:
    """Tampilkan produksi harian sebuah sumur pada rentang tanggal Juli 2026: rata-rata, hari tanpa produksi, dan nilai ekstrem.

    Args:
        kode_sumur: Kode sumur, contoh "SR-041" atau "KN-033".
        dari: Tanggal awal format YYYY-MM-DD, contoh "2026-07-14".
        sampai: Tanggal akhir format YYYY-MM-DD, contoh "2026-07-22".
    """
    r = _cari_sumur(kode_sumur)
    if r is None:
        return f"Sumur {kode_sumur} tidak ditemukan."
    d = _produksi_sumur()
    d = d[(d["kode_sumur"] == r["kode_sumur"]) & (d["tanggal"] >= dari.strip()) & (d["tanggal"] <= sampai.strip())]
    if d.empty:
        return f"Tidak ada data untuk rentang {dari} sampai {sampai}. Data tersedia 2026-07-01 sampai 2026-07-31."
    nol = d[d["minyak_bopd"] == 0]["tanggal"].tolist()
    minyak, air = d["minyak_bopd"].mean(), d["air_bwpd"].mean()
    tinggi, rendah = d.loc[d["minyak_bopd"].idxmax()], d.loc[d["minyak_bopd"].idxmin()]
    teks = [f"{r['kode_sumur']} {d['tanggal'].min()} sampai {d['tanggal'].max()} ({len(d)} hari): rata-rata minyak {minyak:.0f} bopd, "
            f"air {air:.0f} bwpd, water cut {_water_cut(minyak, air):.1f}%.",
            f"Minyak tertinggi {tinggi['minyak_bopd']} bopd ({tinggi['tanggal']}), terendah {rendah['minyak_bopd']} bopd ({rendah['tanggal']}).",
            "Hari tanpa produksi: " + (", ".join(nol) if nol else "tidak ada") + "."]
    if len(d) <= 7:
        teks += [f"- {x['tanggal']}: minyak {x['minyak_bopd']} bopd, air {x['air_bwpd']} bwpd" for _, x in d.iterrows()]
    return "\n".join(teks)


# ---------------------------------------------------------------------------
# Engineering
# ---------------------------------------------------------------------------


@tool(parse_docstring=True)
def ubah_setpoint_vsd(kode_sumur: str, frekuensi_hz: int) -> str:
    """Ubah frekuensi VSD (setpoint) pompa ESP sebuah sumur.

    Args:
        kode_sumur: Kode sumur ESP, contoh "SR-020".
        frekuensi_hz: Frekuensi baru dalam Hz, contoh 48.
    """
    r = _cari_sumur(kode_sumur)
    if r is None:
        return f"Sumur {kode_sumur} tidak ditemukan. Perubahan setpoint tidak dicatat."
    if r["pompa"] != "ESP":
        return f"Sumur {r['kode_sumur']} memakai pompa {r['pompa']}, bukan ESP. VSD hanya untuk ESP, perubahan tidak dicatat."
    if r["status"] != "Produksi":
        return f"Sumur {r['kode_sumur']} berstatus {r['status']}, bukan Produksi. Perubahan setpoint tidak dicatat."
    nomor = f"VSD-UJI-{len(CATATAN_TINDAKAN) + 1:03d}"
    CATATAN_TINDAKAN.append({"nomor": nomor, "jenis": "setpoint VSD", "kode_sumur": r["kode_sumur"], "frekuensi_hz": frekuensi_hz})
    peringatan = " PERINGATAN: di atas 55 Hz memerlukan persetujuan Production Engineer." if frekuensi_hz > 55 else ""
    return f"Setpoint VSD {r['kode_sumur']} dicatat {frekuensi_hz} Hz, sebelumnya {int(r['frekuensi_vsd_hz'])} Hz ({nomor}).{peringatan}"


# ---------------------------------------------------------------------------
# Katalog tool
# ---------------------------------------------------------------------------

# Nama tool yang mengubah sesuatu. Semuanya hanya mencatat ke CATATAN_TINDAKAN, tetapi di sistem nyata
# tool seperti ini harus lewat persetujuan manusia (interrupt).
TULIS = {"buat_work_order", "tutup_work_order", "usulkan_tindakan_korektif", "kirim_notifikasi_hse",
         "catat_serah_terima", "ubah_setpoint_vsd"}

# Keempat use case memakai data dan dokumen perusahaan yang sama, jadi tool-nya sengaja saling terhubung lewat kode yang sama:
# kode sumur (SR-020) juga kode aset pada work order, nomor insiden menghubungkan data insiden dengan tindakan korektif,
# dan SOP, manual, serta laporan dipakai bersama. Dengan begitu satu pertanyaan bisa melintasi beberapa tool (multistep),
# misalnya dari laporan harian ke produksi sumur ke riwayat work order. Tool tulis tetap hanya di use case pemiliknya.
KATALOG: dict[str, list] = {
    "Operasi": [laporan_harian, ringkasan_produksi_bulanan, bandingkan_produksi, hari_berkejadian,
                cek_status_sumur, daftar_sumur, produksi_sumur, riwayat_work_order, cari_dokumen_sop,
                hitung_water_cut, catat_serah_terima],
    "Perawatan": [riwayat_work_order, statistik_kegagalan, aset_downtime_tertinggi, cek_status_sumur, daftar_sumur,
                  produksi_sumur, cari_dokumen_sop, cari_dokumen_manual, buat_work_order, tutup_work_order],
    "HSE": [cari_insiden, ringkasan_insiden, cek_status_sumur, riwayat_work_order, cari_dokumen_sop,
            cari_dokumen_laporan, cari_dokumen_investigasi, usulkan_tindakan_korektif, kirim_notifikasi_hse],
    "Engineering": [cari_dokumen_sop, cari_dokumen_manual, cari_dokumen_laporan, konversi_satuan, hitung_water_cut,
                    cek_status_sumur, daftar_sumur, produksi_sumur, riwayat_work_order, ubah_setpoint_vsd],
}


def semua_tool() -> dict[str, object]:
    """Semua tool katalog tanpa duplikat, nama -> tool, urut menurut kemunculan pertama di KATALOG."""
    unik: dict[str, object] = {}
    for daftar in KATALOG.values():
        for t in daftar:
            unik.setdefault(t.name, t)
    return unik


def use_case_tool(nama: str) -> list[str]:
    """Use case yang memuat tool ini di KATALOG."""
    return [uc for uc, daftar in KATALOG.items() if any(t.name == nama for t in daftar)]


def jenis_tool(t) -> str:
    """'tulis' untuk tool yang mengubah sesuatu (perlu interrupt), 'baca' untuk lainnya."""
    return "tulis" if t.name in TULIS else "baca"
