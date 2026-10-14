# %% [markdown]
# # Contoh 4: Mengobrol dengan Agen Anda
# Jalankan sel satu per satu dengan Shift+Enter, atau seluruh file: `python hari4/11-mini-project/code/04_aplikasi_agen.py`
#
# Aplikasi agen (`aplikasi/app.py`) adalah antarmuka chat untuk agen yang Anda daftarkan di Contoh 3. Fiturnya:
#
# - jawaban tampil saat ditulis (streaming)
# - **jejak kerja agen**: setiap langkah tampil bernomor, dengan expander berisi tool, argumen, dan hasilnya
# - formulir persetujuan (setujui, ubah, tolak) bila agen berhenti di sebuah tool
# - sidebar riwayat percakapan, didukung checkpointer agen, dan pilihan versi agen
#
# Aplikasi ini berjalan di dalam notebook yang sama dengan agen Anda, jadi agen langsung terlihat tanpa menyimpan file apa pun.
# Jalankan Contoh 3 sampai sel pendaftaran dulu. Tanpa agen terdaftar, aplikasi hanya menampilkan petunjuk.

# %%
# Langkah 1 - Menyiapkan jalur modul bab ini
import sys

from migas_shared.config import ROOT

sys.path.insert(0, str(ROOT / "hari4" / "11-mini-project" / "aplikasi"))

import kerangka as k
import peluncur

# %% [markdown]
# ## Langkah 2 - Menjalankan aplikasi agen
# Sel ini menyalakan aplikasi di port 8502 dan menampilkan tautannya. Setelah Anda mendaftarkan versi baru agen
# (menjalankan ulang Contoh 3), tekan **Periksa lagi** atau muat ulang halaman aplikasi: versi terbaru dipilih otomatis.

# %%
print(f"Agen terdaftar saat ini: {list(k.AGEN_TERDAFTAR) or 'belum ada'}")
peluncur.buka("agen")

# %% [markdown]
# ## Langkah 3 - Cara membaca jejak agen
# Setiap jawaban agen tersusun dari langkah-langkah bernomor. Inilah pola **ReAct** (Reason + Act):
#
# | Tampilan | Arti |
# |---|---|
# | **Pikir** (kutipan) | Teks yang ditulis model sebelum memanggil tool: apa yang hendak dilakukan dan mengapa |
# | **Aksi n: nama_tool** | Model memanggil tool. Buka expander untuk melihat argumen yang ia kirim |
# | **Hasil (observasi)** | Teks yang dikembalikan tool. Inilah satu-satunya hal tentang dunia luar yang dibaca model |
# | **Jawaban akhir** | Teks setelah model selesai memakai tool |
#
# Model mengulang Pikir, Aksi, dan Observasi sampai ia cukup yakin untuk menjawab. Bila agen menyimpang, jejak ini menunjukkan
# di langkah mana: salah memilih tool, salah mengisi argumen, atau salah membaca hasil.
#
# ## Langkah 4 - Yang perlu Anda coba
# 1. Ajukan satu pertanyaan sederhana yang butuh satu tool. Buka **Aksi 1** dan cocokkan argumennya dengan pertanyaan Anda.
# 2. Ajukan pertanyaan yang butuh dua tool berurutan (hasil tool pertama menjadi argumen tool kedua). Perhatikan urutan Aksi.
# 3. Minta tindakan tulis. Formulir persetujuan harus muncul sebelum tool berjalan. Coba **Setujui**, **Ubah**, lalu **Tolak** pada percakapan berbeda.
# 4. Klik **Percakapan baru**, lalu kembali ke percakapan lama lewat sidebar. Agen mengingat isinya karena checkpointer.
# 5. Pertanyaan lain yang lebih lengkap, beserta kriteria berhasilnya, ada di aplikasi Panduan uji (Contoh 5).

# %% [markdown]
# ## Ide Utama
# - Aplikasi agen berjalan di proses yang sama dengan notebook, sehingga agen di sel bisa dipakai tanpa file perantara
# - Streamlit menjalankan ulang seluruh skrip pada setiap interaksi, jadi kebenaran disimpan di state agen (checkpointer), bukan di variabel aplikasi
# - Jejak Pikir, Aksi, dan Observasi membuat perilaku agen bisa diperiksa langkah demi langkah
# - Versi agen yang berbeda dapat dibandingkan dengan pertanyaan yang sama
