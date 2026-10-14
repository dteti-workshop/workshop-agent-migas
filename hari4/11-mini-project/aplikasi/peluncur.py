"""Menjalankan aplikasi Streamlit bab ini dari sel notebook, di Google Colab maupun di VS Code.

Ada tiga aplikasi:

  penjelajah   : mengenal tool dan membangun prompt           (port 8501, proses terpisah)
  agen         : mengobrol dengan agen yang Anda rakit        (port 8502, di dalam proses notebook)
  uji          : panduan uji berisi pertanyaan dan kriteria   (port 8503, proses terpisah)

Aplikasi `agen` sengaja berjalan di proses yang sama dengan notebook. Agen yang Anda buat di sel (sebuah objek Python,
lengkap dengan tool dan checkpointer-nya) langsung terlihat oleh aplikasi lewat `kerangka.daftarkan_agen(...)`, tanpa
disimpan ke file. Dua aplikasi lain tidak membutuhkan objek dari notebook, jadi berjalan sebagai proses biasa.

Pemakaian di sel notebook:

    import peluncur
    peluncur.buka("penjelajah")     # menjalankan (atau menampilkan ulang tautan bila sudah berjalan)
    peluncur.hentikan()             # menghentikan semuanya
"""
import atexit
import os
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
ROOT = FOLDER.parents[2]  # root repositori: hari4/11-mini-project/aplikasi -> root

APLIKASI = {
    "penjelajah": {"skrip": "penjelajah.py", "port": 8501, "judul": "Penjelajah tool dan prompt"},
    "agen": {"skrip": "app.py", "port": 8502, "judul": "Aplikasi agen"},
    "uji": {"skrip": "panduan_uji.py", "port": 8503, "judul": "Panduan uji"},
}

_proses: dict[str, subprocess.Popen] = {}
_thread: threading.Thread | None = None
_server = None  # objek Server Streamlit milik aplikasi `agen`, disimpan agar bisa dihentikan


def _sehat(port: int) -> bool:
    try:
        urllib.request.urlopen(f"http://localhost:{port}/_stcore/health", timeout=1)
        return True
    except OSError:
        return False


def _di_colab() -> bool:
    """True di Google Colab. Modul google.colab biasanya sudah dimuat kernel; bila belum, variabel lingkungan Colab menjadi petunjuk."""
    if "google.colab" in sys.modules:
        return True
    if "COLAB_RELEASE_TAG" in os.environ:
        try:
            import google.colab  # noqa: F401
            return True
        except ImportError:
            return False
    return False


def _tampilkan_colab(info: dict) -> None:
    """Tautan ke tab baru, ditambah aplikasinya di dalam sel (iframe).

    `serve_kernel_port_as_window` ditandai Colab "may stop working", jadi dipakai hanya sebagai cadangan. Tautan dibuat dari
    alamat proxy port yang sama yang dipakai Colab untuk iframe.
    """
    from google.colab import output
    from IPython.display import HTML, display

    port, judul = info["port"], info["judul"].lower()
    try:
        alamat = output.eval_js(f"google.colab.kernel.proxyPort({port})")
    except Exception:  # noqa: BLE001 - tanpa tautan, iframe di bawah tetap bisa dipakai
        alamat = None
    if alamat:
        display(HTML(f'<a href="{alamat}" target="_blank">Buka {judul} pada tab baru</a>'))
    if hasattr(output, "serve_kernel_port_as_iframe"):
        output.serve_kernel_port_as_iframe(port, height="700")
    else:
        output.serve_kernel_port_as_window(port, anchor_text=f"Buka {judul} pada tab baru")


def _tampilkan(nama: str) -> None:
    info = APLIKASI[nama]
    if _di_colab():
        _tampilkan_colab(info)
        return
    alamat = f"http://localhost:{info['port']}"
    print(f"{info['judul']} berjalan di {alamat}")
    try:  # tautan yang bisa diklik hanya di kernel Jupyter sungguhan; di tempat lain cukup teks di atas
        from IPython import get_ipython
        from IPython.display import HTML, display

        if get_ipython().__class__.__name__ == "ZMQInteractiveShell":
            display(HTML(f'<a href="{alamat}" target="_blank">Buka {info["judul"].lower()} pada tab baru</a>'))
    except (ImportError, AttributeError):
        pass


