# %% [markdown]
# # Contoh 1: Menjelajahi Tool dan Prompt
# Jalankan sel satu per satu dengan Shift+Enter, atau seluruh file: `python hari4/11-mini-project/code/01_penjelajah.py`
#
# Dua komponen pertama agen adalah tool dan prompt. Sebelum memilihnya, kenali dulu bahannya lewat aplikasi Streamlit
# **Penjelajah** (`aplikasi/penjelajah.py`):
#
# - tab **Tool**: 25 tool dengan ilustrasi, parameter, hasil, contoh pemakaian, dan formulir untuk memanggilnya sendiri
#   (parameter pilihan terbatas berupa dropdown) dan tab **Sumber data**: tabel CSV atau dokumen asli beserta chunk-nya
# - tab **Prompt**: memilih use case, aturan tool, dan gaya jawaban, lalu menekan **Bangun prompt**
# - tab **Pilih tool**: mencentang tool dan mendapatkan snippet kode `TOOLS` untuk disalin
#
# Aplikasi ini tidak memanggil model, jadi aman dan cepat dicoba berulang kali. Hasilnya Anda salin (copy-paste) ke sel
# TODO pada Contoh 3.

# %%
# Langkah 1 - Menyiapkan jalur modul bab ini dan indeks dokumen
import sys

from migas_shared.config import ROOT

sys.path.insert(0, str(ROOT / "hari4" / "11-mini-project" / "aplikasi"))

import alat_data as a
import peluncur

# Pencarian dokumen memakai indeks vektor. Dibangun sekali di sini (di sesi baru termasuk mengunduh model embedding,
# sekitar 1 menit), lalu dipakai ulang oleh penjelajah dan agen Anda.
a.retriever_bab11()
print("Indeks dokumen siap.")

# %% [markdown]
# ## Langkah 2 - Menjalankan penjelajah
# Sel di bawah menyalakan aplikasi di port 8501, lalu menampilkan tautan untuk membukanya di tab baru (di Google Colab
# tautan muncul di bawah sel, dan aplikasinya juga tampil di dalam sel; tab baru lebih lega untuk dipakai). Menjalankan sel ini lagi tidak membuat aplikasi ganda.

# %%
peluncur.buka("penjelajah")

# %% [markdown]
# ## Langkah 3 - Yang perlu Anda coba di penjelajah
# 1. Buka tiga tool dari kelompok berbeda. Baca bagian **Parameter** dan **Yang dikembalikan**, lalu tekan **Jalankan tool**.
# 2. Buka `konversi_satuan` dan coba nilai `dari` serta `ke` yang tidak didukung. Perhatikan pesan errornya: pesan inilah yang nanti dibaca agen.
# 3. Buka satu tool **TULIS** (misalnya `buat_work_order`) dan jalankan. Lihat **Catatan tindakan di memori**: tool hanya mencatat, tidak mengubah sistem nyata.
# 4. Buka `cari_dokumen_investigasi` dan bandingkan dengan `cari_dokumen_sop`. Hanya satu tool yang bisa membaca laporan investigasi.
# 5. Buka **Yang dilihat model tentang tool ini**. Model tidak melihat kode tool; ia hanya membaca nama, deskripsi, dan skema argumen.
# 6. Di tab **Prompt**, bangun prompt untuk satu use case dengan dua gaya berbeda dan bandingkan hasilnya.
# 7. Buka tab **Sumber data** pada beberapa tool: lihat tabel CSV yang dibaca `riwayat_work_order`, lalu dokumen asli dan chunk dari `cari_dokumen_sop`. Jalankan pencariannya dan perhatikan chunk bertanda `[TERAMBIL]`.
# 8. Di tab **Pilih tool**, centang tool untuk agen yang ingin Anda buat. Biarkan tab ini terbuka sampai Contoh 3.

# %% [markdown]
# ## Langkah 4 - Tool yang sama, tanpa antarmuka
# Yang dilakukan tombol **Jalankan tool** hanyalah memanggil `.invoke({...})`. Kode ini sama persis dengan contoh pemakaian
# di penjelajah, dan menghasilkan teks yang sama dengan yang nanti dibaca agen sebagai observasi.

# %%
print(a.hitung_water_cut.invoke({"oil_bopd": 120, "water_bwpd": 480}))
print(a.riwayat_work_order.invoke({"asset_id": "SR-020", "maks": 2}))

# %% [markdown]
# ## Ide Utama
# - Agen hanya setajam tool dan deskripsinya: tool yang salah atau deskripsinya kabur tidak bisa diselamatkan agen sebesar apa pun
# - Uji tool lebih dulu dengan `.invoke({...})` tanpa model, seperti yang dilakukan tombol **Jalankan tool**
# - Tool BACA hanya mengambil data. Tool TULIS mengubah sesuatu dan di sistem nyata harus dipasangi persetujuan manusia (komponen 3)
# - Hak akses ditentukan oleh tool yang Anda pasang: hanya agen dengan `cari_dokumen_investigasi` yang bisa membaca laporan investigasi
# - Prompt dibangun dari tiga bahan: peran, aturan yang menyebut tool dengan namanya, dan gaya jawaban
