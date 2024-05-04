## Run the project

Install Python >=3.10

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Run the tests

```bash
python manage.py test
```

## Project Structure

```
vms/
├── api/
│   ├── migrations/
│   ├── purchase_orders/
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   └── test_api.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── signals.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── signals.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── vendors/
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   └── test_api.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   └── urls.py
├── vms/
│   ├── templates/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt
```