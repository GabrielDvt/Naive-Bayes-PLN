'''
## Algoritmo desenvolvido por:
##
## Gabriel Augusto De Vito
## gabriel.dvt@hotmail.com
##
## Danilo Silva Bentes
## danilosilvabentes@gmail.com
##
## Desenvolvido durante a disciplina de PLN, cursada na Universidade Federal de Goiás
## Professor Sandrerley
##
## Adaptação do algorítmo encontrado em: http://minerandodados.com.br/index.php/2017/03/15/analise-de-sentimentos-twitter-como-fazer/
## Sem a utilização de funções milagrosas das bibliotecas do Python
## 06/2018
##
'''

import pandas as pd
import numpy as np
import re
import time
import csv

#duas variaveis globais (serão utilizadas na função treino e teste)
palavras = []
pesos = []      #vetor que possui o peso de cada palavra
labels = []

def treino():
    start_time = time.time()
    print("Treinando...")
    
    #lê o arquivo (treina com 7000 de um total de 8900 linhas)
    dataset = pd.read_csv('treino.csv', nrows=7000)
    
    #busca o que são tweets e o que são classes
    tweets = dataset['Text'].values
    classes = dataset['Classificacao'].values
    
    #lista que irá conter as palavras, os positivos, negativos e nêutros
    global palavras
    negativas = []
    positivas = []
    neutras = []

    #calcula a frequência de cada palavra  
    probabilidades = []

    #com posse do vetor de positivos, negativos e nêutros, podemos criar as tabelas de probabilidades
    total_positivos = 0
    total_negativos = 0
    total_neutros = 0

    #no final, cada palavra terá uma label (positiva ou negativa) baseada na base de dados
    global labels

    #comentário a comentário
    for i,tweet in np.ndenumerate(tweets):
      
        for word in tweet.split():
            
            #remove aspas, dois pontos, vírgulas, etc
            word = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ\-\/ ]', '', word)

            #zera os negativos positivos e neutros
            pos = 0
            neg = 0
            neutro = 0

            #este comentario tem carater positivo, negativo ou nêutro?
            if (classes[i] == 'Positivo'):
                pos = 1
                        
            elif (classes[i] == 'Neutro'):
                neutro = 1
                        
            elif (classes[i] == 'Negativo'):
                neg = 1
                    
            #se a palavra não estiver na lista, adicionar
            if word not in palavras:
                palavras.append(word)   #adiciona a palavra
                negativas.append(neg)
                positivas.append(pos)
                neutras.append(neutro)

            #se a palavra ja estiver na lista, procurá-la e atualizar os índices
            else:
                index = palavras.index(word)
                positivas[index] += pos
                negativas[index] += neg
                neutras[index] += neutro

    #Apenas contabiliza quantas palavras são positivas, negativas e nêutras
    for p in positivas:
        total_positivos += p

    for n in negativas:
        total_negativos += n

    for neu in neutras:
        total_neutros += neu

    #total de palavras contadas
    total = total_positivos + total_negativos + total_neutros

    #fração positiva: P(positive)
    fracao_positiva = total_positivos / total

    #fração negativa: P(negative)
    fracao_negativa = total_negativos / total

    
    #percorre cada palavra novamente, para buscar estatísticas (montar a tabela de freq)
    for index, palavra in enumerate(palavras):
        
        #soma = quantidade total de vezes que essa palavra apareceu na base de dados
        soma = negativas[index] + positivas[index] + neutras[index]
        
        #vetor probabilidades: contém a probabilidade de cada palavra aparecer na base de dados: P('love')
        probabilidades.append(soma / total)
        
        #Probabilidade desta palavra aparecer e ser positiva (P('love'|positive))
        porcentagem_positiva = positivas[index] / total_positivos

        #Probabilidade desta palavra aparecer e ser negativa (P('love'|negative))
        porcentagem_negativa = negativas[index] / total_negativos

        #Probabilidade desta palavra aparecer e ser neutra
        porcentagem_neutra = neutras[index] / total_neutros

        #calculando:
        
        #P(positive|'love') = P('love'|positive) * P(positive) / P('love')
        probabilidade_positiva = porcentagem_positiva * fracao_positiva / probabilidades[index]
        
        #P(negative|'love') = P('love'|negative) * P(negative) / P('love')
        probabilidade_negativa = porcentagem_negativa * fracao_negativa / probabilidades[index]

        #verifica qual probabilidade é maior e adiciona na label (Utiliza o algoritmo naive bayes)
        #também 
        if (probabilidade_positiva > probabilidade_negativa):
            labels.append("Positivo")
            pesos.append(porcentagem_positiva)      #porcentagem_positiva significa o peso desta palavra
        elif (probabilidade_negativa > probabilidade_positiva):
            labels.append("Negativo")
            pesos.append(porcentagem_negativa)
        else:
            labels.append("Neutro")
            pesos.append(porcentagem_neutra)

    print("Treino finalizado.")
    print('Total de palavras positivas: ', total_positivos)
    print('Total de palavras negativas: ', total_negativos)
    print('Total de palavras neutras: ', total_neutros)
    print('Total de paalvras classificadas: ', total_positivos + total_negativos + total_neutros)
    print("Tempo de execução: %s segundos" % (time.time() - start_time))
    
    return

