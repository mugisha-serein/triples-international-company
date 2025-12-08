E-Commerce Backend (Django + DRF + PostgreSQL) - Triple S International Company Ltd

This is the backend API for a family-owned e-commerce platform used to manage and sell laptops, desktops, monitors, and accessories.
The system is built with Django, Django REST Framework, and PostgreSQL, focusing on clean architecture, security, and scalability.

Features
  Users & Authentication
  User registration
  Login with JWT
  Profile management
  Permission-based access
  Secure password hashing

Products
  Add/update/delete products
  Manage brands & categories
  Product images (upload support)
  Search & filtering
  Stock management

Cart
  Add products to cart
  Update quantities
  Remove items
  Cart total calculation
  Per-user isolated session

Orders
  Create orders from cart
  Track status (pending → shipped → delivered)
  Order history
  Admin/Staff visibility

Payments
  integration structure included
  Ready for Stripe, Flutterwave, PayPal, etc.
  Payment verification logic scaffolded

Notifications
  Order confirmation email
  Email templates included
  Auto-send on new order creation

Tech Stack
  Backend Framework	Django 5 + Django REST Framework
  Database	PostgreSQL
  Auth	JWT (SimpleJWT)
  Email	Django Email Backend
  Storage	Local media or cloud (S3-ready)
  Project Structure
    backend/
    │
    ├── users/        # Authentication, profiles
    ├── products/     # Product, brand, category
    ├── cart/         # Cart logic per user
    ├── orders/       # Orders, checkout, email notifications
    ├── payments/     # Payment integration (optional)
    │
    ├── backend/      # Settings, URLs, configs
    └── media/        # Uploaded product images

Environment Setup
  1. Create virtual environment
    python -m venv venv
    source venv/bin/activate      # Linux/Mac
    venv\Scripts\activate         # Windows
  
  2. Install dependencies
  pip install -r requirements.txt
  
  3. Create .env file
    SECRET_KEY=your_secret_key
    DEBUG=True
    DATABASE_NAME=ecommerce
    DATABASE_USER=postgres
    DATABASE_PASSWORD=your_password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    EMAIL_HOST=smtp.gmail.com
    EMAIL_HOST_USER=your_email
    EMAIL_HOST_PASSWORD=your_app_password
    EMAIL_PORT=587
    EMAIL_USE_TLS=True

Database Setup (PostgreSQL)
  Create DB:
    CREATE DATABASE ecommerce;


  Ensure user has permissions:
    GRANT ALL PRIVILEGES ON DATABASE ecommerce TO postgres;


Run migrations:
  python manage.py migrate

Running the Server
  python manage.py runserver

Authentication (JWT)
  Login
    POST → /api/auth/login/
  
  Register
    POST → /api/auth/register/
    Uses access + refresh tokens.

Core API Endpoints
  Users
    POST /api/auth/register/
    POST /api/auth/login/
    GET  /api/users/me/
  
  Products
    GET    /api/products/
    POST   /api/products/
    GET    /api/products/:id/
    POST   /api/products/:id/upload-image/
  
  Cart
    POST   /api/cart/add/
    GET    /api/cart/
    PATCH  /api/cart/update/
    DELETE /api/cart/remove/
  
  Orders
    POST  /api/orders/create/
    GET   /api/orders/
    GET   /api/orders/:id/
  
  Payments (optional)
    POST  /api/payments/initiate/
    POST  /api/payments/verify/

Order Email Notification
  When an order is created, the system automatically sends:
  Customer order receipt
  Order details summary
  Expected delivery timeline
  Uses Django’s built-in email backend.

Security Features
  JWT authentication
  No shared data between users
  CSRF-safe APIs
  Secure password hashing
  Only owners can modify their data
  Validation on all endpoints
  Product image upload sanitization

Code Quality
  Black formatting
  DRF serializers
  Modular app structure
  Custom user model
  Clean admin integration
  Proper separation of concerns

Future Enhancements
  Wishlist system
  Admin dashboard
  Discounts & coupons
  Multi-language support
  Inventory analytics

🏁 Conclusion
This backend is clean, scalable, and production-ready.
It isolates every user, enforces secure authentication, provides full e-commerce flows, and integrates solid email notifications.
