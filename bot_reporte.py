import pandas as pd 
import glob
#1. BUscar datos y leer archivos
df_medellin = pd.read_csv("sucursal_medellin.csv")
#print(df_medellin)
df_bogota = pd.read_excel("sucursal_bogota.xlsx")
#print(df_bogota)
#print(df_medellin.colomns)
#print(df_bogota.colomns)


archivo_csv = glob.glob("*.csv")
print(f"Archivos encontrados: {archivo_csv}")

archivo_excel = glob.glob("*.xlsx")
print(f"Archivos encontrados: {archivo_excel}")



#2.Guardar en una lista

lista_dataframes = []

for archivo in archivo_csv:
    df = pd.read_csv(archivo)
    lista_dataframes.append(df)
    print(f"Leido: {archivo} - {len(df)} filas")

for archivo in archivo_excel:
    df = pd.read_excel(archivo)
    lista_dataframes.append(df)
    print(f"Leido: {archivo} - {len(df)} filas")  