# Hospital Management System (Full‑Stack)

Monorepo with Next.js frontend and FastAPI backend.

## Backend

```bash
cd backend
python3 -m pip install --user -r requirements.txt
python3 -m uvicorn app.main:app --reload --port 8000
```

Seed demo data (optional):

```bash
python3 -m app.seed
```

## Frontend

```bash
npm install
npm run dev
```

Open http://localhost:3000. Frontend rewrites `/api/*` to `http://localhost:8000/api/*`.

## Auth

- Register: POST `/api/auth/register` (email, password, full_name, role)
- Login: POST `/api/auth/login` (OAuth2 form) → bearer token

## Core endpoints

- Patients: GET/POST `/api/patients`
- Departments: GET/POST `/api/departments`
- Appointments: GET/POST `/api/appointments`
- Doctors, Rooms, Admissions, Prescriptions, Lab Tests, Vitals, Medical Records
- Billing: invoices, items, payments
- Inventory: items CRUD