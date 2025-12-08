E-Commerce Backend

This backend is the engine of an online store for selling electronic devices, and accessories.

It handles users, products, carts, orders, payments integration and emails.

This README explains everything.

✅ What This Backend Does
1. Users

People can create an account

They can log in

They can update their profile

They get their own private data

No user can see another user’s information

2. Products

Admin can add products

Products have names, price, brand, category, description and images

Users can view all products

Users can view single product details

3. Cart

Each user has their own cart

They can add items

Update quantity

Remove items

The cart total updates automatically

4. Orders

Users can place an order

Order summary is saved

Order status updates (Pending → Completed)

User can view all their past orders

5. Emails

When a user places an order, they receive a confirmation email

🛠️ Technologies Used

Django — main backend framework

Django REST Framework — builds APIs

PostgreSQL — database

JWT — secure login system

Email Backend — sends emails when orders are made

🚀 How to Run the Backend
1. Install required packages
pip install -r requirements.txt

2. Set up the database (PostgreSQL)

Create a database:

CREATE DATABASE triples;

3. Run database migrations
python manage.py migrate

4. Start the server
python manage.py runserver


The API will be available at:

http://127.0.0.1:8000/

📌 Main API Endpoints
Users

/api/users/register/ → Create account

/api/users/login/ → Login

/api/users/profile/ → View profile

Products

/api/products/ → List products

/api/products/<id>/ → View product

/api/products/<id>/upload-image/ → Upload image

Cart

/api/cart/ → View cart

/api/cart/add/ → Add product to cart

/api/cart/update/ → Update cart

/api/cart/remove/ → Remove item

Orders

/api/orders/create/ → Place order

/api/orders/ → List user orders

/api/orders/<id>/ → Order details

🔒 Security

Every user has their own private account

Only account owners can change their info

Carts and orders belong to the logged-in user

Passwords are encrypted

API protected with secure tokens (JWT)

📦 Folders Explanation
backend/
│
├── users/        = login, register, profiles
├── products/     = product management
├── cart/         = user carts
├── orders/       = orders and checkout
├── payments/     = future payment integration
└── media/        = product images

🎯 Purpose of This Backend

This backend provides a strong foundation for:

online store

mobile app

inventory system

business website with e-commerce features

It is clean, safe, and ready for real users.

📞 Need Help?

You can build the frontend separately using React, Flutter, or any UI framework.
