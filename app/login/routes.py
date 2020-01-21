from flask import Blueprint, request, Response
import json
import app.login.access as loginMd


mod = Blueprint('login_routes', __name__, url_prefix='/')

@mod.route('/login-ufrj/', methods=['POST'])
def loginUFRJ():
#requests com content-type = application/json
  if request.method == "POST":
    dados = request.get_json()
    usuario = dados["usuario"]
    senha = dados["senha"]
    login_tentativa = loginMd.loginUFRJ(usuario, senha)
   
    if type(login_tentativa) == str:
      resposta = json.dumps({"token": login_tentativa})
      return Response(resposta, status=200)
    return Response('', status=login_tentativa)

@mod.route('/login-nce/', methods=['POST'])
def loginNCE():
#requests com content-type = application/json
  if request.method == "POST":
    dados = request.get_json()
    usuario = dados["usuario"]
    senha = dados["senha"]
    login_tentativa = loginMd.loginNCE(usuario, senha)
   
    if type(login_tentativa) == str:
      return Response(json.dumps({"token": login_tentativa}), status=200)
    return Response('', status=login_tentativa)
