---
doc_id: SOP-MNT-005
title: Megger Test dan Pulling Job ESP
doc_type: SOP
revision: 2
effective_date: 2026-01-10
status: active
owner: Departemen Maintenance
access_group: all
---

# SOP-MNT-005 Rev. 2 — Megger Test dan Pulling Job ESP

> Dokumen FIKTIF untuk keperluan pelatihan.

## 1. Tujuan

Menentukan kapan ESP perlu ditarik (pulling) berdasarkan hasil megger test, dan mengatur langkah pekerjaan pulling agar aman dan terkendali.

## 2. Megger Test

1. Matikan VSD, pasang LOTO pada panel (SOP-HSE-007), dan tunggu kapasitor VSD discharge minimal **10 menit**.
2. Lepas kabel di junction box; ukur isolasi **phase-to-ground** dengan megger **1.000 V DC** selama 1 menit untuk tiap fasa.
3. Ukur resistansi antar fasa (phase-to-phase); selisih maksimum **5%**.

| Pembacaan phase-to-ground | Kesimpulan | Tindakan |
|---|---|---|
| >= 100 Mohm | Baik | Boleh restart |
| 10 sampai 100 Mohm | Menurun | Restart dengan persetujuan Petroleum Engineer, pantau ketat |
| 1 sampai 10 Mohm | Buruk | Jangan restart; jadwalkan pulling |
| **< 1 Mohm atau 0 Mohm** | Gagal total (motor burnt atau kabel putus) | **Pulling job**, jangan dicoba restart |

## 3. Keputusan Pulling

Pulling diajukan bila: megger < 10 Mohm, ground fault berulang, atau sumur memenuhi kriteria bad actor (SOP-OPS-012 bagian 6). Pengajuan memuat nomor work order, hasil megger, dan perkiraan kehilangan produksi per hari.

## 4. Persiapan Pulling

1. Perizinan: PTW untuk pekerjaan rig, pengawas rig berjalan, dan area di sekitar wellhead dibarikade.
2. Sumur dimatikan dan **di-kill** dengan fluida yang sesuai; tekanan wellhead nol sebelum BOP dipasang.
3. Pastikan jalur akses ke sumur aman; saat hujan lebat pekerjaan dijadwalkan ulang bila akses licin.

## 5. Pemeriksaan Setelah Pulling

1. Periksa motor, protector, pompa, dan kabel; catat kondisi (burnt, korosi, scale, pasir).
2. Foto dan simpan komponen gagal untuk analisis akar masalah.
3. Ganti seluruh bagian yang rusak, termasuk **power cable** bila isolasi rusak, kemudian run-in sesuai program.
4. Setelah run-in, start-up dengan prosedur SOP-OPS-012 (35 Hz, naik 5 Hz tiap 5 menit).

## 6. Pencatatan

Hasil megger, penyebab kegagalan, dan lama pekerjaan dicatat di work order. Catatan ini dipakai untuk menghitung MTBF dan kriteria bad actor.
