---
doc_id: SOP-OPS-025
title: Operasi Water Injection Pump
doc_type: SOP
revision: 3
effective_date: 2025-12-01
status: active
owner: Departemen Production Operations
access_group: all
---

# SOP-OPS-025 Rev. 3 — Operasi Water Injection Pump

> Dokumen FIKTIF untuk keperluan pelatihan.

## 1. Tujuan

Menjaga suplai air injeksi yang stabil dari water injection pump (misalnya P-SR1-301) dan mencegah kerusakan pompa akibat kavitasi atau dry running.

## 2. Pemeriksaan Sebelum Start

1. Level tangki suplai (surge tank) minimal **40%**. Di bawah 30% pompa akan trip low suction.
2. Valve suction terbuka penuh, valve discharge tertutup (start melawan valve tertutup dalam waktu singkat).
3. Seal flush dan lube oil normal; tekanan lube oil minimal **1,5 bar**.
4. Tidak ada LOTO yang masih terpasang pada pompa atau motor (SOP-HSE-007).

## 3. Prosedur Start

1. Prime pompa sampai tidak ada gelembung udara pada vent casing.
2. Start motor; setelah mencapai kecepatan penuh, buka valve discharge perlahan sampai laju injeksi target.
3. Catat tekanan suction, tekanan discharge, arus motor, dan vibrasi setiap **1 jam** selama 4 jam pertama.

## 4. Batas Operasi dan Alarm

| Parameter | Normal | Alarm | Trip |
|---|---|---|---|
| Tekanan suction | > 2,0 bar | 1,5 bar | 1,0 bar (low suction) |
| Vibrasi | < 4,5 mm/s | 7,1 mm/s | 11 mm/s |
| Temperatur bearing | < 75 derajat C | 85 derajat C | 95 derajat C |

## 5. Troubleshooting Trip Low Suction

1. Periksa level surge tank. Bila di bawah 30%, naikkan suplai air produksi dari separator atau free water knockout.
2. Periksa strainer suction: bila differential pressure tinggi, bersihkan.
3. **Reset hanya setelah level tangki di atas 40%.** Restart berulang tanpa menaikkan level menyebabkan kavitasi dan merusak impeller.
4. Restart maksimal **2 kali berturut-turut**; setelah itu panggil engineer mekanik.

## 6. Pencatatan

Trip, penyebab, dan waktu pemulihan dicatat di logbook shift dan sistem work order.
