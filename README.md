# Quản lý hóa đơn
Đồ án môn học Python
# Run source
Thay đôỉ port DATABASES trong file du_an/settings.py

Tạo database name là: qlhd_db
```bash
#tạo migration cho model qlhd
python manage.py makemigrations
```
```bash
# chạy migration cho db
python3 manage.py migrate
```
```bash
# run server
python manage.py runserver
```
# Active Env
chạy môi trường pip trên máy mac
```bash
#tạo env nếu chưa có file venv
python3 -m venv --system-site-packages ./venv
#active env
source ./venv/bin/activate 
```

chạy môi trường pip trên máy windows
```bash
#tạo env nếu chưa có file venv
python3 -m venv --system-site-packages ./venv
#active env
.\venv\Scripts\activate 
```

# Tạo file requirements
```bash
pip3 freeze > requirements.txt
```

# Install all packages
```bash
pip install -r requirements.txt
```
# Tạo superuser.
```bash
python manage.py createsuperuser
```
Username: admin
Password: abc@1234
Check tại http://127.0.0.1:8000/admin