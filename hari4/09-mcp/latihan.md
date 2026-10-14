# Latihan: Model Context Protocol (MCP)

Berlatih menghubungkan agen ke layanan eksternal lewat Model Context Protocol (MCP): memakai server jarak jauh, menggabungkan tool MCP dengan tool buatan sendiri, dan akhirnya membangun serta menguji server MCP Anda sendiri.

## Prasyarat

- Sudah menyelesaikan [bab ini](./README.md)
- Sudah menjalankan semua contoh kode di bab
- Sudah menyelesaikan bab [Memulai dengan Agen](../../hari3/03-agen/README.md)

---

## Cara Mengerjakan

1. Buka starter latihan di folder bab ini (`.py` atau `.ipynb`). Setiap starter sudah lengkap kecuali bagian bertanda `TODO(B9.m)`.
2. Baca komentar `TODO` untuk tahu apa yang harus Anda isi, lalu coba tulis sendiri dulu.
3. Kalau sudah mencoba atau buntu, buka PDF bab ini (`09-mcp.pdf` di folder yang sama), bagian **Kode Jawaban Latihan** di akhir. Di sana tertulis cell mana yang diubah dan kode yang harus disalin.
4. Jalankan cell berurutan dari atas ke bawah dan cocokkan hasilnya dengan daftar periksa di bawah.

---

## Latihan 1: Menghubungkan ke Server MCP Context7

**File**: `latihan_1.py` dan `latihan_1.ipynb`

**Tujuan**: Menghubungkan klien MCP ke server publik Context7, mendaftar tool-nya, lalu membuat agen yang memakai tool itu untuk mengambil dokumentasi.

| TODO | Yang Anda isi |
|---|---|
| `TODO(B9.1)` | buat MultiServerMCPClient dengan satu server "context7": transport "streamable_http" ke https://mcp.context7.com/mcp |
| `TODO(B9.2)` | ambil daftar tool lewat client.get_tools(), dijalankan dengan jalankan(...) dan batas waktu 30 detik (asyncio.wait_for) |
| `TODO(B9.3)` | buat agen dari model dan tool MCP |

**Kriteria keberhasilan**:

- Daftar tool dari Context7 tercetak
- Agen memilih sendiri tool Context7 yang dipanggil
- Bila koneksi gagal, pesan error dicetak dan program tidak crash

---

## Latihan 2: Agen Multi-Tool dengan MCP

**File**: `latihan_2.py` dan `latihan_2.ipynb`

**Tujuan**: Menggabungkan tool dari server MCP lapangan (stdio) dengan tool lokal buatan sendiri dalam satu agen.

| TODO | Yang Anda isi |
|---|---|
| `TODO(B9.4)` | definisikan field KerugianInput: downtime_jam dan laju_normal_bopd (float, keduanya >= 0, dengan description) |
| `TODO(B9.5)` | buat tool hitung_kerugian_produksi yang mencetak panggilannya, lalu menghitung barel hilang = laju_normal_bopd * downtime_jam / 24 |
| `TODO(B9.6)` | buat MultiServerMCPClient untuk satu server stdio "lapangan" yang menjalankan PATH_SERVER dengan sys.executable |
| `TODO(B9.7)` | ambil tool MCP dengan jalankan(client.get_tools()), lalu gabungkan dengan tool lokal menjadi semua_tool |
| `TODO(B9.8)` | buat agen dari model dan semua_tool dengan system prompt asisten teknis lapangan (pakai tool, jangan menghitung sendiri) |

**Coba dengan**:

- Water cut dari 95 bopd minyak dan 380 bwpd air (tool MCP)
- Kehilangan produksi SR-020 mati 18 jam pada 120 bopd (tool lokal)
- Status SR-027 lalu kehilangan produksinya (keduanya)

**Kriteria keberhasilan**:

- Daftar tool MCP dan tool lokal dicetak terpisah
- Agen memilih tool menurut deskripsinya, apa pun asalnya
- Pertanyaan ketiga memanggil tool MCP dan tool lokal

