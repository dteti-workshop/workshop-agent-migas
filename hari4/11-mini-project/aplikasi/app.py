"""Aplikasi agen (Streamlit 2). Anda tidak perlu mengubah file ini.

Aplikasi ini mengobrol dengan agen yang Anda rakit di notebook (didaftarkan dengan `kerangka.daftarkan_agen(...)`):

  - chat dengan jawaban yang tampil saat ditulis (streaming)
  - jejak kerja agen: setiap langkah "Aksi" (tool, argumen, hasil) tampil bernomor di expander, dan teks yang ditulis
    model sebelum memanggil tool ditandai "Pikir". Inilah pola ReAct: Pikir -> Aksi -> Observasi -> ... -> Jawaban
  - persetujuan manusia: bila agen berhenti di sebuah tool, formulir approve, edit, atau reject muncul
  - sidebar riwayat percakapan seperti ChatGPT, didukung checkpointer milik agen (bab 5)

Dijalankan dari sel notebook: peluncur.buka("agen"). Fasilitator dapat menampilkan agen contoh dengan
TAMPILKAN_SOLUSI=1:   TAMPILKAN_SOLUSI=1 streamlit run hari4/11-mini-project/aplikasi/app.py
"""
import json
import os
import uuid
from pathlib import Path

import streamlit as st
from langchain_core.messages import HumanMessage

import kerangka as k

LABEL = {"approve": "Setujui", "edit": "Ubah", "reject": "Tolak"}
FOLDER = Path(__file__).resolve().parent
TAMPILKAN_FILE = os.environ.get("TAMPILKAN_SOLUSI") == "1"

st.set_page_config(page_title="Aplikasi Agen", layout="wide")


# ---------------------------------------------------------------------------
# Sumber daya yang bertahan antar rerun Streamlit
# ---------------------------------------------------------------------------


@st.cache_resource
def penyimpanan() -> k.Penyimpanan:
    """Daftar percakapan untuk sidebar (dan checkpointer bersama untuk agen dari file). Hilang bila aplikasi dihentikan."""
    return k.Penyimpanan()


@st.cache_resource(show_spinner="Menyiapkan agen...")
def agen_dari_file(nama: str, versi: float):
    """Agen dari file (agen contoh untuk fasilitator). `versi` (waktu ubah file) membangunnya ulang setelah file diubah."""
    return k.bangun_agen(nama, penyimpanan().saver)


def versi_file(nama: str) -> float:
    files = [FOLDER / "agen" / f"{nama}.py", k.FOLDER_SOLUSI / f"{nama}.py", FOLDER / "alat_data.py"]
    return max(f.stat().st_mtime for f in files if f.exists())


def ambil_agen(nama: str):
    """(judul, pengantar, contoh_pertanyaan, agen) untuk agen terdaftar atau agen dari file."""
    if nama in k.AGEN_TERDAFTAR:
        a = k.AGEN_TERDAFTAR[nama]
        return a.judul, a.pengantar, a.contoh_pertanyaan, a.agen
    modul, agen = agen_dari_file(nama, versi_file(nama))
    return modul.JUDUL, modul.PENGANTAR, modul.CONTOH_PERTANYAAN, agen


def semua_nama_agen() -> list[str]:
    terdaftar = list(reversed(k.AGEN_TERDAFTAR))  # yang terbaru di atas
    return terdaftar + (k.daftar_agen(dengan_solusi=True) if TAMPILKAN_FILE else [])


# ---------------------------------------------------------------------------
# Aksi sidebar
# ---------------------------------------------------------------------------


def percakapan_baru():
    st.session_state.thread_id = None


def buka_percakapan(thread_id: str):
    st.session_state.thread_id = thread_id
    st.session_state.agen = penyimpanan().percakapan[thread_id]["agen"]


def pakai_contoh(teks: str):
    st.session_state.antrean = teks


# ---------------------------------------------------------------------------
# Menggambar jejak kerja agen
# ---------------------------------------------------------------------------


def tampil_hasil(wadah, hasil: str | None):
    """Hasil tool (observasi) dalam kotak kode; hasil yang panjang diberi tinggi tetap agar halaman tidak memanjang."""
    if hasil is None:
        wadah.caption("(belum ada hasil: menunggu persetujuan Anda, atau tool belum dijalankan)")
    else:
        wadah.code(hasil, language="text", wrap_lines=True, height=280 if len(hasil) > 900 else "content")


