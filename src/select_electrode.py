import os
import glob
import pandas as pd
import utils as utils

# Lista de colunas para cada tipo de arquivo
COLUMNS_CP1_CP2 = ['CP1', 'CP2']
COLUMNS_FC1_FC2 = ['FC1', 'FC2']
COLUMNS_CP1_CP2_FC1_FC2 = ['CP1', 'CP2', 'FC1', 'FC2']

csv_folder = glob.glob(os.path.join(utils.PATH_FILES, "*.csv"))

for file in csv_folder:
    fileName = os.path.basename(file)

    if fileName in utils.FILES_SEP:
        df = pd.read_csv(file, sep=",")
    else:
        df = pd.read_csv(file, sep="\t")

    df.columns = df.columns.str.upper()
    df = df.iloc[:, 1:]

    # Arquivos com CP1 e CP2
    if set(COLUMNS_CP1_CP2).issubset(df.columns):
        df_cp1_cp2 = df[COLUMNS_CP1_CP2]
        df_cp1_cp2.to_csv(os.path.join(utils.NEW_PATH_CP1_CP2, fileName), index=False)

    # Arquivos com FC1 e FC2
    if set(COLUMNS_FC1_FC2).issubset(df.columns):
        df_fc1_fc2 = df[COLUMNS_FC1_FC2]
        df_fc1_fc2.to_csv(os.path.join(utils.NEW_PATH_FC1_FC2, fileName), index=False)

    # Arquivos com CP1, CP2, FC1 e FC2
    if set(COLUMNS_CP1_CP2_FC1_FC2).issubset(df.columns):
        df_cp1_cp2_fc1_fc2 = df[COLUMNS_CP1_CP2_FC1_FC2]
        df_cp1_cp2_fc1_fc2.to_csv(os.path.join(utils.NEW_PATH_CP1_CP2_FC1_FC2, fileName), index=False)