---

## Latihan 3 (Bonus): Server MCP Buatan Sendiri

**File**: `latihan_3.py`

**Tujuan**: Menulis server MCP stdio dengan FastMCP yang membuka dua tool hanya-baca: daftar work order terbuka dan perkiraan kerugian downtime.

| TODO | Yang Anda isi |
|---|---|
| `TODO(B9.9)` | tulis tool daftar_wo_terbuka(area) dengan @mcp.tool(): cari WORK_ORDER menurut area (huruf besar di awal), raise ValueError yang menyebut area yang ada bila tidak dikenal, dan kembalikan satu baris per work order (id | deskripsi | prioritas) |
| `TODO(B9.10)` | tulis tool hitung_kerugian_downtime(downtime_jam, laju_bopd, harga_usd_per_bbl=70.0): raise ValueError bila negatif, hitung barel = laju_bopd * downtime_jam / 24, dan kembalikan teks 'Kehilangan X barel, perkiraan kerugian USD Y' |

**Kriteria keberhasilan**:

- Server berjalan lewat stdio dan menawarkan dua tool
- Input tidak valid ditolak dengan error yang jelas
- Docstring tool cukup jelas agar agen memilih tool yang tepat

---

## Latihan 4 (Bonus): Klien Penguji untuk Server Buatan Sendiri

**File**: `latihan_4.py` dan `latihan_4.ipynb`

**Tujuan**: Kerjakan setelah Latihan 3 selesai karena klien ini menjalankan server dari latihan_3.py. Menjalankan server buatan sendiri sebagai subproses, menguji tool-nya langsung tanpa model dengan tiga pemeriksaan di kode, lalu menghubungkan agen ke server itu.

| TODO | Yang Anda isi |
|---|---|
| `TODO(B9.11)` | buat MultiServerMCPClient untuk server stdio "work_order" yang menjalankan PATH_SERVER dengan sys.executable |
| `TODO(B9.12)` | ambil tool server dengan jalankan(client.get_tools()), lalu buat kamus tool_per_nama |
| `TODO(B9.13)` | panggil daftar_wo_terbuka('Kenanga') langsung (ainvoke lewat jalankan), lalu ok = hasilnya memuat WO-26-12611; tambahkan ke lolos |
| `TODO(B9.14)` | panggil daftar_wo_terbuka dengan area 'Atlantis'; ok bernilai True bila hasilnya memuat 'tidak dikenal' (error server dikembalikan sebagai teks) atau ToolException muncul |
| `TODO(B9.15)` | buat agen dari model dan tool server dengan system prompt asisten pemeliharaan (pakai tool, jangan menebak) |

**Kriteria keberhasilan**:

- Tiga uji langsung berstatus LOLOS (daftar work order, kerugian downtime, area tidak dikenal ditolak)
- Agen memakai kedua tool server untuk satu pertanyaan gabungan

---

## Daftar Periksa Pengumpulan

- [ ] Latihan 1: Menghubungkan ke Server MCP Context7
- [ ] Latihan 2: Agen Multi-Tool dengan MCP
- [ ] Latihan 3 (bonus, opsional): Server MCP Buatan Sendiri
- [ ] Latihan 4 (bonus, opsional): Klien Penguji untuk Server Buatan Sendiri

---

## Butuh Bantuan?

- **Kode jawaban**: bagian Kode Jawaban Latihan pada PDF bab ini
- **Contoh yang mirip**: tinjau skrip di [`code/`](./code/)
- **Konsep belum jelas**: baca ulang [bab ini](./README.md)

---

## Langkah Selanjutnya

Setelah menyelesaikan latihan ini, Anda siap untuk:

**[Bab 10: RAG Agentik](../10-agentic-rag/README.md)**

Di bab berikutnya Anda membungkus pencarian dokumen sebagai tool dan membiarkan agen memutuskan kapan mencari.

[Kembali ke MCP](./README.md)
