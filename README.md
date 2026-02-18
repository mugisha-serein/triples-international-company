# TripleS Backend API

A robust, production-ready e-commerce backend built with Django and Django Rest Framework (DRF). This system features a secure service-oriented architecture, atomic transactions for critical operations, and comprehensive API documentation.

## 🚀 Key Features

### 🛡️ Security & Authentication
- **Custom User Model**: Extended `AbstractUser` for flexibility.
- **JWT Authentication**: Secure stateless authentication using `SimpleJWT` with token rotation and blacklisting.
- **Throttling**: Granular rate limiting to prevent abuse:
  - `auth`: 5/minute (Login/Register)
  - `product_search`: 60/minute
  - `payment_attempt`: 3/minute
  - `checkout_attempt`: 2/minute
  - `cart_operations`: 20/minute
- **Global Exception Handling**: Standardized JSON error responses hiding sensitive server details.
- **Security Headers**: Configured via `django-cors-headers` and Django's security middleware.

### 🏗️ Architecture & Performance
- **Service Layer Pattern**: Business logic is decoupled from Views into `services.py` for each app (`users`, `products`, `orders`, `payments`, `cart`), ensuring testability and reusability.
- **Atomic Transactions**: Critical flows like Checkout and Payment use `transaction.atomic()` and `select_for_update()` to prevent race conditions and ensure data integrity.
- **Query Optimization**: Extensive use of `select_related` and `prefetch_related` (including `Prefetch` objects) to eliminate N+1 query problems.
- **Caching**: Product lists and details are cached (5 minutes) to reduce database load.

### 🧩 Core Modules
- **Users**: Registration, Profile management, Secure secure.
- **Products**: Category/Brand management, Image validation, Stock tracking.
- **Cart**: Server-side cart management with stock validation.
- **Orders**: Atomic checkout process, Stock reservation, Email notifications.
- **Payments**: Transaction recording, Integration placeholders for gateways.

## 🛠️ Tech Stack

- **Framework**: Django 6.0
- **API**: Django Rest Framework (DRF)
- **Database**: PostgreSQL
- **Documentation**: OpenAPI 3.0 via `drf-spectacular`
- **Authentication**: `djangorestframework-simplejwt`
- **Utilities**: `django-filter`, `python-dotenv`, `Pillow`

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- PostgreSQL

### 1. Clone the Repository
```bash
git clone <repository-url>
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv env
# Windows
.\env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:

```env
SECRET_KEY=your-super-secret-key-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=triples_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Server
```bash
python manage.py runserver
```

## � API Documentation

The API is fully documented using OpenAPI 3.0. Once the server is running, visit:

- **Swagger UI**: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
- **ReDoc**: [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)
- **Schema YAML**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

## 🧪 Testing

The project includes a comprehensive test suite using Django's test runner and SQLite (for speed).

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test products
python manage.py test orders
python manage.py test payments
python manage.py test cart
```

## 📂 Project Structure

```
backend/
├── cart/           # Cart management service
├── orders/         # Order processing & transactional logic
├── payments/       # Payment recording & gateway integration
├── products/       # Product catalog & stock management
├── triples/        # Project settings & configuration
├── users/          # User authentication & profiles
├── manage.py       # Django CLI entry point
└── requirements.txt
```
