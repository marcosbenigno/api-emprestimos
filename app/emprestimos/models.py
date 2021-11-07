from app import db
import datetime
import requests

class Pessoa(db.Model):
    cpf_pessoa = db.Column(db.Integer, primary_key=True, unique=True)
    nome_pessoa = db.Column(db.String(40))
    contato_pessoa = db.Column(db.String(30))
    def __init__(self, cpf_pessoa, nome_pessoa,contato_pessoa):
        self.cpf_pessoa = cpf_pessoa
        self.nome_pessoa = nome_pessoa
        self.contato_pessoa = contato_pessoa
    def __repr__(self):
        return '<Pessoa %r>' % self.cpf_pessoa
		
class Emprestimo(db.Model):
	cd_emprestimo = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
	cpf_pessoa = db.Column(db.String(11)) 
	cd_chave = db.Column(db.Integer)
	dt_hr_emprestimo = db.Column(db.DateTime)
	dt_hr_devolucao = db.Column(db.DateTime)
	def __init__(self, cd_emprestimo, cpf_pessoa, cd_chave, dt_hr_emprestimo, dt_hr_devolucao):
		self.cd_emprestimo = cd_emprestimo
		self.cpf_pessoa = cpf_pessoa
		self.cd_chave = cd_chave
		self.dt_hr_emprestimo = dt_hr_emprestimo
		self.dt_hr_devolucao = dt_hr_devolucao
	def __repr__(self):
		return '<Emprestimo %r>' % self.cd_emprestimo

class Chave(db.Model):
    cd_chave = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    tag_chave = db.Column(db.String(20))
    desc_chave = db.Column(db.String(20))
    def __init__(self, cd_chave, tag_chave, desc_chave):
        self.cd_chave = cd_chave
        self.tag_chave = tag_chave
        self.desc_chave = desc_chave
    def __repr__(self):
        return '<Chave %r>' % self.cd_chave

def emprestar(cd_chave, cpf_pessoa):
    if not(chaveEmprestada(cd_chave)):
        pessoa = Pessoa.query.filter_by(cpf_pessoa=cpf_pessoa).first()
        cpf = pessoa.cpf_pessoa
        chave = Chave.query.filter_by(cd_chave=cd_chave).first()
        dados = Emprestimo(cd_emprestimo=None,
                            cpf_pessoa=cpf,
                            cd_chave=cd_chave,
                            dt_hr_emprestimo = datetime.datetime.now(),
                            dt_hr_devolucao = None)
        db.session.add(dados)
        db.session.commit()
        if existeEmprestimo({'cd_chave': cd_chave, 'cpf_pessoa': cpf_pessoa}):
            return True
    return False

def removerEmprestimo(cd_emprestimo):
    if existeEmprestimo({'cd_emprestimo': cd_emprestimo}):
        emprestimo = Emprestimo.query.filter_by(cd_emprestimo=cd_emprestimo).first()
        if emprestimo:
            emprestimo.dt_hr_devolucao = datetime.datetime.now()
            db.session.add(emprestimo)
            db.session.commit()
            return True
        return False
    return False



def registrarChave(tag_chave, desc_chave):
    dados = Chave(cd_chave= None,
                            tag_chave= tag_chave,
                            desc_chave= desc_chave)
    db.session.add(dados)
    db.session.commit()
    if Chave.query.filter_by(tag_chave= tag_chave, desc_chave= desc_chave):
        return True
    return False

def removerChave(cd_chave):
    chave = Chave.query.filter_by(cd_chave= cd_chave).first()
    if chave:
        chave.delete()
        db.session.commit()
        return True
    return False

def listarEmprestimos():
    resp = list()
    for emprestimo in Emprestimo.query.all():
        resp.append({"cd_emprestimo": emprestimo.cd_emprestimo,
                    "cd_chave": emprestimo.cd_chave,
                    "cpf": emprestimo.cpf_pessoa})
    return resp

def listarEmprestimosEmAndamento():
    resp = list()
    for emprestimo in Emprestimo.query.filter_by(dt_hr_devolucao= None).all():
        resp.append({"cd_emprestimo": emprestimo.cd_emprestimo,
                     "cd_chave": emprestimo.cd_chave,
                     "cpf": emprestimo.cpf_pessoa})
    return resp

def listarChaves():
    resp = list()
    for chave in Chave.query.all():
        resp.append({"cd_chave":chave.cd_chave,
                    "desc_chave": chave.desc_chave})
    return resp

def chaveEmprestada(cd_chave):
    if Emprestimo.query.filter_by(cd_chave= cd_chave, dt_hr_devolucao= None).first():
        return True
    return False

def existeEmprestimo(kwargs):
    if "cd_chave" in kwargs and "cpf_pessoa" in kwargs:
        if Emprestimo.query.filter_by(cd_chave=kwargs.get('cd_chave'), cpf_pessoa=kwargs.get('cpf_pessoa')).first():
            return True
        return False
    if "cd_emprestimo" in kwargs:
        if Emprestimo.query.filter_by(cd_emprestimo=kwargs.get('cd_emprestimo')).first():
            return True
        return False
    return False

def getEmprestimo(kwargs):
    if "cd_emprestimo" in kwargs:
        emprestimo = Emprestimo.query.filter_by(cd_emprestimo=kwargs.get('cd_emprestimo')).first()
        return {"cd_emprestimo": emprestimo.cd_emprestimo,
                    "cd_chave": emprestimo.cd_chave,
                    "cpf_pessoa": emprestimo.cpf_pessoa}
    if "cd_chave" in kwargs and "cpf_pessoa" in kwargs:
        emprestimo = Emprestimo.query.filter_by(cd_chave=kwargs.get('cd_chave'), cpf_pessoa=kwargs.get('cpf_pessoa')).first()
        return {"cd_emprestimo": emprestimo.cd_emprestimo,
                    "cd_chave": emprestimo.cd_chave,
                    "cpf_pessoa": emprestimo.cpf_pessoa}
    if "cd_chave" in kwargs:
        emprestimo = Emprestimo.query.filter_by(cd_chave=kwargs.get('cd_chave')).first()
        return {"cd_emprestimo": emprestimo.cd_emprestimo,
                    "cd_chave": emprestimo.cd_chave,
                    "cpf_pessoa": emprestimo.cpf_pessoa}
    return False

def getChave(kwargs):
    if "cd_chave" in kwargs:
        chave = Chave.query.filter_by(cd_chave=kwargs.get('cd_chave')).first()
        return {"cd_chave": chave.cd_chave,
                    "desc_chave": chave.desc_chave,
                    "tag_chave": chave.tag_chave}
    if "tag_chave" in kwargs:
        chave = Chave.query.filter_by(tag_chave=kwargs.get('tag_chave')).first()
        return {"cd_chave": chave.cd_chave,
                    "desc_chave": chave.desc_chave,
                    "tag_chave": chave.tag_chave}
    if "desc_chave" in kwargs:
        chave = Chave.query.filter_by(cd_chave=kwargs.get('desc_chave')).first()
        return {"cd_chave": chave.cd_chave,
                    "desc_chave": chave.desc_chave,
                    "tag_chave": chave.tag_chave}
    return False

def getPessoaByTag(tag, token):
    headers = {'Authorization': 'Bearer '+str(token)}
    r = requests.get("https://api.nce.ufrj.br/v1/acesso/associacao/interno/"+str(tag))
    if r.status_code == 200:
        return r.json()
    else:
        return r.status_code