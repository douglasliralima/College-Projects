import os
from processo import processo

def leArquivo():
    arq = open('process.txt', 'r')
    texto = arq.readlines()
    #Vamos fazer um dicionário, com os tempos de entrada e pico de cada processo
    processos = {}
    for lines in texto:
        #Vamos ler o tempo de chegada
        dados = lines.split(" ")
        instante = int(dados[0])
        pico = int(dados[1])
        #Se o processo já existir ele vai para o final da fila daquele processo
        if instante in processos.keys():
            processos[instante].append(pico)
        #Se o instante nunca foi adicionado ao dicionário, inicializamos a fila
        else:
            processos[instante] = [pico] #Tranformação implicita em lista
    arq.close()
    return processos



def FCFS(processos):
    tResposta = [] #Primeira vez que o processo é startado
    tRetorno = [] #Quando processo finaliza
    tEspera = [] #Enquanto o processo está esperando

    #Primeiro pegamos o tempo total de processamento que vai acontecer
    iniciais = list(processos.keys())

    #Vamos pegar o maior tempo total possível no pior caso
    tTotal = 0
    for i in list(processos.keys()):
        tTotal += i #Ir até o instante do processo
        soma = 0
        for j in processos[i]:
            soma += j
        tTotal += soma#Ver quanto tempo aquele instante ficará processando


    fila = [] #Será a fila de processos que vai entrar no processador
    cpu = False #Simboliza se a CPU está cheia ou não
    nProc = 0 #Auxiliar que representa a quantidade de processos na fila

    #Vamos aqui simular cada segundo em um processador nesse tempo
    for tempoAtual in range(tTotal):

        #Vamos verificar se estamos em um tempo de entrada de algum processo
        if tempoAtual in processos.keys():
            #Vamos receber os processo que entram
            fila += processos[tempoAtual]
            #Vamos somar a quantidade atual de processos
            nProc += len(processos[tempoAtual])

        #Esse laço vai ver se o processador está livre e colocar um proc caso esteja
        if cpu == False and nProc > 0:
            #Primeiro vamos pegar o instante de entrada no processador
            instante_inicial = 0
            for instantes in processos.keys():
                if fila[0] in processos[instantes]:
                    instante_inicial = instantes
            #E criar o processo
            proc = processo(fila[0], instante_inicial)
            #Processo criado, ele é startado e retirado da fila
            proc.iniciaProcesso(tempoAtual, instante_inicial)
            del(fila[0])
            cpu = True #Falamos qua há processo no processador

        #Se houver processo no processador o executamos
        elif nProc > 0:
            executado = proc.executaProcesso()
            #Até que chegamos no momento em que o processo acabe de processar
            if executado == False:
                #Guardamos os valores de resposta, retorno e espera em nossa "tabela"
                x, y, z = proc.finalizaProcesso(tempoAtual)
                tResposta.append(x)
                tRetorno.append(y)
                tEspera.append(z)
                nProc -= 1 #Simboliza que um processo morreu
                cpu = False #Esvazia a flag da CPU

    #Fazemos as médias dos tempos para retornar da função
    tRetornoMedio = 0.0
    for i in range(len(tRetorno)):
        tRetornoMedio += tRetorno[i]
    tRetornoMedio /= len(tRetorno)

    tRespostaMedio = 0.0
    for i in range(len(tResposta)):
        tRespostaMedio += tResposta[i]
    tRespostaMedio /= len(tResposta)

    tEsperaMedio = 0.0
    for i in range(len(tEspera)):
        tEsperaMedio += tEspera[i]
    tEsperaMedio /= len(tEspera)

    return tRetornoMedio, tRespostaMedio, tEsperaMedio




def SJF(processos):
    tResposta = [] #Primeira vez que o processo é startado
    tRetorno = [] #Quando processo finaliza
    tEspera = [] #Enquanto o processo está esperando

    
    #Vamos pegar o maior tempo total possível no pior caso
    tTotal = 0
    for i in list(processos.keys()):
        tTotal += i #Ir até o instante do processo
        soma = 0
        for j in processos[i]:
            soma += j
        tTotal += soma#Ver quanto tempo aquele instante ficará processando


    fila = []
    cpu = False #Simboliza se a CPU está cheia ou não
    instanteEntrada = {}
    nProc = 0 #Vamos já considerar o primeiro processo que vai entrar

    for tempoAtual in range(tTotal): #+1 pelo instante 0 ser contado
        if tempoAtual in processos.keys():
            #Vamos receber e ordenar os processo que entram
            fila += processos[tempoAtual]
            #Vamos somar a quantidade atual de processos que entram para saher quantos ainda tem
            nProc += len(processos[tempoAtual])
            #A única diferença aqui é essa, quando processos entram na fila, ela
            #é ordenada
            fila.sort()


        if cpu == False and nProc > 0:
            instante_inicial = 0
            for instantes in processos.keys():
                if fila[0] in processos[instantes]:
                    instante_inicial = instantes
            proc = processo(fila[0], instante_inicial)
            proc.iniciaProcesso(tempoAtual, instante_inicial)
            del(fila[0])
            cpu = True


        elif nProc > 0:
            executado = proc.executaProcesso()
            if executado == False:
                x, y, z = proc.finalizaProcesso(tempoAtual)
                tResposta.append(x)
                tRetorno.append(y)
                tEspera.append(z)
                nProc -= 1
                cpu = False


    #Fazemos as médias dos tempos para retornar da função
    tRetornoMedio = 0.0
    for i in range(len(tRetorno)):
        tRetornoMedio += tRetorno[i]
    tRetornoMedio /= len(tRetorno)

    tRespostaMedio = 0.0
    for i in range(len(tResposta)):
        tRespostaMedio += tResposta[i]
    tRespostaMedio /= len(tResposta)

    tEsperaMedio = 0.0
    for i in range(len(tEspera)):
        tEsperaMedio += tEspera[i]
    tEsperaMedio /= len(tEspera)

    return tRetornoMedio, tRespostaMedio, tEsperaMedio



