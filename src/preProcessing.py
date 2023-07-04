import glob
import os
import numpy as np
import pandas as pd
import utils as utils

nameFile = [] 

# função para ler todos os arquivos dos pacientes em csv 

def read_folder():

    # encontrar todos os arquivos com extensão ".csv" que são armazenados em uma lista chamada csv_folder

    csv_folder = glob.glob(os.path.join(utils.PATH_FILES, "*csv"))

    # faz um for pelos arquivos criando uma lista com o nome deles

    for file in csv_folder:
        FileName = os.path.basename
        nameFile.append(FileName)

        # verificamos se os dados estão separados por ",", os que estão por vírgula foram colocados nesse "FILES_SEP"

        if FileName in utils.FILES_SEP:
            df = pd.read_csv(file, sep = ",", nrows = 3)
            df.columns = df.columns.str.upper()
            df = df.iloc[:, 1:]
            df, channelsMiss = insert_columns(df)
            df = algorithm(df, channelsMiss)
        
        # aqui eles estão separados por tabulação
        
        else:
            df = pd.read_csv(file, sep = "\t", nrows = 3)
            df.columns = df.columns.str.upper()
            df = df.iloc[:, 1:]
            df, channelsMiss = insert_columns(df)
            df = algorithm(df, channelsMiss)
          
        
# função para encontar os eletrodos faltantes e colocar uma coluna com 0 nessses lugares

def insert_columns(df):
    
    df = df.reindex(columns=utils.CHANNELS)
    channelsMiss  = df.columns[df.isna().any()].tolist()
    channelsMiss.pop(0)
    
    return df, channelsMiss

def algorithm(df, channelsMiss):
    for channel in channelsMiss:
        print(f'canal: {channel}')
        

if __name__ == "__main__":
    read_folder()