"""Penjelajah tool dan prompt (Streamlit 1). Anda tidak perlu mengubah file ini.

Tiga tab untuk mengenal bahan agen sebelum merakitnya:

  Tool        : daftar tool beserta ilustrasi, parameter, hasil, contoh pemakaian, dan formulir untuk memanggilnya sendiri
  Prompt      : memilih use case, aturan tool, dan gaya jawaban, lalu menekan "Bangun prompt"
  Pilih tool  : mencentang tool yang akan dipasang ke agen dan mendapatkan snippet kode TOOLS

Hasilnya disalin (copy-paste) ke sel TODO di notebook. Dijalankan dari sel notebook (peluncur.buka("penjelajah")) atau dari
terminal:   streamlit run hari4/11-mini-project/aplikasi/penjelajah.py
"""
import json
import time

import streamlit as st

import alat_data as a
import prompt_bank as pb
from ilustrasi import ilustrasi
from info_tool import info
from sumber_data import tampil_sumber

st.set_page_config(page_title="Penjelajah Tool dan Prompt", layout="wide")

TOOL = a.semua_tool()
LABEL_KELOMPOK = {"Operasi": "Operasi", "Perawatan": "Perawatan", "HSE": "HSE", "Engineering": "Engineering"}


# ---------------------------------------------------------------------------
# Membaca skema argumen tool
# ---------------------------------------------------------------------------


def parameter_tool(t) -> list[dict]:
    """Daftar parameter tool dari skema argumennya: nama, tipe, wajib, bawaan, deskripsi, dan pilihan (enum)."""
    wajib = set(t.tool_call_schema.model_json_schema().get("required", []))
    hasil = []
    for nama, s in t.args.items():
        tipe, enum, kosong = s.get("type"), s.get("enum"), False
        if "anyOf" in s:  # contoh: str | None
            kosong = any(x.get("type") == "null" for x in s["anyOf"])
            jenis = [x for x in s["anyOf"] if x.get("type") != "null"]
            tipe = jenis[0].get("type") if jenis else "string"
            enum = jenis[0].get("enum") if jenis else None
        hasil.append({"nama": nama, "tipe": tipe or "string", "wajib": nama in wajib, "bawaan": s.get("default"),
                      "deskripsi": s.get("description", ""), "enum": enum, "kosong": kosong})
    return hasil


TIPE_INDONESIA = {"string": "teks", "integer": "bilangan bulat", "number": "angka", "boolean": "ya/tidak"}


def tabel_parameter(params: list[dict]) -> str:
    if not params:
        return "_Tool ini tidak memiliki parameter._"
    baris = ["| Parameter | Tipe | Wajib | Bawaan | Keterangan |", "|---|---|---|---|---|"]
    for p in params:
        tipe = TIPE_INDONESIA.get(p["tipe"], p["tipe"])
        if p["enum"]:
            tipe += " (" + " / ".join(map(str, p["enum"])) + ")"
        bawaan = "-" if p["wajib"] else (json.dumps(p["bawaan"], ensure_ascii=False) if p["bawaan"] is not None else "kosong")
        baris.append(f"| `{p['nama']}` | {tipe} | {'ya' if p['wajib'] else 'tidak'} | {bawaan} | {p['deskripsi']} |")
    return "\n".join(baris)


def kode_contoh(nama: str, contoh: dict) -> str:
    argumen = json.dumps(contoh, ensure_ascii=False)
    return f"from alat_data import {nama}\n\nhasil = {nama}.invoke({argumen})\nprint(hasil)"


# ---------------------------------------------------------------------------
# Halaman: daftar tool dan rincian satu tool
# ---------------------------------------------------------------------------


def buka_tool(nama: str):
    st.session_state.tool_dibuka = nama


def tutup_tool():
    st.session_state.tool_dibuka = None


def lencana(nama: str) -> str:
    return ":orange-badge[TULIS]" if a.jenis_tool(TOOL[nama]) == "tulis" else ":blue-badge[BACA]"


