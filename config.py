import os

class Config:
    SECRET_KEY = 'oU6jCyHsifIWbZUP7PlZ3N-dJOqimjam7o9h26vErSg'
    
    # Define la carpeta de subida de archivos en la clase base para que sea accesible en cualquier entorno.
    UPLOAD_FOLDER = os.path.abspath('uploads')

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'bd_rrhh_v4'

# Ya no es necesario definir UPLOAD_FOLDER aquí, ya que hereda de la clase base.

config = {
    'development': DevelopmentConfig
}