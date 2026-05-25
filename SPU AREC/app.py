from flask import Flask, render_template, request, redirect, url_for, flash, session
import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime
import pytz
import urllib.request
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.secret_key = "spu_arec_secure_key_2026"

# กำหนดรหัสผ่านของ Admin
ADMIN_USERNAME = "ADMIN"
ADMIN_PASSWORD = "SPU_ADMIN_999"

# ตั้งค่า Google Sheets
SHEET_NAME = "SPU_AREC_DB"
JSON_FILE = "credentials.json"
sheet_members = None
sheet_duty = None
sheet_checkin = None
sheet_qso = None
sheet_news = None

if os.path.exists(JSON_FILE):
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(JSON_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        
        sheet_members = client.open(SHEET_NAME).sheet1
        
        try: sheet_duty = client.open(SHEET_NAME).worksheet("DutySchedule")
        except: 
            sheet_duty = client.open(SHEET_NAME).add_worksheet(title="DutySchedule", rows="100", cols="10")
            sheet_duty.append_row(["Date", "Time", "Callsign", "Frequency"])
            
        try: sheet_checkin = client.open(SHEET_NAME).worksheet("CheckInLog")
        except:
            sheet_checkin = client.open(SHEET_NAME).add_worksheet(title="CheckInLog", rows="100", cols="10")
            sheet_checkin.append_row(["Timestamp", "Callsign", "Action", "Reason", "DateOnly"])
            
        try: sheet_qso = client.open(SHEET_NAME).worksheet("QSOLog")
        except:
            sheet_qso = client.open(SHEET_NAME).add_worksheet(title="QSOLog", rows="100", cols="10")
            sheet_qso.append_row(["Date", "Time_TH", "Time_UTC", "Frequency", "Mode", "TargetStation", "SignalReport", "Operator"])

        try: sheet_news = client.open(SHEET_NAME).worksheet("NewsLog")
        except:
            sheet_news = client.open(SHEET_NAME).add_worksheet(title="NewsLog", rows="100", cols="5")
            sheet_news.append_row(["Timestamp", "Title", "Content", "Author"])
            
        print("🟢 Connected to Google Sheets All Tabs Successfully!")
    except Exception as e:
        print(f"🔴 Google Sheets Error: {e}")

def get_all_records(): return sheet_members.get_all_records() if sheet_members else []
def get_all_duties(): return sheet_duty.get_all_records() if sheet_duty else []
def get_all_news(): return list(reversed(sheet_news.get_all_records())) if sheet_news else []

def get_external_radio_news():
    try:
        url = "https://news.google.com/rss/search?q=%E0%B8%A7%E0%B8%B4%E0%B8%97%E0%B8%A2%E0%B8%B8%E0%B8%AA%E0%B8%A1%E0%B8%B1%E0%B8%84%E0%B8%A3%E0%B9%80%E0%B8%A5%E0%B9%88%E0%B8%99+OR+%E0%B8%A7%E0%B8%B4%E0%B8%97%E0%B8%A2%E0%B8%B8%E0%B8%AA%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%AA%E0%B8%B2%E0%B8%A3&hl=th&gl=TH&ceid=TH:th"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        news_list = []
        for item in root.findall('./channel/item')[:6]:
            news_list.append({
                'title': item.find('title').text,
                'link': item.find('link').text,
                'pubDate': item.find('pubDate').text[:16]
            })
        return news_list
    except Exception as e:
        print("RSS Error:", e)
        return []

# ==========================================
# 🏠 PORTAL (ระบบล็อกอิน)
# ==========================================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "login":
            callsign = request.form.get("callsign", "").strip().upper()
            password = request.form.get("password", "")
            
            if callsign == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                session["user"] = "ADMIN"
                session["name"] = "ผู้ดูแลระบบ"
                session["role"] = "admin"
                return redirect(url_for("admin_dashboard"))
            
            records = get_all_records()
            for record in records:
                if str(record.get("Callsign", "")).upper() == callsign and str(record.get("Password", "")) == password:
                    if record.get("Status") != "ปกติ":
                        flash("บัญชีรออนุมัติ", "warning")
                        return redirect(url_for("index"))
                    session["user"] = callsign
                    session["name"] = record.get("Name", "")
                    session["role"] = "user"
                    return redirect(url_for("dashboard"))
            flash("รหัสไม่ถูกต้อง", "danger")
    return render_template("portal.html", active_tab="login")

# ==========================================
# 📻 USER SYSTEM (ระบบสมาชิกทั่วไป)
# ==========================================
@app.route("/dashboard")
def dashboard():
    if "user" not in session or session.get("role") != "user": return redirect(url_for("index"))
    tz = pytz.timezone('Asia/Bangkok')
    today_str = datetime.now(tz).strftime("%Y-%m-%d")
    
    members = get_all_records()
    checkins = sheet_checkin.get_all_records() if sheet_checkin else []
    qsos = sheet_qso.get_all_records() if sheet_qso else []
    duties = get_all_duties()
    
    total_members = len([m for m in members if m.get("Status") == "ปกติ"])
    today_checkins = len([c for c in checkins if str(c.get("Timestamp", "")).startswith(today_str) and c.get("Action") == "Check-In"])
    today_qso = len([q for q in qsos if str(q.get("Date", "")) == today_str])
    today_net = next((d for d in duties if str(d.get("Date", "")) == today_str), None)
    
    stats = {
        "total_members": total_members,
        "today_checkins": today_checkins,
        "today_qso": today_qso,
        "today_net": today_net.get("Callsign") if today_net else "ไม่มีเวร"
    }
    
    latest_checkins = list(reversed(checkins))[:5]
    latest_news = get_all_news()[:1]
    
    return render_template("dashboard.html", user=session.get("user"), name=session.get("name"), stats=stats, checkins=latest_checkins, duties=duties[:5], news=latest_news)

@app.route("/checkin")
def checkin():
    if "user" not in session: return redirect(url_for("index"))
    return render_template("checkin.html", user=session.get("user"), name=session.get("name"))

@app.route("/qso")
def qso():
    if "user" not in session: return redirect(url_for("index"))
    return render_template("qso.html", user=session.get("user"), name=session.get("name"))

@app.route("/members")
def members_list():
    if "user" not in session: return redirect(url_for("index"))
    return render_template("members.html", user=session.get("user"), name=session.get("name"))

@app.route("/news")
def news():
    if "user" not in session: return redirect(url_for("index"))
    internal_news = get_all_news()
    external_news = get_external_radio_news()
    return render_template("news.html", user=session.get("user"), name=session.get("name"), news=internal_news, ext_news=external_news)

@app.route("/settings")
def settings():
    if "user" not in session: return redirect(url_for("index"))
    return render_template("settings.html", user=session.get("user"), name=session.get("name"))

# ==========================================
# 🛠️ ADMIN SYSTEM (ระบบแอดมิน)
# ==========================================
@app.route("/admin/dashboard")
def admin_dashboard():
    if "user" not in session or session.get("role") != "admin": return redirect(url_for("index"))
    members = get_all_records()
    news_list = get_all_news()
    duties = get_all_duties()
    checkins = sheet_checkin.get_all_records() if sheet_checkin else []
    return render_template("admin_dashboard.html", user=session.get("user"), name=session.get("name"), members=members, news=news_list, duties=duties, checkins=list(reversed(checkins))[:10])

@app.route("/admin/add-news", methods=["POST"])
def admin_add_news():
    if "user" not in session or session.get("role") != "admin": return redirect(url_for("index"))
    if sheet_news:
        tz = pytz.timezone('Asia/Bangkok')
        timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M")
        title = request.form.get("title")
        content = request.form.get("content")
        sheet_news.append_row([timestamp, title, content, "Admin SPU"])
        flash("เพิ่มประกาศข่าวสารสำเร็จ!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/add-duty", methods=["POST"])
def admin_add_duty():
    if "user" not in session or session.get("role") != "admin": return redirect(url_for("index"))
    if sheet_duty:
        date = request.form.get("date")
        time = request.form.get("time")
        callsign = request.form.get("callsign", "").strip().upper()
        frequency = request.form.get("frequency")
        sheet_duty.append_row([date, time, callsign, frequency])
        flash("จัดตั้งเวร Net Control สำเร็จ!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=8080)