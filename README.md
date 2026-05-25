# 📻 SPU AREC Platform
**Amateur Radio Emergency Communications - Sripatum University**

> **สถานะโครงการ (Project Status):** ⚠️ อยู่ในระหว่างการพัฒนาระบบ (Under Development)
> 
> **ลิขสิทธิ์ (Copyright):** &copy; 2026 SPU Amateur Radio Emergency Communications (SPU AREC). All rights reserved.

ระบบปฏิบัติการและบริหารจัดการฐานข้อมูลสำหรับ **ชมรมวิทยุสมัครเล่น มหาวิทยาลัยศรีปทุม (SPU AREC)** ถูกพัฒนาขึ้นเพื่อเปลี่ยนผ่านระบบการจดบันทึกแบบกระดาษ (Paper-based) ไปสู่ระบบดิจิทัลเต็มรูปแบบ (Digital Transformation) โดยรองรับการบันทึกข้อมูลการเข้าสถานี (Check-In), สมุดบันทึกการติดต่อสื่อสารทางวิทยุ (QSO Log), การจัดการเวรควบคุมข่าย (Net Control) และระบบข่าวสารแบบเรียลไทม์

---

## 💻 โซนที่ 1: Tech Stack & Technologies (เทคโนโลยีที่ใช้พัฒนา)

โปรเจกต์นี้ใช้สถาปัตยกรรมแบบ Server-side Rendering (SSR) โดยผสมผสานเครื่องมือและไลบรารีต่างๆ ดังนี้:

### ⚙️ 1. ระบบหลังบ้าน (Backend Server)
* **Python (v3.x):** ภาษาหลักที่ใช้ประมวลผลตรรกะของระบบ (Core Logic)
* **Flask Framework:** Web Framework น้ำหนักเบาที่ใช้จัดการเส้นทาง (Routing), การรับส่งข้อมูล (HTTP Requests/Responses) และระบบเซสชัน (Session Management) สำหรับแยกสิทธิ์ผู้ใช้งาน
* **Jinja2:** Template Engine ที่ทำงานร่วมกับ Flask เพื่อแทรกตัวแปรและเงื่อนไข (If/Else, For Loops) ของ Python ลงในไฟล์ HTML แบบไดนามิก

### ☁️ 2. ระบบฐานข้อมูลและคลาวด์ (Database & Cloud Storage)
* **Google Sheets API (v4):** ประยุกต์ใช้ Google Sheets เป็นฐานข้อมูลแบบ Serverless (BaaS) เพื่อให้ง่ายต่อการจัดการและเรียกดูข้อมูลดิบ
* **Google Cloud IAM (Service Account):** ระบบยืนยันตัวตน (Authentication) ผ่านไฟล์ credentials.json
* **gspread:** ไลบรารี Python สำหรับเชื่อมต่อ อ่าน และเขียนข้อมูลลงใน Google Sheets
* **google-oauth2-tool:** ไลบรารีสำหรับจัดการ Token และสิทธิ์การเข้าถึง API ของ Google

### 🎨 3. ระบบหน้าบ้าน (Frontend & User Interface)
* **HTML5 / CSS3:** โครงสร้างหลักและการกำหนด Custom CSS Variables เพื่อคุมธีมสี (SPU Blue & Pink)
* **Bootstrap (v5.3.0):** CSS Framework ระดับโลก ใช้สำหรับทำ Responsive Design ให้แสดงผลได้ดีทั้งบน Desktop และ Mobile
* **FontAwesome (v6.4.0):** เวกเตอร์ไอคอนสำหรับตกแต่ง UI ให้สื่อความหมายและดูเป็นมืออาชีพ
* **Google Fonts (Prompt):** ฟอนต์ภาษาไทยหลักของเว็บไซต์เพื่อความอ่านง่ายและทันสมัย

### 📡 4. การประมวลผลข้อมูลและ API ภายนอก (Data Processing)
* **XML ElementTree & urllib:** ใช้ทำ Web Scraping ดึงข้อมูล RSS Feed จาก Google News (คีย์เวิร์ด: วิทยุสมัครเล่น) มาแสดงผลอัตโนมัติ
* **pytz & datetime:** จัดการระบบเวลา (Timezone) ให้ตรงกับเวลาท้องถิ่นของประเทศไทย (Asia/Bangkok) อย่างแม่นยำ 
* **os:** ใช้ตรวจสอบการมีอยู่ของไฟล์ระบบ (เช่น credentials.json) เพื่อป้องกัน Server Crash

