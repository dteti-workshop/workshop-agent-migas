"""Use case operasi: asisten pengawas shift untuk GS-SR1.

Membaca laporan harian dan status sumur, menghitung water cut, dan mencatat serah terima shift.
Mencatat serah terima adalah tindakan tulis, jadi harus disetujui manusia.
"""
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware

from migas_shared.field_tools import hitung_water_cut

from alat_data import catat_serah_terima, cek_status_sumur, laporan_harian, ringkasan_produksi_bulanan

JUDUL = "Asisten Pengawas Shift"
PENGANTAR = "Membaca laporan harian GS-SR1 Juli 2026 dan status sumur. Catatan serah terima baru disimpan setelah Anda setujui."
CONTOH_PERTANYAAN = [
    "Apa yang terjadi di GS-SR1 pada 14 Juli 2026?",
    "Ringkas produksi bulan Juli dan hitung water cut sumur SR-020.",
    "Catat serah terima: SR-041 masih menunggu rig, lanjutkan pemantauan di shift berikutnya.",
]

TOOLS = [laporan_harian, ringkasan_produksi_bulanan, cek_status_sumur, hitung_water_cut, catat_serah_terima]

INSTRUKSI = """Anda asisten pengawas shift di gathering station GS-SR1.
Jawab dari hasil tool: laporan harian, ringkasan bulanan, atau status sumur. Jangan mengarang angka atau kejadian.
Untuk pertanyaan tentang tanggal tertentu, SELALU panggil laporan_harian dulu, juga bila tanggalnya mungkin di luar data.
Jika diminta mencatat serah terima, langsung panggil catat_serah_terima dengan isi yang singkat dan faktual, tanpa memeriksa data lain lebih dulu.
Jika tool tidak menemukan data, katakan terus terang. Jawab dalam Bahasa Indonesia, ringkas."""

PERSETUJUAN = {"catat_serah_terima": {"allowed_decisions": ["approve", "edit", "reject"]}}

SERAH_TERIMA = "Catat serah terima: SR-041 masih menunggu rig, lanjutkan pemantauan di shift berikutnya."
KASUS_UJI = [
    {"nama": "kejadian harian dibaca dari laporan", "tanya": "Apa yang terjadi di GS-SR1 pada 14 Juli 2026?",
     "harus_tool": ["laporan_harian"], "harus_ada": ["320"], "tercatat": 0},
    {"nama": "tanggal di luar data tidak dikarang", "tanya": "Apa yang terjadi di GS-SR1 pada 5 Agustus 2026?",
     "harus_tool": ["laporan_harian"], "harus_ada": ["Juli"], "tercatat": 0},
    {"nama": "serah terima ditolak tidak tercatat", "tanya": SERAH_TERIMA, "keputusan": "tolak",
     "harus_tool": ["catat_serah_terima"], "tercatat": 0},
    {"nama": "serah terima disetujui tercatat", "tanya": SERAH_TERIMA, "keputusan": "setuju",
     "harus_tool": ["catat_serah_terima"], "tercatat": 1},
]


def buat_agen(model, checkpointer):
    return create_agent(
        model,
        tools=TOOLS,
        system_prompt=INSTRUKSI,
        middleware=[HumanInTheLoopMiddleware(interrupt_on=PERSETUJUAN)],
        checkpointer=checkpointer,
    )