def RR(processos):
    tResposta = []
    tRetorno = []
    tEspera = []


    
    #Vamos pegar o maior tempo total possível no pior caso
    tTotal = 0
    for i in list(processos.keys()):
        tTotal += i #Ir até o instante do processo
        soma = 0
        for j in processos[i]:
            soma += j
        tTotal += soma#Ver quanto tempo aquele instante ficará processando


    fila = []
    prontos = []
    cpu = False #Simboliza se a CPU está cheia ou não
    instanteEntrada = {}

    #Tempo do quantum, ele é 1, pois representa o instante 0 e 1
    #Inicializamos ele aqui graças ao segundo if do for abaixo
    quantum = 1 

    nProc = 0 #Vamos já considerar o primeiro processo que vai entrar
    for tempoAtual in range(tTotal):

        if tempoAtual in processos.keys():
            #Vamos receber e ordenar os processo que entram
            fila += processos[tempoAtual]
            #Vamos somar a quantidade atual de processos que entram
            nProc += len(processos[tempoAtual])



        #Verificação a partir do 1º processo se o seu quantum acabou
        if quantum <= 0:
            #Caso tenha acabado o processo é pausado e reincide na fila
            proc.pausaProcesso(tempoAtual)
            fila.append(proc)
            cpu = False


        if cpu == False and nProc > 0:
            quantum = 1 #Quantum passa a voltar a ser 1, caso tenha sido modificado anteriormente
            
            #Se tiver guardado na fila apenas o tempo de pico de um processo
            #Precisamos inicializar e instanciar o processo da mesma maneira que já
            #vinhamos fazendo
            if type(fila[0]) == type(int()):
                instante_inicial = 0
                for instantes in processos.keys():
                    if fila[0] in processos[instantes]:
                        instante_inicial = instantes
                proc = processo(fila[0], instante_inicial)
                proc.iniciaProcesso(tempoAtual, instante_inicial)
                del(fila[0])
                cpu = True
            #Se o processo já foi criado e está na fila, executamos o código abaixo
            #Veja que isso só é necessário quando há preempção
            else:
                proc = fila.pop(0)
                proc.reiniciaProcesso(tempoAtual)

                cpu = True
            

        elif nProc > 0:
            executado = proc.executaProcesso() #Executamos o processo
            if executado == False: #Se acabou seu tempo de execução, ele morre
                x, y, z = proc.finalizaProcesso(tempoAtual)
                tResposta.append(x)
                tRetorno.append(y)
                tEspera.append(z)
                nProc -= 1
                cpu = False
                #E o quantum volta a ser zero
                #n interessando que instante isso aconteceu
                quantum = 1

            else: #Caso o processo continue executando, diminuimos o quantum
                quantum -= 1
                        
    #Fazemos as médias dos tempos para retornar da função
    tRetornoMedio = 0.0
    for i in range(len(tRetorno)):
        tRetornoMedio += tRetorno[i]
    tRetornoMedio /= len(tRetorno)

    tRespostaMedio = 0.0
    for i in range(len(tResposta)):
        tRespostaMedio += tResposta[i]
    tRespostaMedio /= len(tResposta)

    tEsperaMedio = 0.0
    for i in range(len(tEspera)):
        tEsperaMedio += tEspera[i]
    tEsperaMedio /= len(tEspera)

    return tRetornoMedio, tRespostaMedio, tEsperaMedio




processos = leArquivo()
tRetorno, tResposta, tEspera = FCFS(processos)
print('FCFS', tRetorno, tResposta, tEspera)

tRetorno, tResposta, tEspera = SJF(processos)
print('SJF', tRetorno, tResposta, tEspera)

tRetorno, tResposta, tEspera = RR(processos)
print('RR', tRetorno, tResposta, tEspera)