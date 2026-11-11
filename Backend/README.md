# PrimeCloud FastAPI Auth System (Mock)

A lightweight, production-structured FastAPI authentication service designed for quick deployment and testing on **PrimeCloud**.

It runs **without an external database** using an in-memory mock repository pre-seeded with test accounts.

---

## 🚀 Features

- **No DB Setup Required**: Operates using a fast, in-memory mock data store.
- **Pre-seeded Accounts**: Instant login ready for platform verification.
- **Single-step Password Reset**: Direct reset by email and new password.
- **Token-based Authentication**: Fast, opaque Bearer tokens (`prime_<uuid>`).
- **Interactive Swagger UI**: Full OpenAPI docs available at `/docs` with one-click authorization.
- **Platform Health Monitoring**: `/health` endpoint returning platform and memory state.
- **Cloud-Ready**: Includes `Procfile`, dynamic `PORT` binding, and CORS configuration.

---

## 🔑 Pre-Seeded Test Credentials

| Email | Password | Role |
| :--- | :--- | :--- |
| `test@primecloud.io` | `password123` | `admin` |
| `developer@primecloud.io` | `devpass456` | `developer` |

---

## 📁 Project Structure

```text
Backend/
├── main.py            # FastAPI app, endpoints, security middleware
├── mock_db.py         # In-memory mock store and seed data
├── schemas.py         # Pydantic request and response schemas
├── run.py             # Cloud startup script with PORT binding
├── Procfile           # PaaS process configuration for PrimeCloud
├── requirements.txt   # Python dependencies
└── README.md          # Documentation & cURL testing guide
```

---

## 🛠️ Local Development & Testing

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python run.py
# Or with uvicorn directly:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Open Interactive Docs
Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

---

## 📡 API Endpoints & cURL Examples

### 1. Health Check
```bash
curl -X GET http://localhost:8000/health
```

### 2. User Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@primecloud.io", "password": "password123"}'
```
*Response returns `"access_token": "prime_..."`*

### 3. Access Protected Route (`/auth/me`)
```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

### 4. User Signup
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Cloud", "email": "alice@primecloud.io", "password": "securepassword"}'
```

### 5. Password Reset (Single-step)
```bash
curl -X POST http://localhost:8000/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{"email": "test@primecloud.io", "new_password": "newpassword123"}'
```

### 6. Logout
```bash
curl -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

---

## ☁️ PrimeCloud Deployment

### Environment Variables
- `PORT`: Automatically read by `run.py` and `Procfile` (defaults to `8000`).
- `CLOUD_PLATFORM`: Optional label displayed in `/health` (defaults to `"PrimeCloud"`).

### Startup Command
If PrimeCloud asks for a start command:
```bash
python run.py
```
Or via uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```
