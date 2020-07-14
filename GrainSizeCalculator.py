import pandas as pd
import numpy as np
import os

# Calculadora de tamaño de sedimentos
# para no cohesivos, 


for filename in os.listdir(r'C:/Users/Sherwood/Desktop/procesamiento/files/'):

    excel = pd.read_excel(filename,sheet_name='ASCII Data',header=3)
    
    c_nc = 'c' # escribir 'c' para cohesivos o 'nc' para no cohesivos.
    
    if c_nc == 'c':
        a = 21
        b = 53
    else:
        a = 53
        b = 64
    
    df = excel.iloc[1:,a:b]

    df = df.T

    df.reset_index(inplace=True)

    df = df.rename(columns={"index": "Size"})

    excel = excel.iloc[1:,65]
    
    nombres = pd.DataFrame(excel)
    
    df = df.astype(float)
    
    
    result_array = np.array([])

    for column in df:
    
        df = df.sort_values('Size')
    
        # Creando una columna virtual de sumas acumuladas por cada muestra
        cumul = df[column].cumsum()
    
        # Aqui veo la fila donde la suma acumulada alcanza el % deseado
    
        suma_de_frecuencias = df[column].sum()
    
        # Obteniendo el índice donde el acumulado es el 10%, 50% o 90% del total
    
        D10 = sum(cumul < 0.1 * float(suma_de_frecuencias))
    
        D50 = sum(cumul < 0.5 * float(suma_de_frecuencias))
    
        D90 = sum(cumul < 0.9 * float(suma_de_frecuencias))
    
        # Y luego encuentro el "grain size" para esa muestra en la columna 'Size'
    
        D10 = df['Size'].iloc[D10]
    
        D50 = df['Size'].iloc[D50]
    
        D90 = df['Size'].iloc[D90]

        # Guardando los resultados en cada columna
    
        resultado = [D10, D50, D90]
    
        result_array = np.append(result_array, resultado)

        
    result_array = result_array.reshape(len(result_array)//3,3)
    
    dataset = pd.DataFrame(data = result_array, columns = ['D10', 'D50', 'D90'])

    dataset = dataset.append(dict(zip(dataset.columns, result_array)), ignore_index=True)

    dataset = dataset.iloc[1:(len(dataset)-1),0:]
    
    dataset['Nombre_de_Muestra'] = nombres
    
    dataset[['D10', 'D50', 'D90']] = dataset[['D10', 'D50', 'D90']].apply(pd.to_numeric)
    
    # [77] se puede cambiar el índice [-8:] por [-8:-2] si importa sólo el nombre de la muestra mas no su repetición.
    
    final_df = dataset.groupby(dataset['Nombre_de_Muestra'].str[-8:]).mean()
    
    final_df.to_excel(r'C:/Users/Sherwood/Desktop/procesamiento/results/Procesado_' + filename + '.xlsx', index = True, header = True)
    
    # Ver distribución acumulada por punto.
    # Manual de buenas prácticas para Python.
    # Revisar la carpeta de team campo, tener en cuenta que estará duplicado.
    # Cambiar de nombre, añadir LISST.
    # Homologar nombres 
    # Definir subcarpeta de procesamiento.