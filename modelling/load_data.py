# Esta es la primera versión del código, requiere optimización

import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from datetime import datetime

class AnalisisPlano:
    """Esta es una clase que procesa los planos de ventas para generar diferentes informes
    Arguments:
    relative path {string}-- enter relative path for read data
    origin {string}--enter region or dependence

    """
    def __init__(self, path, place):
        self.place = place
        self.path = path

    def basic_reports(self):
        """Devuelve archivo de excel con un conjunto de datos agrupado por transacción para análisis de tiempo de 
        registro y otras variables de interes

        Returns:
            file1: placesummary.xlsx
            file2: placedescribe.xlsx
        """
        data = _read_data(self.path) #Lee el archivo desde el origen de datos
        data = _transform_data(data) #hace transformaciones iniciales y crea columna de tiempos entre registros
        data = _new_data(data) #Se construye una nueva data que consolida por transacción el tiempo total de registro
        data.to_excel(f"Reports\\{self.place}summary.xlsx")
        data.describe().to_excel(f"Reports\\{self.place}describe.xlsx")
        # _visualization(data)
        return data

#Read data
def _read_data(path):
    with open(path, encoding='latin-1') as csvfile:
        datos = pd.DataFrame(csv.DictReader(csvfile, delimiter = ';'))
    return datos

#transform of data
def _transform_data(data):
    df = data.copy()
    df = df[df['TipoMvto'] == 'Venta']
    df = df[df['NombreProducto'] == 'Ing. parque']
    df = df[['FechaHora', 'IdTransaccion', 'Cantidad', 'TipoTarifa', 'Usuario']]
    df['TipoTarifa'] = df['TipoTarifa'].astype('string')
    df['Cantidad'] = df['Cantidad'].astype(int)
    df['FechaHora'] = pd.to_datetime(df['FechaHora'])
    df['timeDiff'] = df['FechaHora'].diff() #Columna que calcula los tiempos entre registros
    componentes = df['timeDiff'].dt.components #descompone el dato de la marca temporal
    df = pd.concat([df, componentes], axis= 1) # junto las componentes con el conjunto de datos
    return df

def _tipo_tarifa(df, tipo):
    tar = 0
    for i in df['TipoTarifa']:
        if i == str(tipo):
            tar = tar+1
        df[f'tarifa_{tipo}'] = tar
        df[f'tarifa_{tipo}'] = df[f'tarifa_{tipo}'].astype('string')
    return df

def _user_name(df):
    df['resp_registro'] = np.unique(df['Usuario'])[0]
    return df

def _new_data(data):
    df = data[['FechaHora', 'IdTransaccion', 'Cantidad', 'minutes', 'seconds', 'TipoTarifa', 'Usuario']]
    dict_ = []
    for i in np.unique(df['IdTransaccion']):
        _filtro = df[df['IdTransaccion'] == i]
        start_seconds = (_filtro['seconds'][:1]+ _filtro['minutes'][:1]*60)
        sum_seconds = (_filtro['seconds'].sum() + _filtro['minutes'].sum()*60)
        total_seconds = sum_seconds-start_seconds
        #En este diccionario guardaremos los registros de cada transacción
        dict_.append({'IdTransaccion':i, 'timeRegistration': total_seconds.values[0],'Cantidad':_filtro['Cantidad'].sum() ,\
                'tarifa_A':_tipo_tarifa(_filtro, 1)['tarifa_1'].values[0],'tarifa_B':_tipo_tarifa(_filtro, 2)['tarifa_2'].values[0],\
                'tarifa_C':_tipo_tarifa(_filtro, 3)['tarifa_3'].values[0], 'tarifa_D':_tipo_tarifa(_filtro, 4)['tarifa_4'].values[0], \
                'Responsable Registro':_user_name(_filtro)['resp_registro'].values[0]})

    df = pd.DataFrame(dict_)
    df = df.fillna(0)
    df['total_time_minutes'] = (df['timeRegistration'] // 60).astype(int).astype(str)+":"+(df['timeRegistration'] % 60).astype(int).astype(str)
    return df

    


