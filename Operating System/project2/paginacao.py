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
    tempos = {}
    for i in paginas:
        paginasAux.pop(0)  
        if i in Ram:
            print("Repetiu", Ram, "\nPáginas para deletar:", paginasAux)
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
            demora = 0
            #Para cada elemento da Ram
            for j in Ram:
                #Primeiro verificamos se aquele elemento aparece novamente na lista
                #Se o elemento não for aparecer mais, consideramos que o seu tempo de espera é
                #infinito, então vamos em FIFO, removendo aqueles que foram colocados 
                #primeiro, mas não aparecerão mais
                if j not in paginasAux:
                    posMaior = Ram.index(j)
                    
                    continue
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
        print("Miss", Ram, "\nPáginas para deletar:", paginasAux)
    return miss

                
                

Ram, tamRam, paginas = leArquivo()

#FIFO(Ram.copy(), tamRam, paginas.copy())
OTM(Ram.copy(), tamRam, paginas.copy())