class processo:
	def __init__(self, tempo_cpu):
		#print("iniciooooooooooooooooou:", tempo_cpu)
		self.instante_entrada = 0
		self._tempo_cpu = tempo_cpu
		self.primeira_vez = tempo_cpu
		self.tResposta = 0
		self.tRetorno = 0
		self.tEspera = 0

	def get_primeira_vez(self):
		return self.primeira_vez


	def reiniciaProcesso(self, instante_atual):
		#Reinizaliza execução
		self.tRetorno += (instante_atual - self.instante_entrada)
		self._tempo_cpu -= 1
		self.tEspera += instante_atual - self.instante_entrada

	def iniciaProcesso(self, instante_atual, instante_entrada):
		#Primeira execução
		self.tRetorno += 1 + (instante_atual - instante_entrada)
		self._tempo_cpu -= 1

		#Inicialização dos contadores
		self.tEspera = instante_atual - instante_entrada
		self.tResposta = instante_atual - instante_entrada
		print("======================resposta_inicio:", self.tResposta)
		self.tEspera += instante_atual - instante_entrada


	def executaProcesso(self):
		#Executa
		self.tRetorno += 1
		self._tempo_cpu -= 1
		#print("tempo restante:", self._tempo_cpu)
		#print("======================resposta_executa:", self.tResposta)
		if self._tempo_cpu <= 0:
			return False #Processo finalizado e não pode executar mais
		elif self._tempo_cpu > 0:
			return True #Processo finalizado e executou 1 segundo


	def pausaProcesso(self, instante_atual):
		#print("======================resposta_inicio:", self.tResposta)
		#Quando o processo é pausado, ele volta a fila, o que se torna atualmente o seu instante entrada 
		self.instante_entrada = instante_atual

	def finalizaProcesso(self):
		print("======================resposta_finaliza:", self.tResposta)
		return self.tResposta, self.tRetorno, self.tEspera