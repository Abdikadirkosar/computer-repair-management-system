# Computer Repair Management System (CRMS)

A simple, clean, professional, beginner-friendly **Computer Repair Management System** designed for small computer repair shops and suitable as a **University Computer Science project**.

This system replaces manual paper records with a streamlined digital workflow to track customers, their devices, repair progress, assigned technicians, payments, and printable receipts.

---

## 🚀 Key Features

* **Authentication & Roles**:
  * Built-in Django authentication (`/login/`, `/logout/`).
  * Self-service password change (`/password-change/`).
  * Admin and Technician roles with personalized dashboards.
* **Customer Management (CRUD)**:
  * Full customer records with name, phone, optional email, address.
  * Instant search by customer name or phone number.
* **Device Management (CRUD)**:
  * Link multiple devices per customer.
  * Supported device types: Laptop, Desktop, Printer, Monitor, Other.
  * Search by brand, model, or serial number.
* **Repair Job Tracking**:
  * Automatic sequential repair number generation (`REP-0001`, `REP-0002`, ...).
  * Priority levels: `Normal`, `Urgent`.
  * Simple 5-stage status workflow: `Pending` → `Repairing` → `Completed` → `Delivered` (or `Cancelled`).
  * **Quick Status & Findings Update**: 1-click update of diagnosis, notes, and status directly on the repair detail page.
  * Smart device dropdown filtering by customer.
* **Technician Management (CRUD)**:
  * Track active technicians, contact info, and specializations.
  * Personalized technician dashboard view: "My Assigned Repairs".
* **Payment & Balance Calculation**:
  * Financial tracking: `Repair Cost - Total Paid = Balance Due`.
  * Payment methods: `Cash`, `ZAAD`, `eDahab`, `Card`, `Bank`.
  * Built-in validation prevents overpayment and negative/zero amounts.
  * Direct payment recording from both repair detail and payment directory (`/payments/record/`).
* **Shop Expenses & Net Profit**:
  * Track operational expenses (Rent, Utilities, Equipment, Parts, Salaries, etc.).
  * Real-time financial health: `Net Profit = Total Revenue - Total Expenses`.
* **Printable Repair Receipt**:
  * Clean, formatted receipt ready for browser printing (`window.print()`).
  * Pure CSS `@media print` eliminates unnecessary UI elements on paper.
* **Modern SaaS Dashboard**:
  * Real-time metrics: Total Customers, Total Devices, Total Repairs, Pending, In Repair, Completed, Revenue, and Net Profit.
  * Recent repairs quick view table.
* **Zero External CSS/JS Dependencies**:
  * Built exclusively using pure semantic HTML5, custom CSS3 (no Bootstrap, no Tailwind), and vanilla JavaScript ES6+.

---

## 🛠️ Technology Stack

* **Language**: Python 3.14+
* **Framework**: Django 5.2 / 6.0+
* **Database**: SQLite3
* **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+)
* **Testing**: Django Test Runner

---

## 📁 Project Structure

```text
computer_repair/
│
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
│
├── computer_repair/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/          # Authentication & user roles
├── dashboard/         # Dashboard statistics & seed command
├── customers/         # Customer model, views, forms, urls
├── devices/           # Device model, views, forms, urls
├── repairs/           # Repair model, views, forms, receipt, urls
├── technicians/       # Technician model, views, forms, urls
├── payments/          # Payment model, validation, views, urls
├── expenses/          # Expense model, categories, views, urls
│
├── templates/         # Centralized HTML templates
│   ├── base.html
│   ├── registration/
│   ├── dashboard/
│   ├── customers/
│   ├── devices/
│   ├── repairs/
│   ├── technicians/
│   └── payments/
│
└── static/            # Static assets
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

---

## 💻 Installation & Setup

### 1. Clone or Open the Project Directory

```bash
cd "Computer Repair Management System  django"
```

### 2. Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
*(Or `pip install django`)*

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Load Demonstration Sample Data (Recommended)

Pre-populates the system with sample customers, devices, technicians, repairs, payments, and users:

```bash
python manage.py seed_data
```

This creates:
* **Admin user**: `admin` / `admin123`
* **Technician user**: `tech` / `tech123`
* Customers: Ahmed Ali, Mohamed Hassan, Abdi Yusuf
* Devices: Dell Latitude 7480, HP ProBook 450 G7, Lenovo ThinkPad T480, Epson EcoTank L3150
* Technicians: Mohamed Hassan, Abdi Omar
* Repairs: REP-0001 (Completed), REP-0002 (Repairing), REP-0003 (Pending), REP-0004 (Delivered)

*(Alternatively, to create your own manual superuser)*:
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to:
```text
http://127.0.0.1:8000/
```

Login with `admin` / `admin123`.

---

## 🧪 Running Unit Tests

Run the full automated test suite verifying customer CRUD, device links, repair sequential numbering, overpayment prevention, balance calculations, and dashboard loading:

```bash
python manage.py test
```

---

## 📄 Printable Receipt Example

To view and print a repair receipt:
1. Navigate to any repair detail page (e.g. `/repairs/1/`).
2. Click **Print Receipt** (or visit `/repairs/1/receipt/`).
3. Click the print button or press `Ctrl + P` / `Cmd + P`. The page automatically formats cleanly for receipt printers or standard paper.

---

## 🔐 Security & Simplicity Rules Followed

* All sensitive actions require authentication (`@login_required`).
* CSRF tokens protected on all POST forms.
* Clean Django ORM queries preventing SQL injection.
* Strict validation preventing negative costs and overpayments.
* Zero external bloated libraries — easy to understand, deploy, and explain in an academic setting.
