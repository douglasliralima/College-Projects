def leArquivo():
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
    print(Ram)
    for i in paginas:
        if i in Ram:
            continue
        else:
            miss += 1
            if pos == tamRam:
                pos = 0
            Ram[pos] = i
            pos+=1
        print(Ram)
    return miss



def OTM(Ram, tamRam, paginas):
    '''
    Vamos primeiro verificar se aquele elemento está na RAM, se não tiver, 
    vamos verificar qual página demorou 
    '''
    pos = 0
    miss = 0
    cheio = False
    paginasAux = paginas.copy()
    for i in paginas:
        paginasAux.pop(0)  
        print(Ram, paginasAux)
        if i in Ram:
            continue
        #Vai encher a Ram
        elif cheio == False:
            miss += 1
            Ram[pos] = i
            pos+=1
            
            if pos == tamRam:
                cheio = True
        #Após a Ram estar cheia
        else:
            '''
            Para verificar a página no futuro, vamos ver qual demora mais para ser
            chamado, o que mais demorar será substituido
            '''
            miss += 1
            pos = 0 #Volta ao inicio
            posMaior = 0
            maiorDemora = 0
            demora = 0
            #Para cada elemento da Ram
            for j in Ram:
                #Verificamos o quanto ele demora para aparecer novamente
                for k in paginasAux:
                    demora += 1
                    if j == k:
                        break
                #Se acharmos algum elemento que demora > 0, ele passa a ser o mais demorado
                if maiorDemora < demora:
                    maiorDemora = demora
                    posMaior = pos
                    
                if pos + 1 != tamRam:
                    pos += 1
            Ram[pos] = i
    return miss
                
                

Ram, tamRam, paginas = leArquivo()

#FIFO(Ram.copy(), tamRam, paginas.copy())
OTM(Ram.copy(), tamRam, paginas.copy())