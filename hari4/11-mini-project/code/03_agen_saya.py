# %% [markdown]
# # Contoh 3: Merakit Agen Anda Sendiri (TODO)
# Jalankan sel satu per satu dengan Shift+Enter, atau seluruh file: `python hari4/11-mini-project/code/03_agen_saya.py`
#
# Sekarang giliran Anda. Bahannya sudah Anda kenal di penjelajah (Contoh 1) dan cara merakitnya sudah Anda lihat di Contoh 2.
# Isi tiga TODO di bawah, dari atas ke bawah:
#
# | TODO | Yang diisi |
# |---|---|
# | `TODO(M.1)` | `TOOLS`: daftar tool yang boleh dipakai agen (tempel dari penjelajah) |
# | `TODO(M.2)` | `checkpointer`: penyimpan percakapan dan keadaan agen |
# | `TODO(M.3)` | `agen`: panggilan `create_agent(...)`, termasuk teks `system_prompt` dan `HumanInTheLoopMiddleware` |
#
# Bagaimana tool tulis dipasangi persetujuan, dan seperti apa teks prompt-nya, Anda tentukan sendiri. Sel ini tidak menilai pilihan
# Anda: lihat saja bagaimana agen bereaksi di aplikasi agen (Contoh 4) dan Panduan uji (Contoh 5).
# Ingin versi agen yang berbeda? Ubah sel TODO, jalankan ulang sampai sel terakhir, dan versi baru muncul di aplikasi agen.

# %%
# Langkah 1 - Mengimpor bahan perakitan (tidak perlu diubah)
import sys

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver

from migas_shared.config import ROOT
from migas_shared.llm import get_chat_model

sys.path.insert(0, str(ROOT / "hari4" / "11-mini-project" / "aplikasi"))

import kerangka as k

# %% [markdown]
# ## Langkah 2 - Tool (TODO M.1)
# Tempel hasil tab **Pilih tool** di penjelajah: baris `from alat_data import (...)` dan `TOOLS = [...]`. Tool dari beberapa
# use case boleh digabung. Tool yang lebih sedikit biasanya membuat agen lebih mudah memilih dengan benar.

# %%
# TODO(M.1): tempel baris `from alat_data import (...)` dan `TOOLS = [...]` dari penjelajah
TOOLS = []

# %% [markdown]
# ## Langkah 3 - Checkpointer (TODO M.2)
# Checkpointer menyimpan keadaan agen di setiap langkah. Tanpanya agen tidak ingat percakapan sebelumnya dan tidak bisa
# berhenti menunggu persetujuan lalu melanjutkan (lihat bab 5). Aplikasi agen memakai checkpointer ini untuk riwayat sidebar.

# %%
# TODO(M.2): buat checkpointer penyimpan memori (lihat bab 5 dan Contoh 2)
checkpointer = None

# %% [markdown]
# ## Langkah 4 - Merakit agen (TODO M.3)
# Satukan semuanya dengan `create_agent(...)`:
#
# - `model` dan `tools`
# - `system_prompt`: teks lengkap, tempel dari tab **Prompt** di penjelajah atau tulis sendiri
# - `middleware`: `HumanInTheLoopMiddleware(interrupt_on={...})` bila ada tool yang harus menunggu persetujuan. Isi `interrupt_on` dengan
#   nama tool dan `allowed_decisions` (lihat bab 6 dan Contoh 2). Tool yang tidak ada di `interrupt_on` berjalan bebas
# - `checkpointer`

# %%
model = get_chat_model()
# TODO(M.3): rakit agen dengan create_agent(...): model, tools, system_prompt (teks lengkap), middleware, dan checkpointer
agen = None

# %% [markdown]
# ## Langkah 5 - Periksa
# Sel ini hanya melihat apakah TODO sudah terisi, dan menampilkan tool yang benar-benar terpasang pada agen. Agen baru bisa
# didaftarkan bila `agen` dan `checkpointer` sudah terisi.

# %%
belum_terisi = []
if not TOOLS:
    belum_terisi.append("TODO(M.1): TOOLS masih kosong")
if checkpointer is None:
    belum_terisi.append("TODO(M.2): checkpointer masih None")
if agen is None:
    belum_terisi.append("TODO(M.3): agen masih None")

if agen is not None:
    print(f"Tool terpasang pada agen: {k.nama_tool_agen(agen) or 'tidak ada'}")
for pesan in belum_terisi:
    print(f"   [BELUM] {pesan}")
siap = agen is not None and checkpointer is not None
print("Siap didaftarkan." if siap else "Belum siap didaftarkan: lengkapi TODO yang bertanda BELUM.")

# %% [markdown]
# ## Langkah 6 - Mendaftarkan agen
# `daftarkan_agen` menaruh agen Anda ke aplikasi agen (Contoh 4). Setiap kali sel ini dijalankan lahir versi baru
# (`Agen Saya #1`, `#2`, ...), dan versi lama tetap bisa dipilih untuk dibandingkan. Isi `CONTOH_PERTANYAAN` bila ingin tombol
# pertanyaan di layar kosong; pertanyaan yang cocok ada di aplikasi Panduan uji.

# %%
JUDUL = "Agen Saya"
PENGANTAR = "Agen yang saya rakit sendiri di mini project."
CONTOH_PERTANYAAN = []

if siap:
    nama_agen = k.daftarkan_agen(agen, JUDUL, PENGANTAR, CONTOH_PERTANYAAN)
    print(f"Agen terdaftar sebagai '{nama_agen}'. Lanjut ke Contoh 4 untuk mengobrol dengannya.")
else:
    print("Agen belum didaftarkan karena ada TODO yang belum diisi (lihat Langkah 5).")

# %% [markdown]
# ## Ide Utama
# - Agen = `create_agent(model, tools, system_prompt, middleware, checkpointer)`: semuanya ditulis langsung di panggilan itu
# - `interrupt_on` menentukan tool mana yang menunggu manusia; tool yang tidak tercantum berjalan bebas
# - Prompt hanya imbauan; yang menahan tindakan berisiko adalah interrupt. Lihat sendiri bedanya di aplikasi agen
# - Tanpa checkpointer, agen tidak bisa mengingat percakapan maupun berhenti menunggu keputusan manusia
# - Mendaftarkan ulang agen membuat versi baru, sehingga dua rancangan bisa dibandingkan dengan pertanyaan yang sama
