admin:

tinhphamtrung
123

Install Virtual Environment 
```
$  pip install virtualenv
```

Create Virtual Environment


For Mac
```
python3 -m venv venv
```

Activate Virtual Environment



For Mac
```
source venv/bin/activate
```

```
pip install -r requirements.txt
```

```python
python manage.py migrate
```

```python
$ python3 manage.py runserver
```


dokcer mýql
docker run -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=123 -d mysql