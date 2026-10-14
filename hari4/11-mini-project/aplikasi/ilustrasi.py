"""Ilustrasi tool untuk penjelajah: satu gambar SVG per tool, digambar oleh kode (tanpa file gambar).

  ilustrasi(nama_tool) -> str   teks SVG, siap untuk st.image(...) atau st.markdown(..., unsafe_allow_html=True)

Warna latar menunjukkan kelompok tool: Operasi (biru), Perawatan (kuning), HSE (merah muda), Engineering (ungu), dan
dokumen (hijau). Setiap tool punya gambar sendiri, dan gambarnya menggambarkan apa yang disentuh tool itu: pompa untuk
status sumur, kalkulator untuk water cut, tabel CSV untuk riwayat work order, dan seterusnya.
"""
NAVY = "#073C5F"
PUTIH = "#FFFFFF"
BIRU, BIRU_T = "#DAE8FC", "#6C8EBF"
HIJAU, HIJAU_T = "#D5E8D4", "#82B366"
KUNING, KUNING_T = "#FFF2CC", "#D6B656"
ORANYE, ORANYE_T = "#FFE6CC", "#D79B00"
UNGU, UNGU_T = "#E1D5E7", "#9673A6"
MERAH, MERAH_T = "#F8CECC", "#B85450"
ABU, ABU_T = "#F5F5F5", "#666666"

LATAR = {"Operasi": "#EAF2FD", "Perawatan": "#FFF8E1", "HSE": "#FDECEA", "Engineering": "#F3ECF7", "Dokumen": "#EAF5E8"}


# ---------------------------------------------------------------------------
# Elemen dasar
# ---------------------------------------------------------------------------