def teste():
    start_time = time.time()
    
    print("Testando...\n")

    dataset = pd.read_csv('treino.csv')
    sample = dataset.sample(n=1700)
    #dataset = pd.read_csv('tweets.csv', encoding="cp1252")

    #pega 1700 frases aleatórias
    #sample = dataset.sample(n=1700) #(sample)

    #busca o que são tweets e o que são classes
    teste = sample['Text'].values
    #vetor de resultados esperados
    #classes = sample['Classificacao'].values
    
    #vetor de resultados, contendo a classificação de cada palavra do teste
    resultado = []
    
    contador = 0
    #falsos positivos, falsos negativos, true positivos, true negativos
    fp = 0
    fn = 0
    tp = 0
    tn = 0
    
    #percorre cada frase do teste
    for frase in teste:
        print(frase)
        contador += 1
        
        print("Categorizadas ", contador, " frases.")
        
        #contador de palavras positivas nessa frase
        cont_pos = 0
        
        #contador de palavras negativas nessa frase
        cont_neg = 0

        #contador de palavras nêutras nessa frase
        cont_neu = 0

        #percorre cada palavra da frase
        for palavra in frase.split():
            
            #remove as coisas desnecessárias
            palavra = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ\-\/ ]', '', palavra)

            #caso a palavra já exista no treino
            if palavra in palavras:
                #verifica o caráter dessa palavra no treino
                index = palavras.index(palavra)
                classificacao = labels[index]
     
                soma_pesos_pos = 0      #somatório dos pesos positivos
                soma_pesos_neg = 0      #somatorio dos pesos negativos
                soma_pesos_neu = 0
                
                if (classificacao == "Positivo"):
                    soma_pesos_pos += pesos[index]
                elif (classificacao == "Negativo"):
                    soma_pesos_neg += pesos[index]
                else:
                    soma_pesos_neu += pesos[index]
                
            
            #caso a palavra não exista no treino, então devemos atribuir a ela o valor de maior frequência no treino
            '''else:
                #conta quantas são positivas
                qtde_pos = labels.count("Positivo")
                #conta quantas são negativas
                qtde_neg = labels.count("Negativo")

                if (qtde_pos > qtde_neg):
                    cont_pos += 1
                elif (qtde_neg > qtde_pos):
                    cont_neg += 1
                else:
                    cont_neu += 1
              '''
        #verifica os contadores e decide se a frase é pos, neg, ou neu
        if (soma_pesos_pos > soma_pesos_neg and soma_pesos_pos > soma_pesos_neu):
            resultado.append("Positivo")
        elif(soma_pesos_neg > soma_pesos_pos and soma_pesos_neg > soma_pesos_neu):
            resultado.append("Negativo")
        else:
            resultado.append("Neutro")

    #cria um novo arquivo csv
    #csvFile = open('resultado.csv', 'a', newline='')
    #csvWriter = csv.writer(csvFile)
    #for (index, frase) in enumerate(teste):
    #    csvWriter.writerow([frase, resultado[index]])

    print("Testes finalizados.")
    print("Tempo de execução: %s segundos" % (time.time() - start_time))
    print("Total de tweets verificados: " ,len(resultado))

    qtdePos = resultado.count("Positivo")
    qtdeNeg = resultado.count("Negativo")
    qtdeNeu = resultado.count("Neutro")

    porcentagemPos = qtdePos*100/len(resultado)
    porcentagemNeg = qtdeNeg*100/len(resultado)
    porcentagemNeu = qtdeNeu*100/len(resultado)

    print("Pos:", qtdePos, " - ", porcentagemPos, '%')
    print("Neu:", qtdeNeu, " - ", porcentagemNeu, '%')
    print("Neg:", qtdeNeg, " - ", porcentagemNeg, '%')
    
    return

#roda o algoritmo
treino()
#teste()
    



