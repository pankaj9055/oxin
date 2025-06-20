# Oxin Crypto Mining Platform

A futuristic web-based cryptocurrency mining platform built with Flask and PostgreSQL.

## Features

- User registration and authentication
- 24-hour mining sessions with OXC token rewards
- Referral system with bonus rewards
- Paid plan upgrades with USDT payments
- Admin dashboard for user and payment management
- Dark neon theme with cyberpunk design

## Deployment on Render

### 1. Connect Repository
- Fork or upload this repository to GitHub
- Connect your GitHub account to Render
- Create a new Web Service from your repository

### 2. Environment Variables
Add these environment variables in Render dashboard:

```
DATABASE_URL=your_postgresql_connection_string
SESSION_SECRET=your_random_secret_key
FLASK_ENV=production
```

### 3. PostgreSQL Database
- Create a PostgreSQL database on Render
- Copy the DATABASE_URL from your Render PostgreSQL dashboard
- Add it to your web service environment variables

### 4. Build Settings
- Build Command: `./build.sh`
- Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 2 main:app`
- Python Version: 3.11.10

### 5. Admin Access
Default admin credentials:
- Email: admin@oxin.com
- Password: admin123

**Important:** Change the admin password after first login!

## Local Development

1. Install dependencies:
```bash
pip install -r pyproject.toml
```

2. Set environment variables:
```bash
export DATABASE_URL=postgresql://user:password@localhost/oxin_db
export SESSION_SECRET=your_secret_key
```

3. Run the application:
```bash
python main.py
```

## Database Schema

- **user**: User accounts and mining data
- **admin_user**: Admin panel access
- **mining_session**: Mining activity tracking
- **deposit**: Payment transactions
- **announcement**: System notifications
- **payment_settings**: Payment configuration

## Payment Integration

- USDT BEP20 payments supported
- QR code generation for easy payments
- Screenshot upload for payment verification
- Admin approval system for plan upgrades

## Tech Stack

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Server**: Gunicorn
- **Database**: PostgreSQL
- **Deployment**: Render