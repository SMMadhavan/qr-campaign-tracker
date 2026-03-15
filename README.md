# 📱 QR Campaign Tracker

A lightweight, open-source tool to generate branded QR codes and track every scan in real-time. Built for small businesses, freelancers, and marketers who want actionable insights from their campaigns — without paying for expensive tools.

---

## 🚀 Features

- **Instant QR Generation** — Create a trackable QR code for any URL in seconds
- **Custom Branding** — Choose your QR code color to match your brand
- **Scan Tracking** — Every scan is logged with timestamp and IP address
- **Campaign Dashboard** — View all your campaigns and their scan counts in one place
- **Scan History** — Drill down into individual scan logs per campaign
- **Downloadable QR Codes** — Export your QR code as a PNG for print or digital use
- **Lightweight & Local** — Runs entirely on your machine, no third-party services needed

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| QR Generation | qrcode, Pillow |
| Frontend | HTML, CSS, Vanilla JS |

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.x installed on your machine
- pip or py package manager

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/qr-campaign-tracker.git
cd qr-campaign-tracker
```

**2. Install dependencies**
```bash
py -m pip install -r requirements.txt
```

**3. Run the app**
```bash
py app.py
```

**4. Open in browser**
```
http://127.0.0.1:5000
```

That's it! No environment variables, no complex setup. 🎉

---

## 📖 How It Works
```
User creates a campaign (name + destination URL)
        ↓
App generates a unique short code + QR image
        ↓
QR code points to → yourserver.com/track/<short_code>
        ↓
When scanned, server logs the scan (time + IP)
        ↓
Server redirects user to the destination URL
        ↓
Dashboard shows real-time scan analytics
```

---

## 📂 Project Structure
```
qr-campaign-tracker/
├── app.py              ← Flask backend (routes + logic)
├── database.py         ← SQLite database operations
├── requirements.txt    ← Python dependencies
├── README.md           ← You are here
├── templates/
│   ├── index.html      ← QR Generator page
│   └── dashboard.html  ← Campaigns dashboard
└── static/
    ├── style.css        ← Stylesheet
    └── qr_codes/        ← Generated QR images (auto-created)
```

---

## 🗺️ Future Roadmap

- [ ] Logo upload — embed your brand logo in the center of the QR
- [ ] Location tracking — detect country/city from scan IP
- [ ] Multiple color themes for QR codes
- [ ] CSV export of scan data
- [ ] Deploy to cloud (Render / Railway) for public URL tracking
- [ ] User authentication — multiple users with separate dashboards
- [ ] QR code expiry dates
- [ ] Campaign performance comparison charts

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!
Feel free to open a pull request or raise an issue.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> Built with ❤️ for small businesses and marketers who deserve better tools without the premium price tag.