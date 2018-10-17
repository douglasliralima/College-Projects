def leArquivo():
    #Paginas 1 tem o caso pequeno
    #Páginas 2 tem o caso maior
    arq = open('paginas.txt', 'r')
    texto = arq.readlines()
    arq.close()
    #Vamos fazer duas listas, uma representando os espaços em memória Ram e outra com as páginas
    tamRam = 0
    primeira = True
    paginas = []
    for lines in texto:
        #Vamos ler o número de páginas possíveis em memória Ram
        if primeira == True:
            tamRam = int(lines)
            primeira = False
            continue
        paginas.append(int(lines))
    Ram = []
    #Criamos uma RAM inicialmente com todas as posições zeradas
    for i in range(tamRam):
        Ram.append('-')
        
    return Ram, tamRam, paginas



def FIFO(Ram, tamRam, paginas):
    '''
    Vamos primeiro verificar se aquele elemento está na RAM, se não tiver, 
    vai ir colocando na última posição
    '''
    pos = 0
    miss = 0
    #print(Ram)
    #Para cada uma das páginas de entrada
    for i in paginas:
        #Se ela já entrou na RAM, executa e já podemos ir para a próxima página
        if i in Ram:
            continue
        #Se não entrou, ela dá miss, e substuimos o que estava naquela posição da RAM
        else:
            miss += 1
            if pos == tamRam: #Vamos fazendo isso em fila
                pos = 0 #Sempre zerando a fila ao chegar no fim
            Ram[pos] = i
            pos+=1
        #print(Ram)
    return "FIFO " + str(miss)



def OTM(Ram, tamRam, paginas):
    '''
    Vamos primeiro verificar se aquele elemento está na RAM, se não tiver, 
    vamos verificar qual página demorou 
    '''
    instante = 0
    pos = 0
    miss = 0
    cheio = False
    paginasAux = paginas.copy()
    tempos = {}
    for i in paginas:
        tempos[paginasAux.pop(0)] = instante
        instante += 1
        if i in Ram:
            #print("Repetiu", Ram, "\nPáginas para deletar:", paginasAux)
            #print("Repetiu", Ram)
            continue
        #Vai encher a Ram
        elif cheio == False:
            miss += 1
            Ram[pos] = i
            pos+=1
            
            if pos == tamRam:
                pos = 0
                cheio = True
        #Após a Ram estar cheia
        else:
            '''
            Para verificar a página no futuro, vamos ver qual demora mais para ser
            chamado, o que mais demorar será substituido
            '''
            miss += 1
            
            posAux = 0 #Volta ao inicio
            posMaior = 0
            maiorDemora = 0
            #Para cada elemento da Ram
            for j in Ram:
                demora = 0
                #Primeiro verificamos o elemento que foi inserido mais antigamente
                #e vemos se ele ainda aparece 
                
                if j not in paginasAux:
                    posMaior = Ram.index(j)
                    break
                #Verificamos o quanto ele demora para aparecer novamente, caso esteja na lista
                for k in paginasAux:
                    demora += 1
                    if j == k:
                        break
                    
                #Se acharmos algum elemento que demora > 0, ele passa a ser o mais demorado
                if maiorDemora < demora:
                    maiorDemora = demora
                    posMaior = posAux
                    
                if posAux + 1 != tamRam:
                    posAux += 1
                    
            Ram[posMaior] = i
            pos = posMaior #O atual elemento que foi inserido passa a ser o mais atual
        #print("Miss", Ram, "\nPáginas para deletar:", paginasAux)
        #print("Miss", Ram)
    return "OTM " + str(miss)

def LRU(Ram, tamRam, paginas):
    '''
    Vamos primeiro verificar se aquele elemento está na RAM, se não tiver, 
    vamos verificar qual foi a última paǵina que foi inserida
    '''
    instante = 0
    pos = 0
    miss = 0
    cheio = False
    paginasAux = paginas.copy()
    tempos = {}
    for i in paginas:
        #Vamos adicionando no dic os instantes de novas páginas ou substituimos os das antigas
        tempos[paginasAux.pop(0)] = instante
        instante += 1
        #Se já está na Ram, executa, pois já está na Ram
        if i in Ram:
            #print("Repetiu", Ram, "\nPáginas para deletar:", paginasAux)
            #print("Repetiu", Ram)
            continue
        #Vamos enchendo a Ram
        elif cheio == False:
            miss += 1
            Ram[pos] = i
            pos+=1
            #Verificação se a RAM ficou cheia
            if pos == tamRam:
                pos = 0
                cheio = True
        #Após a Ram estar cheia
        else:
            '''
            Para verificar a página no passado, vamos ver qual faz mais tempo que foi
            chamada, o que mais fizer será substituido
            '''
            miss += 1
            maiorInst = 0
            maiorPag = 0
            primeiro = True
            #Primeiro vamos verificar qual valor tem o menor instante e qual é essa página
            for j in Ram:
                if primeiro == True:
                    primeiro = False
                    maiorInst = tempos[j]
                    maiorPag = j
                    
                elif maiorInst > tempos[j]:
                    maiorInst = tempos[j]
                    maiorPag = j
            #Depois substituimos na Ram a posição com a página mais antiga, com a nova página
            Ram[Ram.index(maiorPag)] = i
        #print("Miss", Ram, "\nPáginas para deletar:", paginasAux)
        #print("Miss", Ram)
    return "LRU " + str(miss)


Ram, tamRam, paginas = leArquivo()

print(FIFO(Ram.copy(), tamRam, paginas.copy()))
print(OTM(Ram.copy(), tamRam, paginas.copy()))
print(LRU(Ram.copy(), tamRam, paginas.copy()))