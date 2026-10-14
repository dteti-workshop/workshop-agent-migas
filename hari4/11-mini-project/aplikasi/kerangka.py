"""Kerangka bersama aplikasi mini project. Peserta tidak perlu mengubah file ini.

Isinya hal-hal yang sama untuk agen apa pun:

  daftar_agen(), muat_definisi(nama)  : menemukan dan memuat file di folder agen/ (dan agen contoh di solusi/agen_contoh/)
  bangun_agen(nama, checkpointer)     : membuat model dan agen dari file tersebut
  daftarkan_agen(agen, judul, ...)    : mendaftarkan agen yang dirakit di sel notebook, agar tampil di aplikasi agen
  jalankan(...)                       : menjalankan agen sebagai aliran Peristiwa (teks, panggilan tool, hasil tool)
  persetujuan_menunggu(...)           : membaca dari state apakah agen sedang menunggu keputusan manusia
  pesan_untuk_tampilan(...)           : mengubah riwayat pesan menjadi bagian-bagian yang siap digambar
  tanya(...)                          : satu pertanyaan sampai selesai, termasuk 'reviewer' otomatis (untuk uji)
  jalankan_kasus(...)                 : satu kasus uji dari KASUS_UJI, diperiksa di kode

Dipakai oleh app.py (Streamlit) dan code/ (contoh bab 11).
"""
import importlib
import importlib.util
import os
import sys
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from pathlib import Path

from langchain_core.messages import AIMessage, AIMessageChunk, HumanMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

FOLDER = Path(__file__).resolve().parent
FOLDER_SOLUSI = FOLDER.parent / "solusi" / "agen_contoh"  # kunci jawaban: empat agen contoh yang sudah jadi
if str(FOLDER) not in sys.path:
    sys.path.insert(0, str(FOLDER))  # agar `from alat_data import ...` di file agen/ selalu bisa dipakai

WAJIB = ("JUDUL", "PENGANTAR", "CONTOH_PERTANYAAN", "buat_agen")


class ErrorAgen(Exception):
    """File agen tidak lengkap atau tidak bisa dimuat. Pesannya ditulis agar bisa langsung diperbaiki."""


@dataclass
class Peristiwa:
    """Satu kejadian saat agen berjalan. jenis: 'teks', 'tool', atau 'hasil_tool'."""

    jenis: str
    teks: str = ""
    nama: str = ""
    args: dict = field(default_factory=dict)


@dataclass
class Penyimpanan:
    """Memori aplikasi: checkpointer percakapan dan daftar percakapan untuk sidebar. Hidup selama proses berjalan."""

    saver: InMemorySaver = field(default_factory=InMemorySaver)
    percakapan: dict[str, dict] = field(default_factory=dict)  # thread_id -> {"judul": ..., "agen": ...}


@dataclass
class AgenTerdaftar:
    """Agen yang dirakit peserta di sel notebook (bukan dari file di folder agen/)."""

    nama: str
    judul: str
    pengantar: str
    contoh_pertanyaan: list[str]
    agen: object


# Registri milik proses. Aplikasi agen berjalan di proses yang sama dengan notebook, jadi agen yang didaftarkan
# di sebuah sel langsung terlihat oleh aplikasi tanpa file perantara.
AGEN_TERDAFTAR: dict[str, AgenTerdaftar] = {}


def daftarkan_agen(agen, judul: str = "Agen Saya", pengantar: str = "", contoh_pertanyaan: list[str] | None = None) -> str:
    """Daftarkan agen agar muncul di aplikasi agen. Mengembalikan namanya, mis. 'Agen Saya #2'.

    Setiap pendaftaran membuat versi baru. Versi lama tetap ada (beserta riwayat percakapannya, yang disimpan
    di checkpointer agen itu sendiri), sehingga Anda bisa membandingkan versi lama dan baru.
    """
    if not hasattr(agen, "get_state"):
        raise TypeError("daftarkan_agen() menerima agen hasil create_agent(...). Isi dulu sel TODO yang membuat `agen`.")
    if getattr(agen, "checkpointer", None) in (None, False):
        raise ValueError("Agen belum punya checkpointer, jadi percakapan tidak bisa disimpan. Isi TODO checkpointer.")
    nomor = sum(1 for a in AGEN_TERDAFTAR.values() if a.judul == judul) + 1
    nama = f"{judul} #{nomor}"
    AGEN_TERDAFTAR[nama] = AgenTerdaftar(nama, judul, pengantar or "Agen yang Anda rakit sendiri.", list(contoh_pertanyaan or []), agen)
    return nama


# ---------------------------------------------------------------------------
# Memuat agen
# ---------------------------------------------------------------------------


def _nama_di(folder: Path) -> set[str]:
    return {p.stem for p in folder.glob("*.py") if not p.name.startswith("_")}


