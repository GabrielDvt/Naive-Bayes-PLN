import os
import shutil

#O que você deseja procurar?
lookingfor = "Chat"
rootFolder = "arquivos"

#Para cada arquivo na pasta
for filename in os.listdir(rootFolder):
    #abre o arquivo
    f = open(rootFolder + "/" + filename, "r", encoding="utf8")
    if f.mode == "r":
        #transforma cada linha em um vetor
        lines = f.readlines()
        print(lines)
        #for index, x in enumerate(lines):
           # line = x.strip()
            #if lookingfor in line:
                #print ("Encontrei '" + lookingfor + "' na linha " + str(index) + " do arquivo " + filename)
    
            
