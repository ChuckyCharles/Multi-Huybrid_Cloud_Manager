# Multi/Hybrid Cloud Management Platform

A common platform for managing resources across multiple cloud providers (public, private, and Kubernetes) and on-premise infrastructure. This project provides a single dashboard for cloud operations, resource inventory, cost tracking, and user management.

---

## Screenshots

### Dashboard Overview
![Dashboard](Frontend/Charles_v3/src/assets/shot1.png)

### User Profile & Cloud Access
![Profile](Frontend/Charles_v3/src/assets/shot2.png)

### Infrastructure Inventory & AWS Integration
![Inventory](Frontend/Charles_v3/src/assets/shot3.png)

---

## Key Features
- **Single Dashboard:** View and manage resources from AWS, Azure, GCP, on-premise, and Kubernetes clusters.
- **Resource Inventory:** Track cloud and on-premise resources, VMs, Kubernetes pods, and network components.
- **Cost Tracking:** Monitor monthly cloud spend across providers.
- **User Management:** Profile, security, and cloud access management.
- **Recent Activity & Health:** View recent actions and resource health at a glance.

---

## Project Structure
- `Backened/` — FastAPI backend for API, authentication, and cloud integrations
- `Frontend/` — React + Vite + TailwindCSS frontend dashboard

---

## Quick Start

### Backend
1. Navigate to `Backened/`
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables (`.env` file)
5. Initialize the database:
   ```bash
   alembic upgrade head
   ```
6. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend
1. Navigate to `Frontend/Charles_v3/`
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

---

## License
MIT License

---

## Credits
Designed and developed by CharlesCharley and contributors. 