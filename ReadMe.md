# TelecomOS — Mini Telecom Provisioning Platform

A Django-based telecom operations system that simulates real-world management of customer accounts, network lines, billing, and automated service control.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Tech Stack](#tech-stack)
3. [Setup Instructions](#setup-instructions)
4. [Running the Project](#running-the-project)
5. [Frontend Pages](#frontend-pages)
6. [API Endpoints](#api-endpoints)
7. [Management Commands](#management-commands)
8. [System Behaviour](#system-behaviour)
9. [Project Structure](#project-structure)

---

## System Overview

TelecomOS is a mini provisioning platform that supports:

- Customer account creation and management
- Line (SIM/service) provisioning, activation, and suspension
- Plan assignment and monthly billing simulation
- Automatic arrears detection when invoices go overdue
- Automatic line suspension when an account falls into arrears
- Automatic line restoration when payment is made

The system uses Django Signals to automate suspension and restoration — no manual intervention required once billing runs.

---

## Tech Stack

- Python 3.10+
- Django
- Django REST Framework
- SQLite (default database)
- Vue.js 3 (via CDN — no build tools required)

---

## Setup Instructions

### 1. Clone the project

```bash
git clone <your-repo-url>
cd telecom_platform
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django djangorestframework
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (optional, for admin panel access)

```bash
python manage.py createsuperuser
```

---

## Running the Project

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

---

## Frontend Pages

| Page | URL | Description |
|---|---|---|
| Account List | `/accounts/` | View all accounts with status and arrears indicator |
| Account Detail | `/accounts/<id>/` | View a single account's lines and invoices with pay button |
| Line List | `/lines/` | View all lines with activate, suspend, and restore buttons |
| Invoice List | `/invoices/` | View all invoices with overdue indicator and pay button |
| Plan List | `/plans/` | View, add, and delete plans |
| Admin Panel | `/admin/` | Full Django admin interface |
| Browsable API | `/api/` | Django REST Framework browsable API |

---

## API Endpoints

### Accounts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/accounts/` | List all accounts |
| POST | `/api/accounts/` | Create a new account |
| GET | `/api/accounts/<id>/` | Retrieve a single account |
| PUT | `/api/accounts/<id>/` | Update an account |
| DELETE | `/api/accounts/<id>/` | Delete an account |

### Lines

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/lines/` | List all lines |
| POST | `/api/lines/` | Create a new line |
| GET | `/api/lines/<id>/` | Retrieve a single line |
| PUT | `/api/lines/<id>/` | Update a line |
| DELETE | `/api/lines/<id>/` | Delete a line |
| POST | `/api/lines/<id>/activate/` | Activate a provisioned line |
| POST | `/api/lines/<id>/suspend/` | Suspend an active line |
| POST | `/api/lines/<id>/restore/` | Restore a suspended line |

### Plans

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/plans/` | List all plans |
| POST | `/api/plans/` | Create a new plan |
| GET | `/api/plans/<id>/` | Retrieve a single plan |
| PUT | `/api/plans/<id>/` | Update a plan |
| DELETE | `/api/plans/<id>/` | Delete a plan |

### Invoices

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/invoices/` | List all invoices |
| POST | `/api/invoices/` | Create a new invoice manually |
| GET | `/api/invoices/<id>/` | Retrieve a single invoice |
| POST | `/api/invoices/<id>/pay/` | Mark an invoice as paid |
| POST | `/api/invoices/generate_for_account/` | Generate invoice for a single account |
| POST | `/api/invoices/generate_monthly_invoices/` | Generate invoices for all active accounts |
| POST | `/api/invoices/run_arrears_check/` | Detect overdue invoices and flag accounts |

#### Example: Generate invoice for a single account

```json
POST /api/invoices/generate_for_account/
{
    "account_id": 1
}
```

---

## Management Commands

Run these from the terminal in your project root with the virtual environment active.

```bash
# Generate monthly invoices for all active accounts
python manage.py generate_invoices

# Check for overdue invoices and flag accounts in arrears
python manage.py check_arrears

# Suspend all active lines for accounts in arrears
python manage.py block_lines

# Simulate payment for a specific invoice
python manage.py simulate_payment <invoice_id>
```

### Typical monthly workflow

```bash
python manage.py generate_invoices     # Run at start of month
python manage.py check_arrears         # Run after due dates pass
python manage.py block_lines           # Enforce suspensions
python manage.py simulate_payment 1    # When customer pays
```

---

## System Behaviour

### Full billing lifecycle

```
1. Account created
2. Line provisioned and activated
3. Plan assigned to line
4. Invoice generated (monthly fee x active lines)
5. Invoice goes overdue (due_date passes unpaid)
6. Arrears check runs → account flagged as in arrears
7. Signal fires → all active lines suspended automatically
8. Customer pays invoice
9. Arrears cleared (if no remaining unpaid invoices)
10. Signal fires → all suspended lines restored automatically
```

### Automatic suspension (Django Signal)

When `account.is_in_arrears` is set to `True`, a `post_save` signal fires and suspends all active lines on that account instantly — no manual step required.

### Automatic restoration (Django Signal)

When `account.is_in_arrears` is set to `False` (after payment clears all unpaid invoices), the same signal fires and restores all suspended lines.

### Arrears detection logic

An account is flagged as in arrears when it has at least one invoice where:
- `is_paid = False`
- `due_date < today`

---

## Project Structure

```
telecom_platform/
├── core/                   # Django project settings and URLs
├── accounts/               # Customer account management
│   ├── models.py           # Account model
│   ├── views.py            # API and template views
│   ├── serializers.py      # DRF serializers
│   ├── services.py         # Business logic
│   ├── signals.py          # Auto suspend/restore on arrears change
│   └── urls.py
├── lines/                  # Line provisioning and management
│   ├── models.py           # Line model
│   ├── views.py
│   ├── serializers.py
│   ├── services.py         # Provision, activate, suspend, restore
│   └── urls.py
├── billing/                # Plans, invoices, and billing logic
│   ├── models.py           # Plan and Invoice models
│   ├── views.py
│   ├── serializers.py
│   ├── services.py         # Invoice generation, arrears detection
│   ├── urls.py
│   └── management/
│       └── commands/
│           ├── generate_invoices.py
│           ├── check_arrears.py
│           ├── block_lines.py
│           └── simulate_payment.py
├── authentication/         # Authentication app
├── templates/              # Vue.js frontend templates
│   ├── base.html
│   ├── accounts/
│   │   ├── account_list.html
│   │   └── account_detail.html
│   └── billing/
│       ├── invoice_list.html
│       └── plan_list.html
└── manage.py
```