def gambar_tool(nomor: int, nama: str, args: dict, hasil: str | None, terbuka: bool = False):
    """Satu langkah Aksi: expander berisi nama tool, argumen, dan hasilnya."""
    with st.expander(f"Aksi {nomor}: {nama}", expanded=terbuka):
        st.caption("Tool")
        st.code(nama, language="text")
        st.caption("Argumen yang dikirim model")
        st.code(json.dumps(args, indent=2, ensure_ascii=False), language="json")
        st.caption("Hasil (observasi yang dibaca model)")
        tampil_hasil(st, hasil)


def pikir(teks: str):
    st.markdown("> **Pikir.** " + teks.strip().replace("\n", "\n> "))


def gambar_giliran_agen(bagian: list):
    """Bagian-bagian satu giliran asisten: teks sebelum tool = Pikir, tool = Aksi, teks terakhir = Jawaban."""
    terakhir_tool = max((i for i, b in enumerate(bagian) if b[0] == "tool"), default=-1)
    nomor = 0
    for i, b in enumerate(bagian):
        if b[0] == "tool":
            nomor += 1
            gambar_tool(nomor, *b[1:])
        elif i < terakhir_tool:
            pikir(b[1])
        else:
            if nomor:
                st.caption("Jawaban akhir")
            st.markdown(b[1])


def gambar_riwayat(agen, thread_id: str):
    for giliran in k.pesan_untuk_tampilan(agen, thread_id):
        with st.chat_message(giliran["peran"]):
            if giliran["peran"] == "user":
                st.markdown(giliran["teks"])
            else:
                gambar_giliran_agen(giliran["bagian"])


def jalankan_dan_tampilkan(agen, masukan, thread_id: str) -> bool:
    """Jalankan agen sambil menggambar langsung. Kembalikan False bila terjadi error."""
    with st.chat_message("assistant"):
        wadah = st.container()
        tempat, buffer = wadah.empty(), ""
        nomor, antre = 0, {}  # antre: nama tool -> tempat hasil yang menunggu (hasil tiba berurutan menurut panggilan)
        try:
            for p in k.jalankan(agen, masukan, thread_id):
                if p.jenis == "teks":
                    buffer += p.teks
                    tempat.markdown(buffer)
                elif p.jenis == "tool":
                    tempat.empty()
                    if buffer.strip():  # teks yang ditulis model sebelum memanggil tool
                        with wadah:
                            pikir(buffer)
                    nomor += 1
                    with wadah.expander(f"Aksi {nomor}: {p.nama}", expanded=True):
                        st.caption("Argumen yang dikirim model")
                        st.code(json.dumps(p.args, indent=2, ensure_ascii=False), language="json")
                        st.caption("Hasil (observasi yang dibaca model)")
                        slot = st.empty()
                        slot.caption("(menunggu hasil...)")
                    antre.setdefault(p.nama, []).append(slot)
                    tempat, buffer = wadah.empty(), ""
                elif p.jenis == "hasil_tool" and antre.get(p.nama):
                    tampil_hasil(antre[p.nama].pop(0), p.teks)
        except Exception as e:  # noqa: BLE001 - tampilkan error model atau tool apa adanya
            st.error(f"Agen gagal: {type(e).__name__}: {e}")
            return False
    return True


def formulir_persetujuan(menunggu: dict, thread_id: str) -> list[dict] | None:
    """Tampilkan permintaan persetujuan. Kembalikan daftar keputusan setelah dikirim, atau None."""
    with st.chat_message("assistant"):
        st.warning("Agen menunggu keputusan Anda sebelum menjalankan tindakan berikut.")
        with st.form(f"setuju-{thread_id}-{menunggu['id']}"):
            isian = []
            for i, (permintaan, tinjau) in enumerate(zip(menunggu["action_requests"], menunggu["review_configs"])):
                boleh = tinjau["allowed_decisions"]
                st.markdown(f"**{permintaan['name']}**")
                teks_args = json.dumps(permintaan["args"], indent=2, ensure_ascii=False)
                st.code(teks_args, language="json")
                pilihan = st.radio("Keputusan", boleh, format_func=LABEL.get, horizontal=True, key=f"k{i}-{menunggu['id']}")
                args_baru = st.text_area("Argumen baru (JSON), dipakai bila memilih Ubah", teks_args, key=f"a{i}-{menunggu['id']}") \
                    if "edit" in boleh else None
                alasan = st.text_input("Alasan bila ditolak (opsional)", key=f"r{i}-{menunggu['id']}")
                isian.append((permintaan, pilihan, args_baru, alasan))
            kirim = st.form_submit_button("Kirim keputusan", type="primary")
    if not kirim:
        return None
    keputusan = []
    for permintaan, pilihan, args_baru, alasan in isian:
        if pilihan == "approve":
            keputusan.append({"type": "approve"})
        elif pilihan == "reject":
            keputusan.append({"type": "reject", "message": alasan or "Ditolak oleh reviewer"})
        else:
            try:
                keputusan.append({"type": "edit", "edited_action": {"name": permintaan["name"], "args": json.loads(args_baru)}})
            except json.JSONDecodeError as e:
                st.error(f"Argumen baru untuk {permintaan['name']} bukan JSON yang valid: {e}")
                return None
    return keputusan