def halaman_daftar():
    st.write("Klik **Buka** pada sebuah tool untuk melihat parameter, hasil, dan mencobanya sendiri. "
             "Tool **BACA** hanya mengambil data. Tool **TULIS** mengubah sesuatu, jadi di agen nyata ia perlu persetujuan manusia.")
    pilihan = st.radio("Kelompok", ["Semua", *a.KATALOG], horizontal=True, key="kelompok")
    nama_tool = list(TOOL) if pilihan == "Semua" else [t.name for t in a.KATALOG[pilihan]]
    kolom = st.columns(3)
    for i, nama in enumerate(nama_tool):
        with kolom[i % 3]:
            with st.container(border=True):
                st.image(ilustrasi(nama), width="stretch")
                st.markdown(f"**`{nama}`** {lencana(nama)}")
                st.caption(" · ".join(a.use_case_tool(nama)))
                st.button("Buka", key=f"buka-{nama}", on_click=buka_tool, args=(nama,), width="stretch")


def widget_argumen(nama_tool: str, p: dict, nilai_awal):
    """Satu kotak isian sesuai tipe parameter. Mengembalikan nilai, atau None bila dibiarkan kosong."""
    kunci, label = f"arg-{nama_tool}-{p['nama']}", f"{p['nama']}" + (" *" if p["wajib"] else "")
    if p["enum"]:  # pilihan terbatas (Literal di tool): dropdown; hanya parameter yang tipenya boleh None yang punya pilihan kosong
        pilihan = [None, *p["enum"]] if p["kosong"] else list(p["enum"])
        awal = pilihan.index(nilai_awal) if nilai_awal in pilihan else 0
        return st.selectbox(label, pilihan, index=awal, key=kunci, help=p["deskripsi"],
                            format_func=lambda v: "(tidak diisi)" if v is None else str(v))
    if p["tipe"] == "integer":
        return int(st.number_input(label, value=int(nilai_awal if nilai_awal is not None else 0), step=1, key=kunci, help=p["deskripsi"]))
    if p["tipe"] == "number":
        return float(st.number_input(label, value=float(nilai_awal if nilai_awal is not None else 0), key=kunci, help=p["deskripsi"]))
    if p["tipe"] == "boolean":
        return st.checkbox(label, value=bool(nilai_awal), key=kunci, help=p["deskripsi"])
    teks = st.text_input(label, value="" if nilai_awal is None else str(nilai_awal), key=kunci, help=p["deskripsi"])
    return teks if teks.strip() else None


