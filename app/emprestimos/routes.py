from flask import Blueprint, request, Response
import app.emprestimos.models as md
from app import db
mod = Blueprint('routes', __name__, url_prefix='/')

@mod.route('/emprestimos/', methods=['GET', 'POST', 'DELETE'])
def emprestimos():
#requests com content-type = application/json
  if request.method == 'POST':
    dados = request.get_json()
    #necessario: validar json. caso nao seja valido: status = 400
    cpf = dados["cpf"]
    cd_chave = dados["cd_chave"]
    if md.getChave({"cd_chave": cd_chave}):
      #checar se chave está emprestada
      md.emprestar(cd_chave, cpf)
    else:
      resposta = Response('',status=404)
      return resposta
    if md.existeEmprestimo({"cd_chave": cd_chave, "cpf_pessoa": cpf}):
      emprestimo = md.getEmprestimo({"cd_chave": cd_chave, "cpf_pessoa": cpf})
      resposta = Response({"id": emprestimo.cd_emprestimo,
                            "uri": "/emprestimos/"+str(emprestimo.cd_emprestimo),
                            "type": "emprestimo"},
                            status=201)
      return resposta
    resposta = Response('',status=500)
    return resposta

  if request.method == 'DELETE':
    dados = request.get_json()
    #necessario: validar json. caso nao seja valido: status = 400
    cd_emprestimo = dados["cd_emprestimo"]
    if md.getEmprestimo({"cd_emprestimo": cd_emprestimo}):
      md.removerEmprestimo(cd_emprestimo)
    else:
      resposta = Response('',status=404)
      return resposta
    if not(md.existeEmprestimo({"cd_emprestimo": cd_emprestimo})):
      resposta = Response('', status=200)
      return resposta
    resposta = Response('',status=500)
    return resposta

  if request.method == 'GET':
    if md.listarEmprestimos():
      resposta = Response({
                  'data': md.listarEmprestimos()},
                  status=200)
      return resposta
    resposta =  Response({
                  'data': []},
                  status=200)
    return resposta



@mod.route('/emprestimos/<cd_emprestimo>', methods=['GET'])
def emprestimos_cd(cd_emprestimo):
  if request.method == 'GET':
    if existeEmprestimo(cd_emprestimo):
      return Response(getEmprestimo(cd_emprestimo),
                        status=200)
    return Response('', status=404)

@mod.route('/chaves/', methods=['GET', 'POST', 'DELETE'])
def chaves():
  if request.method == 'POST':
    dados = request.get_json()
    #necessario: validar json. caso nao seja valido: status = 400
    desc_chave = dados["desc_chave"]
    tag_chave = dados["tag_chave"]
    if not(md.getChave({"tag_chave": tag_chave})):
      md.registrarChave(tag_chave, desc_chave)
    else:
      if md.getChave({"desc_chave": desc_chave, "tag_chave": tag_chave}):
        chave = md.getChave({"desc_chave": desc_chave, "tag_chave": tag_chave})
        resposta = Response({"id": chave.cd_chave,
                            "uri": "/chaves/"+str(emprestimo.cd_chaves),
                            "type": "chave"},
                            status=201)
        return resposta
    resposta = Response('',status=500)
    return resposta

  if request.method == 'DELETE':
    dados = request.get_json()
    #necessario: validar json. caso nao seja valido: status = 400
    cd_emprestimo = dados["cd_chave"]
    if md.getChave({"cd_chave": cd_chave}):
      md.removerChave(cd_chave)
    else:
      resposta = Response('',status=404)
      return resposta
    if not(md.getChave({"cd_chave": cd_chave})):
      resposta = Response('', status=200)
      return resposta
    resposta = Response('',status=500)
    return resposta

  if request.method == 'GET':
    if md.listarChaves():
      resposta = Response({
                  'data': md.listarChaves()},
                  status=200)
      return resposta
    resposta =  Response({
                  'data': []},
                  status=200)
    return resposta

@mod.route('/chaves/<cd_chave>', methods=['GET'])
def chaves_cd(cd_chave):
  if request.method == 'GET':
    if getChave(cd_chave):
      return Response(getChave(cd_chave),
                        status=200)
    return Response('', status=404)