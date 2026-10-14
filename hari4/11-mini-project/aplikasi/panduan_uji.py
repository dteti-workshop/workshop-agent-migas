"""Panduan uji agen (Streamlit 3). Anda tidak perlu mengubah file ini.

Pilih tool yang terpasang pada agen Anda, lalu aplikasi menampilkan pertanyaan yang cocok beserta KRITERIA BERHASIL.
Alurnya, untuk setiap butir:

  1. salin pertanyaan (ikon salin di pojok kotak)
  2. tempel ke aplikasi agen dan amati jejaknya: Aksi apa, argumen apa, hasil apa
  3. centang kriteria yang terpenuhi. Kriteria yang tidak terpenuhi menunjukkan apa yang perlu diperbaiki
     (prompt, tool, atau aturan persetujuan)

Tidak ada penilaian otomatis: Andalah yang membaca jejak dan menilai. Dijalankan dari sel notebook
(peluncur.buka("uji")) atau dari terminal:   streamlit run hari4/11-mini-project/aplikasi/panduan_uji.py
"""
import streamlit as st

import alat_data as a
import bank_uji as bu

st.set_page_config(page_title="Panduan Uji Agen", layout="wide")

SEMUA_TOOL = list(a.semua_tool())


def isi_dari_use_case():
    st.session_state.uji_tool = [t.name for t in a.KATALOG[st.session_state.uji_use_case]]


def kosongkan():
    st.session_state.uji_tool = []


st.title("Panduan Uji Agen")
st.write("Agen yang terlihat bagus pada satu pertanyaan belum tentu bagus pada pertanyaan lain. Pilih tool yang terpasang pada agen Anda "
         "untuk melihat pertanyaan dan kriteria berhasil yang cocok. Salin pertanyaan ke **aplikasi agen**, amati jejaknya, "
         "lalu centang kriteria yang terpenuhi.")

kiri, kanan = st.columns([3, 1], vertical_alignment="bottom")
with kanan:
    st.selectbox("Mulai dari use case", list(a.KATALOG), key="uji_use_case")
    st.button("Isi dari use case", on_click=isi_dari_use_case, width="stretch")
with kiri:
    st.multiselect("Tool yang terpasang pada agen saya", SEMUA_TOOL, key="uji_tool",
                   format_func=lambda n: f"{n}  [{a.jenis_tool(a.semua_tool()[n]).upper()}]")
    jenis_dipilih = st.multiselect("Jenis butir", list(bu.JENIS), default=list(bu.JENIS), format_func=bu.JENIS.get)

pilihan = set(st.session_state.get("uji_tool", []))
butir = bu.butir_untuk(pilihan, set(jenis_dipilih))

# ------------------------------------------------------------------ ringkasan di sidebar
total = sum(len(b["kriteria"]) for b in butir)
terpenuhi = sum(1 for b in butir for i in range(len(b["kriteria"])) if st.session_state.get(f"krit-{b['id']}-{i}"))
with st.sidebar:
    st.header("Kemajuan")
    st.progress(terpenuhi / total if total else 0.0, text=f"{terpenuhi} dari {total} kriteria terpenuhi")
    st.caption(f"{len(butir)} butir untuk {len(pilihan)} tool terpilih.")
    st.caption("Kriteria yang belum terpenuhi bukan kegagalan Anda. Ia menunjuk bagian yang bisa diperbaiki: instruksi, tool, atau aturan persetujuan.")

if not butir:
    st.info("Belum ada butir. Pilih tool di atas, atau tekan **Isi dari use case**, dan pastikan minimal satu jenis butir dipilih.")

# ------------------------------------------------------------------ butir uji
for jenis, nama_jenis in bu.JENIS.items():
    kelompok = [b for b in butir if b["jenis"] == jenis]
    if not kelompok:
        continue
    st.subheader(nama_jenis)
    for b in kelompok:
        with st.container(border=True):
            lencana = " ".join(f":blue-badge[{t}]" for t in b["butuh"]) or ":gray-badge[tanpa tool]"
            if b.get("tanpa"):
                lencana += " " + " ".join(f":red-badge[tanpa {t}]" for t in b["tanpa"])
            st.markdown(lencana)
            st.caption("Pertanyaan (salin ke aplikasi agen)")
            st.code(b["pertanyaan"], language="text", wrap_lines=True)
            st.caption("Kriteria berhasil")
            ok = 0
            for i, kriteria in enumerate(b["kriteria"]):
                ok += st.checkbox(kriteria, key=f"krit-{b['id']}-{i}")
            st.caption(f"{ok} dari {len(b['kriteria'])} kriteria terpenuhi")
            with st.expander("Apa yang dilihat dan dipelajari"):
                st.write(b["petunjuk"])

# ------------------------------------------------------------------ butir yang hampir cocok
hampir = bu.butir_hampir(pilihan)
if hampir:
    with st.expander(f"{len(hampir)} butir lain butuh satu tool tambahan"):
        for b, kurang in hampir:
            st.markdown(f"- {b['pertanyaan']}  \n  butuh tambahan: " + ", ".join(f"`{t}`" for t in kurang))

st.subheader("Eksperimen yang disarankan")
st.caption("Ubah sel TODO di notebook, daftarkan ulang agen (muncul sebagai versi baru di sidebar aplikasi agen), lalu bandingkan dua versi.")
for judul, isi in bu.EKSPERIMEN:
    with st.expander(judul):
        st.write(isi)
