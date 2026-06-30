# WebHawk Lite — Security Middleware SaaS

WebHawk Lite is a Python Flask backend project that works like a small Web Application Firewall. It sits between the client and the real backend server. Every request goes first to WebHawk. WebHawk checks the request for possible attacks, then either forwards the safe request to the real backend or blocks the dangerous request and saves it in security logs.

The project protects backend applications from common web attacks such as:

- SQL Injection
- XSS — Cross Site Scripting
- Rate Limiting attacks

This project is educational and demonstrates the main idea of a middleware security layer similar to a lightweight WAF.

---

## Project idea

Normal backend flow:

```text
User → Backend Server
WebHawk flow:
User → WebHawk → Backend Server
WebHawk checks:
Request body
Query parameters
Path
Headers
IP address
Then:
Safe request: forwarded to the registered backend
Dangerous request: blocked and saved in security logs
Main features
User registration and login
Password hashing with bcrypt
JWT authentication
Active user sessions
Logout and token/session deactivation
Backend registration
API key generation for each backend
SQL Injection detection
XSS detection
Rate limiting by IP and endpoint
Proxy middleware endpoint
Security logs
Analytics endpoints
Vulnerable demo backend
Docker Compose setup with PostgreSQL
Postico connection support
Postman-ready API flow
Project architecture
webhawk-lite/
│
├── app/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── security/
│   ├── services/
│   ├── utils/
│   ├── config.py
│   └── extensions.py
│
├── migrations/
├── vulnerable_backend/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── run.py
The project is separated into layers:
routes: API endpoints
services: business logic
repositories: database operations
models: database tables
security: attack detection and rate limiting logic
vulnerable_backend: small backend used for testing the proxy
Database tables
The project uses five main tables.
users
Stores WebHawk users.
Important columns:
id
name
email
password_hash
created_at
updated_at
user_sessions
Stores active login sessions and JWT token hashes.
Important columns:
id
user_id
token_hash
ip_address
created_at
expires_at
is_active
backend_registration
Stores backend services registered by users.
Important columns:
id
user_id
service_name
target_url
api_key
is_active
created_at
updated_at
security_logs
Stores scanned requests and blocked attacks.
Important columns:
id
backend_id
ip_address
method
endpoint
attack_type
is_blocked
request_data
created_at
rate_limit
Stores rate limiting data per backend, IP address, and endpoint.
Important columns:
id
backend_id
ip_address
endpoint
request_count
window_start
blocked_until
is_blocked
API endpoints
Authentication
Method	Endpoint	Description
POST	/auth/register	Register a new user
POST	/auth/login	Login and receive JWT
POST	/auth/logout	Logout and deactivate session
GET	/auth/sessions	View active sessions
GET	/auth/me	View current logged-in user

Backend registration
Method	Endpoint	Description
POST	/backends	Register new backend
GET	/backends	Get all user backends
GET	/backends/{id}	Get one backend
PUT	/backends/{id}	Update backend
DELETE	/backends/{id}	Disable backend

Security and proxy
Method	Endpoint	Description
POST	/security/scan	Manually scan request data
ANY	/proxy/{api_key}/{path}	Main middleware proxy
GET	/logs/security	View security logs

Analytics
Method	Endpoint	Description
GET	/analytics/summary	Total scanned, blocked, and allowed requests
GET	/analytics/attacks-by-type	Attack statistics by type
GET	/analytics/recent-attacks	Recent blocked attacks

Health
Method	Endpoint	Description
GET	/health	Check if WebHawk is running

Run locally without Docker
1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
2. Install requirements
pip install -r requirements.txt
3. Create .env
You can copy from .env.example:
cp .env.example .env
For simple local development, use SQLite:
DATABASE_URL=sqlite:///webhawk.db
4. Run database migrations
flask --app run.py db upgrade
5. Start WebHawk
flask --app run.py run --debug --port 8000
WebHawk will run on:
http://localhost:8000
6. Start vulnerable backend
Open another terminal:
cd ~/Desktop/python_project
source .venv/bin/activate
python vulnerable_backend/app.py
The vulnerable backend will run on:
http://localhost:5001
Run with Docker
The project can run using Docker Compose with three services:
WebHawk API
PostgreSQL database
Vulnerable backend
Start everything:
docker compose up --build
Docker services:
Service	URL
WebHawk API	http://localhost:5050
Vulnerable backend	http://localhost:5001
PostgreSQL	localhost:5433

Check WebHawk:
curl http://localhost:5050/health
Expected result:
{
  "environment": "production",
  "service": "WebHawk Lite",
  "status": "ok"
}
Stop Docker:
docker compose down
Postico database connection
When using Docker, connect Postico to PostgreSQL using:
Host: localhost
Port: 5433
Database: webhawk
User: webhawk
Password: webhawk_password
Important backend target URLs
When running locally without Docker, register the vulnerable backend as:
{
  "service_name": "Local Demo Backend",
  "target_url": "http://localhost:5001"
}
When running inside Docker, register the vulnerable backend as:
{
  "service_name": "Docker Demo Backend",
  "target_url": "http://vulnerable-backend:5001"
}
This difference is important because Docker services communicate using service names.
Demo flow
Step 1: Register user
POST /auth/register
Example body:
{
  "name": "Demo User",
  "email": "demo@example.com",
  "password": "Password123!"
}
Step 2: Login
POST /auth/login
Example body:
{
  "email": "demo@example.com",
  "password": "Password123!"
}
The response returns a JWT token. Use it as:
Authorization: Bearer YOUR_TOKEN
Step 3: Register backend
POST /backends
Example body for local run:
{
  "service_name": "Demo Store",
  "target_url": "http://localhost:5001"
}
The response returns an API key like:
webhawk_abc123
Step 4: Send safe request through WebHawk
GET /proxy/API_KEY/products?category=phones
Expected result:
Request is allowed
Request is forwarded to vulnerable backend
Product data is returned
Step 5: Send SQL Injection attack
GET /proxy/API_KEY/products?id=' OR 1=1 --
Expected result:
{
  "status": "blocked",
  "attack_type": "SQL_INJECTION",
  "message": "Request blocked by WebHawk"
}
Step 6: Send XSS attack
POST /proxy/API_KEY/comments
Example body:
{
  "comment": "<script>alert(1)</script>"
}
Expected result:
{
  "status": "blocked",
  "attack_type": "XSS",
  "message": "Request blocked by WebHawk"
}
Step 7: Trigger rate limiting
Send more than the allowed number of requests from the same IP in one minute.
Expected result:
{
  "status": "blocked",
  "attack_type": "RATE_LIMIT",
  "message": "Request blocked by rate limiter"
}
Step 8: View logs
GET /logs/security
Step 9: View analytics
GET /analytics/summary
GET /analytics/attacks-by-type
GET /analytics/recent-attacks
Security detection examples
SQL Injection patterns
WebHawk detects examples like:
' OR 1=1 --
UNION SELECT
DROP TABLE
INSERT INTO
DELETE FROM
XSS patterns
WebHawk detects examples like:
<script>alert(1)</script>
<img src=x onerror=alert(1)>
javascript:
onerror=
onclick=
Testing
Run:
python3 -m pytest
If there are no test files yet, this command will show no tests collected. The project can still be tested manually using the demo flow and Postman.
Environment variables
Variable	Description
APP_ENV	development, testing, or production
SECRET_KEY	Flask secret key
JWT_SECRET_KEY	JWT signing secret
DATABASE_URL	Database connection URL
JWT_EXPIRATION_HOURS	JWT expiration time
RATE_LIMIT_REQUESTS	Max requests in the time window
RATE_LIMIT_WINDOW_SECONDS	Rate limit time window
RATE_LIMIT_BLOCK_SECONDS	Block duration after rate limit
PROXY_TIMEOUT_SECONDS	Timeout when forwarding request
MAX_CONTENT_LENGTH	Maximum request body size

Project status
Completed:
User authentication
JWT login
Logout and sessions
Backend registration
API key generation
SQL Injection scanner
XSS scanner
Security logs
Analytics endpoints
Proxy middleware
Rate limiting
Vulnerable backend
Docker Compose setup
PostgreSQL setup
Team contribution
Team member	Contribution
Abdallah	Authentication, backend registration, Docker setup, documentation
Yazan	Security scanner, proxy middleware, rate limiting, demo backend

Notes
WebHawk Lite is an educational project. It demonstrates how security middleware works, but it is not a replacement for a production Web Application Firewall. Real systems should also use prepared SQL statements, input validation, output encoding, HTTPS, secure headers, and production-grade monitoring.

Then save and run:

```bash
git status
docker compose config
If docker compose config still passes, you can test Docker and commit.