# ---------------------------------------------------------------------------
# Halaman
# ---------------------------------------------------------------------------

simpan = penyimpanan()
st.session_state.setdefault("thread_id", None)
st.session_state.setdefault("jumlah_terdaftar", 0)

# Agen baru didaftarkan dari notebook: pindah ke versi terbaru dan mulai percakapan baru.
if len(k.AGEN_TERDAFTAR) != st.session_state.jumlah_terdaftar:
    st.session_state.jumlah_terdaftar = len(k.AGEN_TERDAFTAR)
    if k.AGEN_TERDAFTAR:
        st.session_state.agen = list(k.AGEN_TERDAFTAR)[-1]
        st.session_state.thread_id = None

nama_agen_semua = semua_nama_agen()
if not nama_agen_semua:
    st.title("Aplikasi Agen")
    st.info("Belum ada agen yang didaftarkan. Di notebook, jalankan sel TODO sampai sel `daftarkan_agen(...)`, lalu tekan tombol di bawah.")
    st.button("Periksa lagi")
    st.stop()

with st.sidebar:
    st.header("Aplikasi Agen")
    st.selectbox("Agen", nama_agen_semua, key="agen", on_change=percakapan_baru,
                 help="Setiap kali sel pendaftaran dijalankan, lahir versi baru. Versi lama tetap bisa dipilih untuk dibandingkan.")
    st.button("Percakapan baru", on_click=percakapan_baru, width="stretch")
    st.subheader("Riwayat percakapan")
    if not simpan.percakapan:
        st.caption("Belum ada percakapan.")
    for tid, info in reversed(list(simpan.percakapan.items())):
        st.button(f"{info['judul']}", key=f"buka-{tid}", on_click=buka_percakapan, args=(tid,), width="stretch",
                  type="primary" if tid == st.session_state.thread_id else "secondary", help=f"Agen: {info['agen']}")
    st.caption("Riwayat disimpan di checkpointer agen (memori) dan hilang saat notebook dimulai ulang.")

nama_agen = st.session_state.agen
try:
    judul, pengantar, contoh_pertanyaan, agen = ambil_agen(nama_agen)
except k.ErrorAgen as e:
    st.error(str(e))
    st.stop()

thread_id = st.session_state.thread_id

st.title(judul)
st.caption(f"{nama_agen}. {pengantar}")
with st.expander("Tool yang terpasang pada agen ini"):
    nama_tool = k.nama_tool_agen(agen)
    st.write(", ".join(f"`{n}`" for n in nama_tool) if nama_tool else "Tidak ada tool terpasang.")

menunggu = k.persetujuan_menunggu(agen, thread_id) if thread_id else None
if thread_id:
    gambar_riwayat(agen, thread_id)
elif contoh_pertanyaan:
    st.write("Coba salah satu pertanyaan ini, atau tulis sendiri di kotak bawah:")
    for i, contoh in enumerate(contoh_pertanyaan):
        st.button(contoh, key=f"contoh-{i}", on_click=pakai_contoh, args=(contoh,))
else:
    st.write("Tulis pertanyaan di kotak bawah. Pertanyaan contoh beserta kriteria berhasilnya ada di aplikasi Panduan uji.")

if menunggu:
    keputusan = formulir_persetujuan(menunggu, thread_id)
    if keputusan is not None:
        jalankan_dan_tampilkan(agen, k.lanjutkan(keputusan), thread_id)
        st.rerun()

prompt = st.session_state.pop("antrean", None) or st.chat_input("Tulis pertanyaan...", disabled=menunggu is not None)
if prompt:
    if thread_id is None:
        thread_id = uuid.uuid4().hex[:8]
        st.session_state.thread_id = thread_id
        simpan.percakapan[thread_id] = {"judul": k.judul_dari(prompt), "agen": nama_agen}
    with st.chat_message("user"):
        st.markdown(prompt)
    if jalankan_dan_tampilkan(agen, {"messages": [HumanMessage(content=prompt)]}, thread_id):
        st.rerun()
