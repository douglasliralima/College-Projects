class processo:
    def __init__(self, tempo_cpu, instante_inicial):
        self.instante_entrada = 0
        self._tempo_cpu = tempo_cpu
        self.instante_inicial = instante_inicial
        self.cpu_primeira_vez = tempo_cpu
        self.tResposta = 0
        self.tRetorno = 0
        self.tEspera = 0
        

    def get_primeira_vez(self):
        return self.cpu_primeira_vez

    def get_cpu(self):
        return self._tempo_cpu


    def reiniciaProcesso(self, instante_atual):
        #Reinizaliza execução
        self._tempo_cpu -= 1
        self.tEspera += (instante_atual - self.instante_entrada)


    def iniciaProcesso(self, instante_atual, instante_entrada):
        #Primeiro instante de execução
        self.tRetorno = 1
        self._tempo_cpu -= 1

        #Inicialização dos contadores
        self.tEspera = instante_atual - self.instante_inicial
        self.tResposta = instante_atual - instante_entrada


    def executaProcesso(self):
        #Executa
        self._tempo_cpu -= 1
        if self._tempo_cpu <= 0:
            return False #Processo finalizado e não pode executar mais
        elif self._tempo_cpu > 0:
            return True #Processo finalizado e executou 1 segundo


    def pausaProcesso(self, instante_atual):
        #Quando o processo é pausado, ele volta a fila, o que se torna atualmente o seu instante entrada 
        self.instante_entrada = instante_atual
        

    def finalizaProcesso(self, instante_atual):
        self.tRetorno = (instante_atual - self.instante_inicial) + 1#Somo com 1 para contabilizar o começo do próximo segundo
        return self.tResposta, self.tRetorno, self.tEspera
