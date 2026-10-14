# %% [markdown]
# # Contoh 2: Merakit Agen dengan create_agent
# Jalankan sel satu per satu dengan Shift+Enter, atau seluruh file: `python hari4/11-mini-project/code/02_rakit_agen.py`
#
# Sebuah agen dirakit dengan satu panggilan `create_agent(...)`. Yang Anda tentukan:
#
# 1. `tools`: tool apa yang boleh dipakai agen (dari penjelajah di Contoh 1)
# 2. `system_prompt`: peran dan aturan agen, berupa teks biasa
# 3. `middleware`: `HumanInTheLoopMiddleware(interrupt_on={...})` untuk tool yang harus menunggu persetujuan manusia (bab 6)
# 4. `checkpointer`: penyimpan keadaan agen, supaya percakapan diingat dan agen bisa berhenti menunggu keputusan (bab 5)
#
# Contoh ini merakit agen untuk use case Operasi. Di Contoh 3 Anda merakit agen Anda sendiri dengan cara yang sama.

# %%
# Langkah 1 - Mengimpor bahan perakitan
import sys

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver

from migas_shared.config import ROOT
from migas_shared.llm import get_chat_model

sys.path.insert(0, str(ROOT / "hari4" / "11-mini-project" / "aplikasi"))

import alat_data as a
import kerangka as k

# %% [markdown]
# ## Langkah 2 - Tool
# Empat tool dari katalog Operasi: tiga tool baca dan satu tool tulis. Tool dipilih di penjelajah lalu ditempel sebagai `import`.

# %%
from alat_data import (
    laporan_harian,
    cek_status_sumur,
    hitung_water_cut,
    catat_serah_terima,
)

TOOLS = [laporan_harian, cek_status_sumur, hitung_water_cut, catat_serah_terima]
for t in TOOLS:
    print(f"   [{a.jenis_tool(t):<5}] {t.name}")

# %% [markdown]
# ## Langkah 3 - System prompt
# System prompt adalah teks biasa yang diteruskan ke `system_prompt=`. Di bab ini teksnya disalin dari tab **Prompt** di penjelajah,
# lalu boleh diubah sesuka Anda.

# %%
system_prompt = """Anda asisten pengawas shift di gathering station GS-SR1.
Jawab dari laporan harian atau status sumur, dan pakai hitung_water_cut untuk water cut.
Untuk pertanyaan tentang tanggal tertentu, SELALU panggil laporan_harian dulu.
Catat serah terima hanya bila pengguna memintanya dengan jelas.
Jangan mengarang angka. Jika tool tidak menemukan data, katakan terus terang. Jawab dalam Bahasa Indonesia, ringkas."""
print(system_prompt)

# %% [markdown]
# ## Langkah 4 - Checkpointer
# `InMemorySaver` menyimpan keadaan agen di memori. Tanpa checkpointer, agen tidak ingat percakapan sebelumnya dan tidak bisa berhenti
# menunggu keputusan manusia lalu melanjutkan.

# %%
checkpointer = InMemorySaver()

# %% [markdown]
# ## Langkah 5 - Merakit agen
# Semuanya masuk ke `create_agent(...)`. Parameter `interrupt_on` pada `HumanInTheLoopMiddleware` adalah kamus dari nama tool ke
# keputusan yang diizinkan reviewer: `approve` (setuju), `edit` (ubah argumen), dan `reject` (tolak). Di sini hanya `catat_serah_terima`
# yang menunggu persetujuan, dan reviewer tidak boleh mengubah isinya. Tool yang tidak ada di kamus berjalan bebas.

# %%
agen = create_agent(
    get_chat_model(),
    tools=TOOLS,
    system_prompt=system_prompt,
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "catat_serah_terima": {"allowed_decisions": ["approve", "reject"]},
            }
        )
    ],
    checkpointer=checkpointer,
)
print(f"Agen siap. Tool terpasang: {k.nama_tool_agen(agen)}")

# %% [markdown]
# ## Ide Utama
# - Agen = `create_agent(model, tools, system_prompt, middleware, checkpointer)`: semua yang dibutuhkan ada dalam satu panggilan
# - `system_prompt` hanyalah teks; yang Anda tulis di sana adalah imbauan bagi model
# - `interrupt_on` menentukan tool mana yang berhenti menunggu manusia, dan keputusan apa yang diizinkan
# - Checkpointer menyimpan keadaan agen di setiap langkah, sehingga percakapan dan permintaan persetujuan yang tertunda tidak hilang
