Comando de secuencia para la instalacion

Crear entorno virtual

    python3 -m venv env
    
Activamos entorno virtual

    source env/bin/activate

Instalamos librerias

    pip install -r requirements.amb

Configurar archivo .env

    FINDER_SECRET_KEY='django-insecure-mmiuzz_p+*l@rng*j!1(i0qjf&v^ghps*_it-d&kiw^qtscrxo'
    FINDER_DEBUG=True
    FINDER_DB_NAME=<nombre de la base de datos>
    FINDER_DB_USER=<usuario de postgres>
    FINDER_DB_PASS=<contraseña de postgres>
    FINDER_DB_HOST=<host de postgres, en caso local localhost>
    FINDER_DB_PORT=<puerto de postgres, el puerto default es 5432>
    FINDER_EMAIL_HOST='smtp.gmail.com'
    FINDER_EMAIL_PORT=587
    FINDER_EMAIL_USER=<correo de gmail>
    FINDER_EMAIL_PASS=<contraseña de aplicación de gmail>
    FINDER_EMAIL_TLS=True
    FINDER_EMAIL_SSL=False

Aplicamos migraciones

    python manage.py makemigrations users jobs materials subscriptions notifications chat
    python manage.py migrate

Creamos un superusurio

    python manage.py createsuperuser

Corremos proyecto 
    
    python manage.py runserver	