def halaman_rincian(nama: str):
    t, ket = TOOL[nama], info(nama)
    params = parameter_tool(t)
    tulis = a.jenis_tool(t) == "tulis"

    st.button("< Kembali ke daftar tool", on_click=tutup_tool)
    kiri, kanan = st.columns([1, 2], gap="large")
    with kiri:
        st.image(ilustrasi(nama), width="stretch")
    with kanan:
        st.subheader(f"`{nama}`")
        st.markdown(f"{lencana(nama)}  Dipakai di use case: {', '.join(a.use_case_tool(nama))}")
        st.write(ket["fungsi"])
        st.caption(f"Sumber: {ket['sumber']}")
        if tulis:
            st.warning("Tool TULIS. Di agen nyata, tool seperti ini harus berhenti menunggu persetujuan manusia (komponen 3). "
                       "Di bab ini ia hanya mencatat ke memori, jadi aman dicoba.")

    tab_ring, tab_sumber, tab_model = st.tabs(["Parameter dan coba sendiri", "Sumber data", "Yang dilihat model"])
    with tab_ring:
        st.markdown("#### Parameter")
        st.markdown(tabel_parameter(params))

        st.markdown("#### Yang dikembalikan")
        st.write(ket["hasil"])

        st.markdown("#### Contoh pemakaian")
        st.code(kode_contoh(nama, ket["contoh"]), language="python")
        st.caption("Contoh pertanyaan yang membuat agen memilih tool ini (salin untuk dicoba di aplikasi agen):")
        for q in ket["tanya"]:
            st.code(q, language="text", wrap_lines=True)

        st.markdown("#### Coba sendiri")
        with st.form(f"coba-{nama}"):
            args = {}
            for p in params:
                nilai = widget_argumen(nama, p, ket["contoh"].get(p["nama"], p["bawaan"]))
                if nilai is not None:
                    args[p["nama"]] = nilai
            jalan = st.form_submit_button("Jalankan tool", type="primary")
        if jalan:
            with st.spinner("Menjalankan tool..."):
                mulai = time.perf_counter()
                try:
                    hasil = t.invoke(args)
                    st.session_state.hasil_tool = (nama, args, str(hasil), time.perf_counter() - mulai, None)
                except Exception as e:  # noqa: BLE001 - tampilkan error tool apa adanya, ini bagian dari belajar
                    st.session_state.hasil_tool = (nama, args, None, time.perf_counter() - mulai, f"{type(e).__name__}: {e}")
        tersimpan = st.session_state.get("hasil_tool")
        if tersimpan and tersimpan[0] == nama:
            _, args_dipakai, hasil, detik, pesan_error = tersimpan
            st.caption(f"Argumen yang dikirim ({detik:.2f} detik)")
            st.code(json.dumps(args_dipakai, indent=2, ensure_ascii=False), language="json")
            if pesan_error:
                st.error(pesan_error)
                st.caption("Error dari tool juga dilihat agen. Pesan yang jelas membantu agen memperbaiki panggilannya.")
            else:
                st.caption("Hasil (inilah yang dibaca model sebagai observasi)")
                st.code(hasil, language="text")
        if tulis:
            with st.expander(f"Catatan tindakan di memori ({len(a.CATATAN_TINDAKAN)})"):
                if a.CATATAN_TINDAKAN:
                    st.json(a.CATATAN_TINDAKAN)
                else:
                    st.caption("Belum ada catatan.")
                if st.button("Hapus semua catatan", key=f"hapus-{nama}"):
                    a.CATATAN_TINDAKAN.clear()
                    st.rerun()

    with tab_sumber:
        tersimpan_sumber = st.session_state.get("hasil_tool")
        terakhir = tersimpan_sumber[2] if tersimpan_sumber and tersimpan_sumber[0] == nama else None
        tampil_sumber(nama, terakhir)
    with tab_model:
        st.caption("Model tidak melihat kode tool. Ia hanya membaca nama, deskripsi, dan skema argumen berikut, lalu memutuskan "
                   "apakah tool ini cocok. Deskripsi yang jelas membuat agen memilih tool dengan benar.")
        st.markdown(f"**Nama**: `{t.name}`")
        st.text(t.description)
        st.json(t.args)


# ---------------------------------------------------------------------------
# Tab Prompt
# ---------------------------------------------------------------------------


