---
doc_id: SOP-OPS-040
title: Operasi Separator dan Pengendalian Level
doc_type: SOP
revision: 2
effective_date: 2026-02-01
status: active
owner: Departemen Production Operations
access_group: all
---

# SOP-OPS-040 Rev. 2 — Operasi Separator dan Pengendalian Level

> Dokumen FIKTIF untuk keperluan pelatihan.

## 1. Tujuan

Menjaga separator (contoh V-SR1-101 dan V-SR1-102) bekerja pada level cairan yang aman, supaya tidak terjadi carry-over cairan ke jalur gas atau carry-under gas ke jalur cairan.

## 2. Parameter Normal

| Parameter | Nilai normal | High alarm (LAH) | Low alarm (LAL) |
|---|---|---|---|
| Level cairan | 40% sampai 60% | **75%** | 25% |
| Tekanan | 3,0 sampai 3,5 bar | 4,0 bar | 2,0 bar |
| Level interface minyak-air | 30% sampai 50% | 65% | 15% |

Level di atas **85%** memicu high-high level (LAHH) dan shutdown separator (SDV tertutup).

## 3. Level Control Valve (LCV)

1. LCV mengatur laju keluar cairan berdasarkan sinyal transmitter level. Mode normal: **AUTO**.
2. Gejala LCV bermasalah: level naik terus walau output controller 100%, atau level berosilasi (hunting) dengan periode kurang dari 2 menit.
3. Penyebab umum: positioner rusak atau kotor, suplai udara instrumen rendah (< 4 bar), atau valve macet oleh deposit.

## 4. Tindakan Saat High Level Alarm

1. Konfirmasi level dengan **gauge glass** dan bandingkan dengan pembacaan transmitter.
2. Pindahkan LCV ke **MANUAL** dan buka bertahap sambil memantau level.
3. Bila level tidak turun, buka **bypass LCV**, dan beri tahu pengawas shift. Kurangi laju masuk dengan menutup sebagian wing valve sumur dengan produksi terbesar.
4. Bila level mencapai **85%**, SDV akan menutup otomatis. Jangan melakukan bypass interlock.
5. Produksi GS yang dialihkan ke separator lain (misalnya dari V-SR1-101 ke V-SR1-102) dicatat sebagai deferred pada laporan harian.

## 5. Pencatatan

Kejadian high level, durasi pemotongan produksi (cut), dan perbaikan LCV dicatat pada laporan harian dan work order (kategori Instrumentation/Control).

## 6. Referensi

- MAN-LCV-250 Manual Level Control Valve dan Positioner
- SOP-HSE-007 LOTO