def daftar_agen(dengan_solusi: bool | None = None) -> list[str]:
    """Nama agen untuk dropdown (tanpa .py): semua file di agen/. 'saya' selalu pertama.

    Agen contoh di solusi/agen_contoh/ (kunci jawaban) ikut bila dengan_solusi=True, atau bila variabel lingkungan
    TAMPILKAN_SOLUSI=1 (untuk fasilitator: `TAMPILKAN_SOLUSI=1 streamlit run ...`).
    """
    if dengan_solusi is None:
        dengan_solusi = os.environ.get("TAMPILKAN_SOLUSI") == "1"
    nama = _nama_di(FOLDER / "agen") | (_nama_di(FOLDER_SOLUSI) if dengan_solusi else set())
    return sorted(nama, key=lambda n: (n != "saya", n))


def _impor_modul(nama: str):
    """agen/<nama>.py bila ada; kalau tidak, solusi/agen_contoh/<nama>.py. Selalu dibaca ulang dari disk."""
    if (FOLDER / "agen" / f"{nama}.py").exists():
        return importlib.reload(importlib.import_module(f"agen.{nama}"))
    file = FOLDER_SOLUSI / f"{nama}.py"
    if not file.exists():
        raise FileNotFoundError(f"tidak ada agen/{nama}.py")
    spek = importlib.util.spec_from_file_location(f"agen_contoh_{nama}", file)
    modul = importlib.util.module_from_spec(spek)
    spek.loader.exec_module(modul)
    return modul


def muat_definisi(nama: str):
    """Impor file agen <nama> (diimpor ulang agar perubahan Anda terbaca) dan periksa isinya."""
    try:
        modul = _impor_modul(nama)
    except Exception as e:  # noqa: BLE001 - tampilkan apa pun yang salah sebagai pesan yang jelas
        raise ErrorAgen(f"agen/{nama}.py gagal dimuat: {type(e).__name__}: {e}") from e
    kurang = [n for n in WAJIB if not hasattr(modul, n)]
    if kurang:
        raise ErrorAgen(f"agen/{nama}.py belum mendefinisikan: {', '.join(kurang)}")
    return modul


def bangun_agen(nama: str, checkpointer):
    """Kembalikan (modul, agen). Model dibaca dari file .env lewat migas_shared."""
    from migas_shared.llm import get_chat_model

    modul = muat_definisi(nama)
    try:
        return modul, modul.buat_agen(get_chat_model(), checkpointer)
    except Exception as e:  # noqa: BLE001
        raise ErrorAgen(f"buat_agen() di agen/{nama}.py gagal: {type(e).__name__}: {e}") from e


# ---------------------------------------------------------------------------
# Menjalankan agen
# ---------------------------------------------------------------------------


def teks_dari(isi) -> str:
    """Isi pesan bisa berupa string atau daftar blok (model penalar). Ambil teksnya saja."""
    if isinstance(isi, str):
        return isi
    return "".join(b.get("text", "") for b in isi if isinstance(b, dict) and b.get("type") == "text")


def _config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}


def jalankan(agen, masukan, thread_id: str) -> Iterator[Peristiwa]:
    """Jalankan agen dan keluarkan Peristiwa saat terjadi.

    masukan : {"messages": [...]} untuk giliran baru, atau Command(resume=...) untuk melanjutkan setelah interrupt.
    Setelah iterator habis, panggil persetujuan_menunggu() untuk tahu apakah agen berhenti menunggu manusia.
    """
    for mode, data in agen.stream(masukan, _config(thread_id), stream_mode=["messages", "updates"]):
        if mode == "messages":
            chunk, meta = data
            if isinstance(chunk, AIMessageChunk) and meta.get("langgraph_node") == "model" and chunk.text:
                yield Peristiwa("teks", chunk.text)
            continue
        for node, pembaruan in data.items():
            if not isinstance(pembaruan, dict):
                continue  # '__interrupt__': ditangani lewat state, bukan dari sini
            for pesan in pembaruan.get("messages", []):
                if isinstance(pesan, AIMessage) and node == "model":
                    for p in pesan.tool_calls:
                        yield Peristiwa("tool", nama=p["name"], args=p["args"])
                elif isinstance(pesan, ToolMessage):
                    yield Peristiwa("hasil_tool", teks=teks_dari(pesan.content), nama=pesan.name or "")


def persetujuan_menunggu(agen, thread_id: str) -> dict | None:
    """Permintaan persetujuan yang sedang menunggu, atau None.

    Bentuknya {"action_requests": [...], "review_configs": [...], "id": ...}; id berbeda untuk setiap interrupt.
    """
    state = agen.get_state(_config(thread_id))
    return {**state.interrupts[0].value, "id": state.interrupts[0].id} if state.interrupts else None


def lanjutkan(keputusan: list[dict]) -> Command:
    """Bungkus daftar keputusan (satu per permintaan, urutan sama) menjadi perintah untuk jalankan()."""
    return Command(resume={"decisions": keputusan})


def keputusan_setuju(permintaan: dict, boleh: list[str]) -> dict:
    return {"type": "approve"}


def keputusan_tolak(permintaan: dict, boleh: list[str]) -> dict:
    return {"type": "reject", "message": "Ditolak oleh reviewer"}


@dataclass
class Hasil:
    jawaban: str
    tool: list[str] = field(default_factory=list)          # nama tool yang dipanggil, berurutan
    keputusan: list[tuple[str, str]] = field(default_factory=list)  # (nama tool, jenis keputusan)


