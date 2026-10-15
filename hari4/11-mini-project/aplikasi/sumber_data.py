"""Sumber data setiap tool, untuk tab "Sumber data" di Penjelajah.

Peserta perlu tahu dari mana sebuah tool mengambil jawabannya, dan seperti apa data yang mungkin ia tarik:

  csv      : tabel yang dibaca tool (file CSV, kolom yang dipakai, seluruh baris)
  dokumen  : dokumen asli (teks atau PDF), chunk hasil pemecahan, dan dokumen mana yang terjangkau tool
  rumus    : tool yang menghitung dan tidak membaca data
  memori   : tool tulis yang hanya mencatat ke daftar CATATAN_TINDAKAN

SUMBER[nama_tool] memetakan tool ke jenis sumbernya; tampil_sumber() menggambarnya di Streamlit.
"""
import re
from pathlib import Path

import pandas as pd
import streamlit as st

import alat_data as a
from migas_shared import rag_pipeline as rp
from migas_shared.config import ROOT

TABEL = {
    "harian": {
        "judul": "Laporan produksi harian GS-SR1, Juli 2026",
        "file": ["data/eval/daily_gs_sr1_2026-07.csv"],
        "baca": a.tabel_harian,
        "catatan": "Satu baris per hari. Kolom `event` kosong pada hari tanpa kejadian khusus.",
    },
    "work_order": {
        "judul": "Work order pemeliharaan",
        "file": ["data/raw/work_orders.csv", "data/eval/work_orders_truth.csv"],
        "baca": a.tabel_work_order,
        "catatan": "Dua file digabung pada `wo_id`. Kolom `deskripsi` adalah teks mentah dari laporan lapangan; kolom lain "
                   "(aset, tipe peralatan, kategori kegagalan, komponen, tindakan, downtime) adalah hasil ekstraksi terstruktur "
                   "seperti yang dikerjakan di hari 1.",
    },
    "sumur": {
        "judul": "Daftar sumur dan statusnya per 31 Juli 2026",
        "file": ["data/field/sumur.csv"],
        "baca": a.tabel_sumur,
        "catatan": "Satu baris per sumur (Seruni, Kenanga, Melati). Mewakili sistem pemantauan sumur (SCADA). Kolom `frekuensi_vsd_hz` hanya terisi "
                   "untuk sumur ESP yang berproduksi. Sumur yang tidak berproduksi punya minyak dan air 0.",
    },
    "produksi_sumur": {
        "judul": "Produksi harian semua sumur, Juli 2026",
        "file": ["data/field/produksi_sumur_2026-07.csv"],
        "baca": a.tabel_produksi_sumur,
        "catatan": "Satu baris per sumur per hari (196 sumur x 31 hari). Jumlah minyak dan air sumur Seruni pada satu hari sama dengan "
                   "laporan harian GS-SR1; sumur yang berhenti (misalnya SR-014, SR-041, KN-033) bernilai 0 pada hari itu.",
    },
    "insiden": {
        "judul": "Insiden HSE",
        "file": ["data/raw/hse_incidents.csv", "data/eval/hse_incidents_truth.csv"],
        "baca": a.tabel_insiden,
        "catatan": "Dua file digabung pada `incident_id`. Kolom `narasi` adalah teks mentah; `incident_type`, `hazard`, dan `severity` "
                   "adalah hasil klasifikasi seperti yang dikerjakan di hari 1.",
    },
}

