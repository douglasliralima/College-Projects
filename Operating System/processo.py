class processo:
    #Inicialização do processo
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


    #Caso a gente inicialize o processo pela primeira vez
    def iniciaProcesso(self, instante_atual, instante_entrada):
        #Primeiro instante de execução
        self.tRetorno = 1 #Primeira execução e sua demora para retornar
        self._tempo_cpu -= 1 #Execução em si

        #Inicialização dos contadores
        self.tEspera = instante_atual - self.instante_inicial #Caso tenha sido mandado no 4, mas apenas inicializado no 6
        self.tResposta = instante_atual - self.instante_inicial 


    #Caso a gente reinicie o código, ele executa nesse instante de reinicialização
    #E atualizamos apenas o tempo de espera
    def reiniciaProcesso(self, instante_atual):
        #Reinizaliza execução
        self._tempo_cpu -= 1
        self.tEspera += (instante_atual - self.instante_entrada)


    #Caso a gente queira apenas executar o processo
    def executaProcesso(self):
        self._tempo_cpu -= 1 #Executa
        if self._tempo_cpu <= 0: #Caso o seu tempo tenha acabado
            return False #Processo finalizado e não pode executar mais
        elif self._tempo_cpu > 0: #Caso não
            return True #Processo finalizado e executou 1 segundo


    def pausaProcesso(self, instante_atual):
        #Quando o processo é pausado, ele volta a fila, o que se torna atualmente o seu instante entrada na fila
        self.instante_entrada = instante_atual
        
    #Verificamos quanto tempo demorou para executar
    #Retornamos todos os tempos daquele processo
    def finalizaProcesso(self, instante_atual):
        #Somo com 1 para contabilizar o começo do segundo de finalização
        self.tRetorno = (instante_atual - self.instante_inicial) + 1
        return self.tResposta, self.tRetorno, self.tEspera
