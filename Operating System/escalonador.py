import os
import numpy as np
#Implementar algoritmos de escalonamento(FCFS, SJF, RR)
#Ler processos com seus respectivos, tempos de chegado e de duração 
#Saída devera imprimir uma tabela com as métricas de cada processo: Tempo de retorno, resposta e espera média

def leArquivo():
	arq = open('process.txt', 'r')
	texto = arq.readlines()
	#Vamos fazer um dicionário, onde cada processo terá uma lista com os tempos do processo
	listaProcess = []
	listaTempo = []
	maior = 0
	processos = {}
	for lines in texto:
		#Vamos ler o tempo de chegada
		dados = lines.split(" ")
		if dados[0] in processos.keys():
			processos[dados[0]].append(int(dados[1]))
		else:
			processos[dados[0]] = [int(dados[1])] #Tranformação implicita em lista
	arq.close()
	return processos

def FCFS(processos):
	tResposta = [] #Primeira vez que o processo é startado
	tRetorno = [] #Quando processo finaliza
	tEspera = [] #Enquanto o processo está esperando

	#Vamos ver o tempo máximo de chegada dos processos que representa no instante máximo do dicionário
	tempoAtual = 0
	for i in range(int(max(processos.keys())) + 1):
		#Para os processos nesse instante
		print(str(i) in processos.keys())
		print('i:', i)
		if str(i) in processos.keys():
			for j in range(len(processos[str(i)])):
				print("j:", j)
				tEspera.append(tempoAtual - i)
				tResposta.append(tempoAtual - i)
				tRetorno.append(processos[str(i)][j] + tempoAtual)
				tempoAtual += processos[str(i)][j]
				print("Tempo Atual:", tempoAtual)

	print('Retorno', tRetorno, "Resposta:", tResposta, 'Espera', tEspera, sep = '\n')
	print('Retorno', np.mean(tRetorno), "Resposta:", np.mean(tResposta),'Espera', np.mean(tEspera), sep = '\n')
	return np.mean(tRetorno), np.mean(tResposta), np.mean(tEspera)

def SJF(processos):
	tResposta = []
	tRetorno = []
	tEspera = []


	#Vamos ver o tempo máximo de chegada dos processos que representa no instante máximo do dicionário
	ordem = []
	executando = 0
	tempoAtual = 0
	for i in range(int(max(processos.keys())) + 1):
		#Vamos jogar todos os processos em uma lista
		if str(i) in processos.keys():
			ordem += processos[str(i)]
			ordem.sort()
			print(ordem)
			#Se no instante que aquele processo entrou não há nada no processador, ele é executado
			if tempoAtual <= i:
			#Executa
				tEspera.append(tempoAtual - i)
				tResposta.append(tempoAtual - i)
				tRetorno.append(ordem[0] + tempoAtual) #Tem que pensar onde por isso
				tempoAtual += ordem[0]
				executando = ordem[0]
				del(ordem[0])

			#Verificamos se aquele processo que estaria no processador n é maior que o atual que acabou de entrar
			#elif (executando - i) > ordem[0] :



	
	instanteProcess = 0
	while ordem != []:
		print(ordem)
		for i in range(int(max(processos.keys())) + 1):
			if str(i) in processos.keys():
				aux = ordem[0]
				if aux in processos[str(i)]:
					instanteProcess = i
		#Executa
		tEspera.append(tempoAtual - instanteProcess)
		tResposta.append(tempoAtual - instanteProcess)
		tRetorno.append(ordem[0] + tempoAtual)
		tempoAtual += ordem[0]
		del(ordem[0])
	print('Retorno', tRetorno, "Resposta:", tResposta, 'Espera', tEspera, sep = '\n')
	print('Retorno', np.mean(tRetorno), "Resposta:", np.mean(tResposta),'Espera', np.mean(tEspera), sep = '\n')

		#Caso haja um novo processo, verificamos se há outros processos por lá e ordenamos 


processos = leArquivo()
#FCFS(processos)
SJF(processos)
#Perfeito, agora que estamos lendo os arquivos, vamos mandar a um método próprio cada processo
#Ele vai retornar a string com os dados que passamos