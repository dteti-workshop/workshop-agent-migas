"""Agen dalam bentuk file: padanan modul dari agen yang dirakit di notebook (code/03_agen_saya.py).

Peserta merakit agen di sel notebook dan mendaftarkannya dengan kerangka.daftarkan_agen(...). File ini memuat susunan yang
sama sebagai modul, dibaca oleh studio.py (perintah `langgraph dev`) dan oleh fasilitator.

  KOMPONEN 1  TOOLS       : tool apa yang boleh dipakai agen (pilih dari KATALOG di alat_data.py, atau tulis sendiri)
  KOMPONEN 2  INSTRUKSI   : peran dan aturan agen (salin dan ubah dari prompt_bank.py, atau tulis sendiri)
  KOMPONEN 3  PERSETUJUAN : tool mana yang berhenti menunggu manusia (interrupt), dan keputusan apa yang diizinkan

Nama lain yang dibaca dari file agen:

  JUDUL              : judul di bagian atas halaman
  PENGANTAR          : satu atau dua kalimat tentang apa yang bisa dilakukan agen
  CONTOH_PERTANYAAN  : pertanyaan contoh yang tampil di layar kosong
  buat_agen(...)     : fungsi yang mengembalikan agen (hasil create_agent); biasanya tidak diubah
  KASUS_UJI          : (opsional) daftar kasus untuk solusi/uji_agen_contoh.py (alat fasilitator)

Melihat semua tool yang tersedia: aplikasi Penjelajah (code/01_penjelajah.py).
"""
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware

from prompt_bank import PERTANYAAN, susun_prompt

# Komponen yang sudah terpasang di bawah adalah contoh agen Perawatan yang hanya membaca. Ganti dengan use case Anda.
from alat_data import aset_downtime_tertinggi, riwayat_work_order, statistik_kegagalan
# from alat_data import buat_work_order, tutup_work_order            # tool TULIS Perawatan: wajib dipasangi KOMPONEN 3
# from alat_data import cari_dokumen_sop, cari_dokumen_manual        # pencarian SOP dan manual (satu tool per jenis dokumen)
# from alat_data import KATALOG                                      # semua tool per use case: KATALOG["HSE"], dst.

JUDUL = "Agen Saya"
PENGANTAR = "Titik awal mini project: susun tool, prompt, dan aturan persetujuan sesuai use case Anda."
CONTOH_PERTANYAAN = PERTANYAAN["Perawatan"]["baca"] + PERTANYAAN["Perawatan"]["multi"]

# KOMPONEN 1 - Tool yang boleh dipakai agen.
TOOLS = [riwayat_work_order, statistik_kegagalan, aset_downtime_tertinggi]

# KOMPONEN 2 - Peran dan aturan agen. susun_prompt(use_case, gaya) menggabungkan peran, aturan tool, dan gaya jawaban.
# Gaya yang tersedia: minimal, ketat, ramah, tabel, sitasi, hati_hati (satu nama atau daftar). Atau tulis sendiri INSTRUKSI = """..."""
INSTRUKSI = susun_prompt("Perawatan", "ketat")

# KOMPONEN 3 - Tool yang harus disetujui manusia sebelum berjalan. Kosong berarti semua tool berjalan bebas.
# Contoh mengaktifkan (tool harus ada di TOOLS):
#   {"buat_work_order": {"allowed_decisions": ["approve", "edit", "reject"]}}
# Pilihan yang diizinkan per tool: approve (setuju), edit (ubah argumen), reject (tolak). Untuk tindakan yang
# tidak boleh diubah reviewer, hapus "edit".
PERSETUJUAN: dict = {}

# Kasus uji untuk solusi/uji_agen_contoh.py (alat fasilitator). Kunci: nama, tanya, harus_tool, tanpa_tool, harus_ada,
# keputusan ("setuju" atau "tolak"), tercatat.
KASUS_UJI = [
    {"nama": "riwayat aset dibaca dari data", "tanya": "Bagaimana riwayat work order sumur SR-020?",
     "harus_tool": ["riwayat_work_order"], "harus_ada": ["SR-020"]},
    {"nama": "aset tanpa data dijawab jujur", "tanya": PERTANYAAN["Perawatan"]["tanpa_data"][0],
     "harus_tool": ["riwayat_work_order"], "harus_ada": ["Tidak ada"]},
]


def buat_agen(model, checkpointer):
    # Model dan checkpointer disediakan pemanggil (aplikasi atau studio.py). Bagian ini biasanya tidak diubah.
    middleware = [HumanInTheLoopMiddleware(interrupt_on=PERSETUJUAN)] if PERSETUJUAN else []
    return create_agent(
        model,
        tools=TOOLS,
        system_prompt=INSTRUKSI,
        middleware=middleware,
        checkpointer=checkpointer,
    )
