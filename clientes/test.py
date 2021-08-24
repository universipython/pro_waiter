def busca(lista, nome):
    return {rec[0]:rec[1]for rec in lista}.get(nome)

lista = [
	['João', 'Microsoft'],
	['Maria','Google'],
	['Pedro','Oracle'],
	['Fátima','Mcafee'],
]

print(busca(lista, 'teste'))