---

## 🚀 โซนที่ 2: Core Features (ระบบการทำงานหลัก)

### 👤 ฝั่งผู้ใช้งานทั่วไป (User / Operator)
* **Secure Login:** ระบบเข้าสู่ระบบด้วยสัญญาณเรียกขาน (Callsign) และรหัสผ่าน พร้อมตรวจสอบสถานะ "อนุมัติ" จากแอดมิน
* **Interactive Dashboard:** หน้าต่างสรุปผลรายวัน (จำนวนเช็คอิน, จำนวน QSO, และผู้ปฏิบัติหน้าที่ Net Control ประจำวัน)
* **Station Check-In/Out:** ระบบลงชื่อเข้าใช้สถานีวิทยุ พร้อมระบุภารกิจ (Reason of Operation)
* **Digital QSO Log:** ระบบบันทึกประวัติการติดต่อสื่อสารทางวิทยุ (ระบุสถานีปลายทาง, ความถี่, โหมดปฏิบัติการ และ RS/RST Report)
* **News Portal:** ศูนย์รวมข่าวสาร แบ่งเป็นประกาศจากชมรม (ออฟฟิเชียล) และฟีดข่าวสารวงการวิทยุระดับโลก (อัปเดตอัตโนมัติ)
* **Member Directory:** ระบบแสดงรายชื่อสมาชิกและสถานะการติดต่อ

### 🛡️ ฝั่งผู้ดูแลระบบ (Admin)
* **Admin Dashboard:** แพลตฟอร์มแยกเฉพาะสำหรับผู้ดูแลระบบ
* **User Management:** ตารางตรวจสอบข้อมูลสมาชิกทั้งหมดแบบเรียลไทม์
* **Activity Logs:** ระบบตรวจสอบประวัติการเข้า-ออกสถานี (Check-In Logs) ของสมาชิกทุกคน
* **Duty Scheduling:** ฟอร์มจัดตั้งตารางเวรปฏิบัติการ Net Control เพื่อกระจายข้อมูลไปยังหน้า Dashboard ของสมาชิก
* **Announcement Broadcast:** ระบบประกาศข่าวสารด่วนจากส่วนกลาง ส่งตรงเข้าฐานข้อมูลและแสดงผลให้สมาชิกทุกคนเห็นทันที

---

## 🛠️ โซนที่ 3: Prerequisites & Installation (การติดตั้งและใช้งาน)

### สิ่งที่ต้องมีเบื้องต้น
1. Python 3.8 ขึ้นไป
2. บัญชี Google Cloud Platform (สำหรับสร้าง Service Account)
3. ฐานข้อมูล Google Sheets (ชื่อ SPU_AREC_DB)

### วิธีการรันโปรเจกต์ในเครื่อง (Local Setup)

**1. Clone Repository นี้ลงมาที่เครื่อง:**
เปิด Terminal แล้วพิมพ์คำสั่งตามลำดับ:
git clone https://github.com/your-username/spu-arec-platform.git
cd spu-arec-platform

**2. ติดตั้งไลบรารีที่จำเป็น (Dependencies):**
พิมพ์คำสั่งนี้เพื่อติดตั้งเครื่องมือ:
pip install flask gspread google-auth pytz

(หมายเหตุ: หากคุณมีไฟล์ requirements.txt สามารถใช้คำสั่ง pip install -r requirements.txt ได้เลย)

**3. การตั้งค่าสิทธิ์เข้าถึง (Credentials):**
นำไฟล์ credentials.json (ที่ได้จาก Google Cloud) มาวางไว้ในโฟลเดอร์หลัก ซึ่งก็คือโฟลเดอร์เดียวกับไฟล์ app.py

**4. รันเซิร์ฟเวอร์:**
พิมพ์คำสั่งนี้ใน Terminal เพื่อเปิดระบบ:
python3 app.py

**5. การเข้าใช้งาน:**
เปิดเว็บเบราว์เซอร์ของคุณแล้วไปที่ลิงก์: http://127.0.0.1:8080

---

> 💡 Note for Contributors: โปรเจกต์นี้ถูกออกแบบมาเพื่อการศึกษาและพัฒนาต่อยอด หากพบปัญหาการใช้งานหรือต้องการเสนอแนะฟีเจอร์เพิ่มเติม สามารถเปิด Issues หรือส่ง Pull Request ได้ทันทีครับ!