SUMBER = {
    "laporan_harian": {"jenis": "csv", "tabel": "harian", "kolom": ["tanggal", "oil_bopd", "water_bwpd", "gas_mmscfd", "wells_on", "deferred_bbl", "event"]},
    "ringkasan_produksi_bulanan": {"jenis": "csv", "tabel": "harian", "kolom": ["tanggal", "oil_bopd", "water_bwpd", "deferred_bbl", "event"]},
    "bandingkan_produksi": {"jenis": "csv", "tabel": "harian", "kolom": ["tanggal", "oil_bopd", "water_bwpd", "gas_mmscfd", "deferred_bbl"]},
    "hari_berkejadian": {"jenis": "csv", "tabel": "harian", "kolom": ["tanggal", "event", "deferred_bbl"]},
    "riwayat_work_order": {"jenis": "csv", "tabel": "work_order",
                           "kolom": ["wo_id", "tanggal", "asset_id", "failure_category", "component", "action_category", "downtime_hours"]},
    "cari_work_order": {"jenis": "csv", "tabel": "work_order",
                        "kolom": ["wo_id", "tanggal", "asset_id", "equipment_type", "area", "failure_category", "component", "action_category", "downtime_hours"]},
    "statistik_kegagalan": {"jenis": "csv", "tabel": "work_order", "kolom": ["equipment_type", "failure_category", "downtime_hours"]},
    "aset_downtime_tertinggi": {"jenis": "csv", "tabel": "work_order", "kolom": ["asset_id", "equipment_type", "wo_id", "downtime_hours"]},
    "tutup_work_order": {"jenis": "csv", "tabel": "work_order", "kolom": ["wo_id"],
                         "catatan": "Tool ini hanya membaca kolom `wo_id` untuk memastikan nomor ada, lalu mencatat penutupan ke memori."},
    "cari_insiden": {"jenis": "csv", "tabel": "insiden", "kolom": ["incident_id", "tanggal", "lokasi", "narasi", "incident_type", "hazard", "severity"]},
    "ringkasan_insiden": {"jenis": "csv", "tabel": "insiden", "kolom": ["hazard", "severity", "lokasi"]},
    "cek_status_sumur": {"jenis": "csv", "tabel": "sumur",
                         "kolom": ["kode_sumur", "area", "stasiun", "pompa", "status", "minyak_bopd", "air_bwpd", "frekuensi_vsd_hz", "catatan"]},
    "daftar_sumur": {"jenis": "csv", "tabel": "sumur", "kolom": ["kode_sumur", "area", "pompa", "status", "minyak_bopd", "air_bwpd"]},
    "produksi_sumur": {"jenis": "csv", "tabel": "produksi_sumur", "kolom": ["tanggal", "kode_sumur", "minyak_bopd", "air_bwpd"],
                       "catatan": "Tool hanya membaca baris untuk satu sumur dan rentang tanggal yang diminta."},
    "ubah_setpoint_vsd": {"jenis": "csv", "tabel": "sumur", "kolom": ["kode_sumur", "pompa", "status", "frekuensi_vsd_hz"],
                          "catatan": "Tool memeriksa bahwa sumur ada, berpompa ESP, dan berstatus Produksi, lalu mencatat perubahan ke memori (file CSV tidak berubah). "
                                     "Nilai di atas 55 Hz memunculkan peringatan."},
    "hitung_water_cut": {"jenis": "rumus"},
    "konversi_satuan": {"jenis": "rumus"},
    "catat_serah_terima": {"jenis": "memori"},
    "buat_work_order": {"jenis": "memori"},
    "usulkan_tindakan_korektif": {"jenis": "memori"},
    "kirim_notifikasi_hse": {"jenis": "memori"},
    "cari_dokumen_sop": {"jenis": "dokumen"},
    "cari_dokumen_manual": {"jenis": "dokumen"},
    "cari_dokumen_laporan": {"jenis": "dokumen"},
    "cari_dokumen_investigasi": {"jenis": "dokumen"},
}

_BLOK = re.compile(r'<dokumen id="([^"]+)" revisi="([^"]*)" status="[^"]*" bagian="([^"]*)">')


# ---------------------------------------------------------------------------
# Data dokumen
# ---------------------------------------------------------------------------


@st.cache_data(show_spinner=False)
def dokumen_asli() -> list[dict]:
    """Semua dokumen bab 11 (data/docs dan data/docs_bab11): metadata, file asal, dan teks isinya (PDF diekstrak oleh loader hari 2)."""
    hasil = []
    for d in a.muat_dokumen():
        m = d.metadata
        hasil.append({"doc_id": m.get("doc_id", "?"), "judul": m.get("title", ""), "jenis": m.get("doc_type", ""),
                      "revisi": m.get("revision", ""), "status": m.get("status", ""), "akses": m.get("access_group", ""),
                      "file": Path(m.get("source", "")).as_posix(), "folder": m.get("folder", "docs"), "tipe_file": m.get("file_type", ""), "isi": d.page_content})
    return hasil


