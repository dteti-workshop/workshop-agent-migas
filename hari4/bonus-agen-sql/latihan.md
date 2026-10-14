# Latihan: Membangun Agen SQL

Berlatih membangun agen SQL untuk database **baru**: beri ia tool skema, jaga agar hanya-baca, lalu buktikan ia bekerja dengan menilai jawabannya terhadap kebenaran yang Anda hitung sendiri.

## Prasyarat

- Sudah menyelesaikan [bab ini](./README.md)
- Sudah menjalankan semua contoh kode di bab
- Memahami tool skema, lapisan keamanan SQL, dan jawaban bertipe
- Sudah menyelesaikan bab [Guardrails dan Middleware Keamanan](../../hari3/07-guardrails-middleware/README.md)

---

## Cara Mengerjakan

1. Buka starter latihan di folder bab ini (`.py` atau `.ipynb`). Setiap starter sudah lengkap kecuali bagian bertanda `TODO(BQ.m)`.
2. Baca komentar `TODO` untuk tahu apa yang harus Anda isi, lalu coba tulis sendiri dulu.
3. Kalau sudah mencoba atau buntu, buka PDF bab ini (`bonus-agen-sql.pdf` di folder yang sama), bagian **Kode Jawaban Latihan** di akhir. Di sana tertulis cell mana yang diubah dan kode yang harus disalin.
4. Jalankan cell berurutan dari atas ke bawah dan cocokkan hasilnya dengan daftar periksa di bawah.

---

## Latihan 1: Analis Produksi

**File**: `latihan_1.py` dan `latihan_1.ipynb`

**Tujuan**: Menerapkan pola agen SQL pada database baru (produksi harian enam sumur) dan menilai agen terhadap kebenaran yang dihitung langsung dengan SQL.

| TODO | Yang Anda isi |
|---|---|
| `TODO(BQ.1)` | kembalikan kamus kebenaran dari lima query SQL: jumlah_sumur, total_minyak_barel, sumur_air_terbanyak, pendapatan_minyak_0610, dan baris_produksi |
| `TODO(BQ.2)` | buat agen dengan tiga tool SQL, system prompt PROMPT_SISTEM_SQL (tanpa kalimat tambahan), response_format=JawabanQuery, dan ModelCallLimitMiddleware(run_limit=15, exit_behavior="end") |
| `TODO(BQ.3)` | bandingkan jawaban agen dengan nilai diharapkan setelah keduanya dinormalkan dengan hanya_alfanumerik |

**Coba dengan**:

- Jumlah sumur
- Total barel minyak
- Sumur dengan air terbanyak
- Pendapatan minyak pada 2026-06-10
- Serangan: hapus data produksi (database harus tidak berubah)

**Kriteria keberhasilan**:

- Lima pemeriksaan berstatus LOLOS
- Jawaban agen dibandingkan dengan angka yang dihitung SQL, bukan dengan perasaan
- Database tidak berubah setelah serangan

---

## Latihan 2 (Bonus): Analis Percakapan

**File**: `latihan_2.py` dan `latihan_2.ipynb`

**Tujuan**: Menggabungkan agen SQL dengan memori agar pertanyaan lanjutan yang merujuk jawaban sebelumnya bisa dijawab.

| TODO | Yang Anda isi |
|---|---|
| `TODO(BQ.4)` | buat agen SQL dengan tiga tool, prompt yang memperbolehkan pertanyaan lanjutan, ModelCallLimitMiddleware(run_limit=15, exit_behavior="end"), dan checkpointer=InMemorySaver() |
| `TODO(BQ.5)` | panggil agent.invoke dengan HumanMessage dan config thread yang sama |
| `TODO(BQ.6)` | ambil state utas dengan agent.get_state(config) |

**Kriteria keberhasilan**:

- "Bagaimana dengan air?" dijawab dengan benar karena agen mengingat pertanyaan pertama
- Pertanyaan ketiga memakai kedua jawaban sebelumnya
- Utas menyimpan pertanyaan, panggilan SQL, dan hasilnya

---

## Daftar Periksa Pengumpulan

- [ ] Latihan 1: Analis Produksi
- [ ] Latihan 2 (bonus, opsional): Analis Percakapan

---

## Butuh Bantuan?

- **Kode jawaban**: bagian Kode Jawaban Latihan pada PDF bab ini
- **Contoh yang mirip**: tinjau skrip di [`code/`](./code/)
- **Konsep belum jelas**: baca ulang [bab ini](./README.md)

---

## Langkah Selanjutnya

Setelah menyelesaikan latihan ini, Anda siap untuk:

**[Bab 9: Model Context Protocol (MCP)](../09-mcp/README.md)**

Di bab berikutnya Anda belajar bagaimana agen menemukan dan memakai tool yang berada di program dan layanan lain, lewat protokol standar dan bukan integrasi buatan sendiri.

[Kembali ke Agen SQL](./README.md)
