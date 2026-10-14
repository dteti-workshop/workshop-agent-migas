# %% [markdown]
# # Solusi Contoh: Agen Investigasi Sumur
# Jalankan sel satu per satu dengan Shift+Enter, atau seluruh file: `python hari4/11-mini-project/solusi/investigasi_sumur.py`
#
# Agen lintas sumber untuk menyusun lini masa dan investigasi sebuah sumur. Menggabungkan tiga hal yang diminta
# mini project: tool yang Anda tulis sendiri, pencarian dokumen (RAG), dan persetujuan manusia untuk tindakan tulis.
#
# - `lini_masa_sumur`: tool BARU, menggabungkan work order, laporan harian, dan narasi insiden untuk satu kode
# - `cari_dokumen_sop` dan `cari_dokumen_investigasi`: SOP dan laporan investigasi (INV-2026-011)
# - `usulkan_tindakan_korektif`: tindakan tulis, hanya boleh disetujui atau ditolak
#
# Cara pakai:
# 1. Fasilitator: salin file ini ke `hari4/11-mini-project/aplikasi/agen/investigasi_sumur.py`, lalu jalankan
#    `streamlit run hari4/11-mini-project/aplikasi/app.py` dan pilih agen "investigasi_sumur"
# 2. Peserta: pola yang sama dapat ditulis di sel notebook (lihat Bagian 3 bab ini)
#
# Saat dijalankan langsung (bukan diimpor aplikasi), sel terakhir menguji kasusnya tanpa perlu menyalin file ke `agen/`.

# %%
# Langkah 1 - Impor
import sys

import pandas as pd
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool

from migas_shared.config import DATA, ROOT

# Agar `import alat_data` berhasil, baik dari folder solusi/ maupun setelah disalin ke aplikasi/agen/
sys.path.insert(0, str(ROOT / "hari4" / "11-mini-project" / "aplikasi"))

from alat_data import cari_dokumen_investigasi, cari_dokumen_sop, usulkan_tindakan_korektif

# %% [markdown]
# ## Langkah 2 - Identitas agen untuk aplikasi
# Aplikasi mini project membaca `JUDUL`, `PENGANTAR`, dan `CONTOH_PERTANYAAN` dari setiap file di `agen/`.

# %%
JUDUL = "Investigasi Sumur"
PENGANTAR = "Menyusun lini masa kejadian sebuah sumur dari work order, laporan harian, dan insiden, lalu menghubungkannya dengan SOP dan laporan investigasi."
CONTOH_PERTANYAAN = [
    "Susun lini masa kejadian sumur SR-027 dan jelaskan temuan investigasi H2S-nya.",
    "Apa batas alarm H2S menurut SOP dan apakah pembacaan 12 ppm di SR-027 melampauinya?",
]

# %% [markdown]
# ## Langkah 3 - Tool baru: lini masa sumur
# Menggabungkan tiga sumber data (work order, laporan harian, insiden) untuk satu kode sumur.

# %%
@tool(parse_docstring=True)
def lini_masa_sumur(kode_sumur: str, maks: int = 10) -> str:
    """Susun lini masa kejadian sebuah sumur dari work order, laporan harian GS-SR1, dan narasi insiden HSE.

    Args:
        kode_sumur: Kode sumur, contoh "SR-027".
        maks: Jumlah kejadian terbaru yang ditampilkan (1 sampai 20).
    """
    kode = kode_sumur.strip().upper()
    kejadian: list[tuple[str, str, str]] = []  # (tanggal, sumber, uraian)

    wo = pd.read_csv(DATA / "raw" / "work_orders.csv")
    for _, r in wo[wo["deskripsi"].str.upper().str.contains(kode, regex=False)].iterrows():
        kejadian.append((r["tanggal"], f"work order {r['wo_id']}", r["deskripsi"][:110]))

    harian = pd.read_csv(DATA / "eval" / "daily_gs_sr1_2026-07.csv").dropna(subset=["event"])
    for _, r in harian[harian["event"].str.upper().str.contains(kode, regex=False)].iterrows():
        kejadian.append((r["tanggal"], "laporan harian", r["event"][:110]))

    insiden = pd.read_csv(DATA / "raw" / "hse_incidents.csv")
    for _, r in insiden[insiden["narasi"].str.upper().str.contains(kode, regex=False)].iterrows():
        kejadian.append((r["tanggal"], f"insiden {r['incident_id']}", r["narasi"][:110]))

    if not kejadian:
        return f"Tidak ada kejadian yang menyebut {kode} di work order, laporan harian, atau insiden."
    kejadian.sort()
    tampil = kejadian[-max(1, min(maks, 20)):]
    baris = [f"{kode}: {len(kejadian)} kejadian ditemukan, {len(tampil)} terbaru ditampilkan berurutan waktu:"]
    baris += [f"- {t} [{s}] {u}" for t, s, u in tampil]
    return "\n".join(baris)

