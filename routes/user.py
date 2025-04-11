from flask import Blueprint, jsonify, request
from models import Usuario
from config import db  # ← Asegúrate de tener esta línea
from controllers.Users_Controller import create_usuario, login_usuario

usuario_bp = Blueprint('usuarios', __name__)

# Ruta para obtener la lista de usuarios
@usuario_bp.route('/', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.to_dict() for usuario in usuarios])

# Ruta para crear un nuevo usuario
@usuario_bp.route('/', methods=['POST'])
def create_usuario_route():
    data = request.get_json()
    nuevo_usuario = Usuario(**data)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify(nuevo_usuario.to_dict()), 201

# Ruta para actualizar un usuario
@usuario_bp.route('/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.get_json()
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    usuario.nombre = data['nombre']
    db.session.commit()
    return jsonify(usuario.to_dict())

# Ruta para eliminar un usuario
@usuario_bp.route('/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    db.session.delete(usuario)
    db.session.commit()
    return '', 204

# Ruta de login
@usuario_bp.route('/login', methods=['POST'])
def login_usuario_route():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "El email y la contraseña son requeridos"}), 400

    return login_usuario(email, password)
