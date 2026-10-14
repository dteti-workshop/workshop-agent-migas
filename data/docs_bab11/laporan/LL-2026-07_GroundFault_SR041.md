---
doc_id: LL-2026-07
title: Lessons Learned — Ground Fault Kabel ESP SR-041 dan Akses Terputus
doc_type: Lessons Learned
revision: 1
effective_date: 2026-08-10
status: active
owner: Production Engineering Area Seruni
access_group: all
---

# Lessons Learned LL-2026-07 — Ground Fault Kabel ESP SR-041

> Dokumen FIKTIF untuk keperluan pelatihan.

## 1. Apa yang Terjadi

Pada 17 Juli 2026 hujan lebat memutus akses jalan ke SR-041 selama satu shift sehingga sumur tidak bisa diperiksa langsung. Pada **19 Juli**, ESP SR-041 trip dengan alarm **ground fault**. Hasil megger menunjukkan isolasi kabel di bawah 1 Mohm. Sumur dimatikan dan menunggu rig pada 20 Juli. **Rig masuk 21 Juli** dan **power cable diganti**. SR-041 kembali berproduksi pada 22 Juli, sekitar 104 bopd.

Total produksi tertunda sekitar **330 barel** (110 barel per hari selama tiga hari).

## 2. Penyebab

1. Isolasi power cable rusak pada bagian yang terpapar gas dan panas, dan kerusakan sudah berkembang sebelum trip.
2. Akses jalan ke sumur tidak tahan hujan sehingga pemantauan fisik tertunda.
3. Megger terakhir pada SR-041 dilakukan lebih dari 6 bulan sebelumnya, melewati interval rekomendasi manual vendor (MAN-ESP-540).

## 3. Pelajaran

- **Jangan restart** ESP yang trip ground fault; lakukan megger dahulu (SOP-OPS-012 dan SOP-MNT-005).
- Megger rutin **tiap 6 bulan** dijadwalkan di sistem work order dengan pengingat.
- Rencana kontingensi untuk sumur yang aksesnya terputus karena cuaca: pemantauan jarak jauh dan prioritas perbaikan jalan.
- Kontak awal dengan penyedia rig dilakukan di hari yang sama dengan trip untuk memperpendek waktu tunggu.

## 4. Tindak Lanjut

| Tindakan | Penanggung jawab | Tenggat |
|---|---|---|
| Jadwalkan megger 6-bulanan semua ESP Seruni | Maintenance | 31 Agustus 2026 |
| Perbaikan jalan akses SR-041 | Fasilitas | 30 September 2026 |
| Tinjau kriteria sumur kritis untuk akses cuaca buruk | Production Engineering | 30 September 2026 |
