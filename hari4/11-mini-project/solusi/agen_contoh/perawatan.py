"""Use case pemeliharaan: asisten perencana pemeliharaan.

Membaca riwayat work order dan statistik kegagalan, mencari prosedur di SOP, dan mengusulkan work order baru.
Membuat work order adalah tindakan tulis: boleh disetujui, diubah, atau ditolak.
"""
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware

from alat_data import buat_work_order, cari_dokumen_sop, riwayat_work_order, statistik_kegagalan

JUDUL = "Asisten Perencana Pemeliharaan"
PENGANTAR = "Membaca riwayat work order dan statistik kegagalan, mencari SOP, lalu mengusulkan work order baru yang menunggu persetujuan Anda."
CONTOH_PERTANYAAN = [
    "Bagaimana riwayat work order sumur SR-020?",
    "Kategori kegagalan apa yang paling banyak menyebabkan downtime pada ESP?",
    "Buat work order prioritas sedang untuk memeriksa level controller V-SR1-101.",
]

TOOLS = [riwayat_work_order, statistik_kegagalan, cari_dokumen_sop, buat_work_order]

INSTRUKSI = """Anda asisten perencana pemeliharaan lapangan migas.
Untuk riwayat dan statistik, pakai riwayat_work_order dan statistik_kegagalan. Untuk prosedur, pakai cari_dokumen_sop
dan beri sitasi [DOC_ID bagian]. Buat work order HANYA bila pengguna memintanya secara jelas, dan dalam kasus itu langsung panggil buat_work_order.
Jangan mengarang nomor work order atau angka downtime. Jika data tidak ada, katakan terus terang.
Jawab dalam Bahasa Indonesia, ringkas."""

PERSETUJUAN = {"buat_work_order": {"allowed_decisions": ["approve", "edit", "reject"]}}

WO = "Buat work order prioritas sedang untuk memeriksa level controller V-SR1-101."
KASUS_UJI = [
    {"nama": "riwayat aset dibaca dari data", "tanya": "Bagaimana riwayat work order sumur SR-020?",
     "harus_tool": ["riwayat_work_order"], "harus_ada": ["SR-020"], "tercatat": 0},
    {"nama": "statistik kegagalan ESP", "tanya": "Kategori kegagalan apa yang paling banyak menyebabkan downtime pada ESP?",
     "harus_tool": ["statistik_kegagalan"], "harus_ada": ["Electrical"], "tercatat": 0},
    {"nama": "work order ditolak reviewer tidak tercatat", "tanya": WO, "keputusan": "tolak",
     "harus_tool": ["buat_work_order"], "tercatat": 0},
    {"nama": "work order disetujui reviewer tercatat", "tanya": WO, "keputusan": "setuju",
     "harus_tool": ["buat_work_order"], "tercatat": 1},
    {"nama": "tidak membuat work order tanpa diminta", "tanya": "Sumur SR-020 sering trip. Apa yang perlu diperiksa?",
     "tanpa_tool": ["buat_work_order"], "tercatat": 0},
]


def buat_agen(model, checkpointer):
    return create_agent(
        model,
        tools=TOOLS,
        system_prompt=INSTRUKSI,
        middleware=[HumanInTheLoopMiddleware(interrupt_on=PERSETUJUAN)],
        checkpointer=checkpointer,
    )
