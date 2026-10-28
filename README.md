# Physcom Reference

คู่มือสอบปฏิบัติ Arduino UNO R4 WiFi ภาษาไทย ครอบคลุมเซนเซอร์ วงจร ตัวอย่างโค้ด MQTT และเครื่องมือคำนวณ พร้อมค้นหา คัดลอกโค้ด และดาวน์โหลดไฟล์ตัวอย่าง

เว็บใช้ HTML ไฟล์เดียว ฝังรูป ฟอนต์ และ JavaScript ไว้ครบ ไม่มี backend และไม่ต้องติดตั้งแพ็กเกจสำหรับใช้งาน

## แก้เนื้อหาและเผยแพร่

แก้ไฟล์ใน `source/` แล้วใช้ Python 3 สร้างเว็บใหม่จากโฟลเดอร์นี้:

```sh
python source/build.py
```

ผลลัพธ์อยู่ที่ `public/index.html` และ `public/licenses/` สคริปต์ใช้เฉพาะ Python standard library ไม่ต้องติดตั้ง dependency เพิ่ม จากนั้นบันทึกซอร์สและผลลัพธ์ขึ้น GitHub:

```sh
git add source public
git commit -m "Update Physcom reference"
git push origin main
```

Vercel เชื่อมกับ GitHub เพื่อ deploy เมื่อ push ขึ้น `main` โดยเสิร์ฟไฟล์ที่ commit ไว้ใน `public/` โดยตรง ไม่รันคำสั่ง build หรือติดตั้ง dependency การตั้งค่าอยู่ใน `vercel.json`

## ใช้ออฟไลน์

คัดลอกหรือดาวน์โหลดไฟล์ต้นฉบับ `public/index.html` แล้วเปิดในเบราว์เซอร์ได้โดยไม่ต้องใช้ server เนื้อหา รูปวงจร ตัวคำนวณ และการดาวน์โหลดโค้ดทำงานในเครื่อง ส่วนลิงก์อ้างอิงและการส่ง MQTT ไป Broker จริงต้องมีอินเทอร์เน็ต

Repository นี้เก็บเว็บและซอร์สสำหรับแก้ไข ไม่รวม PDF สไลด์และชุดเครื่องมือ Arduino ข้อความอ้างถึงชุด ZIP ในเว็บหมายถึงชุดไฟล์ออฟไลน์ที่จัดเตรียมแยกไว้

## โครงสร้าง

- `source/content.py` — เนื้อหาและ Arduino sketches
- `source/app.js`, `source/style.css`, `source/index.tpl` — หน้าเว็บและการทำงาน
- `source/assets/`, `source/lab-images.json` — รูปวงจรและคำอธิบายต้นทาง
- `source/vendor/` — ฟอนต์และ Eclipse Paho ที่ฝังใน HTML
- `source/licenses/`, `public/licenses/` — ประกาศสิทธิ์และที่มาของรูป/dependency
- `public/index.html` — เว็บพร้อมเผยแพร่และใช้แบบออฟไลน์

เก็บประกาศสิทธิ์และที่มาของรูปไว้เมื่อเผยแพร่หรือส่งต่อ ตัวอย่างโค้ดใช้ข้อมูล WiFi/MQTT แบบ placeholder ให้แก้ตามโจทย์จริงและตรวจพินของอุปกรณ์ก่อนใช้งาน โค้ดยังไม่ได้ยืนยันด้วยการทดลองฮาร์ดแวร์ครบทุกวงจร