def alasan_tidak_terjangkau(d: dict, nama_tool: str) -> str:
    """Kosong bila dokumen terjangkau tool, selain itu alasannya dalam satu frasa."""
    jenis, peran = a.SUMBER_DOKUMEN[nama_tool]
    if d["jenis"] not in jenis:
        return f"jenis {d['jenis']}"
    if d["status"] != "active":
        return f"status {d['status']}"
    if d["akses"] not in rp.ROLE_GROUPS[peran]:
        return f"akses {d['akses']} butuh peran lain"
    return ""


def chunk_dokumen(doc_id: str, revisi: str) -> list:
    return [c for c in a.retriever_bab11().chunks if c.metadata.get("doc_id") == doc_id and str(c.metadata.get("revision")) == str(revisi)]


def blok_terambil(hasil: str | None) -> set[tuple[str, str, str]]:
    """(doc_id, revisi, bagian) dari blok <dokumen ...> pada hasil sebuah tool pencarian."""
    return set(_BLOK.findall(hasil or ""))


# ---------------------------------------------------------------------------
# Tampilan
# ---------------------------------------------------------------------------


def _csv(nama: str, spek: dict) -> None:
    tabel = TABEL[spek["tabel"]]
    df = tabel["baca"]()
    st.markdown(f"**{tabel['judul']}**: {len(df)} baris, {len(df.columns)} kolom")
    st.caption("File: " + ", ".join(f"`{b}`" for b in tabel["file"]))
    st.caption(tabel["catatan"])
    if spek.get("catatan"):
        st.caption(spek["catatan"])
    hanya = st.toggle("Hanya kolom yang dibaca tool ini", value=True, key=f"kolom-{nama}")
    st.dataframe(df, height=340, hide_index=True, column_order=spek["kolom"] if hanya else None)
    st.caption("Tabel di atas bisa diurutkan dan dicari. Inilah semua data yang mungkin ditarik tool; agen hanya melihat hasil yang dikembalikan tool.")


def _rumus(nama: str) -> None:
    if nama == "hitung_water_cut":
        st.markdown("Tool ini **tidak membaca data**. Ia menghitung dari dua angka yang diberikan:")
        st.latex(r"\text{water cut (\%)} = \frac{\text{air (bwpd)}}{\text{minyak (bopd)} + \text{air (bwpd)}} \times 100")
        st.dataframe(pd.DataFrame({"minyak (bopd)": [120, 95, 0], "air (bwpd)": [480, 380, 0],
                                   "hasil": [a.hitung_water_cut.invoke({"oil_bopd": m, "water_bwpd": w}) for m, w in [(120, 480), (95, 380), (0, 0)]]}),
                     hide_index=True)
    else:
        st.markdown("Tool ini **tidak membaca data**. Ia memakai faktor konversi tetap:")
        baris = [(d, k, a.konversi_satuan.invoke({"nilai": 1, "dari": d, "ke": k})) for d, k in [("bbl", "m3"), ("m3", "bbl"), ("psi", "bar"), ("bar", "psi")]]
        st.dataframe(pd.DataFrame(baris, columns=["dari", "ke", "hasil untuk nilai 1"]), hide_index=True)
        st.caption("Pasangan satuan lain (misalnya psi ke m3) tidak ada di tabel dan menghasilkan pesan error.")


def _memori(nama: str) -> None:
    st.markdown("Tool ini **tidak membaca data**. Ia hanya menambah satu catatan ke daftar `CATATAN_TINDAKAN` di memori proses:")
    st.json(a.CATATAN_TINDAKAN[-3:] if a.CATATAN_TINDAKAN else [], expanded=True)
    st.caption("Di sistem nyata tool seperti ini menulis ke sistem lain (work order, logbook, pesan), itulah sebabnya perlu persetujuan manusia. "
               "Catatan lengkap dan tombol hapus ada di bawah formulir **Coba sendiri**.")