def _tunggu(nama: str, hidup, log: Path | None) -> None:
    port = APLIKASI[nama]["port"]
    for _ in range(90):  # sampai sekitar 90 detik; impor LangChain pada proses pertama bisa lambat
        if _sehat(port):
            return
        if not hidup():
            break
        time.sleep(1)
    isi = log.read_text(encoding="utf-8", errors="replace")[-2000:] if log and log.exists() else ""
    raise RuntimeError(f"Aplikasi '{nama}' gagal dijalankan. Pesan terakhir:\n{isi}")


def _buka_proses(nama: str) -> None:
    info = APLIKASI[nama]
    proses = _proses.get(nama)
    if proses is not None and proses.poll() is None and _sehat(info["port"]):
        return  # sudah berjalan
    if proses is not None and proses.poll() is None:
        proses.terminate()
    (ROOT / "outputs").mkdir(exist_ok=True)
    log = ROOT / "outputs" / f"streamlit_{nama}.log"
    env = {**os.environ, "PYTHONUTF8": "1"}
    _proses[nama] = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", str(FOLDER / info["skrip"]), "--server.port", str(info["port"]),
         "--server.headless", "true", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false",
         "--browser.gatherUsageStats", "false", "--logger.hideWelcomeMessage", "true"],
        cwd=ROOT, env=env, stdout=open(log, "w", encoding="utf-8"), stderr=subprocess.STDOUT)
    _tunggu(nama, lambda: _proses[nama].poll() is None, log)


def _buka_di_kernel(nama: str) -> None:
    """Jalankan server Streamlit di thread proses ini (bukan subprocess)."""
    global _thread, _server
    info = APLIKASI[nama]
    if _thread is not None and _thread.is_alive() and _sehat(info["port"]):
        return
    from streamlit.web import bootstrap

    if str(FOLDER) not in sys.path:
        sys.path.insert(0, str(FOLDER))  # skrip aplikasi memakai kerangka yang sama dengan notebook
    opsi = {"server.port": info["port"], "server.headless": True, "server.fileWatcherType": "none",
            "server.enableCORS": False, "server.enableXsrfProtection": False,
            "browser.gatherUsageStats": False, "logger.hideWelcomeMessage": True, "logger.level": "error"}
    bootstrap.load_config_options(opsi)

    # `signal.signal` hanya boleh dipanggil dari thread utama, sedangkan server berjalan di thread latar.
    # Kernel Jupyter juga tidak boleh kehilangan penangan SIGINT miliknya.
    bootstrap._set_up_signal_handler = lambda server: None
    server_asli = getattr(bootstrap, "_Server_asli", bootstrap.Server)
    bootstrap._Server_asli = server_asli

    def _simpan_server(*args, **kwargs):
        global _server
        _server = server_asli(*args, **kwargs)
        return _server

    bootstrap.Server = _simpan_server
    _thread = threading.Thread(
        target=bootstrap.run, args=(str(FOLDER / info["skrip"]), False, [], opsi), name="streamlit-agen", daemon=True)
    _thread.start()
    _tunggu(nama, _thread.is_alive, None)


def buka(nama: str) -> None:
    """Jalankan aplikasi `nama` ('penjelajah', 'agen', atau 'uji') dan tampilkan tautan untuk membukanya."""
    if nama not in APLIKASI:
        raise ValueError(f"nama harus salah satu dari {list(APLIKASI)}, bukan {nama!r}")
    if nama == "agen":
        _buka_di_kernel(nama)
    else:
        _buka_proses(nama)
    _tampilkan(nama)


def hentikan() -> None:
    """Hentikan semua aplikasi yang dijalankan dari notebook ini."""
    global _server
    for nama, proses in list(_proses.items()):
        if proses.poll() is None:
            proses.terminate()
            try:
                proses.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proses.kill()
            print(f"Aplikasi '{nama}' dihentikan.")
    _proses.clear()
    if _server is not None and _thread is not None and _thread.is_alive():
        try:
            _server.stop()
            _thread.join(timeout=10)
            print("Aplikasi 'agen' dihentikan.")
        except Exception as e:  # noqa: BLE001 - menghentikan hanyalah kenyamanan; runtime yang ditutup juga mematikannya
            print(f"Aplikasi 'agen' tidak bisa dihentikan dengan rapi ({type(e).__name__}); akan berhenti saat notebook ditutup.")
    _server = None


atexit.register(lambda: [p.terminate() for p in _proses.values() if p.poll() is None])
