import glob
import os
import numpy as np
import pandas as pd
import utils as utils
import distance as dist
import math 

#* Função para ler todos os arquivos dos pacientes em csv 
def read_folder():

    csv_folder = glob.glob(os.path.join(utils.PATH_FILES, "*csv")) #* cria um vetor com os paths de todos os arquivos .csv contidos na pasta "PATH_FILES"

   

    for file in csv_folder: #* percorre o vetor com os paths dos arquivos .csv
        fileName = os.path.basename(file)

        #* verificamos se os dados estão separados por ",", os que estão por vírgula foram colocados nesse "FILES_SEP"

        if fileName in utils.FILES_SEP:
            df = pd.read_csv(file, sep = ",")
            df.columns = df.columns.str.upper()
            df = df.iloc[:, 1:] #* retirando coluna "Time"
            df, channelsMiss = insert_columns(df)
            df = algorithm(df, channelsMiss, fileName)
        
        
        else:
            df = pd.read_csv(file, sep = "\t") #* arquivos separados por tabulação
            df.columns = df.columns.str.upper()
            df = df.iloc[:, 1:]
            df, channelsMiss = insert_columns(df)
            df = algorithm(df, channelsMiss, fileName)
          
def save_file(fileName, nameFile, df):
    df.to_csv(''.join(fileName) + "/" + nameFile, index= False)  

#* Função que ordena, cria um vetor com os eletrodos faltantes e insere uma coluna -1 no local 
def insert_columns(df):
    
    df = df.reindex(columns=utils.CHANNELS) #* reordenando as colunas com base da ordem do vetor "CHANNELS" contido em utils
    channelsMiss  = df.columns[df.isna().any()].tolist() #* vetor com os eletrodos faltantes do arquivo 
    channelsMiss.pop(0) #* retirando CZ do vetor de faltantes
    df = df.fillna(-1) #* substituindo os valores NaN por -1 
    df['CZ'] = 0 
    
    return df, channelsMiss

#* Função que realiza a interpolação e salva o novo csv         
def algorithm(df, channelsMiss, fileName):
    
    dfInterpol = pd.DataFrame(columns=channelsMiss) #* criando um dataframe apenas com os eletrodos que serão interpolados
    matrixDistance = dist.df #* importando a matriz de distâncias 
      
    for electrode in channelsMiss:
        channelsInterpol = [] #* matriz que irá guardar as interpolações de cada eletrodo
        distanceChannel = matrixDistance[electrode] 
        
        
    #* O método interrows() retorna uma tupla contendo o índice e uma série com os valores daquela linha.
        for index, data in df.iterrows():
            accumuDen = 0 #* acumulador responsável pelo somatório do denominador
            accumuNum = 0 #* acumulador responsável pelo somatório do numerador
            
            #* o método items() percorre a série e retorna o rótulo da coluna e seu valor
            for row, channel in zip(data.items(), distanceChannel):
                column, value = row #* descompactando o retorno de data.items()
               
                if value !=-1: #*verificando se não é um eletrodo faltantes
                    accumuNum += value * math.exp(-channel)  #* channel é o valor da distância do eletrodo faltante para todos os outros eletrodos
                    accumuDen += math.exp(-channel)
                    
            interpol = round(accumuNum/accumuDen, 4)
            channelsInterpol.append(interpol) 
            
        dfInterpol[electrode] = channelsInterpol
        
    df = df.drop(columns=channelsMiss) 
    dfFinal = pd.concat([df, dfInterpol], axis=1) 
    dfFinal = dfFinal.reindex(columns=utils.CHANNELS)
    dfFinal = dfFinal.iloc[:, 1:] #* retirando a coluna do eletrodo CZ

    save_file(utils.PATH_INTERPOL_FILE, fileName, dfFinal)
    
if __name__ == "__main__":
    read_folder()