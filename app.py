from flask import Flask
from config import db, migrate
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.user import usuario_bp

# Cargar las variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de CORS (permite solicitudes de otros dominios)
CORS(app)

# Configuración de la clave secreta para JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'Clave secreta para examen')

# Configuración de la URI de la base de datos RDS
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:contraseña@database-5.cajiy68ymdse.us-east-1.rds.amazonaws.com:3306/nombre_basededatos'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Para evitar advertencias

# Inicializar la base de datos y las migraciones
db.init_app(app)
migrate.init_app(app, db)

# Inicializar el JWT Manager para la autenticación
jwt = JWTManager(app)

# Ruta principal
@app.route('/')
def home():
    return 'API realizada para el tercer examen de Aplicaciones Web'

# Importar y registrar las rutas de usuario
from routes.user import usuario_bp
app.register_blueprint(usuario_bp, url_prefix='/usuarios')

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
    
app.register_blueprint(usuario_bp, url_prefix='/usuarios')
print(app.url_map)
 # Configuración de la URI de la base de datos RDS
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
