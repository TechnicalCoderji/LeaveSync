# LeaveSync 🗓️

**LeaveSync** is a lightweight, internal organization management web application built with Python and Django. It simplifies the employee leave request process by allowing employees to apply for time off while enabling managers to review, approve, or reject requests for their specific organization.

---

## 🌟 Key Features

### 🏢 Organization-Based Roles

* **Manager:**
  * Registers a new organization upon sign-up.
  * Views a centralized dashboard of all leave requests submitted by employees within their organization.
  * Approves or rejects pending leave requests.

* **Employee:**
  * Registers under an existing organization name.
  * Views personal leave application history along with current status (`Pending`, `Approved`, `Rejected`).
  * Submits new leave requests specifying the start date, end date, and reason.
  * Tracks remaining allowed annual leave days.

### 🧮 Smart Business Logic

* **Automatic Weekend Calculation:** Automatically calculates total leave duration between the start date and end date while **excluding weekends** (Saturdays and Sundays).
* **Leave Balance Deduction:** Deducts only valid working days from the employee's total available leave balance.

---

## 🛠️ Tech Stack

* **Language:** Python `3.11.4`
* **Framework:** Django
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap

---

## 📁 Project Directory Structure

```text
LeaveSync/
├── accounts/          # User authentication, organization creation, and role management
├── app/               # Main business logic (leave requests, approvals, balance deduction)
├── config/            # Main Django configuration, settings, and root URLs
├── static/            # Static assets (custom CSS, JS files, images)
├── templates/         # Jinja/Django HTML templates
├── .gitignore         # Specifies intentionally untracked files to ignore
├── db.sqlite3         # SQLite database file
├── LICENSE            # MIT License file
├── manage.py          # Django project management script
├── README.md          # Project documentation
└── requirements.txt   # Python dependency requirements
```

---

## 🚀 Getting Started

Follow these step-by-step instructions to get a local development environment up and running.

### Prerequisites

* **Python 3.11.4** installed on your system.
* **Git** installed on your system.

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/TechnicalCoderji/LeaveSync.git
   cd LeaveSync
   ```

2. **Create a Virtual Environment**

   * **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   * **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser (Optional - Django Admin Access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**

   Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 🔄 App Workflow

1. **Manager Sign Up:** A manager creates an account and specifies a new **Organization Name**.
2. **Employee Sign Up:** Employees register using the **exact Organization Name** created by their manager.
3. **Submitting Requests:** Employees log in, check their available leave balance, and submit leave requests.
4. **Approval Process:** Managers log into their organization dashboard to review pending requests and approve or reject them.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.