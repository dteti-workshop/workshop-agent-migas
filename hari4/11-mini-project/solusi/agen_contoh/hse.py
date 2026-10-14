"""Use case HSE: asisten petugas HSE.

Mencari dan meringkas insiden, membaca SOP dan laporan investigasi (peran hse), dan mencatat usulan tindakan korektif.
Tindakan korektif hanya boleh disetujui atau ditolak, tidak boleh diubah oleh reviewer.
"""
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware

from alat_data import (cari_dokumen_investigasi, cari_dokumen_sop, cari_insiden, ringkasan_insiden,
                       usulkan_tindakan_korektif)

JUDUL = "Asisten Petugas HSE"
PENGANTAR = "Mencari insiden menurut lokasi dan bahaya, membaca SOP HSE, dan mengusulkan tindakan korektif yang menunggu persetujuan Anda."
CONTOH_PERTANYAAN = [
    "Ringkas semua insiden HSE: bahaya apa yang paling sering?",
    "Tampilkan insiden H2S dan apa tindakan SOP jika alarm H2S mencapai 10 ppm.",
    "Usulkan tindakan korektif untuk insiden HSE-26-0004: pagar wellhead diberi pembatas dan rambu.",
]

TOOLS = [cari_insiden, ringkasan_insiden, cari_dokumen_sop, cari_dokumen_investigasi, usulkan_tindakan_korektif]

INSTRUKSI = """Anda asisten petugas HSE di lapangan migas.
Untuk data insiden, pakai cari_insiden dan ringkasan_insiden. Untuk prosedur dan batas alarm, pakai cari_dokumen_sop; untuk isi laporan investigasi, pakai
cari_dokumen_investigasi. Beri sitasi [DOC_ID bagian]. Usulkan tindakan korektif HANYA bila pengguna memintanya. Dalam kasus itu langsung panggil usulkan_tindakan_korektif
dengan nomor insiden dari pengguna, tanpa pencarian tambahan.
Jangan menarik kesimpulan yang tidak didukung data. Jawab dalam Bahasa Indonesia, ringkas."""

PERSETUJUAN = {"usulkan_tindakan_korektif": {"allowed_decisions": ["approve", "reject"]}}

CAPA = "Usulkan tindakan korektif untuk insiden HSE-26-0004: pagar wellhead diberi pembatas dan rambu."
KASUS_UJI = [
    {"nama": "ringkasan insiden dari data", "tanya": "Ringkas semua insiden HSE: bahaya apa yang paling sering?",
     "harus_tool": ["ringkasan_insiden"], "harus_ada": ["Hot Work"], "tercatat": 0},
    {"nama": "batas alarm H2S dari SOP dengan sitasi", "tanya": "Apa tindakan jika alarm H2S mencapai 10 ppm?",
     "harus_tool": ["cari_dokumen_sop"], "harus_ada": ["SOP-HSE-001"], "tercatat": 0},
    {"nama": "tindakan korektif ditolak tidak tercatat", "tanya": CAPA, "keputusan": "tolak",
     "harus_tool": ["usulkan_tindakan_korektif"], "tercatat": 0},
    {"nama": "tindakan korektif disetujui tercatat", "tanya": CAPA, "keputusan": "setuju",
     "harus_tool": ["usulkan_tindakan_korektif"], "tercatat": 1},
]


def buat_agen(model, checkpointer):
    return create_agent(
        model,
        tools=TOOLS,
        system_prompt=INSTRUKSI,
        middleware=[HumanInTheLoopMiddleware(interrupt_on=PERSETUJUAN)],
        checkpointer=checkpointer,
    )
