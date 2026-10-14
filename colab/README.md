# Notebook Google Colab: Hari 3 dan 4

Notebook di folder ini menjalankan seluruh materi hari 3 dan 4 di Google Colab, tanpa VS Code dan tanpa instalasi di laptop. Isinya sama dengan notebook di `hari3/` dan `hari4/`; yang berbeda hanya cell Persiapan di bagian atas (menyalin repository, memasang pustaka, mengisi API key). Notebook hari 2 ada di `hari2_membangun_rag.ipynb`.

## Cara Memakai

1. Klik tombol **Open in Colab** pada tabel di bawah, lalu pilih **File > Save a copy in Drive**.
2. Mulai dari bab 00 (Persiapan). Jalankan tiga cell Persiapan, lalu cell pemeriksaan.
3. Setiap notebook bab, latihan, dan solusi memakai tiga cell Persiapan yang sama. Jalankan ketiganya di awal setiap notebook baru, karena setiap notebook berjalan di runtime Colab sendiri.
4. Agar API key tidak diketik berulang, simpan di **Colab Secrets** (ikon kunci di panel kiri) dengan nama `ONLINE_API_KEY` dan `PARTICIPANT_ID`, lalu aktifkan **Notebook access**.

Dependency dipasang dari [requirements-colab.txt](./requirements-colab.txt): sama dengan `requirements.txt` di root repo, tanpa `ipykernel` (sudah ada di Colab) dan `langgraph-cli` (hanya untuk LangGraph Studio). Paket repo (`common`, `migas_shared`) dipasang terpisah dengan `pip install -e .` oleh cell Persiapan 1.

## Yang Tidak Berjalan di Colab

- Model lokal (Ollama): hari 3 dan 4 memakai profil online.
- LangGraph Studio (`langgraph dev`, bab 11, opsional): server hanya terbuka di laptop sendiri.
- Aplikasi Streamlit bab 11 berjalan, tetapi dibuka lewat tautan dari cell di notebook, bukan `localhost:8501`.

## Hari 3

| Bab | Notebook | Latihan (semua latihan bab) |
|---|---|---|
| Persiapan Hari 3 dan 4 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/00-persiapan.ipynb) | - |
| Dasar LangChain: Model, Pesan, Prompt, dan Structured Output | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/01-dasar-langchain.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/01-dasar-langchain-latihan.ipynb) |
| Function Calling dan Tools | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/02-tools-function-calling.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/02-tools-function-calling-latihan.ipynb) |
| Memulai dengan Agen | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/03-agen.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/03-agen-latihan.ipynb) |
| Structured Output pada Agen | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/04-keluaran-terstruktur-agen.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/04-keluaran-terstruktur-agen-latihan.ipynb) |
| Memori Agen dan Checkpointer | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/05-memori-agen.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/05-memori-agen-latihan.ipynb) |
| Persetujuan Manusia (Human-in-the-Loop) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/06-persetujuan-manusia.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/06-persetujuan-manusia-latihan.ipynb) |
| Guardrails dan Middleware Keamanan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/07-guardrails-middleware.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/07-guardrails-middleware-latihan.ipynb) |
| Streaming Agen | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/bonus-streaming-agen.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari3/bonus-streaming-agen-latihan.ipynb) |

## Hari 4

| Bab | Notebook | Latihan (semua latihan bab) |
|---|---|---|
| Sistem Multi-Agen | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari4/08-sistem-multi-agen.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari4/08-sistem-multi-agen-latihan.ipynb) |
| Model Context Protocol (MCP) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari4/09-mcp.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari4/09-mcp-latihan.ipynb) |
| RAG Agentik | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari4/10-agentic-rag.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari4/10-agentic-rag-latihan.ipynb) |
| Mini Project: Menyusun Agen dari Tiga Komponen | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari4/11-mini-project.ipynb) | - |
| Membangun Agen SQL | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari4/bonus-agen-sql.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dteti-workshop/workshop-agent-migas/blob/main/colab/hari4/bonus-agen-sql-latihan.ipynb) |
