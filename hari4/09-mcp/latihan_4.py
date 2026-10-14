# %% [markdown]
# # Latihan Bonus: Server MCP Buatan Sendiri + Klien Pengujinya
# Isi bagian bertanda `TODO(...)` dengan kode dari bagian **Kode Jawaban Latihan** pada PDF bab ini, lalu jalankan sel satu per satu
# dengan Shift+Enter. Baris `... = None  # TODO` atau `raise NotImplementedError` berarti kode itu harus Anda ganti.
#
# Server ada di `latihan_3.py`. Skrip ini:
#
# 1. Menjalankan server sebagai subproses (stdio) dan mendaftar tool-nya
# 2. Menguji tool LANGSUNG dengan input yang valid dan tidak valid (tanpa model), diperiksa di kode
# 3. Menghubungkan agen ke server dan mengajukan satu pertanyaan gabungan
#
# Kode async dijalankan lewat `jalankan(...)` dari `migas_shared.tampil`, yang bekerja di skrip biasa maupun
# di Jupyter/Interactive Window.

# %%
# Langkah 1 - Impor dan model
import os
import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import ToolException
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

from migas_shared.config import ROOT
from migas_shared.tampil import jalankan

load_dotenv()

PATH_SERVER = ROOT / "hari4" / "09-mcp" / "latihan_3.py"

model = ChatOpenAI(
    model=os.getenv("ONLINE_MODEL"),
    base_url=os.getenv("ONLINE_BASE_URL"),
    api_key=os.getenv("ONLINE_API_KEY"),
    reasoning_effort=os.getenv("LLM_REASONING_EFFORT", "none"),
)

# %% [markdown]
# ## Langkah 2 - Mendaftar tool dari server buatan sendiri
# Klien membuka sesi per panggilan dan menutupnya sendiri, jadi tidak ada yang perlu ditutup antar sel.

# %%
# TODO(B9.11): buat MultiServerMCPClient untuk server stdio "work_order" yang menjalankan PATH_SERVER dengan sys.executable
client = None  # TODO: ganti dengan implementasi Anda
# TODO(B9.12): ambil tool server dengan jalankan(client.get_tools()), lalu buat kamus tool_per_nama
tools = []  # TODO: ganti dengan implementasi Anda
tool_per_nama = {}  # TODO: ganti dengan implementasi Anda
print(f"Tool dari server buatan sendiri: {list(tool_per_nama)}\n")

# %% [markdown]
# ## Langkah 3 - Uji langsung 1: daftar work order terbuka
# Pengujian tanpa model, diperiksa di kode. Hasil `daftar_wo_terbuka('Kenanga')` harus memuat WO-26-12611.

# %%
print("Uji langsung (tanpa model):")
lolos = 0

# TODO(B9.13): panggil daftar_wo_terbuka('Kenanga') langsung (ainvoke lewat jalankan), lalu ok = hasilnya memuat WO-26-12611; tambahkan ke lolos
ok = False  # TODO: ganti dengan implementasi Anda
lolos += ok
print(f"   {'LOLOS' if ok else 'GAGAL'}  daftar_wo_terbuka('Kenanga') memuat WO-26-12611")

# %% [markdown]
# ## Langkah 4 - Uji langsung 2: kerugian downtime
# 12 jam pada 100 bopd harus menghasilkan 50 barel dan USD 3.500.

# %%
hasil_kerugian = str(jalankan(tool_per_nama["hitung_kerugian_downtime"].ainvoke({"downtime_jam": 12, "laju_bopd": 100})))
ok = "50.0 barel" in hasil_kerugian and "3,500" in hasil_kerugian
lolos += ok
print(f"   {'LOLOS' if ok else 'GAGAL'}  hitung_kerugian_downtime(12 jam, 100 bopd) = 50 barel, USD 3.500")

# %% [markdown]
# ## Langkah 5 - Uji langsung 3: input tidak valid
# Area yang tidak dikenal harus ditolak dengan error yang jelas.

# %%
# TODO(B9.14): panggil daftar_wo_terbuka dengan area 'Atlantis'; ok bernilai True bila hasilnya memuat 'tidak dikenal' (error server dikembalikan sebagai teks) atau ToolException muncul
ok = False  # TODO: ganti dengan implementasi Anda
lolos += ok
print(f"   {'LOLOS' if ok else 'GAGAL'}  area tidak dikenal ditolak dengan error")

print(f"\nHasil uji langsung: {lolos}/3 lolos\n")

# %% [markdown]
# ## Langkah 6 - Agen memakai server
# Satu pertanyaan gabungan: daftar work order terbuka dan kerugian downtime.

# %%
# TODO(B9.15): buat agen dari model dan tool server dengan system prompt asisten pemeliharaan (pakai tool, jangan menebak)
agent = None  # TODO: ganti dengan implementasi Anda
pertanyaan = "Work order apa yang terbuka di Kenanga, dan berapa kerugian bila sumurnya mati 48 jam pada laju 90 bopd?"
print(f"Pengguna: {pertanyaan}")
response = jalankan(agent.ainvoke({"messages": [("human", pertanyaan)]}))
panggilan = [c["name"] for m in response["messages"] for c in getattr(m, "tool_calls", [])]
print(f"   Tool yang dipanggil: {panggilan}")
print(f"Agen: {response['messages'][-1].content}")