# %% [markdown]
# ## Langkah 4 - Tool, instruksi, dan aturan persetujuan
# Tindakan tulis `usulkan_tindakan_korektif` berhenti menunggu manusia: hanya boleh disetujui atau ditolak.

# %%
TOOLS = [lini_masa_sumur, cari_dokumen_sop, cari_dokumen_investigasi, usulkan_tindakan_korektif]

INSTRUKSI = """Anda asisten investigasi untuk petugas HSE di lapangan migas.
Untuk riwayat kejadian sebuah sumur, pakai lini_masa_sumur. Untuk batas alarm, prosedur, dan temuan investigasi,
pakai cari_dokumen_sop (prosedur) dan cari_dokumen_investigasi (temuan investigasi), dan beri sitasi [DOC_ID bagian]. Pisahkan dengan jelas apa yang berasal dari data dan apa dari dokumen.
Usulkan tindakan korektif HANYA bila diminta. Dalam kasus itu langsung panggil usulkan_tindakan_korektif dengan nomor
insiden dari pengguna, tanpa pencarian tambahan. Jangan menyimpulkan penyebab yang tidak didukung data atau dokumen. Jawab dalam Bahasa Indonesia, ringkas."""

PERSETUJUAN = {"usulkan_tindakan_korektif": {"allowed_decisions": ["approve", "reject"]}}

# %% [markdown]
# ## Langkah 5 - Kasus uji
# Daftar `KASUS_UJI` dipakai fasilitator untuk memeriksa agen ini; tiap kasus diperiksa di kode.

# %%
KASUS_UJI = [
    {"nama": "lini masa SR-027 memakai tool baru", "tanya": "Susun lini masa kejadian sumur SR-027.",
     "harus_tool": ["lini_masa_sumur"], "harus_ada": ["SR-027"], "tercatat": 0},
    {"nama": "temuan investigasi dari dokumen dengan sitasi", "tanya": "Apa temuan laporan investigasi H2S di sumur SR-027?",
     "harus_tool": ["cari_dokumen_investigasi"], "harus_ada": ["INV-2026-011"], "tercatat": 0},
    {"nama": "sumur tanpa kejadian dijawab jujur", "tanya": "Susun lini masa kejadian sumur ZZ-999.",
     "harus_tool": ["lini_masa_sumur"], "harus_ada": ["tidak"], "tercatat": 0},
    {"nama": "tindakan korektif ditolak tidak tercatat", "tanya": "Usulkan tindakan korektif untuk insiden HSE-26-0004: beri pembatas pada pagar wellhead.",
     "keputusan": "tolak", "harus_tool": ["usulkan_tindakan_korektif"], "tercatat": 0},
]

# %% [markdown]
# ## Langkah 6 - Fungsi buat_agen
# Kontrak aplikasi: setiap file agen menyediakan `buat_agen(model, checkpointer)`.

# %%
def buat_agen(model, checkpointer):
    return create_agent(
        model,
        tools=TOOLS,
        system_prompt=INSTRUKSI,
        middleware=[HumanInTheLoopMiddleware(interrupt_on=PERSETUJUAN)],
        checkpointer=checkpointer,
    )

# %% [markdown]
# ## Langkah 7 - Menguji kasus langsung dari solusi/
# Sel ini hanya berjalan kalau file dijalankan langsung. Kalau file disalin ke `aplikasi/agen/` dan diimpor
# aplikasi, `DIJALANKAN_LANGSUNG` bernilai `False` sehingga uji dilewati.

# %%
DIJALANKAN_LANGSUNG = __name__ == "__main__"

if DIJALANKAN_LANGSUNG:
    from langgraph.checkpoint.memory import InMemorySaver

    import kerangka as k
    from migas_shared.llm import get_chat_model

    agen = buat_agen(get_chat_model(), InMemorySaver())
    lolos = 0
    for i, kasus in enumerate(KASUS_UJI, 1):
        gagal = k.jalankan_kasus(agen, kasus, f"solusi-{i}")
        lolos += not gagal
        print(f"[{'LOLOS' if not gagal else 'GAGAL'}] {kasus['nama']}")
        for g in gagal:
            print(f"        - {g}")
    print(f"\nHasil: {lolos} dari {len(KASUS_UJI)} kasus lolos")