def tanya(agen, pertanyaan: str, thread_id: str,
          reviewer: Callable[[dict, list[str]], dict] = keputusan_tolak) -> Hasil:
    """Satu pertanyaan sampai agen selesai. Setiap permintaan persetujuan dijawab oleh `reviewer`.

    Dipakai untuk menguji agen dari terminal tanpa antarmuka. Di aplikasi, reviewer-nya adalah Anda.
    """
    hasil = Hasil(jawaban="")
    masukan = {"messages": [HumanMessage(content=pertanyaan)]}
    while True:
        for p in jalankan(agen, masukan, thread_id):
            if p.jenis == "tool":
                hasil.tool.append(p.nama)
        menunggu = persetujuan_menunggu(agen, thread_id)
        if menunggu is None:
            hasil.jawaban = teks_dari(agen.get_state(_config(thread_id)).values["messages"][-1].content)
            return hasil
        keputusan = []
        for permintaan, tinjau in zip(menunggu["action_requests"], menunggu["review_configs"]):
            k = reviewer(permintaan, tinjau["allowed_decisions"])
            hasil.keputusan.append((permintaan["name"], k["type"]))
            keputusan.append(k)
        masukan = lanjutkan(keputusan)


REVIEWER = {"setuju": keputusan_setuju, "tolak": keputusan_tolak}


def jalankan_kasus(agen, kasus: dict, thread_id: str) -> list[str]:
    """Jalankan satu kasus uji dari KASUS_UJI sebuah agen contoh dan kembalikan daftar kegagalan; kosong berarti lolos.

    Dipakai fasilitator untuk memeriksa agen contoh. Peserta menilai agennya sendiri lewat panduan uji.
    """
    import alat_data

    sebelum = len(alat_data.CATATAN_TINDAKAN)
    hasil = tanya(agen, kasus["tanya"], thread_id, REVIEWER[kasus.get("keputusan", "tolak")])
    gagal = []
    for t in kasus.get("harus_tool", []):
        if t not in hasil.tool:
            gagal.append(f"tool {t} tidak dipanggil (dipanggil: {hasil.tool or 'tidak ada'})")
    for t in kasus.get("tanpa_tool", []):
        if t in hasil.tool:
            gagal.append(f"tool {t} dipanggil padahal tidak boleh")
    for kata in kasus.get("harus_ada", []):
        if kata.lower() not in hasil.jawaban.lower():
            gagal.append(f"jawaban tidak memuat '{kata}'")
    if "tercatat" in kasus:
        bertambah = len(alat_data.CATATAN_TINDAKAN) - sebelum
        if bertambah != kasus["tercatat"]:
            gagal.append(f"catatan tindakan bertambah {bertambah}, seharusnya {kasus['tercatat']}")
    return gagal


# ---------------------------------------------------------------------------
# Untuk tampilan
# ---------------------------------------------------------------------------


def pesan_untuk_tampilan(agen, thread_id: str) -> list[dict]:
    """Ubah riwayat pesan di state menjadi daftar giliran siap gambar.

    Setiap giliran: {"peran": "user", "teks": ...} atau {"peran": "assistant", "bagian": [...]}, dengan bagian berupa
    ("teks", isi) atau ("tool", nama, args, hasil). Pesan asisten yang berurutan digabung menjadi satu giliran.
    """
    state = agen.get_state(_config(thread_id))
    pesan = state.values.get("messages", []) if state.values else []
    giliran: list[dict] = []
    posisi_tool: dict[str, tuple[int, int]] = {}  # tool_call_id -> (indeks giliran, indeks bagian)
    for m in pesan:
        if isinstance(m, HumanMessage):
            giliran.append({"peran": "user", "teks": teks_dari(m.content)})
        elif isinstance(m, AIMessage):
            if not giliran or giliran[-1]["peran"] != "assistant":
                giliran.append({"peran": "assistant", "bagian": []})
            teks = teks_dari(m.content)
            if teks.strip():
                giliran[-1]["bagian"].append(("teks", teks))
            for p in m.tool_calls:
                giliran[-1]["bagian"].append(("tool", p["name"], p["args"], None))
                posisi_tool[p["id"]] = (len(giliran) - 1, len(giliran[-1]["bagian"]) - 1)
        elif isinstance(m, ToolMessage) and m.tool_call_id in posisi_tool:
            g, b = posisi_tool[m.tool_call_id]
            _, nama, args, _ = giliran[g]["bagian"][b]
            giliran[g]["bagian"][b] = ("tool", nama, args, teks_dari(m.content))
    return giliran


def nama_tool_agen(agen) -> list[str]:
    """Nama tool yang terpasang pada agen hasil create_agent (kosong bila tidak ada atau tidak terbaca)."""
    try:
        return list(agen.nodes["tools"].bound.tools_by_name)
    except (AttributeError, KeyError):
        return []


def judul_dari(teks: str, maks: int = 36) -> str:
    teks = " ".join(teks.split())
    return teks if len(teks) <= maks else teks[: maks - 3].rstrip() + "..."
