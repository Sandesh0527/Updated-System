@echo off

REM Step 1: Install requirements
pip install -r requirements.txt

REM Step 2: Run Django development server
start cmd /k "python manage.py migrate"
start cmd /k "python manage.py runserver"

start cmd /k "python manage.py load_exam_data"

REM Step 3: Open login URL in a browser
timeout /t 10 >nul
start http://127.0.0.1:8000/exam/login/
