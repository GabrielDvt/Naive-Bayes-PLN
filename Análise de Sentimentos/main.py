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
from string import punctuation
import numpy as np
import re
import time

#duas variaveis globais (serão utilizadas na função treino e teste)
palavras = []
labels = []

def treino():
    print("Treinando...")
    #lê o arquivo (treina com 7000 palavras)
    dataset = pd.read_csv('tweets.csv')
    
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
           
        #para cada palavra do comentário
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

    for p in positivas:
        total_positivos += p

    for n in negativas:
        total_negativos += n

    for neu in neutras:
        total_neutros += neu

    #total de palavras contadas
    total = total_positivos + total_negativos + total_neutros

    #fração positiva
    fracao_positiva = total_positivos / total

    #fração negativa
    fracao_negativa = total_negativos / total

    #percorre cada palavra novamente, para buscar estatísticas (montar a tabela de freq)
    for index, palavra in enumerate(palavras):
        #soma = quantidade total de vezes que essa palavra apareceu na base de dados
        soma = negativas[index] + positivas[index] + neutras[index]
        probabilidades.append(soma / total)

        #Quantas vezes essa palavra apareceu como positiva no total?
        porcentagem_positiva = positivas[index] / total_positivos

        #Quantas vezes essa palavra apareceu como negativa no total?
        porcentagem_negativa = negativas[index] / total_negativos

        #calculando:
        probabilidade_positiva = porcentagem_positiva * fracao_positiva / probabilidades[index]
        probabilidade_negativa = porcentagem_negativa * fracao_negativa / probabilidades[index]

        #verifica qual probabilidade é maior e adiciona na label
        if (probabilidade_positiva > probabilidade_negativa):
            labels.append("Positivo")
        elif (probabilidade_negativa > probabilidade_positiva):
            labels.append("Negativo")
        else:
            labels.append("Neutro")
    
    #print(labels)
    print("Treino finalizado.")
    return

def teste():
    
    start_time = time.time()
    
    print("Testando...\n")
    
    dataset = pd.read_csv('tweets.csv')

    #pega 1700 frases aleatórias
    sample = dataset.sample(n=1700)

    #busca o que são tweets e o que são classes
    teste = sample['Text'].values
    #vetor de resultados esperados
    classes = sample['Classificacao'].values
    
    #vetor de resultados reais
    resultado = []
    contador = 0
    #falsos positivos, falsos negativos, true positivos, true negativos
    fp = 0
    fn = 0
    tp = 0
    tn = 0
    
    #percorre cada frase do teste
    for frase in teste:
        
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

            #verifica se essa palavra existe no treino
            if palavra in palavras:
                #verifica o caráter dessa palavra no treino
                index = palavras.index(palavra)
                classificacao = labels[index]
                if (classificacao == "Positivo"):
                    cont_pos += 1
                elif (classificacao == "Negativo"):
                    cont_neg += 1
                else:
                    cont_neu += 1
                
            #caso a palavra não exista no treino, então devemos atribuir a ela o valor de maior frequência no treino
            else:
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
                
        #verifica os contadores e decide se a palavra é pos, neg, ou neu
        if (cont_pos > cont_neg) and (cont_pos > cont_neu):
            resultado.append("Positivo")
        elif (cont_neg > cont_pos) and (cont_neg > cont_neu):
            resultado.append("Negativo")
        else:
            resultado.append("Neutro")

    #verifica falsos positivos, falsos negativos e calcula a precisão do método
    '''for index, res in enumerate(resultado):
        if (res == "Positivo") and (res == classes[index]):
            tp += 1
        elif (res == "Positivo") and (res != classes[index]):
            fp += 1
        elif (res == "Negativo") and (res == classes[index]):
            tn += 1
        elif (res == "Negativo") and (res != classes[index]):
            fn += 1'''
    
        
    
    print("Testes finalizados.")
    
    print("Tempo de execução: %s segundos" % (time.time() - start_time))

    a = np.array(resultado)
    b = np.array(classes)

    print("Total de tweets verificados: " ,len(resultado))
    print("Acerto: ", ((a == b).sum() * 100 / len(resultado)), "%")
    print("Erros: ", ((a != b).sum() * 100 / len(resultado)), "%")

    return


treino()
teste()
    
#    print("Palavra: ", palavra)
 #   print("Prob. Pos: ", prob_positiva)
  #  print("Prob. Neg: ", prob_negativa, "\n")


'''print('positivos', total_positivos)
print('negativos', total_negativos)
print('neutros', total_neutros)
print('fracao_positiva', fracao_positiva)
print('fracao_negativa', fracao_negativa)
print('Vetor de probabilidades: ', probabilidades)'''


        
