# Workshop Implementasi Agentic AI untuk Oil & Gas Industry

Kode hands-on untuk topik LLM & Prompt Engineering (`hari1/`), RAG & Enterprise Knowledge Management (`hari2/`), dan Agentic AI dengan LangChain dan LangGraph (`hari3/` dan `hari4/`).
Pusat Kajian LKFT, Fakultas Teknik, Universitas Gadjah Mada.

> Semua data di repo ini **fiktif** (lapangan "Blok Sungai Jernih", perusahaan "PT Hulu Energi Nusantara").
> SOP dan manual dibuat untuk keperluan pelatihan dan **bukan** prosedur resmi perusahaan mana pun.

## Panduan penggunaan

```bash
git clone https://github.com/dteti-workshop/workshop-agent-migas.git
cd workshop-agent-migas
python -m venv .venv
# Windows: .venv\Scripts\activate      macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env      # macOS/Linux: cp .env.example .env  -> lalu isi API key
python setup_check.py
```

Satu repo, satu virtual environment, dan satu file `.env` dipakai dari hari 1 sampai hari 4. Kalau Anda sudah clone repo ini di hari 1, cukup `git pull` lalu `pip install -r requirements.txt` untuk menambah paket LangChain dan LangGraph.

Panduan lengkap setiap unit, termasuk instalasi dan daftar error yang mungkin muncul, terdapat pada labsheet yang dibagikan instruktur (hari 1 dan 2) dan pada PDF di folder tiap bab (hari 3 dan 4).

## Struktur

```
common/            helper hari 1-2: config (.env), llm.py (chat, retry, cache, biaya), embeddings.py
migas_shared/      paket bersama hari 3-4: LLM lewat LangChain, embedding, pipeline RAG, tool lapangan dan tool dokumen
data/
  raw/             work_orders.csv (400 WO teks bebas), hse_incidents.csv (120 narasi), daily_reports/
  docs/            korpus RAG: sop/, manual/ (PDF), laporan/, investigasi/ (rahasia), glosarium/
  docs_bab11/      18 dokumen tambahan khusus bab 11 (sop/, manual/, laporan/, investigasi/); indeks terpisah dari data/docs
  eval/            ground truth & golden set (untuk mengukur akurasi)
  field/           data sumur untuk bab 11: sumur.csv (196 sumur, status per 31 Juli 2026), produksi_sumur_2026-07.csv (produksi harian semua sumur)
  contoh_upload/   file contoh untuk latihan upload (SOP baru, revisi SOP, laporan shift)
hari1/             satu file per unit (unit2 sampai unit7), app_asisten_wo.py (Unit 8: chat + upload file)
hari2/             rag_pipeline.py (pustaka RAG), satu file per unit (unit1 sampai unit6), app_doc_qa.py (Unit 7: chat + lampiran session + upload knowledge)
hari3/             bab 00 sampai 07 (LangChain: model, tool, agen, memori, persetujuan manusia, guardrail) dan bab bonus streaming agen
hari4/             bab 08 sampai 11 (multi-agen, MCP, RAG agentik, mini project) dan bab bonus agen SQL
scripts/           reset_knowledge.py (mengembalikan knowledge base ke kondisi awal)
setup_check.py     cek kesiapan laptop untuk hari 1 sampai 4
GLOSARIUM.md       istilah hari 3 dan 4
```

## Cara mengerjakan unit

- Buka file `hari1/unit*.py` atau `hari2/unit*.py` di VS Code (urutan unit mengikuti labsheet; Unit 1 pada `hari1/` adalah instalasi dan setup). Setiap blok `# %%` adalah satu sel. Klik **Run Cell** atau tekan
  `Shift+Enter` (butuh ekstensi Python + Jupyter).
- Cari komentar `# TODO(Ux.y)` dan lengkapi kodenya sesuai labsheet.
- Pada `hari2/`, file `rag_pipeline.py` adalah pustaka yang sudah lengkap. Bagian TODO berada pada file setiap unit.
- Aplikasi Streamlit dijalankan dari **root repo**:
  `streamlit run hari1/app_asisten_wo.py` dan `streamlit run hari2/app_doc_qa.py`.

## Hari 3 dan 4: LangChain dan LangGraph

Hari 3 dan 4 tidak mengulang konsep model bahasa dan RAG dari hari 1 dan 2. Fokusnya hal baru: tool, agen, memori, persetujuan manusia, guardrail, multi-agen, MCP, RAG agentik, dan mini project. Dua bab bonus (Streaming Agen di hari 3 dan Agen SQL di hari 4) bersifat opsional: tidak dibutuhkan bab lain dan dikerjakan bila waktu tersisa. Mulai dari [hari3/00-persiapan](./hari3/00-persiapan/README.md).

**Memakai Google Colab (tanpa VS Code).** Semua bab, latihan, dan solusi hari 3 dan 4 juga tersedia sebagai notebook Colab, tanpa instalasi apa pun di laptop. Mulai dari [Persiapan di Colab](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/00-persiapan.ipynb), lalu pilih bab pada tabel di [colab/README.md](./colab/README.md).

