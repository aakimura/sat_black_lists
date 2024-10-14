import os
import glob

import pandas as pd

from datetime import datetime as dt


# Constants
FILE_TRANSLATE = {
    'Cancelados.csv': 'cancelled',
    'No localizados.csv': 'not_located',
    'ReduccionArt74CFF.csv': 'fine_reduction',
    'Condonadosart146BCFF.csv': 'pardoned_by_bankrupcy',
    'Condonadosart21CFF.csv': 'surchage_reduction',
    'CondonadosporDecreto.csv': 'pardoned_by_decree',
    'Condonados_07_15.csv': 'pardoned_2007-2015',
    'Cancelados_07_15.csv': 'cancelled_2007-2015',
    'Retornoinversiones.csv': 'investment_repatriation',
    'Exigibles.csv': 'exigible',
    'Firmes.csv': 'solid',
    'Sentencias.csv': 'sentences',
    'CSDsinefectos.csv': 'invalid_csd',
    'EntespublicosydeGobiernoomisos.csv': 'public_entities'
}


HOME_PATH = os.getcwd()
DATA_PATH = os.path.join(HOME_PATH, 'data/')
SAT_PATH = os.path.join(DATA_PATH, 'sat/')
PROCESSED_PATH = os.path.join(DATA_PATH, 'processed/')
BLACK_LIST_PATH = os.path.join(SAT_PATH, 'black_lists/')


def get_latest_folder(return_path: bool = True):
    """
    Gets the latest folder by verifying their represented date on the directory
    name

    Parameters
    ----------
    return_path<bool>: Whether the path should be returned with the folder name.

    Returns
    -------
    String representing the latest folder (path)
    """
    contents = os.listdir(BLACK_LIST_PATH)

    def join_path(d):
        return os.path.join(BLACK_LIST_PATH, d)

    # Get only folders
    folders = [d for d in contents if os.path.isdir(join_path(d))]

    # Parse dates in folder
    dates = [dt.strptime(d, '%Y%m%d') for d in folders]

    # Get latest folder
    latest_date = max(dates)
    latest_folder = latest_date.strftime('%Y%m%d')

    if return_path:
        latest_folder = os.path.join(BLACK_LIST_PATH, latest_folder)

    return latest_folder

if __name__ == '__main__':
    # Read latest folder available
    folder = get_latest_folder(return_path=False)

    # Read all files in folder
    path = os.path.join(BLACK_LIST_PATH, folder)
    db = pd.DataFrame()

    files = os.listdir(path)
    files = [f for f in files if f.endswith('.csv')]

    for file in files:
        filepath = os.path.join(path, file)
        df = pd.read_csv(filepath, encoding='latin-1')

        # Transform columns to uppercase
        cols = [c.upper().strip() for c in df.columns]
        df.columns = cols
        df.rename(columns={
            'NOMBRE, DENOMINACIÓN O RAZÓN SOCIAL': 'RAZÓN SOCIAL'
        })

        print("Appending to database..")
        source = FILE_TRANSLATE[file]
        df['source'] = source
        db = pd.concat([db, df])

    output_path = os.path.join(PROCESSED_PATH, f'{folder}.csv')
    db.to_csv(output_path)
