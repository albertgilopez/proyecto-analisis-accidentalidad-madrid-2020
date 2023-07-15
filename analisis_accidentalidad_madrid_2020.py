
# PROYECTO: Análisis Accidentalidad Madrid 2020
# AUTOR: Albert Gil López
# LINKEDIN: https://www.linkedin.com/in/albertgilopez/

""" DESCRIPCIÓN: Este proyecto se centra en el análisis de los accidentes de tráfico que ocurrieron en Madrid durante el año 2020. 
El conjunto de datos inicial contiene información detallada sobre cada accidente, incluyendo la fecha y hora, la ubicación, el tipo de accidente, las condiciones meteorológicas, el tipo de vehículo y de persona involucrada, la edad y el sexo de las personas involucradas, y la gravedad de las lesiones.

El primer paso del proyecto consiste en una serie de operaciones de limpieza de datos. 
Esto incluye la eliminación de registros duplicados, la gestión de valores nulos, y la corrección de los tipos de datos. 
También se realizan algunas transformaciones en los datos, como la creación de una nueva columna para el mes del accidente.

Una vez que los datos están limpios y en el formato correcto, se realizan una serie de visualizaciones para explorar los datos y extraer insights. 
Esto incluye un gráfico de barras del número de accidentes por distrito, un gráfico de líneas del número de accidentes a lo largo del tiempo, un gráfico de pastel de la proporción de tipos de accidentes, y un gráfico de caja de la distribución de la lesividad en diferentes categorías de accidentes.

Los gráficos proporcionan una visión clara y comprensible de los datos, permitiendo identificar patrones y tendencias, y ofreciendo insights valiosos sobre la accidentalidad en Madrid durante el año 2020."""

import pandas as pd
import numpy as np
import os 

# Documentación de Pandas https://pandas.pydata.org/pandas-docs/stable/reference/index.html

pd.options.display.min_rows = 6 # por defecto nos muestra 6 registros

# Este análisis consisten en analizar la calidad de datos de un dataset que contiene los accidentes de tráfico en Madrid durante 2020.
# Está en Excel, se llama 2020_Accidentalidad.xlsx.

directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_excel = os.path.join(directorio_actual, "2020_Accidentalidad.xlsx")

# Importa el archivo en el objeto df y visualizalo por pantalla.

df = pd.read_excel(ruta_excel, sheet_name = "2020_Accidentalidad", index_col = "Nº  EXPEDIENTE",
                              parse_dates = ["FECHA"]) # solo podemos importar por hojas (le indicamos el número de hoja o el nombre)
print(df.head(2))
df.info()

# Algunas conclusiones sobre la importación:

# - El índice debería ser el número de expediente
# - Nos importaba casi todas las variables como objeto
# - Los nombres de variables tenían acentos símbolos y espacios
# - Las 2 últimas variables no contienen información
# - Había registros duplicados
# - Teníamos muchos nulos

# Vamos a ir paso a paso. Comenzamos por corregir los nombres.
# Le pasamos una lista los mismos nombres pero quitando acentos y símbolos, y todo en minúscula

cabecera = ['expediente','fecha','hora','calle','numero','distrito','tipo_accidente','tiempo','vehiculo','persona','edad','sexo','lesividad','unamed_1','unamed_2']

df = pd.read_excel(ruta_excel,
                        sheet_name = "2020_Accidentalidad",
                        index_col = "expediente",
                        header = 0,
                        names = cabecera,
                        parse_dates = ["fecha"]) # solo podemos importar por hojas (le indicamos el número de hoja o el nombre)

# na_values = ["-","DESCONOCIDA"],

# O podemos utilizar:
# from janitor import clean_names
# print(clean_names(df))

df = df.drop("unamed_1", axis = 1)
df = df.drop("unamed_2", axis = 1)

# Eliminamos los registros duplicados

df.drop_duplicates(inplace = True)

# Corrigimos los tipos de variables

tipos = {'distrito':'category',
         'tipo_accidente':'category',
         'tiempo':'category',
         'vehiculo':'category',
         'persona':'category',
         'edad':'category',
         'sexo':'category'}

df = df.astype(tipos)

# Otra solución: df.loc[;,"distrito":"sexo"] = df.loc[;,"distrito":"sexo"].astype("category")

# Ahora vamos a gestionar los nulos.

# Analizando la naturaleza y el conteo de cada variable podríamos llegar las siguientes conclusiones:

# - En numero y distrito son solo 2 nulos: eliminar nulos
# - tipo_persona, tipo_accidente y tipo_vehiculo tienen pocos nulos y podemos imputarlos por la moda
# - En el sexo y estado_metereológico vamos a crear una categoría "Desconocido"
# - En lesividad, a diferencia de las anteriores podría ser que no hubo lesión en ese accidente, así que sustituiremos por cero
# - Acuérdate de ir guardando en df en cada paso.

