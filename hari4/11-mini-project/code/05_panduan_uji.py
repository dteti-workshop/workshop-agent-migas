# %% [markdown]
# # Contoh 5: Menguji Agen dengan Panduan Uji
# Jalankan sel satu per satu dengan Shift+Enter, atau seluruh file: `python hari4/11-mini-project/code/05_panduan_uji.py`
#
# Agen yang terlihat bagus pada satu pertanyaan belum tentu bagus pada pertanyaan lain. Menyusun kumpulan uji yang benar
# membutuhkan kunci jawaban, dan itu bukan pekerjaan yang masuk akal di workshop. Karena itu pengujian di bab ini dilakukan
# **dengan mengamati**: aplikasi **Panduan uji** (`aplikasi/panduan_uji.py`) menyediakan pertanyaan beserta kriteria berhasil,
# dan Anda sendiri yang membaca jejak agen lalu menilai.
#
# Alurnya untuk setiap pertanyaan:
#
# 1. pilih tool yang terpasang pada agen Anda, lalu salin pertanyaan yang muncul
# 2. tempel ke aplikasi agen (Contoh 4) dan amati jejaknya
# 3. centang kriteria yang terpenuhi di Panduan uji

# %%
# Langkah 1 - Menyiapkan jalur modul bab ini
import sys

from migas_shared.config import ROOT

sys.path.insert(0, str(ROOT / "hari4" / "11-mini-project" / "aplikasi"))

import peluncur

# %% [markdown]
# ## Langkah 2 - Menjalankan panduan uji
# Sel ini menyalakan aplikasi di port 8503. Buka bersama aplikasi agen (port 8502) di dua tab, sehingga Anda bisa bolak-balik.

# %%
peluncur.buka("uji")

# %% [markdown]
# ## Langkah 3 - Yang perlu Anda lakukan
# 1. Pilih tool yang sama dengan `TOOLS` di agen Anda (atau tekan **Isi dari use case**). Daftar pertanyaan menyesuaikan.
# 2. Jalankan sedikitnya satu pertanyaan dari tiap jenis: **Baca**, **Gabungan**, **Tindakan tulis**, **Data tidak ada**, dan **Di luar cakupan**.
# 3. Untuk setiap kriteria yang **tidak** terpenuhi, tentukan penyebabnya: instruksi kurang tegas, deskripsi tool kabur, tool yang dibutuhkan tidak dipasang, atau aturan persetujuan belum ada.
# 4. Perbaiki di sel TODO Contoh 3, daftarkan ulang (versi baru), lalu ulangi pertanyaan yang sama. Apakah kriterianya kini terpenuhi?
# 5. Coba satu **Eksperimen** di bagian bawah Panduan uji dan bandingkan dua versi agen.
#
# Kriteria yang gagal bukan kesalahan Anda. Ia menunjukkan bagian mana dari tiga komponen yang perlu diperbaiki.

# %% [markdown]
# ## Langkah 4 - Menghentikan aplikasi
# Jalankan sel ini bila Anda sudah selesai. Aplikasi juga berhenti sendiri saat notebook ditutup.

# %%
peluncur.hentikan()

# %% [markdown]
# ## Ide Utama
# - Uji agen dengan banyak pertanyaan yang mewakili perilaku yang Anda inginkan, bukan dengan satu jawaban yang tampak bagus
# - Kriteria yang bisa dilihat mata (tool apa, argumen apa, isi jawaban) cukup untuk menemukan sebagian besar kelemahan
# - Pertanyaan negatif sama pentingnya: data tidak ada, di luar cakupan, dan tindakan tulis tanpa persetujuan
# - Setiap kegagalan menunjuk ke satu dari tiga komponen: tool, prompt, atau persetujuan
# - Untuk pemakaian nyata, pertanyaan nyata pengguna dikumpulkan menjadi kumpulan uji yang diperiksa otomatis