| Hari | Bab | Judul |
|---|---|---|
| 3 | 00 | [Persiapan Hari 3 dan 4](./hari3/00-persiapan/README.md) |
| 3 | 01 | [Dasar LangChain](./hari3/01-dasar-langchain/README.md) |
| 3 | 02 | [Function Calling dan Tools](./hari3/02-tools-function-calling/README.md) |
| 3 | 03 | [Memulai dengan Agen](./hari3/03-agen/README.md) |
| 3 | 04 | [Structured Output pada Agen](./hari3/04-keluaran-terstruktur-agen/README.md) |
| 3 | 05 | [Memori Agen dan Checkpointer](./hari3/05-memori-agen/README.md) |
| 3 | 06 | [Persetujuan Manusia](./hari3/06-persetujuan-manusia/README.md) |
| 3 | 07 | [Guardrails dan Middleware Keamanan](./hari3/07-guardrails-middleware/README.md) |
| 4 | 08 | [Sistem Multi-Agen](./hari4/08-sistem-multi-agen/README.md) |
| 4 | 09 | [Model Context Protocol (MCP)](./hari4/09-mcp/README.md) |
| 4 | 10 | [RAG Agentik](./hari4/10-agentic-rag/README.md) |
| 4 | 11 | [Mini Project](./hari4/11-mini-project/README.md) |

Bab bonus (opsional; tidak dibutuhkan bab lain, kerjakan bila waktu tersisa):

| Hari | Bab bonus | Judul |
|---|---|---|
| 3 | bonus-streaming-agen | [Streaming Agen](./hari3/bonus-streaming-agen/README.md) |
| 4 | bonus-agen-sql | [Agen SQL](./hari4/bonus-agen-sql/README.md) |

Isi satu folder bab:

```
README.md        teks bab dan keluaran
NN-nama-bab.ipynb  notebook dengan sel yang sama seperti README
NN-nama-bab.pdf  panduan bergaya labsheet, ditambah bagian Latihan berisi kode jawaban
code/            skrip contoh bernomor, ditulis sebagai sel (# %%)
latihan_N.py     starter latihan (N = 1, 2, ...): bagian inti kosong dengan komentar TODO(Bx.y)
latihan_N.ipynb  starter yang sama dalam bentuk notebook
latihan.md       petunjuk singkat latihan
```

Cara mengerjakan latihan hari 3 dan 4 sama seperti hari 1 dan 2: isi baris `... = None  # TODO` pada `latihan_1.py` (dan seterusnya) dengan kode dari bagian **Kode Jawaban Latihan** di PDF bab. Bab 11 adalah mini project berkelompok: TODO-nya (`TODO(M.1)` sampai `TODO(M.3)`) ada di sel notebook bab itu, dan kuncinya di PDF bab 11. Skrip contoh dijalankan dari **root repo**, misalnya `python hari3/03-agen/code/01_basic_agent.py`.

## Aturan pemakaian API key bersama

- Satu API key dipakai seluruh peserta. Isi `PARTICIPANT_ID` di `.env` agar pemakaian bisa dipantau.
- Jangan menaikkan `LLM_MAX_CONCURRENCY` (default 4).
- Panggilan dengan `temperature=0` di hari 1 dan 2 otomatis di-cache di `.cache/`, jadi menjalankan ulang sel tidak menambah biaya. Hari 3 dan 4 tidak memakai cache itu.
- Jangan commit file `.env`, jangan tempel API key di chat/forum.

## Profil model online vs lokal

`LLM_PROFILE=online` memakai OpenRouter (default DeepSeek V4 Flash). Mode reasoning diatur lewat `LLM_REASONING_EFFORT` (default `none`) atau parameter `chat(..., reasoning="high")`. `LLM_PROFILE=local` memakai server lokal yang
kompatibel dengan API OpenAI (Ollama/vLLM). Hari 1 dan 2 memakai antarmuka yang sama untuk keduanya, jadi cukup mengganti `.env`.

Hari 3 dan 4 hanya membaca `ONLINE_API_KEY`, `ONLINE_BASE_URL`, dan `ONLINE_MODEL`. Untuk memakai server lokal di hari 3 dan 4, isi ketiga variabel itu dengan nilai server lokal.

## Catatan

- Folder `hari1/` dan `hari2/` berisi kode awal (starter) dengan bagian TODO yang dilengkapi peserta. Folder `hari3/` dan `hari4/` berisi bab beserta starter latihan (bab 01 sampai 10).
- Kembalikan knowledge base ke kondisi awal setelah latihan upload: `python scripts/reset_knowledge.py`. Index Chroma (`chroma_db/`) dipakai bersama oleh hari 2, 3, dan 4.
- Versi yang diuji (Okt 2026, Python 3.11 dan 3.12): openai 3.29, langchain 1.4, langgraph 1.2, langchain-core 1.6, langchain-openai 1.6, langchain-chroma 1.1,
  chromadb 1.5, fastembed 0.9, streamlit 1.65, pandas 3.0, pydantic 2.14.

## Atribusi dan lisensi

Struktur bab, penjelasan, dan kode dasar hari 3 dan 4 diadaptasi dari kursus *LangChain for Beginners* milik Microsoft (lisensi MIT; lihat [hari3/LICENSE](./hari3/LICENSE) dan [hari4/LICENSE](./hari4/LICENSE)), lalu disesuaikan ke bahasa Indonesia, konteks migas, dan data fiktif workshop. Pada kursus asal, diagram bergaya Mermaid diganti ilustrasi buatan kode.
