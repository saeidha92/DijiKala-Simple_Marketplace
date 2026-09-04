<div align="center">

# 🛍️ DijiKala — Simple Marketplace

**A small e-commerce demo built with Django — sellers create stores & sell products, customers shop, cart, and checkout.**

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-blueviolet?style=for-the-badge)

</div>

---

<div align="center">
  <img src="docs/demo.gif" alt="DijiKala demo walkthrough" width="800">
  <p><em>Full walkthrough: sign up → create store → add product → shop → checkout</em></p>
</div>

---

## ✨ Features

| 👤 Role         | What they can do                                                                           |
| --------------- | ------------------------------------------------------------------------------------------ |
| 🛠️ **Admin**    | Full access via Django admin — manage all users, stores, products & orders                 |
| 🏪 **Seller**   | Create stores, add/edit products, track store balance                                      |
| 🛒 **Customer** | Browse products, search & filter, add to cart, top up wallet, checkout, view order history |

### 🎁 Bonus features

- 🔍 Product **search bar**
- 🏷️ Product **categories**
- 🖼️ Product **image upload**
- 📦 Basic **stock/inventory** management
- 🎉 **"Thank you"** page after checkout

---

## 🧰 Tech Stack

<div align="center">

| Layer    | Technology                                                                                                       |
| -------- | ---------------------------------------------------------------------------------------------------------------- |
| Backend  | ![Django](https://img.shields.io/badge/-Django-092E20?style=flat-square&logo=django&logoColor=white)             |
| Database | ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white) |
| Frontend | Server-rendered templates + custom CSS (no frontend framework)                                                   |
| Auth     | Django's built-in authentication system                                                                          |

</div>

---

## 📂 Project Structure

```
dijikala_marketplace/
├── 🗂️ dijikala_marketplace/   # Project settings, root urls.py
├── 🗂️ market/                 # Main app
│   ├── models.py             # SellerProfile, CustomerProfile, Store,
│   │                          #   Category, Product, CartItem, Order, OrderItem
│   ├── views.py               # All page logic (function-based views)
│   ├── forms.py                # Signup, Store, Product, Add-balance forms
│   ├── urls.py                 # market:* url names
│   ├── admin.py                 # Django admin registrations
│   └── tests.py                  # Automated tests for the core flows
├── 🗂️ templates/               # HTML templates (base.html + one per page)
├── 🗂️ static/css/style.css      # Shared minimal/modern theme
├── 🗂️ media/                    # Uploaded product images (created at runtime)
├── 📄 requirements.txt
├── 📄 .env                       # Local secrets (never committed)
└── 📄 manage.py
```

---

## 🚀 Getting Started

### 1️⃣ Clone & set up a virtual environment

```bash
git clone https://github.com/saeidha92/DijiKala-Simple_Marketplace.git
cd DijiKala-Simple_Marketplace

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure your database

Create a `.env` file in the project root:

```ini
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=dijikala_db
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432
```

> 💡 Make sure a matching empty database (`dijikala_db`) already exists in PostgreSQL / pgAdmin4.

### 4️⃣ Migrate & run 🎉

```bash
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Open **http://127.0.0.1:8000/** 🌐 — the Django admin panel is at **/admin/**.

---

## ✅ Running the Tests

```bash
python manage.py test market
```

Covers: the landing page listing products, a customer adding a product to
cart & checking out (with balance + stock + store-balance updates), a
seller creating a new store, and access control between roles.

<div align="center">

```
Found 5 test(s).
Ran 5 tests in 2.467s

OK ✅
```

</div>

---

## 🗺️ URL Map

| URL                                               | Page                                                                   |
| ------------------------------------------------- | ---------------------------------------------------------------------- |
| `/`                                               | 🏠 Landing page — all products, newest first, search & category filter |
| `/stores/`                                        | 🏬 List of all stores                                                  |
| `/stores/<id>/`                                   | 🔍 Store detail — products + "＋ Add Product" for the owner            |
| `/seller/`                                        | 🏪 Seller panel — the seller's own stores                              |
| `/seller/store/create/`                           | ➕ Create a new store                                                  |
| `/seller/store/<id>/add-product/`                 | ➕ Add a product to a store                                            |
| `/customer/`                                      | 👤 Customer panel — name, phone, balance, quick actions                |
| `/customer/orders/`                               | 📜 Order history                                                       |
| `/cart/`                                          | 🛒 Cart — remove items, checkout                                       |
| `/payment/`                                       | 💳 Add balance (demo top-up form)                                      |
| `/signup/` `/accounts/login/` `/accounts/logout/` | 🔐 Auth pages                                                          |
| `/admin/`                                         | ⚙️ Django admin                                                        |

---

## 📝 Notes / Limitations

> This is a learning project, so a few things are intentionally simplified:

- 💳 "Payment" and "checkout" only move numbers around in the database — no real payment processor.
- 🏪 There's no separate seller wallet model beyond `Store.balance`; a completed order credits the store and reduces product stock as demo logic.
- 🎨 Styling is intentionally minimal, since the assignment prioritizes models/views/URLs over visual design.

---

<div align="center">

Made with 🐍 + 🎯 as a Django class project

</div>
