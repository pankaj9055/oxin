# Render Deployment Guide for Oxin Crypto Mining Platform

## Step-by-Step Deployment Process

### 1. Prepare Your Repository
- Upload all project files to GitHub repository
- Ensure all files are committed and pushed

### 2. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub account
- Connect your GitHub repository

### 3. Deploy PostgreSQL Database FIRST

**Important: Create database before web service**

1. In Render dashboard, click "New" → "PostgreSQL"
2. Settings:
   - Name: `oxin-postgres-db`
   - Database: `oxin_db`
   - User: `oxin_user`
   - Region: Choose closest to your location
   - Plan: Free tier available
3. Click "Create Database"
4. **Save the connection details** (you'll need DATABASE_URL)

### 4. Create Web Service

1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configuration:
   - Name: `oxin-crypto-mining`
   - Environment: `Python 3`
   - Region: Same as database
   - Branch: `main`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 2 main:app`

### 5. Environment Variables

Add these in "Environment" section:

```
DATABASE_URL=postgresql://oxin_user:password@hostname:port/oxin_db
SESSION_SECRET=your_random_32_character_string
FLASK_ENV=production
```

**How to get DATABASE_URL:**
1. Go to your PostgreSQL database in Render
2. Click "Connect" tab
3. Copy "External Database URL"
4. Use this as your DATABASE_URL value

**Generate SESSION_SECRET:**
```python
import secrets
print(secrets.token_hex(32))
```

### 6. Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Install dependencies
   - Create database tables
   - Start the application
3. Wait for deployment to complete (5-10 minutes)

### 7. Access Your Application

- Your app will be available at: `https://your-service-name.onrender.com`
- Admin panel: `https://your-service-name.onrender.com/admin`
- Default admin login: `admin@oxin.com` / `admin123`

### 8. Post-Deployment Setup

1. **Change Admin Password:**
   - Login to admin panel
   - Create new admin user
   - Delete default admin

2. **Test All Features:**
   - User registration
   - Mining functionality
   - Payment system
   - Admin controls

### 9. Production Configuration

**SSL Certificate:** Automatically provided by Render

**Custom Domain:** Available in Render dashboard settings

**Database Backups:** Automatic with PostgreSQL plans

### Common Issues & Solutions

**Build Fails:**
- Check build logs in Render dashboard
- Ensure all dependencies in pyproject.toml

**Database Connection Error:**
- Verify DATABASE_URL format
- Ensure PostgreSQL service is running
- Check network connectivity

**App Won't Start:**
- Check start command syntax
- Verify Gunicorn installation
- Review application logs

### Monitoring

- Logs available in Render dashboard
- Set up monitoring alerts
- Monitor database performance

### Scaling

- Upgrade PostgreSQL plan for more connections
- Increase web service resources
- Add multiple workers for high traffic

**Support:** Contact Render support for deployment issues

**Database URL Format:**
```
postgresql://username:password@hostname:port/database_name
```

**Example:**
```
DATABASE_URL=postgresql://oxin_user:abc123@dpg-xxxxx-a.oregon-postgres.render.com:5432/oxin_db
```