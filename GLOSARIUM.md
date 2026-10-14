# Glosarium

Definisi istilah yang dipakai di kursus ini dalam bahasa sehari-hari. Setiap entri menyebut bab tempat Anda pertama kali menemuinya.

Indeks: [A](#a) | [B](#b) | [C](#c) | [D](#d) | [E](#e) | [F](#f) | [G](#g) | [H](#h) | [I](#i) | [K](#k) | [L](#l) | [M](#m) | [P](#p) | [R](#r) | [S](#s) | [T](#t) | [U](#u) | [V](#v) | [W](#w)

---

## A

### Agen (agent)
*Bab 3.* Program tempat model memutuskan, langkah demi langkah, tool mana yang dipakai berikutnya sampai ia bisa menjawab. Dibuat dengan `create_agent()`.

**Approval** -> lihat *Human-in-the-loop*.

### `astream()` / `ainvoke()`
*Bab bonus Streaming Agen.* Versi asinkron dari `stream()` / `invoke()`. Pakai di dalam `async def` agar satu proses melayani banyak pengguna sekaligus.

### Audit trail (jejak audit)
*Bab 6, 7, bonus Agen SQL.* Catatan tentang apa yang ditanyakan kepada agen, apa yang ia lakukan, dan apa yang diputuskan manusia. Diperlukan untuk kepercayaan dan penelusuran masalah.

## B

### Bad actor
*Bab bonus Agen SQL.* Peralatan yang paling sering rusak atau paling banyak menyebabkan downtime. Biasanya ditemukan dengan analisis Pareto atas data work order.

### bopd (barrel of oil per day)
*Bab 2.* Satuan laju produksi minyak: barel minyak per hari. Lawannya `bwpd`, barel air per hari.

### Bump test
*Bab 7, 8, 09.* Pemeriksaan singkat alat deteksi gas dengan memaparkannya ke gas uji untuk memastikan alarm berbunyi. Pada SOP-HSE-001 Rev 3 dilakukan setiap hari.

## C

### Checkpoint
*Bab 5.* Salinan tersimpan dari keadaan agen setelah satu langkah. Satu thread adalah rangkaian checkpoint.

### Checkpointer
*Bab 5.* Komponen yang menyimpan dan memuat checkpoint (`InMemorySaver`, `SqliteSaver`, `PostgresSaver`). Diperlukan untuk memori dan untuk persetujuan manusia.

### Chunk
*Hari 2, bab 5, bonus Streaming Agen.* (1) Bagian dokumen setelah dipecah (hari 2). (2) Bagian kecil pesan model yang dialirkan (`AIMessageChunk`, bab bonus Streaming Agen).

### `Command`
*Bab 6.* Objek yang Anda kirim ke `invoke()` untuk melanjutkan agen yang sedang berhenti: `Command(resume={"decisions": [...]})`.

### Context window
Jumlah teks maksimum (dihitung dalam token) yang bisa dibaca model dalam satu permintaan. Percakapan yang panjang bisa melampauinya.

## D

### Decision (keputusan)
*Bab 6.* Jawaban reviewer terhadap tindakan yang ditahan: `approve`, `edit`, `reject` (dengan alasan) atau `respond`.

### Defense in depth (pertahanan berlapis)
*Bab 7, bonus Agen SQL.* Melindungi sistem dengan beberapa lapisan yang saling bebas, sehingga satu kegagalan tidak fatal.

### Downtime
*Bab 1, bonus Agen SQL.* Lama waktu peralatan atau sumur berhenti beroperasi, biasanya dalam jam. Pada data work order tertulis bebas ("5 jam", "1 hari", "07.30 s/d 15.00").

## E

### Embedding
*Hari 2.* Deretan angka yang mewakili makna sebuah teks. Makna yang mirip menghasilkan angka yang mirip.

### Enum / `Literal`
*Bab 4.* Kolom yang hanya boleh berisi salah satu dari kumpulan nilai tetap (misalnya `"Rendah"`, `"Sedang"`, `"Tinggi"`).

### ESP (Electrical Submersible Pump)
*Bab 2.* Pompa benam listrik, dipasang di dalam sumur untuk mengangkat fluida ke permukaan. Contoh aset: SR-020.

## F

### Fallback model
*Bab 7.* Model cadangan yang dipakai saat panggilan model utama gagal (`ModelFallbackMiddleware`).

### Function calling
*Bab 2.* Fitur model: alih-alih menjawab dengan teks, model mengembalikan *nama* fungsi dan *argumen* untuk memanggilnya. Program Anda yang kemudian menjalankan fungsi itu. Begitulah tool bekerja. (Model tidak pernah menjalankan apa pun sendiri.)

## G

### Golden set
*Hari 2, bab 10, 11.* Kumpulan pertanyaan dengan sumber dan butir jawaban kunci yang sudah diketahui, dipakai untuk mengukur kualitas pencarian dan jawaban.

### Guardrail
*Bab 7.* Aturan yang dijalankan oleh kode (bukan oleh prompt) untuk memeriksa, membatasi atau mengubah apa yang masuk ke dan keluar dari agen.

## H

### H2S (hidrogen sulfida)
*Bab 7, 10.* Gas beracun dan mudah terbakar yang bisa ada pada fluida produksi. Dasar SOP-HSE-001: alarm bertingkat 5, 10 dan 50 ppm.

### Hash (strategi PII)
*Bab 7.* Mengganti nilai sensitif dengan sidik jari yang stabil, sehingga nilai yang sama bisa dibandingkan tanpa bisa dibaca.

### Human-in-the-loop (HITL)
*Bab 6.* Menghentikan agen sebelum tindakan berisiko agar seseorang bisa menyetujui, mengubah atau menolaknya.

### Hybrid search (pencarian hybrid)
*Hari 2.* Menggabungkan pencarian semantik (embedding) dan pencarian kata kunci (BM25) dengan Reciprocal Rank Fusion (RRF), sehingga dokumen yang baik di kedua daftar naik ke atas.

## I

### Interrupt
*Bab 6.* Penghentian sementara agen yang dipicu oleh `HumanInTheLoopMiddleware` untuk menunggu keputusan manusia. `invoke()` kembali lebih awal dengan kunci `"__interrupt__"` berisi tindakan yang diusulkan.

### `invoke()`
*Bab 3.* Menjalankan agen dan menunggu hasil akhirnya. Bandingkan dengan `stream()`.

## K

### Kasus uji (test case)
*Bab 11.* Satu pertanyaan beserta kriteria berhasil (tool yang dipanggil, isi jawaban, efek pada data). Di bab 11 kriteria dinilai sendiri oleh peserta dengan membaca jejak agen; di pemakaian nyata diperiksa kode dan dijalankan berulang setiap kali agen diubah.

### Katalog tool
*Bab 11.* Kumpulan tool siap pakai per use case (Operasi, Perawatan, HSE, Engineering) di `alat_data.py`, diberi tanda baca atau tulis. Peserta memilih dari katalog, atau menulis tool sendiri, sebagai komponen pertama agen.

### Konteks runtime (runtime context)
*Bab 8.* Fakta tepercaya (pengguna, area, peran) yang dikirim bersama permintaan dengan `invoke(..., context=...)`. Tool membacanya lewat `ToolRuntime`; model tidak bisa melihat atau mengubahnya.

## L

### LLM-as-a-judge (penilai berbasis model)
*Bab 7, 10.* Memakai panggilan model kedua untuk menilai atau mengklasifikasi sesuatu, misalnya "apakah ini serangan?" atau "apakah jawaban ini sesuai butir jawaban kunci?".

### LOTO (Lock Out Tag Out)
*Bab 6.* Prosedur mengunci dan menandai sumber energi sebelum pekerjaan perawatan agar peralatan tidak menyala tiba-tiba. Lihat SOP-HSE-007.

## M

### Mask (strategi PII)
*Bab 7.* Menyembunyikan sebagian besar nilai sensitif tetapi menyisakan petunjuk, seperti `**** **** **** 1111`.

### MCP (Model Context Protocol)
*Bab 9.* Cara standar bagi agen untuk menemukan dan memakai tool yang disediakan program atau layanan lain.

### Memori jangka pendek
*Bab 5.* Riwayat percakapan satu thread yang disimpan oleh checkpointer.

### Middleware
*Bab 6, 7.* Kode tambahan yang berjalan pada titik tertentu dalam loop agen (sebelum agen, di sekitar panggilan model, di sekitar panggilan tool, setelah agen) untuk menambah perilaku tanpa mengubah tool atau prompt.

### Mini project
*Bab 11.* Prototipe agen sederhana yang disusun berkelompok untuk satu use case dari tiga komponen (tool, prompt, interrupt), dirakit di sel notebook, dijalankan di aplikasi Streamlit, lalu diuji dengan panduan uji dan didemokan.

### MoC (Management of Change)
*Bab 10, 11.* Proses resmi untuk menilai dan menyetujui perubahan pada peralatan, prosedur atau organisasi sebelum perubahan itu dijalankan.

### Multi-agen (multi-agent system)
*Bab 8.* Beberapa agen bekerja bersama, misalnya agen pengawas yang mendelegasikan pekerjaan ke agen spesialis.

### Muster point
*Bab 2, 7, 10.* Titik kumpul darurat. Pada SOP-HSE-001 Rev 3, letaknya minimal 50 m di arah datangnya angin dari sumber gas.

## P

### PII (Personally Identifiable Information)
*Bab 7.* Data yang mengidentifikasi seseorang: alamat email, nomor telepon, NIK, nomor kartu, nama pekerja.

### Prompt bank
*Bab 11.* Kumpulan variasi prompt (gaya jawaban seperti ketat, ramah, tabel, hati-hati) dan pertanyaan contoh per use case di `prompt_bank.py`, untuk disalin, diubah, dan dibandingkan sebagai komponen kedua agen.

### Prompt injection
*Bab 7.* Teks yang dirancang agar model mengabaikan instruksinya ("abaikan instruksi sebelumnya..."). Bisa datang dari dokumen yang dicari, bukan hanya dari pengguna.

### PTW (Permit to Work)
*Bab 6.* Izin kerja tertulis untuk pekerjaan berisiko, misalnya pekerjaan panas (hot work). Lihat SOP-HSE-004. Persetujuan agen mengikuti pola yang sama.

### Pydantic model
*Bab 1, 4.* Kelas Python yang menjelaskan bentuk dan aturan data. Dipakai untuk argumen tool dan structured output.

## R

### RAG (Retrieval-Augmented Generation)
*Bab 10.* Memberikan chunk dokumen yang relevan, ditemukan lewat pencarian, kepada model untuk dijadikan dasar jawaban.

### ReAct
*Bab 3, 11.* Loop agen: Reason (berpikir), Act (memakai tool), Observe (membaca hasil), lalu ulangi. Di bab 11 setiap langkah tampil sebagai Pikir, Aksi, dan Observasi pada jejak agen di aplikasi.

### Read-only connection (koneksi hanya-baca)
*Bab bonus Agen SQL.* Koneksi database yang menolak penulisan. Perlindungan terkuat untuk agen SQL.

### Redact (strategi PII)
*Bab 7.* Mengganti nilai sensitif dengan penanda seperti `[REDACTED_EMAIL]`.

### `response_format`
*Bab 4.* Argumen `create_agent()` yang membuat jawaban akhir agen berupa objek bertipe, tersedia di `response["structured_response"]`.

### Retrieval
*Hari 2, bab 10.* Langkah mencari chunk dokumen yang paling relevan terhadap sebuah pertanyaan. Kursus ini memakai pencarian hybrid (embedding dan kata kunci BM25 digabung dengan RRF).

## S

### Schema (skema)
(1) Deskripsi struktur data (model Pydantic, argumen tool). (2) Tabel dan kolom sebuah database (bab bonus Agen SQL).

### Server-Sent Events (SSE)
*Bab bonus Streaming Agen.* Format teks sederhana (baris `data: ...`) untuk mendorong aliran langsung dari server ke browser.

### Sitasi (citation)
*Bab 10.* Rujukan ke dokumen sumber di dalam jawaban, dengan format `[DOC_ID bagian]`. Sitasi harus berasal dari dokumen yang benar-benar diambil.

### SRP (Sucker Rod Pump)
*Bab 2.* Pompa angguk: pompa di dalam sumur yang digerakkan batang pompa dari unit pemompa di permukaan. Contoh aset: KN-xxx.

### State (keadaan)
*Bab 5.* Data yang dibawa agen selama satu proses, terutama daftar pesannya.

### Stream mode
*Bab bonus Streaming Agen.* Apa yang dihasilkan `stream()`: `values` (seluruh state), `updates` (perubahan), `messages` (token) atau `custom` (peristiwa kiriman tool).

### Streamlit
*Bab 11.* Pustaka Python untuk membuat aplikasi web dari skrip. Skrip dijalankan ulang dari atas pada setiap interaksi pengguna, sehingga data yang harus bertahan disimpan di luar variabel biasa.

### Structured output
*Bab 1, 4.* Jawaban model yang dikembalikan sebagai data tervalidasi (objek Pydantic), bukan teks bebas.

### Subagent / agen spesialis
*Bab 8.* Agen yang dipanggil oleh agen pengawas, biasanya dibungkus sebagai tool.

### Supervisor (agen pengawas)
*Bab 8.* Agen yang tool-nya adalah agen lain; ia mendelegasikan pekerjaan dan menggabungkan jawabannya.

## T

### Text-to-SQL
*Bab bonus Agen SQL.* Mengubah pertanyaan bahasa biasa menjadi kueri SQL. Agen SQL melakukannya lalu menjalankan kueri itu.

### Thread / `thread_id`
*Bab 5.* Satu percakapan di dalam checkpointer. `thread_id` pada `config` memilih percakapan tersimpan mana yang dilanjutkan.

### Token
Satuan kecil teks (satu kata atau bagian kata) yang dibaca dan ditulis model. Harga dan batas dihitung dalam token.

### Tool (alat)
*Bab 2.* Fungsi yang bisa diminta model untuk dijalankan program Anda, dijelaskan oleh nama, deskripsi dan argumen bertipe.

### `ToolRuntime`
*Bab 8.* Parameter khusus tool yang memberi akses ke konteks runtime dan state. Disembunyikan dari model.

### Transport MCP (stdio dan Streamable HTTP)
*Bab 9.* Cara klien dan server MCP berkomunikasi. `stdio`: server berjalan sebagai subproses klien dan berbicara lewat stdin/stdout. `streamable_http`: server berjalan mandiri dan dihubungi lewat URL.

## U

### Use case
*Bab 11.* Satu masalah kerja yang diselesaikan dengan agen. Layak dikerjakan bila datanya sudah ada, bisa diintegrasikan ke tool dalam waktu yang tersedia, dan akibat kesalahannya terkendali (keamanan).

## V

### Validasi (validation)
*Bab 4.* Memeriksa bahwa data mengikuti aturan skemanya. Kalau jawaban terstruktur tidak valid, error-nya dikirim kembali ke model agar mencoba lagi.

### Vector store
*Hari 2.* Database yang menyimpan embedding dan menemukan yang paling dekat dengan sebuah kueri.

## W

### Water cut
*Bab 2.* Persentase air dalam total cairan produksi: `bwpd / (bopd + bwpd) x 100`. Contoh perhitungan pada tool `hitung_water_cut`.

### WO (Work Order)
*Bab 1, bonus Agen SQL.* Perintah kerja perawatan. Catatan lapangan WO biasanya teks bebas penuh singkatan, sehingga perlu diekstrak menjadi data terstruktur.
