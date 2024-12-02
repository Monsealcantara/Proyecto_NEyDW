Comandos de secuencia para la instalación

Crear entorno virtual

    python3 -m venv env
    
Activamos entorno virtual

En Linux:

    source env/bin/activate
    
En Windows:

    env\Scripts\activate

Instalamos librerias

    pip install -r requirements.amb

Configurar archivo .env (crear un archivo '.env' en la misma carpeta del "manage.py"):

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

    python manage.py makemigrations users jobs materials subscriptions notifications chat venta carrito
    python manage.py migrate

Creamos un superusurio

    python manage.py createsuperuser

Corremos proyecto 
    
    python manage.py runserver	
    
    
Para entrar al administrador es con 

    http://127.0.0.1:8000/admin/

Crear subscripciones antes de registrar archivos

    plan_name   price
1    PREMIUM     200
2    GRATUITA    0

Crear el usuario empresa
Opcion 1
    >Entrar al administrador >USERS >Usuarios >AGREGAR USUARIO

    Llenar los campos, solo en contraseña poner:

    pbkdf2_sha256$870000$3UFd66pX0ZIl237aNl60Ro$fyMmmADJh0QHH3WWxTpkWsupFRjtmIMXhcqWYz5ii+0=

    la contraseña sera empresa
    
Opcion2
    Registrar en el sistema como cliente o traajador 
    >Entrar al administrador >USERS >Usuarios > usuario creado
    Editar el rol a empresa
