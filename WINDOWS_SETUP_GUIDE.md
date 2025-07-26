# 🏥 Windows Setup Guide - Clinic Management System

## 📋 Prerequisites

Before starting, ensure you have:
- Windows 10/11 (64-bit)
- Administrator privileges
- Internet connection for downloads
- At least 2GB free disk space

---

## 🚀 Step 1: Install Python

1. **Download Python 3.8+**
   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Download the latest Python 3.x version (3.8 or higher)
   - **IMPORTANT**: Check "Add Python to PATH" during installation

2. **Verify Installation**
   - Open Command Prompt as Administrator
   - Run: `python --version`
   - Should show Python 3.x.x

---

## 🗄️ Step 2: Install PostgreSQL

1. **Download PostgreSQL**
   - Go to [postgresql.org/download/windows](https://www.postgresql.org/download/windows/)
   - Download PostgreSQL 14 or higher
   - Run the installer as Administrator

2. **Installation Settings**
   - **Port**: 5432 (default)
   - **Password**: Set a strong password (remember this!)
   - **Locale**: Default locale
   - **Stack Builder**: Uncheck (not needed)

3. **Verify Installation**
   - Open Command Prompt
   - Run: `psql --version`
   - Should show PostgreSQL version

---

## 🛠️ Step 3: Set Up Database

1. **Open PostgreSQL Command Line**
   - Press `Win + R`, type `cmd`, press Enter
   - Run: `psql -U postgres`
   - Enter your PostgreSQL password

2. **Create Database and User**
   ```sql
   -- Create database
   CREATE DATABASE clinicdb;
   
   -- Create user
   CREATE USER clinicuser WITH PASSWORD 'admin';
   
   -- Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE clinicdb TO clinicuser;
   
   -- Connect to clinicdb
   \c clinicdb
   
   -- Grant schema privileges
   GRANT ALL ON SCHEMA public TO clinicuser;
   
   -- Exit
   \q
   ```

---

## 📁 Step 4: Download and Extract Application

1. **Download the Application**
   - Copy the entire `lamsatgit2.0 copy` folder to your Windows machine
   - Place it in a convenient location (e.g., `C:\clinic-system\`)

2. **Open Command Prompt in Application Directory**
   - Navigate to the application folder
   - Right-click in the folder → "Open in Terminal" or "Open command window here"

---

## 🐍 Step 5: Set Up Python Environment

1. **Create Virtual Environment**
   ```cmd
   python -m venv venv
   ```

2. **Activate Virtual Environment**
   ```cmd
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

---

## 🚀 Step 6: Start the Application

### Option A: Using the Batch File (Recommended)
1. **Double-click** `start_clinic_server.bat`
2. The server will start automatically
3. Access at: `http://localhost:5050`

### Option B: Manual Start
1. **Activate virtual environment**:
   ```cmd
   venv\Scripts\activate
   ```

2. **Start the application**:
   ```cmd
   python app.py
   ```

3. **Access the application**:
   - Open browser
   - Go to: `http://localhost:5050`

---

## 👥 Step 7: Create Admin User

1. **Access the application** in your browser
2. **Register** a new user account
3. **Use the admin setup script**:
   ```cmd
   python add_user.py
   ```
   - Follow the prompts to create an admin user

---

## 🔧 Step 8: Configure Windows Firewall

1. **Open Windows Defender Firewall**
   - Press `Win + R`, type `wf.msc`, press Enter

2. **Add Inbound Rule**
   - Click "Inbound Rules" → "New Rule"
   - Select "Port" → "Next"
   - Select "TCP" → "Specific local ports" → "5050" → "Next"
   - Select "Allow the connection" → "Next"
   - Select all profiles → "Next"
   - Name: "Clinic Management System" → "Finish"

---

## 🖥️ Step 9: Create Desktop Shortcut

1. **Run the shortcut creator**:
   - Double-click `create_desktop_shortcut.bat`
   - This creates a desktop shortcut for easy access

---

## 🌐 Step 10: Network Access Setup

### For Other Computers to Connect:

1. **Find your computer's IP address**:
   ```cmd
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. **On other computers**:
   - Run `connect_to_clinic.bat`
   - Enter your computer's IP address
   - Browser will open to the clinic system

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed and in PATH
- [ ] PostgreSQL installed and running
- [ ] Database `clinicdb` created
- [ ] User `clinicuser` with password `admin` created
- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] Application starts without errors
- [ ] Can access `http://localhost:5050`
- [ ] Admin user created
- [ ] Windows Firewall configured
- [ ] Desktop shortcut created

---

## 🚨 Troubleshooting

### Common Issues:

1. **"Python not found"**
   - Reinstall Python with "Add to PATH" checked
   - Restart Command Prompt

2. **"Cannot connect to PostgreSQL"**
   - Ensure PostgreSQL service is running
   - Check password is correct
   - Verify database and user exist

3. **"Port 5050 already in use"**
   - Change port in `app.py` (line with `app.run()`)
   - Or stop other applications using port 5050

4. **"Module not found"**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

5. **"Permission denied"**
   - Run Command Prompt as Administrator
   - Check Windows Firewall settings

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs in the application
3. Ensure all prerequisites are met
4. Try restarting the computer

---

## 🔄 Auto-Start Setup (Optional)

To make the application start automatically on Windows boot:

1. **Create a batch file** for auto-start:
   ```cmd
   @echo off
   cd /d "C:\path\to\your\clinic-system"
   call venv\Scripts\activate.bat
   python app.py
   ```

2. **Add to Windows Startup**:
   - Press `Win + R`, type `shell:startup`, press Enter
   - Copy the batch file to this folder

---

**🎉 Congratulations! Your Clinic Management System is now ready to use!** 