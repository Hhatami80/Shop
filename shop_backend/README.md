مراحل نصب و اجرا
1. کلون کردن پروژه
git clone https://github.com/username/project-name.git
cd project-name

3. ساخت محیط مجازی (virtual environment)
python -m venv venv


4. فعال‌سازی محیط مجازی:
لینوکس / مک:
source venv/bin/activate

ویندوز:
venv\Scripts\activate


5. نصب پکیج‌ها:
pip install -r requirements.txt


6. ساخت فایل .env:
SECRET_KEY=یک_کلید_امن
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=sqlite:///db.sqlite3


7. اجرای مایگریشن‌ها:
python manage.py migrate


8. اجرای سرور:
python manage.py runserver
