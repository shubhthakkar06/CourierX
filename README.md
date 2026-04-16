CourierX — Fast Track Courier Management System
================================================

A full-featured **CLI-based courier management system** built with Python and MySQL.

## Features

| Feature | Details |
|---|---|
| 🔐 **Authentication** | Sign up / Sign in with email, password policy, recovery code |
| 📦 **Order Management** | Place, view, modify, track, and cancel courier orders |
| 🏠 **Address Book** | Add, select, and update delivery addresses |
| 👤 **Profile** | Update username, email, password, DOB — delete account |
| 🛡️ **Admin Panel** | View Users, Addresses, Orders tables |
| 📊 **Feedback Analytics** | Pie chart feedback visualisation via Matplotlib |
| 🔒 **Security** | Wrong-password lockout (3 attempts before forced reset) |

## Project Structure

```
CourierX/
│
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── README.md
│
├── backend/                 # All backend logic
│   ├── __init__.py
│   ├── db.py                # MySQL connection
│   ├── validation.py        # Input validators (username, password, DOB, address)
│   ├── auth.py              # Sign up / Sign in / password & userid reset
│   ├── orders.py            # Order placement, tracking, modification, cancellation
│   ├── address.py           # Address CRUD
│   ├── profile.py           # User profile management
│   ├── admin.py             # Admin login + dashboard
│   ├── navigation.py        # Home screen, menu, About Us
│   └── utils.py             # Date helpers, delivery ID generator, CSV login log
│
├── frontend/                # Web frontend (coming soon)
│   ├── __init__.py
│   └── index.html           # Placeholder page
│
└── Project.py               # Original monolithic file (kept for reference)
```

## Getting Started

### Prerequisites
- Python 3.9+
- MySQL Server running locally
- Database named `Project` with the required tables

### Installation

```bash
# Clone the repository
git clone https://github.com/shubhthakkar06/CourierX.git
cd CourierX

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate   # macOS / Linux
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
python main.py
```

## Database Schema

| Table | Key Columns |
|---|---|
| `user` | userid, username, password, DOB, recoverycode |
| `addresses` | userid, pincode, reciever_name, reciever_city, reciever_street, reciever_house, reciever_no |
| `orders` | orderID, address, weight, price, order_date, userid |
| `delivery` | orderid, delivery_no |
| `feedback` | review, orderid |
| `wpd` | attemps |
| `wtscale` | min_weight, max_weight, price |

## Tech Stack

- **Language:** Python 3
- **Database:** MySQL (`mysql-connector-python`)
- **CLI Table Rendering:** `tabulate`
- **Data Visualisation:** `matplotlib`
- **Image Display:** `Pillow`

## Author

**Shubh Thakkar** — [GitHub](https://github.com/shubhthakkar06)
