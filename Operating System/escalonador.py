import os
import numpy as np
from processo import processo
#Implementar algoritmos de escalonamento(FCFS, SJF, RR)
#Ler processos com seus respectivos, tempos de chegado e de duração 
#Saída devera imprimir uma tabela com as métricas de cada processo: Tempo de retorno, resposta e espera média

def leArquivo():
	arq = open('process.txt', 'r')
	texto = arq.readlines()
	#Vamos fazer um dicionário, onde cada processo terá uma lista com os tempos do processo
	listaProcess = []
	listaTempo = []
	processos = {}
	maior = 0
	for lines in texto:
		#Vamos ler o tempo de chegada
		dados = lines.split(" ")
		instante = int(dados[0])
		pico = int(dados[1])
		if instante in processos.keys():
			processos[instante].append(pico)
		else:
			processos[instante] = [pico] #Tranformação implicita em lista desse primeiro instante
	arq.close()
	return processos

def FCFS(processos):
	tResposta = [] #Primeira vez que o processo é startado
	tRetorno = [] #Quando processo finaliza
	tEspera = [] #Enquanto o processo está esperando

	
	tTotal = 0
	for i in processos.values():
		tTotal += sum(i)

	fila = []
	cpu = False #Simboliza se a CPU está cheia ou não
	instanteEntrada = {}
	nProc = 0 #Vamos já considerar o primeiro processo que vai entrar
	for tempoAtual in range(tTotal + 10): #+1 pelo instante 0 ser contado
		print("segundo:", tempoAtual)
		if tempoAtual in processos.keys():
			#Vamos receber e ordenar os processo que entram
			fila += processos[tempoAtual]
			#Vamos somar a quantidade atual de processos que entram para saher quantos ainda tem
			nProc += len(processos[tempoAtual])
			#Guardamos o momento que aquele processo entrou na fila de espera
			for i in processos[tempoAtual]:
				instanteEntrada[i] = tempoAtual

		if cpu == False and nProc > 0:
			proc = processo(fila[0])
			proc.iniciaProcesso(tempoAtual, instanteEntrada[fila[0]])
			del(fila[0])
			cpu = True


		elif nProc > 0:
			executado = proc.executaProcesso()
			if executado == False:
				x, y, z = proc.finalizaProcesso()
				tResposta.append(x)
				tRetorno.append(y)
				tEspera.append(z)
				nProc -= 1
				cpu = False
		print('nProc', nProc)

	print('Retorno', tRetorno, "Resposta:", tResposta, 'Espera', tEspera, sep = '\n')
	print('Retorno', np.mean(tRetorno), "Resposta:", np.mean(tResposta),'Espera', np.mean(tEspera), sep = '\n')


def SJF(processos):
	tResposta = [] #Primeira vez que o processo é startado
	tRetorno = [] #Quando processo finaliza
	tEspera = [] #Enquanto o processo está esperando

	
	tTotal = 0
	for i in processos.values():
		tTotal += sum(i)

	fila = []
	cpu = False #Simboliza se a CPU está cheia ou não
	instanteEntrada = {}
	nProc = 0 #Vamos já considerar o primeiro processo que vai entrar
	for tempoAtual in range(tTotal + 10): #+1 pelo instante 0 ser contado
		print("segundo:", tempoAtual)
		if tempoAtual in processos.keys():
			#Vamos receber e ordenar os processo que entram
			fila += processos[tempoAtual]
			#Vamos somar a quantidade atual de processos que entram para saher quantos ainda tem
			nProc += len(processos[tempoAtual])
			#Guardamos o momento que aquele processo entrou na fila de espera
			for i in processos[tempoAtual]:
				instanteEntrada[i] = tempoAtual
			fila.sort()


		if cpu == False and nProc > 0:
			proc = processo(fila[0])
			proc.iniciaProcesso(tempoAtual, instanteEntrada[fila[0]])
			del(fila[0])
			cpu = True


		elif nProc > 0:
			executado = proc.executaProcesso()
			if executado == False:
				x, y, z = proc.finalizaProcesso()
				tResposta.append(x)
				tRetorno.append(y)
				tEspera.append(z)
				nProc -= 1
				cpu = False
		print('nProc', nProc)

	print('Retorno', tRetorno, "Resposta:", tResposta, 'Espera', tEspera, sep = '\n')
	print('Retorno', np.mean(tRetorno), "Resposta:", np.mean(tResposta),'Espera', np.mean(tEspera), sep = '\n')

def RR(processos):
	tResposta = [] #Primeira vez que o processo é startado
	tRetorno = [] #Quando processo finaliza
	tEspera = [] #Enquanto o processo está esperando

	
	tTotal = 0
	for i in processos.values():
		tTotal += sum(i)
	j = 0
	fila = []
	prontos = []
	cpu = False #Simboliza se a CPU está cheia ou não
	instanteEntrada = {}
	quantum = 1
	nProc = 0 #Vamos já considerar o primeiro processo que vai entrar
	for tempoAtual in range(tTotal): #+1 pelo instante 0 ser contado
		print("segundo:", tempoAtual)

		if tempoAtual in processos.keys():
			#Vamos receber e ordenar os processo que entram
			fila += processos[tempoAtual]
			#Vamos somar a quantidade atual de processos que entram para saher quantos ainda tem
			nProc += len(processos[tempoAtual])
			#Guardamos o momento que aquele processo entrou na fila de espera
			for i in processos[tempoAtual]:
				instanteEntrada[i] = tempoAtual
		#print(fila)



		#Verificação quanto ao tempo daquele processo
		#print('quantum:', quantum)
		if quantum == 0:
			#print("pop processo")
			print("=========================Ciclo", j, "====================", sep = "")
			j += 1
			proc.pausaProcesso(tempoAtual)
			fila.append(proc)
			cpu = False
		#print('nProc', nProc)


		if cpu == False and nProc > 0:
			quantum = 1 #Segundo inicial já é uma execução e o segundo é 0
			#print("entrou no if", "cpu:", cpu, "nProc:", nProc)
			#Se tiver guardado na fila apenas o tempo de pico, executamos o código abaixo
			if type(fila[0]) == type(int()):
				proc = processo(fila[0], tempoAtual)
				print("-------------Processo inicializado:", proc.get_primeira_vez())
				proc.iniciaProcesso(tempoAtual, instanteEntrada[fila[0]])
				del(fila[0])
				cpu = True
			#Se o próprio processo estiver na fila, executamos o código abaixo
			else:
				proc = fila.pop(0)
				print("-------------Processo reiniciado:", proc.get_primeira_vez())
				print("-------------Quantum:", quantum, "Tempo de pico atual:", proc.get_cpu())
				proc.reiniciaProcesso(tempoAtual)

				cpu = True
			

		elif nProc > 0:
			executado = proc.executaProcesso()
			if executado == False:
				x, y, z = proc.finalizaProcesso(tempoAtual)
				#print("*********Quantum:", quantum,"Processo:", proc.get_primeira_vez())
				tResposta.append(x)
				tRetorno.append(y)
				tEspera.append(z)
				nProc -= 1
				cpu = False
				quantum = 1

			else:
				quantum -= 1
			

	print('Retorno', tRetorno, "Resposta:", tResposta, 'Espera', tEspera, sep = '\n')
	print('Retorno', np.mean(tRetorno), "Resposta:", np.mean(tResposta),'Espera', np.mean(tEspera), sep = '\n')


processos = leArquivo()
#FCFS(processos)
#SJF(processos)
RR(processos)