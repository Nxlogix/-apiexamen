# controllers/Users_Controller.py
from flask import jsonify
from models import Usuario
from config import db
from flask_jwt_extended import create_access_token

def create_usuario(nombre, email, password):
    existente = Usuario.query.filter_by(email=email).first()
    if existente:
        return jsonify({"error": "Ya existe un usuario con ese email"}), 400

    nuevo_usuario = Usuario(nombre=nombre, email=email, password=password)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario creado exitosamente", "usuario": nuevo_usuario.to_dict()}), 201

def login_usuario(email, password):
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.check_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=usuario.id)
    return jsonify({"mensaje": "Login exitoso", "access_token": access_token, "usuario": usuario.to_dict()}), 200

def get_all_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.to_dict() for usuario in usuarios]), 200
