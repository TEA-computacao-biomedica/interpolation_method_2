import glob
import os
import numpy as np
import pandas as pd
import utils as utils
import distance as dist
import math 

#* função para ler todos os arquivos dos pacientes em csv 

def read_folder():

    #* encontrar todos os arquivos com extensão ".csv" que são armazenados em uma lista chamada csv_folder

    csv_folder = glob.glob(os.path.join(utils.PATH_FILES, "*csv"))

    #* faz um for pelos arquivos criando uma lista com o nome deles

    for file in csv_folder:
        fileName = os.path.basename(file)

        #* verificamos se os dados estão separados por ",", os que estão por vírgula foram colocados nesse "FILES_SEP"

        if fileName in utils.FILES_SEP:
            df = pd.read_csv(file, sep = ",")
            df.columns = df.columns.str.upper()
            df = df.iloc[:, 1:]
            df, channelsMiss = insert_columns(df)
            df = algorithm(df, channelsMiss, fileName)
        
        #* arquivos separados por tabulação
        
        else:
            df = pd.read_csv(file, sep = "\t")
            df.columns = df.columns.str.upper()
            df = df.iloc[:, 1:]
            df, channelsMiss = insert_columns(df)
            df = algorithm(df, channelsMiss, fileName)
          
def save_file(fileName, nameFile, df):
    df.to_csv(''.join(fileName) + "/" + nameFile, index= False)  
        
#* função para encontar os eletrodos faltantes e colocar uma coluna com -1 nessses lugares
   

def insert_columns(df):
    
    df = df.reindex(columns=utils.CHANNELS) #* reordenando as colunas com base da ordem do vetor "CHANNELS"
    channelsMiss  = df.columns[df.isna().any()].tolist() #* vetor com os eletrodos faltantes do arquivo 
    channelsMiss.pop(0) #* retirando CZ do vetor de faltantes
    df = df.fillna(-1) #* substituindo os valores NaN por -1 
    df['CZ'] = 0 
    
    return df, channelsMiss

#* Função que faz a interpolação e salva o novo csv         
def algorithm(df, channelsMiss, fileName):
    
    dfInterpol = pd.DataFrame(columns=channelsMiss) #* criando um dataframe apenas com os eletrodos que serão interpolados
    matrixDistance = dist.df #* importando a matriz de distâncias 
      
    for electrode in channelsMiss:
        channelsInterpol = [] #* matriz que irá guardar as interpolações de cada eletrodo
        distanceChannel = matrixDistance[electrode] 
        
        
    #* O método interrows() retorna uma tupla contendo o índice da linha e uma série com os valores daquela linha.
        for index, data in df.iterrows():
            accumuDen = 0
            accumuNum = 0
            
            #* o método row.items() percorre a série e retorna o nome da coluna e seu valor
            for row, channel in zip(data.items(), distanceChannel):
                column, value = row #* descompactando o retorno de data.items()
                
                #* accumuDen é o acumulador responsável pelo somatório do denominador
                #* channel é o valor da distância do eletrodo alvo para todos os outros eletrodos
                if value !=-1: #*verificando se não é um eletrodo faltantes
                    accumuNum += value * math.exp(-channel)
                    accumuDen += math.exp(-channel)
                    
            interpol = round(accumuNum/accumuDen, 4)
            channelsInterpol.append(interpol) 
            
        dfInterpol[electrode] = channelsInterpol
        
    df = df.drop(columns=channelsMiss) 
    dfFinal = pd.concat([df, dfInterpol], axis=1) 
    dfFinal = dfFinal.reindex(columns=utils.CHANNELS)

    save_file(utils.PATH_INTERPOL_FILE, fileName, dfFinal)
    
if __name__ == "__main__":
    read_folder()