def tab_prompt():
    st.write("Susun **system prompt** dari tiga bahan: peran use case, aturan yang menyebut tool, dan gaya jawaban. "
             "Pilih, tekan **Bangun prompt**, lalu salin teksnya dan tempel sebagai `system_prompt=` di `create_agent(...)` pada sel TODO. "
             "Teksnya boleh Anda ubah atau tulis sendiri dari nol.")
    kiri, kanan = st.columns(2, gap="large")
    with kiri:
        use_case = st.selectbox("Use case", list(pb.PERAN), key="pb_use_case")
        st.markdown("**Aturan tool** (sebut tool dengan namanya)")
        aturan = []
        for i, r in enumerate(pb.KHUSUS[use_case]):
            if st.checkbox(f"Aturan {i + 1}", value=True, key=f"pb_aturan_{use_case}_{i}"):
                aturan.append(r)
            st.caption(r)
    with kanan:
        gaya = st.multiselect("Gaya jawaban (boleh lebih dari satu)", list(pb.GAYA), default=["ketat"], key="pb_gaya",
                              format_func=lambda g: g)
        for g in gaya:
            st.caption(f"**{g}**: {pb.GAYA_KETERANGAN[g]}")
        st.markdown("**Pertanyaan contoh untuk use case ini**")
        for jenis in ("baca", "tulis", "tanpa_data", "di_luar"):
            st.caption(f"{jenis}: {pb.PERTANYAAN[use_case][jenis][0]}")
    if st.button("Bangun prompt", type="primary"):
        st.session_state.prompt_dibangun = (use_case, pb.susun_prompt(use_case, gaya or "minimal", aturan))
    if "prompt_dibangun" in st.session_state:
        use_case_jadi, teks = st.session_state.prompt_dibangun
        st.markdown(f"##### Hasil: teks system prompt untuk {use_case_jadi}")
        st.code(teks, language="text", wrap_lines=True)
        disebut = [n for n in TOOL if n in teks]
        keranjang = set(st.session_state.get("keranjang", []))
        if disebut:
            st.caption("Tool yang disebut prompt ini: " + ", ".join(f"`{n}`" for n in disebut))
            hilang = [n for n in disebut if keranjang and n not in keranjang]
            if hilang:
                st.warning("Prompt menyebut tool yang belum Anda pilih di tab **Pilih tool**: "
                           + ", ".join(f"`{n}`" for n in hilang) + ". Agen akan diperintah memakai tool yang tidak ia miliki.")


# ---------------------------------------------------------------------------
# Tab Pilih tool
# ---------------------------------------------------------------------------


def isi_dari_use_case():
    st.session_state.keranjang = [t.name for t in a.KATALOG[st.session_state.contoh_use_case]]


def tab_pilih():
    st.write("Centang tool yang akan dipasang ke agen. Anda boleh mengambil dari beberapa use case sekaligus. "
             "Tool yang lebih sedikit biasanya membuat agen lebih mudah memilih dengan benar.")
    kiri, kanan = st.columns([3, 1], vertical_alignment="bottom")
    with kanan:
        st.selectbox("Mulai dari use case", list(a.KATALOG), key="contoh_use_case")
        st.button("Isi dari use case", on_click=isi_dari_use_case, width="stretch")
    with kiri:
        st.multiselect("Tool untuk agen Anda", list(TOOL), key="keranjang",
                       format_func=lambda n: f"{n}  [{a.jenis_tool(TOOL[n]).upper()}]")
    pilih = st.session_state.get("keranjang", [])
    if not pilih:
        st.info("Belum ada tool yang dipilih.")
        return
    tulis = [n for n in pilih if a.jenis_tool(TOOL[n]) == "tulis"]
    impor = "from alat_data import (\n" + "".join(f"    {n},\n" for n in pilih) + ")"
    kode = impor + "\n\nTOOLS = [\n" + "".join(f"    {n},\n" for n in pilih) + "]"
    st.markdown("##### Komponen 1: TOOLS")
    st.code(kode, language="python")
    if tulis:
        st.warning("Tool TULIS yang Anda pilih: " + ", ".join(f"`{n}`" for n in tulis) + ". Tool tulis mengubah sesuatu. Anda sendiri yang "
                   "menentukan apakah dan bagaimana tool ini dipasangi `HumanInTheLoopMiddleware` (bab 6), lalu amati reaksi agen di "
                   "aplikasi agen dan Panduan uji.")
    else:
        st.caption("Semua tool yang dipilih hanya membaca.")


# ---------------------------------------------------------------------------
# Halaman utama
# ---------------------------------------------------------------------------

st.title("Penjelajah Tool dan Prompt")
st.session_state.setdefault("tool_dibuka", None)
tab_tool, tab_pr, tab_pil = st.tabs(["Tool", "Prompt", "Pilih tool"])
with tab_tool:
    if st.session_state.tool_dibuka:
        halaman_rincian(st.session_state.tool_dibuka)
    else:
        halaman_daftar()
with tab_pr:
    tab_prompt()
with tab_pil:
    tab_pilih()
