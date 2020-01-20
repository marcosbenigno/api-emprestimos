from flask import Blueprint, request
import app.emprestimos.models as md
from app import db
mod = Blueprint('routes', __name__, url_prefix='/')

@mod.route('/emprestimos/', methods=['GET', 'POST', 'DELETE'])
def emprestimos():
  if request.method == 'POST':
    dados = request.get_json()
    #necessario: validar json. caso nao seja valido: status = 400
    cpf = dados["cpf"]
    cd_chave = dados["cd_chave"]
    md.emprestar(cd_chave, cpf)
    if md.existeEmprestimo({"cd_chave": cd_chave, "cpf_pessoa": cpf}):
      resposta = {'status': 201}
      return resposta
    resposta = {'status': 500}
    return resposta

  if request.method == 'DELETE':
    dados = request.get_json()
    #necessario: validar json. caso nao seja valido: status = 400
    cd_emprestimo = dados["codigo_emprestimo"]
    md.removerEmprestimo(cd_emprestimo)
    if not(md.existeEmprestimo({"cd_emprestimo": cd_emprestimo})):
      resposta = {'status': 200}
      return resposta
    resposta = {'status': 500}
    return resposta

  if request.method == 'GET':
    if md.listarEmprestimos():
      resposta = {'status': 200,
                  'data': md.listarEmprestimos()}
      return resposta
    resposta = {'status': 200,
                  'data': []}
    return resposta