# Eliminar nulos en 'numero' y 'distrito'
df = df.dropna(subset=['numero', 'distrito'])

# Imputar nulos en 'tipo_persona', 'tipo_accidente' y 'tipo_vehiculo' con la moda
for column in ['persona', 'tipo_accidente', 'vehiculo']:
    df[column].fillna(df[column].mode()[0], inplace=True)

# Crear una categoría "Desconocido" para nulos en 'sexo' y 'estado_metereológico'

df["sexo"] = df.sexo.cat.add_categories('Desconocido')
df["tiempo"] = df.tiempo.cat.add_categories('Desconocido')

for column in ['sexo', 'tiempo']:
    df[column].fillna('Desconocido', inplace=True)

# Sustituir nulos en 'lesividad' con cero
df['lesividad'].fillna(0, inplace=True)

# Sacamos el conteo de nulos para comprobar que todo es correcto:

print(df.value_counts(dropna=False)) # conteo de Status incluyendo nulos

# Hacemos un análisis de nulos a ver cuantos tenemos por variable.

print(df.isna().sum().sort_values(ascending = False))

# GRÁFICOS

import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('fivethirtyeight')

# Gráfico de barras del número de accidentes por distrito:
# Este gráfico muestra el número total de accidentes que ocurrieron en cada distrito de Madrid en 2020. 
# Los distritos se muestran en el eje y, y el número de accidentes en el eje x.

plt.figure(figsize=(15,10))
distrito_counts = df['distrito'].value_counts()
bar_plot = sns.barplot(y=distrito_counts.index, x=distrito_counts.values, palette="viridis")
plt.title('Número de accidentes por distrito', fontsize=20)
plt.xlabel('Número de accidentes', fontsize=16)
plt.ylabel('Distrito', fontsize=16)
plt.xticks(fontsize=12)

# Rotar las etiquetas del eje y
bar_plot.set_yticklabels(bar_plot.get_yticklabels(), rotation=45)

plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

# Gráfico de líneas del número de accidentes a lo largo del tiempo:

# Este gráfico muestra cómo cambió el número total de accidentes en Madrid a lo largo de los meses de 2020. 
# Los meses se muestran en el eje x, y el número de accidentes en el eje y.

# Crear una lista con los nombres de los meses
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

df['mes'] = df['fecha'].dt.month # crea una nueva columna con el mes del accidente
accidentes_por_mes = df.groupby('mes').size()

plt.figure(figsize=(15,10))
sns.lineplot(x=accidentes_por_mes.index, y=accidentes_por_mes.values, linewidth=2.5)

# Reemplazar los números de los meses por los nombres de los meses y rotar las etiquetas 45 grados
plt.xticks(ticks=np.arange(1, 13), labels=meses, fontsize=12, rotation=45)

plt.title('Número de accidentes a lo largo del tiempo', fontsize=20)
plt.xlabel('Mes', fontsize=16)
plt.ylabel('Número de accidentes', fontsize=16)
plt.yticks(fontsize=12)
plt.show()

# Gráfico de pastel de la proporción de tipos de accidentes:
# Este gráfico muestra la proporción de cada tipo de accidente en el total de accidentes ocurridos en Madrid en 2020.

tipo_accidente_counts = df['tipo_accidente'].value_counts()

plt.figure(figsize=(15,15)) 
wedges, texts, autotexts = plt.pie(tipo_accidente_counts, autopct='%1.1f%%', textprops={'fontsize': 14}, pctdistance=0.85)

# Dibujar un círculo blanco en el centro
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Igualar aspecto para que sea un círculo
plt.axis('equal')  

plt.title('Proporción de tipos de accidentes', fontsize=20)

# Añadir leyenda en lugar de etiquetas en el gráfico
plt.legend(wedges, tipo_accidente_counts.index,
          title="Tipos de accidentes",
          loc="upper left",
          bbox_to_anchor=(0, 1))

plt.show()

# Gráfico de caja de la distribución de la lesividad en diferentes categorías de accidentes:
# Este gráfico muestra la distribución de la gravedad de las lesiones (lesividad) para cada tipo de accidente ocurrido en Madrid en 2020. 
# Los tipos de accidentes se muestran en el eje y, y la lesividad en el eje x.

plt.figure(figsize=(15,10))
box_plot = sns.boxplot(y='tipo_accidente', x='lesividad', data=df, palette="viridis")
plt.xlim(0, 15)
plt.title('Distribución de la lesividad en diferentes categorías de accidentes', fontsize=20)
plt.xlabel('Lesividad', fontsize=16)
plt.ylabel('Tipo de Accidente', fontsize=16)
plt.xticks(fontsize=12)

# Rotar las etiquetas del eje y
box_plot.set_yticklabels(box_plot.get_yticklabels(), rotation=45)

plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()
