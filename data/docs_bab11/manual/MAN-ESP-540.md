---
doc_id: MAN-ESP-540
title: Manual Sistem Pompa ESP Seri 540
doc_type: Manual
revision: 1.0
effective_date: 2024-06-01
status: active
owner: Vendor Fiktif-Lift (didistribusikan oleh Dept. Production Engineering)
access_group: all
---

# Manual Sistem Pompa ESP Seri 540

> Dokumen FIKTIF untuk keperluan pelatihan.

## Bab 1. Gambaran Sistem

Sistem ESP seri 540 terdiri dari pompa multistage, intake atau gas separator, protector (seal section), motor submersible, kabel tenaga (power cable) dengan kabel penghubung (motor lead extension), dan VSD di permukaan. Diameter casing minimum yang disarankan adalah 5,5 inci.

## Bab 2. Spesifikasi Utama

| Parameter | Nilai |
|---|---|
| Laju desain | 200 sampai 1.800 bpd cairan |
| Frekuensi operasi | 35 sampai 60 Hz |
| Frekuensi start-up | 35 Hz, naik bertahap |
| Arus nameplate motor | 42 A pada 50 Hz |
| Batas arus overload (OL) | **120% nameplate** (sekitar 50 A) |
| Batas arus underload (UL) | **60% nameplate** (sekitar 25 A) |
| Suhu motor maksimum | 150 derajat C |
| Run life desain | 36 bulan pada kondisi normal |

## Bab 3. Pengaturan Setpoint

1. Menurunkan frekuensi mengurangi laju cairan, arus motor, dan panas. Menaikkan frekuensi sebaliknya.
2. Perubahan frekuensi dilakukan bertahap **maksimal 2 Hz per 10 menit**.
3. Frekuensi di atas **55 Hz** hanya dengan persetujuan Production Engineer, karena beban shaft dan motor melampaui batas rekomendasi vendor.
4. Untuk sumur yang sering underload, turunkan frekuensi 2 sampai 5 Hz agar pump intake pressure naik dan fluid level pulih.

## Bab 4. Kode Penyebab Trip dan Tindakan

| Gejala | Kemungkinan penyebab | Tindakan |
|---|---|---|
| Arus tinggi lalu trip OL | Pasir, emulsi, atau pompa macet sebagian | Cek amp chart, lakukan flushing, megger |
| Arus rendah lalu trip UL | Gas lock, fluid level rendah, shaft patah | Tunggu 30 menit, turunkan frekuensi |
| Alarm ground fault | Isolasi kabel atau motor rusak | Jangan restart, lakukan megger (lihat SOP-MNT-005) |
| Arus tidak seimbang > 5% | Tegangan suplai tidak seimbang, kabel rusak | Periksa transformer dan sambungan |

## Bab 5. Pemeriksaan Rutin

- Catat arus, tegangan, frekuensi, dan pump intake pressure setiap shift.
- Megger test kabel dan motor **setiap 6 bulan** atau setelah trip OL ke-3 dalam 30 hari.
- Periksa filter udara dan kipas panel VSD tiap bulan.

## Bab 6. Pembongkaran dan Pemeriksaan Setelah Pulling

Periksa shaft, impeller, bearing, dan protector. Catat tanda aus oleh pasir (erosi stage) dan scale. Unit dengan kegagalan berulang dikirim ke vendor untuk analisis teardown.
