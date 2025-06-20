# Render Environment Variables Guide

## What to Put in Each Variable

### 1. DATABASE_URL
**Yaha PostgreSQL database ka connection string dalna hai:**

**Steps:**
1. Render me PostgreSQL database banao (pehle database, phir web service)
2. Database dashboard me jao
3. "Connect" tab me click karo
4. "External Database URL" copy karo

**Example format:**
```
postgresql://username:password@hostname:5432/database_name
```

**Real example:**
```
DATABASE_URL=postgresql://oxin_user:abc123xyz@dpg-ch7k2m5umphs73f4bqhg-a.oregon-postgres.render.com:5432/oxin_db
```

### 2. SESSION_SECRET
**Yaha random 32-character string dalna hai security ke liye:**

**Generate karne ke liye:**
```python
import secrets
print(secrets.token_hex(32))
```

**Example:**
```
SESSION_SECRET=a1b2c3d4e5f6789012345678901234567890abcdef123456
```

**Or manually banao:**
```
SESSION_SECRET=myapp2025secretkey12345678901234567890
```

### 3. FLASK_ENV
**Production deployment ke liye:**
```
FLASK_ENV=production
```

## Complete Example for Render:

```
DATABASE_URL=postgresql://your_db_user:your_password@your-host.render.com:5432/your_db_name
SESSION_SECRET=your32characterrandomstringforsecurity123
FLASK_ENV=production
```

## Step-by-Step Process:

1. **First:** Create PostgreSQL database in Render
2. **Copy:** Database URL from Render dashboard
3. **Generate:** Session secret (random 32 characters)
4. **Set:** All three variables in web service environment section
5. **Deploy:** Your web service

## Important Notes:
- Database URL milega Render PostgreSQL dashboard se
- Session secret random hona chahiye (security ke liye)
- FLASK_ENV production hi rakhna hai Render pe