def _dokumen(nama: str, hasil_terakhir: str | None) -> None:
    jenis, peran = a.SUMBER_DOKUMEN[nama]
    izin = rp.ROLE_GROUPS[peran]
    semua = dokumen_asli()
    st.markdown(f"Tool ini mencari di dokumen berjenis **{', '.join(sorted(jenis))}**, berstatus `active`, dengan hak akses **{', '.join(izin)}** "
                f"(peran tetap `{peran}`).")
    tabel = pd.DataFrame([{"doc_id": d["doc_id"], "judul": d["judul"], "jenis": d["jenis"], "revisi": d["revisi"], "status": d["status"],
                           "akses": d["akses"], "file": d["file"], "terjangkau": "ya" if not (al := alasan_tidak_terjangkau(d, nama)) else f"tidak ({al})"}
                          for d in semua]).sort_values(["terjangkau", "doc_id"], key=lambda s: s.str.startswith("tidak") if s.name == "terjangkau" else s)
    with st.expander(f"Seluruh {len(tabel)} dokumen di basis pengetahuan dan apakah terjangkau tool ini", expanded=False):
        st.dataframe(tabel, hide_index=True)
        st.caption("Dokumen berstatus `superseded` (revisi lama) dan dokumen berakses terbatas tidak ikut pencarian. Inilah cara hak akses dan status ditegakkan.")

    milik = [d for d in semua if d["jenis"] in jenis]
    terambil = blok_terambil(hasil_terakhir)
    kunci = f"dok-{nama}"
    if terambil and st.session_state.get(f"{kunci}-hasil") != hasil_terakhir:  # hasil baru: buka dokumen yang terambil lebih dulu
        st.session_state[f"{kunci}-hasil"] = hasil_terakhir
        pertama = next((i for i, x in enumerate(milik) if (x["doc_id"], str(x["revisi"])) in {(t[0], t[1]) for t in terambil}), None)
        if pertama is not None:
            st.session_state[kunci] = pertama
    pilih = st.selectbox("Pilih dokumen untuk dibaca", range(len(milik)), key=kunci,
                         format_func=lambda i: f"{milik[i]['doc_id']} rev {milik[i]['revisi']} ({milik[i]['status']}): {milik[i]['judul']}")
    d = milik[pilih]
    if terambil:
        st.info(f"Hasil pencarian terakhir mengambil {len(terambil)} chunk. Chunk yang terambil ditandai pada tab Chunk.")
    tab_asli, tab_chunk = st.tabs(["Dokumen asli", "Chunk hasil pemecahan"])
    with tab_asli:
        st.caption(f"File `data/{d['folder']}/{d['file']}`, status {d['status']}, akses {d['akses']}.")
        if d["tipe_file"] == "pdf":
            path = ROOT / "data" / d["folder"] / d["file"]
            st.download_button("Unduh PDF asli", path.read_bytes(), file_name=path.name, mime="application/pdf", key=f"unduh-{nama}-{d['doc_id']}")
            st.caption("Teks hasil ekstraksi PDF (inilah yang dibaca dan dipecah menjadi chunk):")
        st.code(d["isi"], language="markdown", wrap_lines=True, height=420)
    with tab_chunk:
        with st.spinner("Memuat chunk dari indeks..."):
            chunk = chunk_dokumen(d["doc_id"], d["revisi"])
        if not chunk:
            st.warning("Dokumen ini tidak punya chunk di indeks (misalnya indeks dibangun sebelum dokumen ditambahkan).")
        else:
            st.caption(f"{len(chunk)} chunk, dipecah per heading (strategi `markdown`, sekitar 800 karakter). Setiap chunk diawali satu baris "
                       "penanda dokumen dan bagian, supaya bisa dikutip sebagai [DOC_ID bagian].")
        for c in chunk:
            m = c.metadata
            kena = (str(m.get("doc_id")), str(m.get("revision")), str(m.get("section"))) in terambil
            with st.expander(f"{'[TERAMBIL] ' if kena else ''}{m.get('chunk_id')}  |  bagian: {m.get('section')}  |  {len(c.page_content)} karakter", expanded=kena):
                st.code(c.page_content, language="markdown", wrap_lines=True)


def tampil_sumber(nama: str, hasil_terakhir: str | None = None) -> None:
    """Gambar bagian "Sumber data" untuk tool `nama`. hasil_terakhir: teks hasil panggilan terakhir tool ini (untuk menandai chunk)."""
    spek = SUMBER.get(nama)
    if spek is None:
        st.info("Sumber data tool ini belum dijelaskan.")
    elif spek["jenis"] == "csv":
        _csv(nama, spek)
    elif spek["jenis"] == "rumus":
        _rumus(nama)
    elif spek["jenis"] == "memori":
        _memori(nama)
    else:
        _dokumen(nama, hasil_terakhir)
