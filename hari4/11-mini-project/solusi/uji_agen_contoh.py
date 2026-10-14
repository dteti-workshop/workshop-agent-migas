# %% [markdown]
# # Uji Otomatis Agen Contoh (untuk fasilitator)
# Jalankan sel satu per satu dengan Shift+Enter, atau seluruh file: `python hari4/11-mini-project/solusi/uji_agen_contoh.py`
#
# Peserta menguji agennya dengan mengamati, memakai aplikasi Panduan uji (Contoh 5). Skrip ini untuk fasilitator: ia menjalankan
# `KASUS_UJI` pada empat agen contoh di `solusi/agen_contoh/` dan memeriksa HASILNYA DI KODE, sehingga perubahan pada tool,
# prompt, atau model dapat diperiksa dengan cepat. Kunci yang dipakai setiap kasus:
#
# - `harus_tool`: tool-tool ini harus dipanggil
# - `tanpa_tool`: tool-tool ini tidak boleh dipanggil (misalnya tool tulis tanpa diminta)
# - `harus_ada`: kata atau angka yang harus muncul pada jawaban
# - `keputusan`: 'setuju' atau 'tolak' (default tolak): jawaban reviewer berskrip kalau agen meminta persetujuan
# - `tercatat`: berapa catatan tindakan yang harus bertambah (0 berarti tool tulis tidak boleh berjalan)
#
# Kasus "tercatat" memeriksa efek nyata pada data, bukan hanya apa yang diklaim agen dalam jawabannya.
# Model bisa berbeda tiap eksekusi, jadi satu kasus kadang lolos dan kadang gagal; jalankan beberapa kali sebelum menyimpulkan.

# %%
# Langkah 1 - Memilih agen yang diuji (agen contoh di solusi/agen_contoh/)
import sys

from langgraph.checkpoint.memory import InMemorySaver

from migas_shared.config import ROOT

sys.path.insert(0, str(ROOT / "hari4" / "11-mini-project" / "aplikasi"))

import kerangka as k

PILIHAN_AGEN = ["operasi", "perawatan", "hse", "engineering"]  # nama file agen contoh (tanpa .py)

pilihan = PILIHAN_AGEN
print(f"Agen yang diuji: {pilihan}")

# %% [markdown]
# ## Langkah 2 - Menjalankan semua kasus uji
# Setiap kasus diperiksa di kode: tool yang dipanggil, kata pada jawaban, dan catatan tindakan yang bertambah.

# %%
total = lolos = 0
for nama in pilihan:
    modul, agen = k.bangun_agen(nama, InMemorySaver())
    daftar = getattr(modul, "KASUS_UJI", [])
    print(f"Agen {nama} ({len(daftar)} kasus)")
    if not daftar:
        print("   belum ada KASUS_UJI di file agen ini\n")
        continue
    for i, kasus in enumerate(daftar, 1):
        gagal = k.jalankan_kasus(agen, kasus, f"uji-{nama}-{i}")
        total += 1
        lolos += not gagal
        print(f"   [{'LOLOS' if not gagal else 'GAGAL'}] {kasus['nama']}")
        for g in gagal:
            print(f"           - {g}")
    print()

print(f"Hasil: {lolos} dari {total} kasus lolos")

# %% [markdown]
# ## Ide Utama
# - Uji agen dengan banyak kasus yang diperiksa kode, bukan dengan membaca satu jawaban yang tampak bagus
# - Periksa efek nyata (tool dipanggil, data tercatat), jangan hanya percaya kalimat jawaban
# - Kasus yang gagal menunjukkan apa yang harus diperbaiki: instruksi, deskripsi tool, atau aturan persetujuan
