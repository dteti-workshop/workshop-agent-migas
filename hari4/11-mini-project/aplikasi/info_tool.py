"""Keterangan tool untuk penjelajah: penjelasan singkat, data sumber, hasil, contoh masukan, dan contoh pertanyaan.

Nama, deskripsi, dan parameter tool dibaca langsung dari tool-nya (docstring dan skema argumen), jadi tidak diulang di sini.
Yang ditulis di sini hanya yang tidak bisa dibaca dari kode: untuk apa tool dipakai, dari mana datanya, dan contoh pemakaiannya.

  INFO[nama_tool] = {
      "fungsi"  : satu atau dua kalimat bahasa awam tentang apa yang dikerjakan tool
      "sumber"  : dari mana data atau efeknya berasal
      "hasil"   : apa yang dikembalikan tool (bentuk teksnya)
      "contoh"  : masukan contoh yang aman dicoba, persis seperti `tool.invoke({...})`
      "tanya"   : pertanyaan ke agen yang membuat agen memilih tool ini
  }
"""

INFO = {
    # ------------------------------------------------------------------ Operasi
    "laporan_harian": {
        "fungsi": "Membuka laporan produksi satu hari di gathering station GS-SR1: minyak, air, gas, jumlah sumur aktif, deferred (produksi tertunda akibat gangguan), dan kejadian hari itu.",
        "sumber": "File CSV laporan harian Juli 2026 (`data/eval/daily_gs_sr1_2026-07.csv`).",
        "hasil": "Satu kalimat ringkasan hari itu. Bila tanggal tidak ada di data, hasilnya pesan bahwa laporan tidak ada beserta rentang tanggal yang tersedia.",
        "contoh": {"tanggal": "2026-07-14"},
        "tanya": ["Apa yang terjadi di GS-SR1 pada 14 Juli 2026?"],
    },
    "ringkasan_produksi_bulanan": {
        "fungsi": "Meringkas produksi GS-SR1 selama Juli 2026: rata-rata minyak dan air, water cut, total deferred (produksi tertunda), dan jumlah hari berkejadian.",
        "sumber": "File CSV laporan harian Juli 2026.",
        "hasil": "Satu paragraf angka ringkasan satu bulan. Tidak butuh parameter.",
        "contoh": {},
        "tanya": ["Ringkas produksi GS-SR1 selama Juli 2026."],
    },
    "bandingkan_produksi": {
        "fungsi": "Membandingkan laporan harian dua tanggal: selisih minyak, air, gas, dan deferred (produksi tertunda akibat gangguan).",
        "sumber": "File CSV laporan harian Juli 2026.",
        "hasil": "Satu kalimat selisih (tanggal B dikurangi tanggal A). Bila salah satu tanggal tidak ada, hasilnya pesan yang menyebut tanggal itu.",
        "contoh": {"tanggal_a": "2026-07-10", "tanggal_b": "2026-07-14"},
        "tanya": ["Bandingkan produksi 10 Juli dan 14 Juli 2026."],
    },
    "hari_berkejadian": {
        "fungsi": "Mendaftar hari-hari di bulan Juli yang punya kejadian khusus, beserta produksi yang tertunda (deferred) pada hari itu.",
        "sumber": "File CSV laporan harian Juli 2026 (kolom kejadian).",
        "hasil": "Daftar bertanda strip: tanggal, ringkasan kejadian, dan deferred.",
        "contoh": {"maks": 3},
        "tanya": ["Hari apa saja pada Juli yang punya kejadian?"],
    },
    "cek_status_sumur": {
        "fungsi": "Memeriksa status satu sumur: area, jenis pompa, status, produksi, frekuensi VSD (khusus ESP), dan catatan terakhir. Tool ini mewakili koneksi ke sistem pemantauan sumur.",
        "sumber": "File CSV `data/field/sumur.csv`: 196 sumur Seruni, Kenanga, dan Melati dengan status per 31 Juli 2026 (fiktif, pengganti SCADA).",
        "hasil": "Teks status sumur. Kode sumur yang tidak dikenal menghasilkan pesan yang menyebut pola kode yang berlaku.",
        "contoh": {"kode_sumur": "SR-020"},
        "tanya": ["Apa status sumur SR-020?"],
    },
    "daftar_sumur": {
        "fungsi": "Mendaftar sumur menurut area, jenis pompa, dan status, lalu mengurutkannya menurut minyak, water cut, atau kode. Cocok untuk pertanyaan yang tidak menyebut kode sumur.",
        "sumber": "File CSV `data/field/sumur.csv` (196 sumur, status per 31 Juli 2026).",
        "hasil": "Satu baris ringkasan (jumlah sumur, total minyak dan air, water cut) lalu daftar bertanda strip dengan produksi dan water cut tiap sumur.",
        "contoh": {"area": "Seruni", "urutkan": "water_cut_tertinggi", "maks": 5},
        "tanya": ["Sumur Seruni mana yang water cut-nya paling tinggi?", "Sumur apa saja yang sedang menunggu pulling?"],
    },
    "produksi_sumur": {
        "fungsi": "Menampilkan produksi harian satu sumur pada rentang tanggal: rata-rata, hari tanpa produksi, nilai tertinggi dan terendah.",
        "sumber": "File CSV `data/field/produksi_sumur_2026-07.csv`: produksi harian 196 sumur Juli 2026. Jumlah sumur Seruni sama dengan laporan harian GS-SR1.",
        "hasil": "Ringkasan rentang tanggal, dan rincian harian bila rentangnya tujuh hari atau kurang. Kode sumur yang tidak dikenal menghasilkan pesan tidak ditemukan.",
        "contoh": {"kode_sumur": "SR-041", "dari": "2026-07-18", "sampai": "2026-07-22"},
        "tanya": ["Bagaimana produksi SR-041 antara 18 dan 22 Juli?", "Berapa hari SR-014 tidak berproduksi pada Juli?", "Sejak kapan KN-033 berhenti berproduksi?"],
    },
    "hitung_water_cut": {
        "fungsi": "Menghitung water cut (persentase air dalam total cairan) dari produksi minyak dan air. Kalkulator ini mencegah model menghitung di kepala.",
        "sumber": "Rumus: air / (minyak + air) x 100. Tidak membaca data.",
        "hasil": "Satu kalimat dengan persentase water cut.",
        "contoh": {"oil_bopd": 120, "water_bwpd": 480},
        "tanya": ["Hitung water cut jika produksi minyak 120 bopd dan air 480 bwpd."],
    },
    "catat_serah_terima": {
        "fungsi": "Menyimpan catatan serah terima shift. Ini tindakan TULIS: di sistem nyata ia mengubah logbook, jadi perlu persetujuan manusia.",
        "sumber": "Hanya menambah satu baris ke daftar `CATATAN_TINDAKAN` di memori (aman dicoba).",
        "hasil": "Satu kalimat berisi nomor catatan (`SHIFT-UJI-...`).",
        "contoh": {"catatan": "SR-041 masih menunggu rig, lanjutkan pemantauan di shift berikutnya."},
        "tanya": ["Catat serah terima: SR-041 masih menunggu rig, lanjutkan pemantauan di shift berikutnya."],
    },
    # ------------------------------------------------------------------ Perawatan
    "riwayat_work_order": {
        "fungsi": "Menampilkan riwayat work order satu aset: tanggal, kategori kegagalan, komponen, tindakan, dan downtime.",
        "sumber": "Dua file CSV work order (`data/raw/work_orders.csv` digabung dengan hasil ekstraksi terstruktur).",
        "hasil": "Baris pembuka (jumlah work order dan total downtime) diikuti satu baris per work order terbaru.",
        "contoh": {"asset_id": "SR-020", "maks": 3},
        "tanya": ["Bagaimana riwayat work order sumur SR-020?"],
    },
    "cari_work_order": {
        "fungsi": "Mencari work order menurut aset, kategori kegagalan, komponen, tipe peralatan, area, dan rentang tanggal. Tanpa kode aset, pencarian mencakup seluruh aset; dengan kode aset, ia menyaring riwayat satu aset.",
        "sumber": "Dua file CSV work order (`data/raw/work_orders.csv` digabung dengan hasil ekstraksi terstruktur): 400 work order, Januari sampai September 2026.",
        "hasil": "Baris pembuka (jumlah work order yang cocok, total downtime, jumlah yang ditampilkan) diikuti satu baris per work order terbaru. Komponen yang tidak dikenal menghasilkan daftar komponen yang ada.",
        "contoh": {"kategori": "Electrical", "dari": "2026-07-01", "sampai": "2026-07-31", "maks": 5},
        "tanya": ["Work order kelistrikan apa saja yang terjadi pada Juli 2026?", "Berapa work order komponen VSD di area Seruni?", "Work order kelistrikan SR-014 pada Juli 2026?"],
    },
    "statistik_kegagalan": {
        "fungsi": "Menghitung jumlah work order dan total downtime per kategori kegagalan, untuk satu tipe peralatan atau semuanya.",
        "sumber": "File CSV work order.",
        "hasil": "Satu baris total, lalu satu baris per kategori kegagalan, terurut dari downtime terbesar.",
        "contoh": {"tipe_peralatan": "ESP"},
        "tanya": ["Kategori kegagalan apa yang paling banyak menyebabkan downtime pada ESP?"],
    },
    "aset_downtime_tertinggi": {
        "fungsi": "Mengurutkan aset berdasarkan total downtime dari seluruh work order.",
        "sumber": "File CSV work order.",
        "hasil": "Daftar aset teratas dengan total jam downtime dan jumlah work order.",
        "contoh": {"maks": 3},
        "tanya": ["Aset mana yang downtime-nya paling tinggi?"],
    },
    "buat_work_order": {
        "fungsi": "Membuat work order pemeliharaan baru. Ini tindakan TULIS: di sistem nyata ia membuka pekerjaan bagi tim lapangan.",
        "sumber": "Hanya menambah satu baris ke `CATATAN_TINDAKAN` di memori (aman dicoba).",
        "hasil": "Satu kalimat berisi nomor work order (`WO-UJI-...`).",
        "contoh": {"asset_id": "V-SR1-101", "uraian": "Periksa level controller", "prioritas": "sedang"},
        "tanya": ["Buat work order prioritas sedang untuk memeriksa level controller V-SR1-101."],
    },
    "tutup_work_order": {
        "fungsi": "Menutup work order yang pekerjaannya sudah selesai. Ini tindakan TULIS dan hanya berhasil untuk nomor yang ada di riwayat.",
        "sumber": "Memeriksa nomor ke CSV work order, lalu menambah satu baris ke `CATATAN_TINDAKAN` di memori.",
        "hasil": "Kalimat penutupan dicatat, atau pesan bahwa work order tidak ditemukan.",
        "contoh": {"wo_id": "WO-26-12115", "catatan": "Pulling motor selesai"},
        "tanya": ["Tutup work order WO-26-12115 dengan catatan pekerjaan pulling motor selesai."],
    },
    # ------------------------------------------------------------------ HSE
    "cari_insiden": {
        "fungsi": "Mencari insiden HSE menurut lokasi, jenis bahaya, dan tingkat keparahan. Semua filter opsional.",
        "sumber": "Dua file CSV insiden HSE (`data/raw/hse_incidents.csv` digabung dengan hasil ekstraksi terstruktur).",
        "hasil": "Jumlah insiden yang cocok, lalu satu baris per insiden terbaru dengan nomor, tanggal, lokasi, bahaya, dan tingkat.",
        "contoh": {"bahaya": "H2S/Gas", "maks": 3},
        "tanya": ["Tampilkan tiga insiden tingkat Tinggi terbaru."],
    },
    "ringkasan_insiden": {
        "fungsi": "Meringkas seluruh insiden HSE: jumlah per jenis bahaya, per tingkat keparahan, dan lokasi yang paling sering.",
        "sumber": "File CSV insiden HSE.",
        "hasil": "Empat baris angka ringkasan. Tidak butuh parameter.",
        "contoh": {},
        "tanya": ["Ringkas semua insiden HSE: bahaya apa yang paling sering?"],
    },
    "usulkan_tindakan_korektif": {
        "fungsi": "Mencatat usulan tindakan korektif untuk sebuah insiden. Ini tindakan TULIS dan perlu persetujuan manusia.",
        "sumber": "Hanya menambah satu baris ke `CATATAN_TINDAKAN` di memori (aman dicoba).",
        "hasil": "Satu kalimat berisi nomor usulan (`CAPA-UJI-...`) dan penanggung jawab.",
        "contoh": {"incident_id": "HSE-26-0004", "tindakan": "Pagar wellhead diberi pembatas dan rambu", "penanggung_jawab": "Supervisor HSE"},
        "tanya": ["Usulkan tindakan korektif untuk insiden HSE-26-0004: pagar wellhead diberi pembatas dan rambu."],
    },
    "kirim_notifikasi_hse": {
        "fungsi": "Mengirim notifikasi HSE kepada seseorang atau kelompok. Ini tindakan TULIS: pesan yang sudah terkirim tidak bisa ditarik.",
        "sumber": "Hanya menambah satu baris ke `CATATAN_TINDAKAN` di memori; tidak ada pesan nyata yang dikirim.",
        "hasil": "Satu kalimat berisi nomor notifikasi (`NOTIF-UJI-...`).",
        "contoh": {"penerima": "Supervisor HSE", "pesan": "Alarm H2S di SR-027 mencapai 12 ppm, area dibatasi."},
        "tanya": ["Kirim notifikasi ke Supervisor HSE: alarm H2S di SR-027 mencapai 12 ppm, area dibatasi."],
    },
    # ------------------------------------------------------------------ Engineering
    "konversi_satuan": {
        "fungsi": "Mengonversi satuan: bbl dan m3, psi dan bar. Kalkulator konversi yang menjamin angka tidak ditebak model.",
        "sumber": "Rumus konversi tetap. Tidak membaca data.",
        "hasil": "Satu kalimat hasil konversi. Pasangan satuan yang tidak didukung menghasilkan error yang jelas.",
        "contoh": {"nilai": 1200, "dari": "psi", "ke": "bar"},
        "tanya": ["Berapa bar tekanan 1.200 psi?"],
    },
    "ubah_setpoint_vsd": {
        "fungsi": "Mengubah frekuensi VSD (setpoint) pompa ESP sebuah sumur. Ini tindakan TULIS berisiko: setpoint yang salah dapat merusak pompa.",
        "sumber": "Membaca `data/field/sumur.csv` untuk memeriksa sumur (harus ESP dan berstatus Produksi), lalu menambah satu baris ke `CATATAN_TINDAKAN` di memori. Nilai di atas 55 Hz memunculkan peringatan.",
        "hasil": "Satu kalimat berisi frekuensi baru, frekuensi sebelumnya, dan nomor perubahan (`VSD-UJI-...`), dengan peringatan bila di atas 55 Hz. Sumur non-ESP atau yang tidak berproduksi ditolak dengan pesan.",
        "contoh": {"kode_sumur": "SR-020", "frekuensi_hz": 48},
        "tanya": ["Ubah setpoint VSD sumur SR-020 menjadi 48 Hz."],
    },
    # ------------------------------------------------------------------ Dokumen
    "cari_dokumen_sop": {
        "fungsi": "Mencari prosedur kerja (SOP): batas alarm, langkah kerja, dan tindakan darurat. Hanya membaca dokumen berstatus aktif.",
        "sumber": "Indeks dokumen hari 2 (`chroma_db`), disaring ke jenis SOP. Mewakili pencarian di basis pengetahuan.",
        "hasil": "Beberapa blok `<dokumen id=... revisi=... bagian=...>` berisi chunk teks, yang bisa dikutip sebagai [DOC_ID bagian].",
        "contoh": {"query": "alarm H2S 10 ppm tindakan", "k": 2},
        "tanya": ["Apa tindakan SOP jika alarm H2S mencapai 10 ppm?"],
    },
    "cari_dokumen_manual": {
        "fungsi": "Mencari manual perangkat, misalnya kode alarm dan cara operasi VSD FD-500.",
        "sumber": "Indeks dokumen hari 2, disaring ke jenis Manual (PDF).",
        "hasil": "Beberapa blok `<dokumen ...>` berisi chunk manual.",
        "contoh": {"query": "kode alarm overcurrent VSD FD500", "k": 2},
        "tanya": ["Apa arti kode alarm pada VSD FD500 dan apa langkah pertamanya?"],
    },
    "cari_dokumen_laporan": {
        "fungsi": "Mencari laporan bulanan dan lessons learned.",
        "sumber": "Indeks dokumen hari 2, disaring ke jenis Laporan dan Lessons Learned.",
        "hasil": "Beberapa blok `<dokumen ...>` berisi chunk laporan.",
        "contoh": {"query": "kebakaran kecil saat grinding", "k": 2},
        "tanya": ["Apa pelajaran dari kebakaran kecil saat grinding di workshop?"],
    },
    "cari_dokumen_investigasi": {
        "fungsi": "Mencari laporan investigasi insiden HSE. Dokumen ini terbatas: tool lain tidak dapat membacanya, jadi hanya agen yang dipasangi tool ini yang bisa menjawab dari laporan investigasi.",
        "sumber": "Indeks dokumen hari 2, disaring ke jenis Investigasi dengan hak akses HSE.",
        "hasil": "Beberapa blok `<dokumen ...>` berisi chunk laporan investigasi.",
        "contoh": {"query": "penyebab paparan H2S di SR-027", "k": 2},
        "tanya": ["Apa temuan laporan investigasi H2S di sumur SR-027?"],
    },
}


def info(nama: str) -> dict:
    """Keterangan tool; tool yang belum punya keterangan mendapat isian kosong yang aman."""
    return INFO.get(nama, {"fungsi": "", "sumber": "", "hasil": "", "contoh": {}, "tanya": []})
