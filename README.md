# Amigo Invisible Version: 0.1.0

Aplicación web para sorteos de amigo invisible.[Amigo Invisible Logo](./static/img/logo.png) 


**Amigo Invisible** es una aplicación para hacer sorteos de amigo invisible sin poner en riesgo la privacidad de los participantes. Los datos introducidos se utilizan exclusivamente para enviar la información a cada participante sobre a quién tienen que regalar.

Permite múltiples eventos por usuario, múltiples participantes por evento e incluir exclusiones (cuando un participante no puede regalar a otro participante).

[![platform](https://img.shields.io/badge/platform-linux-green)](https://ubuntu.com/)
[![python](https://img.shields.io/badge/python-3.9-blue.svg?logo=python&labelColor=yellow)](https://www.python.org/downloads/)
[![platform](https://img.shields.io/badge/django-3.1-blue)](https://www.djangoproject.com/)


## Instalar desde fuentes (Linux Ubuntu 21.04)

1. Clona el repositorio:
```
git clone https://github.com/mercaderd/AmigoInvisible.git
```

2. Instalar dependencias:

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install wget python3 python3-pip python3-venv
```

3. Crear fichero .env a partir del ejemplo incluido:

```    
cp .env.dist .env
```

4. Edita .env para establecer el valor de SECRET_KEY, DEBUG, ALLOWED_HOSTS y la configuración del servidor de correo pare el envío de email de alta de usuario e informativo a los participantes:
```  
nano .env
``` 

Modifica las siguientes líneas según la configuración de tu sistema:
```     
# SECURITY WARNING: don't run with the debug turned on in production!
DEBUG=False

# Secret Key for your App. Change it and keep it secret
SECRET_KEY='django-insecure-_z)5%_o0onjgg7_s=vz6n^yzf&ldevpn!dzt7q5fs^*26iqv0e'

# Set email SMTP server for sending emails to users
EMAIL_HOST='smtp.example.com'
EMAIL_HOST_PASSWORD='your_password_hete'
EMAIL_HOST_USER='myapp@example.com'

# Set allowed hosts
ALLOWED_HOSTS=127.0.0.1,localhost
``` 
Pulsa Ctrl+x para salir y guarda los cambios.

5. Instala la aplicación:
```
./install.sh
``` 
6. Ejecuta la aplicación:
``` 
./run_srv.sh
``` 

6.- Navega a http://127.0.0.1:8000 para comenzar!