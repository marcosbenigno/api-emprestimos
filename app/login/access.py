import requests

def loginUFRJ(cpf, senha):
	body = {"usuario": cpf,
				"senha": senha}
	r = requests.post("https://apince.nce.ufrj.br/v1/auth/loginufrj", data=body)
	if r.status_code == 200:
		response = r.json()
		return response.get("access_token")
	else:
		return r.status_code

def loginNCE(usuario, senha):
	body = {"usuario": usuario,
				"senha": senha}
	r = requests.post("https://apince.nce.ufrj.br/v1/auth/login", data=body)
	if r.status_code == 200:
		response = r.json()
		return response.get("access_token")
	else:
		return r.status_code

def tokenValido(token):
	r = requests.get("https://apince.nce.ufrj.br/v1/auth/token/valido?jwt_token=" + token)
	if r.status_code == 204:
		return True
	return False

