---
doc_id: MAN-LCV-250
title: Manual Level Control Valve dan Positioner Seri 250
doc_type: Manual
revision: 1.1
effective_date: 2024-09-01
status: active
owner: Vendor Fiktif-Valve (didistribusikan oleh Dept. Instrumentasi)
access_group: all
---

# Manual Level Control Valve dan Positioner Seri 250

> Dokumen FIKTIF untuk keperluan pelatihan.

## Bab 1. Gambaran

Valve seri 250 adalah control valve globe berpenggerak diafragma pneumatik dengan positioner elektro-pneumatik. Dipakai sebagai level control valve (LCV) pada separator, misalnya pada V-SR1-101 dan V-SR1-102.

## Bab 2. Spesifikasi

| Parameter | Nilai |
|---|---|
| Sinyal kontrol | 4 sampai 20 mA |
| Tekanan udara instrumen | 4 sampai 7 bar (disarankan 5,5 bar) |
| Aksi saat kehilangan udara | Fail close (FC) |
| Waktu stroke penuh | 8 detik |
| Histeresis positioner | Kurang dari 1% |

## Bab 3. Kode Alarm Positioner

| Kode | Arti | Tindakan |
|---|---|---|
| **E01** | Posisi tidak sesuai sinyal (valve macet) | Periksa deposit, gerakkan manual, lalu kalibrasi |
| **E02** | Tekanan udara suplai rendah (< 3,5 bar) | Periksa regulator dan filter udara |
| **E03** | Sinyal 4-20 mA hilang | Periksa kabel dan transmitter |
| **E07** | Hunting (osilasi posisi) | Turunkan gain, periksa positioner dan linkage |

## Bab 4. Kalibrasi dan Uji Fungsi

1. Isolasi valve; pasang bypass terbuka sebelum bekerja pada positioner (lihat SOP-OPS-040).
2. Uji stroke pada 0, 25, 50, 75, 100% sinyal; selisih posisi maksimal 1%.
3. Uji **fail-safe**: matikan udara dan pastikan valve menutup dalam batas waktu.
4. Kalibrasi ulang tiap **12 bulan**, atau setelah penggantian positioner.

## Bab 5. Troubleshooting Valve Macet

- **Gejala**: level naik walau output controller 100%, kode E01.
- **Penyebab umum**: positioner rusak, stem macet karena deposit parafin atau scale, atau packing terlalu kencang.
- **Tindakan**: pindah ke manual dan bypass; bersihkan stem; ganti positioner bila tidak merespons sinyal. Catat kejadian sebagai work order Instrumentation/Control.
