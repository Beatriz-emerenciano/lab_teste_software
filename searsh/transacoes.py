# está separado porque a função classificar_transacao representa uma responsabilidade diferente da carteira digital:

def classificar_transacao(valor):
	if valor < 100:
		return "pequena"
	elif valor < 1000:
		return "media"
	else:
		return "grande"