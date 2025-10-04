# Deployment Guide

## 📋 **Files Created for Deployment:**

1. ✅ **requirements.txt** - Python dependencies
2. ✅ **Procfile** - For Heroku deployment
3. ✅ **.env.example** - Environment variables template
4. ✅ **.gitignore** - Git ignore rules
5. ✅ **config.py** - Updated with production config

## 🚀 **Deployment Steps:**

### **For Heroku:**

1. **Install Heroku CLI and login:**
   ```bash
   heroku login
   ```

2. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your-super-secret-key
   heroku config:set JWT_SECRET_KEY=your-jwt-secret-key
   ```

4. **Add PostgreSQL database:**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

6. **Run database migration:**
   ```bash
   heroku run python update_db_goals.py
   ```

### **For Other Platforms (Railway, Render, etc.):**

1. **Connect your GitHub repository**
2. **Set environment variables:**
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key`
   - `JWT_SECRET_KEY=your-jwt-secret`
   - `DATABASE_URL=your-database-url`

3. **Deploy from GitHub**

## 🔧 **Local Testing with Production Config:**

```bash
# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=test-secret
export JWT_SECRET_KEY=test-jwt-secret

# Run the app
python run.py
```

## 📝 **Environment Variables Needed:**

- `FLASK_ENV` - production/staging/development
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT token secret
- `DATABASE_URL` - PostgreSQL connection string
- `CORS_ORIGINS` - Allowed CORS origins (optional)

## 🔒 **Security Notes:**

1. **Never commit .env files** - Use .env.example as template
2. **Use strong secret keys** - Generate random keys for production
3. **Set CORS origins** - Don't use '*' in production
4. **Use HTTPS** - Always use SSL/TLS in production

## 📊 **Database Setup for Production:**

Your production database will need the same tables. The app will automatically create them on first run, or you can run:

```bash
python update_db_goals.py
```

## 🎯 **API Endpoints Available:**

- `GET /` - Health check
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/profile` - User profile
- `POST /api/add/goal` - Add goal
- `GET /api/goals` - Get all goals
- `PUT /api/goal/<id>` - Update goal
- `DELETE /api/goal/<id>` - Delete goal
- `GET /api/goal/<id>` - Get single goal