def _r(x, y, w, h, isi=PUTIH, garis=NAVY, rx=4, tebal=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{isi}" stroke="{garis}" stroke-width="{tebal}"/>'


def _c(x, y, jari, isi=PUTIH, garis=NAVY, tebal=2):
    return f'<circle cx="{x}" cy="{y}" r="{jari}" fill="{isi}" stroke="{garis}" stroke-width="{tebal}"/>'


def _l(x1, y1, x2, y2, garis=NAVY, tebal=2, ujung="round", putus=""):
    d = f' stroke-dasharray="{putus}"' if putus else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{garis}" stroke-width="{tebal}" stroke-linecap="{ujung}"{d}/>'


def _p(d, isi="none", garis=NAVY, tebal=2):
    return f'<path d="{d}" fill="{isi}" stroke="{garis}" stroke-width="{tebal}" stroke-linecap="round" stroke-linejoin="round"/>'


def _t(x, y, teks, ukuran=14, isi=NAVY, anchor="middle", tebal=True):
    w = "bold" if tebal else "normal"
    return (f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{ukuran}" font-weight="{w}" '
            f'fill="{isi}" text-anchor="{anchor}">{teks}</text>')


def _svg(isi: str, kelompok: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="320" height="200">'
            f'<rect width="320" height="200" rx="14" fill="{LATAR[kelompok]}"/>{isi}</svg>')


# ---------------------------------------------------------------------------
# Komponen yang dipakai ulang
# ---------------------------------------------------------------------------


def _kaca_pembesar(x, y, skala=1.0):
    """Lensa berpusat di (x, y); gagang ke kanan bawah."""
    r = 22 * skala
    return (_l(x + r * 0.7, y + r * 0.7, x + r * 1.9, y + r * 1.9, NAVY, 7 * skala) +
            _c(x, y, r, "#FFFFFF99", NAVY, 3))


def _dokumen(x, y, w=90, h=116, isi=PUTIH, garis_isi=BIRU_T, baris=5):
    """Lembar dokumen dengan sudut terlipat dan beberapa baris teks."""
    lipat = 18
    badan = _p(f"M{x} {y} H{x + w - lipat} L{x + w} {y + lipat} V{y + h} H{x} Z", isi, NAVY, 2.5)
    sudut = _p(f"M{x + w - lipat} {y} V{y + lipat} H{x + w}", "none", NAVY, 2)
    garis = "".join(_l(x + 12, y + 32 + i * 14, x + w - 12 - (i % 2) * 14, y + 32 + i * 14, garis_isi, 3) for i in range(baris))
    return badan + sudut + garis


def _kalender(x, y, w=110, h=100, judul="JUL", tandai=(), merah=()):
    isi = _r(x, y, w, h, PUTIH, NAVY, 8, 2.5) + _p(f"M{x} {y + 24} V{y + 8} Q{x} {y} {x + 8} {y} H{x + w - 8} Q{x + w} {y} {x + w} {y + 8} V{y + 24} Z", MERAH, NAVY, 2.5)
    isi += _t(x + w / 2, y + 18, judul, 14, PUTIH)
    for i in range(20):
        kol, bar = i % 5, i // 5
        cx, cy = x + 16 + kol * ((w - 32) / 4), y + 42 + bar * 14
        warna = MERAH_T if i in merah else (ORANYE_T if i in tandai else "#C9D3DD")
        isi += _c(cx, cy, 4.5 if (i in tandai or i in merah) else 3.5, warna, warna, 1)
    return isi


def _tabel(x, y, kolom=4, baris=5, lebar=170, tinggi=110, kepala=BIRU):
    """Tabel bergaya spreadsheet/CSV: baris kepala berwarna dan garis sel."""
    lk, tb = lebar / kolom, tinggi / baris
    isi = _r(x, y, lebar, tinggi, PUTIH, NAVY, 4, 2.5) + f'<rect x="{x}" y="{y}" width="{lebar}" height="{tb}" fill="{kepala}" stroke="{NAVY}" stroke-width="2.5"/>'
    for i in range(1, kolom):
        isi += _l(x + i * lk, y, x + i * lk, y + tinggi, NAVY, 1.2)
    for j in range(1, baris):
        isi += _l(x, y + j * tb, x + lebar, y + j * tb, NAVY, 1.2)
    return isi


def _kunci_pas(x, y, skala=1.0, warna=ORANYE_T):
    """Kunci pas miring ke kanan bawah, kepala di (x, y)."""
    s = skala
    return (f'<g transform="translate({x} {y}) rotate(45) scale({s})">' +
            _r(-6, 0, 12, 56, warna, NAVY, 4, 2) +
            _p("M-14 -6 A18 18 0 1 1 14 -6 L7 -6 V-14 H-7 V-6 Z", warna, NAVY, 2) + '</g>')


def _papan_klip(x, y, w=96, h=124, isi=PUTIH):
    return (_r(x, y, w, h, "#E8C98A", NAVY, 8, 2.5) + _r(x + 8, y + 14, w - 16, h - 22, isi, NAVY, 4, 2) +
            _r(x + w / 2 - 20, y - 6, 40, 18, ABU_T, NAVY, 5, 2))


def _lonceng(x, y, skala=1.0, warna=KUNING_T):
    s = skala
    return (f'<g transform="translate({x} {y}) scale({s})">' +
            _p("M-34 24 Q-30 24 -30 4 Q-30 -30 0 -32 Q30 -30 30 4 Q30 24 34 24 Z", warna, NAVY, 3) +
            _l(-34, 24, 34, 24, NAVY, 3) + _c(0, 32, 7, warna, NAVY, 3) + _c(0, -36, 5, warna, NAVY, 3) + '</g>')


def _segitiga_awas(x, y, ukuran=34, warna=KUNING_T):
    h = ukuran * 0.9
    return (_p(f"M{x} {y - h} L{x + ukuran} {y + h * 0.4} H{x - ukuran} Z", warna, NAVY, 3) +
            _l(x, y - h * 0.45, x, y + h * 0.05, NAVY, 4) + _c(x, y + h * 0.22, 2.5, NAVY, NAVY, 1))


def _centang(x, y, skala=1.0, warna=HIJAU_T, tebal=8):
    return _p(f"M{x - 18 * skala} {y} L{x - 5 * skala} {y + 14 * skala} L{x + 20 * skala} {y - 16 * skala}", "none", warna, tebal * skala)


# ---------------------------------------------------------------------------
# Satu fungsi per tool
# ---------------------------------------------------------------------------


def _laporan_harian():
    isi = _kalender(40, 36, 120, 124, "JUL", tandai=(13,))
    isi += _t(100, 150, "14", 20, ORANYE_T)
    # lembar laporan kecil di kanan
    isi += _dokumen(178, 40, 100, 124, PUTIH, BIRU_T, 4)
    isi += _p("M192 150 Q208 120 222 132 T262 108", "none", HIJAU_T, 4) + _c(262, 108, 4, HIJAU_T, HIJAU_T, 1)
    return _svg(isi, "Operasi")


def _ringkasan_produksi_bulanan():
    isi = _r(36, 30, 248, 140, PUTIH, NAVY, 8, 2.5)
    isi += _l(56, 150, 266, 150, NAVY, 2) + _l(56, 150, 56, 46, NAVY, 2)
    isi += _l(56, 96, 266, 96, ORANYE_T, 2, putus="6 5")
    isi += _p("M56 110 L84 100 L110 108 L136 78 L160 120 L186 88 L212 82 L238 70 L266 64", "none", BIRU_T, 4)
    for px, py in [(136, 78), (160, 120), (266, 64)]:
        isi += _c(px, py, 4.5, BIRU_T, NAVY, 1.5)
    isi += _t(272, 92, "rata-rata", 10, ORANYE_T, "end") + _t(160, 168, "satu bulan", 11, ABU_T, "middle", False)
    return _svg(isi, "Operasi")


def _bandingkan_produksi():
    isi = _l(40, 160, 280, 160, NAVY, 2.5)
    isi += _r(70, 70, 56, 90, BIRU, BIRU_T, 4, 2.5) + _t(98, 182, "A", 15)
    isi += _r(190, 40, 56, 120, KUNING, KUNING_T, 4, 2.5) + _t(218, 182, "B", 15)
    isi += _p("M134 70 H178", "none", NAVY, 2.5) + _p("M168 62 L178 70 L168 78", "none", NAVY, 2.5)
    isi += _c(158, 112, 18, PUTIH, ORANYE_T, 3) + _t(158, 118, "+/-", 14, ORANYE_T)
    return _svg(isi, "Operasi")


def _hari_berkejadian():
    isi = _kalender(52, 34, 150, 130, "JUL", merah=(2, 7, 8, 13, 16))
    isi += _segitiga_awas(246, 90, 36)
    return _svg(isi, "Operasi")


def _cek_status_sumur():
    # penampang sumur: kepala sumur di permukaan, lubang bor ke bawah, pompa ESP di dasar, kartu status di kiri
    isi = _r(14, 70, 292, 116, "#D9C8A9", "#8A7550", 6, 2.5)  # tanah
    isi += _r(142, 70, 36, 108, "#B8C7D6", NAVY, 3, 2.5)  # lubang bor berisi fluida
    isi += _r(132, 40, 56, 14, ABU, NAVY, 3, 2.5) + _r(150, 54, 20, 16, "#C9D3DD", NAVY, 3, 2.5)  # kepala sumur
    isi += _l(188, 47, 250, 47, NAVY, 5) + _l(250, 47, 250, 62, NAVY, 5)  # flowline
    isi += _r(146, 100, 28, 44, BIRU, BIRU_T, 8, 2.5) + _l(150, 112, 170, 112, BIRU_T, 2) + _l(150, 122, 170, 122, BIRU_T, 2)
    isi += _r(148, 144, 24, 24, KUNING_T, NAVY, 5, 2.5)  # motor
    isi += _r(30, 26, 84, 54, PUTIH, NAVY, 8, 2.5) + _c(52, 44, 8, HIJAU_T, NAVY, 2) + _t(92, 50, "ESP", 14) + _l(42, 66, 100, 66, BIRU_T, 3)
    isi += _r(204, 112, 78, 48, "#FFFFFF99", NAVY, 6, 2) + _t(243, 133, "status:", 11, ABU_T, "middle", False) + _t(243, 150, "Produksi", 12)
    return _svg(isi, "Operasi")


def _daftar_sumur():
    # peta lapangan: banyak titik sumur, sebagian ditandai oleh corong filter (area, pompa, status)
    isi = _r(20, 22, 280, 156, "#DDE9D6", "#7FA46D", 10, 2.5)
    titik = [(48, 54), (84, 78), (60, 112), (104, 48), (122, 98), (84, 142), (150, 60), (170, 118), (140, 152),
             (212, 52), (236, 96), (200, 142), (262, 62), (268, 128), (236, 150)]
    for i, (x, y) in enumerate(titik):
        pilih = i in (1, 4, 6, 7, 10)
        isi += _c(x, y, 7.5 if pilih else 5.5, ORANYE if pilih else PUTIH, ORANYE_T if pilih else NAVY, 2.5 if pilih else 1.8)
    isi += _p("M40 30 H110 L84 62 V92 L66 82 V62 Z", PUTIH, NAVY, 2.5)  # corong filter
    isi += _t(212, 36, "196 sumur", 11, ABU_T, "middle", False)
    return _svg(isi, "Operasi")


def _produksi_sumur():
    # grafik produksi harian satu sumur yang jatuh ke nol beberapa hari lalu pulih
    isi = _r(32, 28, 256, 144, PUTIH, NAVY, 8, 2.5)
    isi += _l(52, 148, 270, 148, NAVY, 2) + _l(52, 148, 52, 44, NAVY, 2)
    isi += _p("M52 76 L82 70 L112 78 L136 72 L148 146 L186 146 L204 74 L234 70 L268 78", "none", BIRU_T, 4)
    isi += _c(148, 146, 5, MERAH, MERAH_T, 2) + _c(186, 146, 5, MERAH, MERAH_T, 2)
    isi += _t(168, 134, "0 bopd", 10, MERAH_T, "middle") + _t(160, 166, "satu sumur, per hari", 11, ABU_T, "middle", False)
    return _svg(isi, "Operasi")


def _hitung_water_cut():
    isi = _r(52, 24, 112, 152, "#D6DCE4", NAVY, 10, 2.5) + _r(64, 36, 88, 30, PUTIH, NAVY, 4, 2) + _t(144, 59, "80%", 18, NAVY, "end")
    for i in range(12):
        isi += _r(64 + (i % 4) * 22, 80 + (i // 4) * 28, 18, 22, PUTIH if i != 11 else ORANYE, ORANYE_T if i == 11 else NAVY, 4, 1.8)
    isi += _t(73, 97, "7", 11) + _t(95, 97, "8", 11) + _t(117, 97, "9", 11)
    # gelas minyak dan air
    isi += _p("M200 52 H268 L260 164 H208 Z", "#FFFFFF99", NAVY, 3)
    isi += _p("M204.5 108 H263.5 L260 164 H208 Z", BIRU, BIRU_T, 2) + _p("M202 76 H266 L263.5 108 H204.5 Z", "#E8B84A", KUNING_T, 2)
    isi += _t(234, 96, "minyak", 10, NAVY) + _t(234, 142, "air", 10, NAVY)
    return _svg(isi, "Operasi")


def _catat_serah_terima():
    isi = _r(58, 28, 130, 148, KUNING, KUNING_T, 8, 2.5) + _l(78, 28, 78, 176, KUNING_T, 3)
    for i in range(6):
        isi += _l(92, 58 + i * 20, 172, 58 + i * 20, BIRU_T, 3)
    isi += _t(120, 48, "SHIFT", 12)
    # pensil
    isi += '<g transform="translate(228 70) rotate(35)">' + _r(-8, -42, 16, 70, KUNING_T, NAVY, 3, 2.5) + _p("M-8 28 L0 46 L8 28 Z", "#F4D7B0", NAVY, 2.5) + _r(-8, -52, 16, 10, MERAH, MERAH_T, 3, 2) + '</g>'
    isi += _p("M196 154 q10 -12 22 0 t22 0", "none", ORANYE_T, 3)
    return _svg(isi, "Operasi")


def _riwayat_work_order():
    isi = _tabel(34, 38, 4, 5, 170, 120, KUNING)
    isi += _t(60, 55, "WO", 11) + _t(98, 55, "aset", 11) + _t(139, 55, "jam", 11) + _t(180, 55, "ket", 11)
    for j in range(1, 5):
        isi += _l(42, 38 + 24 * j + 12, 66, 38 + 24 * j + 12, "#C9D3DD", 4)
    isi += _t(52, 176, "CSV", 13, ABU_T) + _kunci_pas(232, 74, 1.2)
    return _svg(isi, "Perawatan")


def _statistik_kegagalan():
    isi = _c(110, 100, 62, PUTIH, NAVY, 3)
    isi += _p("M110 100 L110 38 A62 62 0 0 1 164 131 Z", BIRU, NAVY, 2.5)
    isi += _p("M110 100 L164 131 A62 62 0 0 1 82 156 Z", KUNING, NAVY, 2.5)
    isi += _p("M110 100 L82 156 A62 62 0 0 1 60 56 Z", MERAH, NAVY, 2.5)
    isi += _c(110, 100, 22, LATAR["Perawatan"], NAVY, 2.5)
    for k, (w, nama) in enumerate([(BIRU, "listrik"), (KUNING, "mekanik"), (MERAH, "lainnya")]):
        isi += _r(206, 62 + k * 30, 20, 16, w, NAVY, 3, 2) + _t(234, 75 + k * 30, nama, 13, NAVY, "start")
    return _svg(isi, "Perawatan")


def _aset_downtime_tertinggi():
    isi = ""
    for k, (lebar, nama, warna) in enumerate([(210, "1", MERAH), (150, "2", ORANYE), (100, "3", KUNING)]):
        y = 32 + k * 44
        isi += _r(70, y, lebar, 32, warna, NAVY, 5, 2.5) + _c(46, y + 16, 15, PUTIH, NAVY, 2.5) + _t(46, y + 22, nama, 16)
    isi += _t(175, 178, "total jam downtime", 12, ABU_T, "middle", False)
    return _svg(isi, "Perawatan")


def _buat_work_order():
    isi = _papan_klip(80, 34) + _l(104, 82, 140, 82, KUNING_T, 3) + _l(104, 100, 150, 100, KUNING_T, 3) + _l(104, 118, 138, 118, KUNING_T, 3)
    isi += _c(214, 132, 34, HIJAU, HIJAU_T, 3) + _l(214, 114, 214, 150, HIJAU_T, 8) + _l(196, 132, 232, 132, HIJAU_T, 8)
    isi += _t(214, 56, "baru", 14, ORANYE_T)
    return _svg(isi, "Perawatan")


def _tutup_work_order():
    isi = _papan_klip(60, 34) + _l(84, 82, 120, 82, KUNING_T, 3) + _l(84, 100, 130, 100, KUNING_T, 3) + _l(84, 118, 118, 118, KUNING_T, 3)
    isi += '<g transform="translate(216 116) rotate(-14)">' + _r(-52, -22, 104, 44, "none", MERAH_T, 8, 4) + _t(0, 8, "TUTUP", 20, MERAH_T) + '</g>'
    isi += _centang(110, 148, 0.7)
    return _svg(isi, "Perawatan")


def _cari_insiden():
    isi = _segitiga_awas(110, 98, 48)
    isi += _kaca_pembesar(190, 96, 1.2)
    isi += _r(210, 150, 60, 10, PUTIH, NAVY, 3, 1.5) + _r(228, 166, 42, 8, PUTIH, NAVY, 3, 1.5)
    return _svg(isi, "HSE")


def _ringkasan_insiden():
    isi = _l(40, 160, 280, 160, NAVY, 2.5)
    for k, (tinggi, warna) in enumerate([(100, MERAH), (70, ORANYE), (46, KUNING), (28, BIRU)]):
        isi += _r(54 + k * 54, 160 - tinggi, 40, tinggi, warna, NAVY, 4, 2.5)
    isi += _segitiga_awas(262, 54, 22) + _t(160, 182, "jenis bahaya", 11, ABU_T, "middle", False)
    return _svg(isi, "HSE")


def _usulkan_tindakan_korektif():
    isi = _dokumen(48, 34, 108, 130, PUTIH, MERAH_T, 3) + _t(94, 62, "CAPA", 14, MERAH_T)
    # perisai dengan centang: tindakan korektif yang disetujui
    isi += _p("M236 56 L280 70 V108 Q280 142 236 162 Q192 142 192 108 V70 Z", HIJAU, HIJAU_T, 3.5) + _centang(236, 110, 0.9, HIJAU_T, 8)
    return _svg(isi, "HSE")


def _kirim_notifikasi_hse():
    isi = _lonceng(112, 96, 1.5)
    for r in (48, 66):
        isi += _p(f"M{112 + r} {96 - 26} A{r} {r} 0 0 1 {112 + r} {96 + 26}", "none", ORANYE_T, 3.5)
        isi += _p(f"M{112 - r} {96 - 26} A{r} {r} 0 0 0 {112 - r} {96 + 26}", "none", ORANYE_T, 3.5)
    isi += _r(204, 128, 78, 50, PUTIH, NAVY, 6, 2.5) + _p("M204 134 L243 160 L282 134", "none", NAVY, 2.5)
    return _svg(isi, "HSE")


def _konversi_satuan():
    isi = _r(34, 58, 86, 84, BIRU, BIRU_T, 10, 3) + _t(77, 108, "psi", 24) + _r(200, 58, 86, 84, KUNING, KUNING_T, 10, 3) + _t(243, 108, "bar", 24)
    isi += _p("M128 86 H192", "none", NAVY, 4) + _p("M180 74 L194 86 L180 98", "none", NAVY, 4)
    isi += _p("M192 116 H128", "none", NAVY, 4) + _p("M140 104 L126 116 L140 128", "none", NAVY, 4)
    isi += _t(77, 160, "1200", 14, BIRU_T) + _t(243, 160, "82,7", 14, KUNING_T)
    return _svg(isi, "Engineering")


def _ubah_setpoint_vsd():
    isi = _r(36, 22, 130, 156, "#C9D3DD", NAVY, 8, 3) + _r(48, 34, 106, 40, "#0F2A3F", NAVY, 4, 2)
    isi += _t(101, 62, "48 Hz", 20, "#7CF08A")
    isi += _c(101, 116, 28, PUTIH, NAVY, 3) + _l(101, 116, 118, 98, ORANYE_T, 5) + _c(101, 116, 5, NAVY, NAVY, 1)
    isi += _c(58, 160, 5, HIJAU_T, NAVY, 1.5) + _c(76, 160, 5, MERAH_T, NAVY, 1.5)
    # gelombang frekuensi, lalu motor dan pompa yang berputar mengikutinya
    isi += _p("M186 66 q14 -26 28 0 t28 0 t28 0", "none", UNGU_T, 4)
    isi += _l(166, 128, 190, 128, NAVY, 4) + _r(190, 112, 44, 32, UNGU, UNGU_T, 6, 3) + _l(234, 128, 250, 128, NAVY, 4)
    isi += _c(270, 128, 20, UNGU, UNGU_T, 3) + _p("M270 128 m-10 0 a10 10 0 0 1 20 0", "none", UNGU_T, 3) + _c(270, 128, 4, UNGU_T, UNGU_T, 1)
    return _svg(isi, "Engineering")


def _cari_dokumen_sop():
    isi = _dokumen(56, 28, 110, 138, PUTIH, "#C9D3DD", 0)
    for k in range(4):
        isi += _r(72, 56 + k * 24, 12, 12, PUTIH, NAVY, 2, 2) + _l(92, 62 + k * 24, 148 - (k % 2) * 16, 62 + k * 24, BIRU_T, 3)
    isi += _centang(78, 76, 0.28, HIJAU_T, 8) + _centang(78, 100, 0.28, HIJAU_T, 8)
    isi += _kaca_pembesar(214, 92, 1.1) + _t(110, 184, "SOP", 13, HIJAU_T)
    return _svg(isi, "Dokumen")


def _cari_dokumen_manual():
    isi = _p("M40 44 Q100 30 160 50 V170 Q100 150 40 164 Z", PUTIH, NAVY, 3) + _p("M160 50 Q220 30 280 44 V164 Q220 150 160 170 Z", KUNING, NAVY, 3)
    isi += _l(160, 50, 160, 170, NAVY, 3)
    # roda gigi di halaman kanan
    isi += _c(222, 98, 24, PUTIH, NAVY, 3) + _c(222, 98, 9, KUNING, NAVY, 2.5)
    for a in range(8):
        isi += f'<g transform="translate(222 98) rotate({a * 45})">' + _r(-5, -34, 10, 12, PUTIH, NAVY, 2, 2.5) + '</g>'
    isi += _l(60, 80, 140, 84, BIRU_T, 3) + _l(60, 100, 140, 104, BIRU_T, 3) + _l(60, 120, 124, 124, BIRU_T, 3) + _t(100, 150, "FD-500", 13, ABU_T)
    return _svg(isi, "Dokumen")


def _cari_dokumen_laporan():
    isi = _dokumen(70, 36, 100, 128, ABU, "#C9D3DD", 3) + _dokumen(52, 28, 100, 128, PUTIH, BIRU_T, 2)
    isi += _r(66, 98, 14, 24, BIRU, BIRU_T, 2, 2) + _r(86, 84, 14, 38, KUNING, KUNING_T, 2, 2) + _r(106, 70, 14, 52, HIJAU, HIJAU_T, 2, 2)
    isi += _kaca_pembesar(220, 100, 1.2)
    return _svg(isi, "Dokumen")


def _cari_dokumen_investigasi():
    isi = _p("M40 160 V56 Q40 46 50 46 H110 L128 66 H220 Q230 66 230 76 V160 Z", KUNING, NAVY, 3)
    isi += _r(40, 88, 190, 76, "#F8E3A0", NAVY, 6, 3)
    # gembok: dokumen terbatas
    isi += _p("M118 130 V120 A16 16 0 0 1 150 120 V130", "none", NAVY, 4) + _r(108, 128, 52, 34, ORANYE, ORANYE_T, 5, 3) + _c(134, 144, 5, NAVY, NAVY, 1)
    isi += _kaca_pembesar(250, 104, 1.0) + _t(134, 36, "terbatas", 12, MERAH_T)
    return _svg(isi, "Dokumen")


_GAMBAR = {
    "laporan_harian": _laporan_harian,
    "ringkasan_produksi_bulanan": _ringkasan_produksi_bulanan,
    "bandingkan_produksi": _bandingkan_produksi,
    "hari_berkejadian": _hari_berkejadian,
    "cek_status_sumur": _cek_status_sumur,
    "daftar_sumur": _daftar_sumur,
    "produksi_sumur": _produksi_sumur,
    "hitung_water_cut": _hitung_water_cut,
    "catat_serah_terima": _catat_serah_terima,
    "riwayat_work_order": _riwayat_work_order,
    "statistik_kegagalan": _statistik_kegagalan,
    "aset_downtime_tertinggi": _aset_downtime_tertinggi,
    "buat_work_order": _buat_work_order,
    "tutup_work_order": _tutup_work_order,
    "cari_insiden": _cari_insiden,
    "ringkasan_insiden": _ringkasan_insiden,
    "usulkan_tindakan_korektif": _usulkan_tindakan_korektif,
    "kirim_notifikasi_hse": _kirim_notifikasi_hse,
    "konversi_satuan": _konversi_satuan,
    "ubah_setpoint_vsd": _ubah_setpoint_vsd,
    "cari_dokumen_sop": _cari_dokumen_sop,
    "cari_dokumen_manual": _cari_dokumen_manual,
    "cari_dokumen_laporan": _cari_dokumen_laporan,
    "cari_dokumen_investigasi": _cari_dokumen_investigasi,
}


def ilustrasi(nama_tool: str) -> str:
    """Teks SVG untuk sebuah tool. Tool yang belum punya gambar mendapat kotak abu-abu bernama tool itu."""
    if nama_tool in _GAMBAR:
        return _GAMBAR[nama_tool]()
    return _svg(_r(60, 50, 200, 100, ABU, ABU_T, 10, 3) + _t(160, 106, nama_tool[:22], 14), "Dokumen")


def daftar_ilustrasi() -> list[str]:
    return list(_GAMBAR)
