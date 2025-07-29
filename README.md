# Fotoplane_HR_Portal
Here's a complete `README.md` for your **Fotoplane HR Portal** project:

---

# 📋 Fotoplane HR Portal

**Fotoplane HR Portal** is a lightweight internal web application built using Flask to manage HR operations such as employee records, work logs, leave tracking, and HR policy document management. It supports admin and employee-level access.

## 🚀 Features

### 👨‍💼 Admin Portal

* Secure login for HR/Admin using a password.
* Add/view employee details (name, ID, email, DOB).
* Log employee work hours (WFO, WFH, Leave).
* Track leave quotas and availed leaves.
* Upload, rename, and delete HR policy PDF files.
* View all employee logs and leave summaries.

### 👩‍💻 Employee Portal

* Employee login using Employee ID and registered Email.
* View personal work logs and attendance.
* View remaining leave balance.
* Access to uploaded HR documents.

### 📄 HR Policies

* Upload and manage PDFs categorized under headings.
* Display "🆕 New" badge for files uploaded in the last 24 hours.

---

## 🛠️ Technologies Used

* **Backend:** Flask (Python)
* **Frontend:** HTML, Bootstrap 5
* **File Handling:** `Werkzeug`, `os`
* **Session Management:** Flask session
* **Data Storage:** In-memory dictionaries (can be extended to DB)

---

## 🔐 Default Admin Login

| Username | Password   |
| -------- | ---------- |
| admin    | `admin123` |

> ⚠️ You can change the password inside `app.py` for better security.

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/aasthamathur139/Fotoplane_HR_Portal.git
cd Fotoplane_HR_Portal
```

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install flask
```

### 4. Run the Application

```bash
python app.py
```

Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📁 Folder Structure

```
Fotoplane_HR_Portal/
├── app.py                 # Main Flask application
├── uploads/               # Uploaded PDF files stored here
├── README.md              # Project documentation
└── requirements.txt       # (Optional) Package dependencies
```

---

## 🧠 Possible Improvements

* ✅ Add persistent storage (SQLite or JSON files)
* ✅ Use hashed passwords (`werkzeug.security`)
* ✅ Add pagination for employee lists
* ✅ Add CSV/Excel export of logs
* ✅ Add email notifications for leave approvals

---

## 👩‍💼 Developed By
**Aastha Mathur**
📧 [aastha@fotoplane.com](mailto:aastha@fotoplane.com)
🌐 [fotoplane.com](https://fotoplane.com)

---
