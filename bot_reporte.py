# Importación de librerías requeridas
import pandas as pd  # Manipulación y análisis de datos mediante DataFrames
import glob       # Búsqueda de patrones de nombres de archivos en el sistema

# 1. Buscar datos y leer archivos específicos
# Carga de datos desde un archivo con formato CSV (Sucursal Medellín)
df_medellin = pd.read_csv("sucursal_medellin.csv")
# print(df_medellin)

# Carga de datos desde un archivo con formato Excel (Sucursal Bogotá)
df_bogota = pd.read_excel("sucursal_bogota.xlsx")
# print(df_bogota)

# Comprobación de nombres de columnas (Nota: 'colomns' tiene un error de sintaxis, lo correcto es '.columns')
# print(df_medellin.colomns)
# print(df_bogota.colomns)


# Obtiene la lista de todos los archivos con extensión .csv en la carpeta actual
archivo_csv = glob.glob("*.csv")
print(f"Archivos encontrados: {archivo_csv}")

# Obtiene la lista de todos los archivos con extensión .xlsx en la carpeta actual
archivo_excel = glob.glob("*.xlsx")
print(f"Archivos encontrados: {archivo_excel}")


# 2. Carga masiva de archivos y almacenamiento en una lista

# Lista vacía que contendrá todos los DataFrames individuales cargados
lista_dataframes = []

# Recorre cada archivo CSV encontrado, lo lee y lo agrega a la lista
for archivo in archivo_csv:
    df = pd.read_csv(archivo)
    lista_dataframes.append(df)
    print(f"Leido: {archivo} - {len(df)} filas")

# Recorre cada archivo Excel encontrado, lo lee y lo agrega a la lista
for archivo in archivo_excel:
    df = pd.read_excel(archivo)
    lista_dataframes.append(df)
    print(f"Leido: {archivo} - {len(df)} filas")


df_consolidado = pd.concat(lista_dataframes, ignore_index=True)  # Combina todos los DataFrames en uno solo
df_consolidado.to_excel("reporte_desordenado.xlsx", index=False)  # Guarda el DataFrame consolidado en un archivo Excel

# Reto: uno de los 4 archivos tiene columnas con nombres distintos 
# a los demás. Deben:
# 1. Identificar cual archivo es (revisen las columnas de cada uno)
# 2. Identificar cual columna unica sirve para reconocerlo
# 3. Crear el diccionario de renombrado completo

for i, df in enumerate(lista_dataframes):
    if 'Fecha_Venta' in df.columns:
        lista_dataframes[i] = df.rename(columns={
            "Fecha_Venta":"fecha",
            "Cant" : "cantidad",
            "Producto" : "producto",
            "Valor_Unitario" : "precio_unitario",
            "Vendedor": "vendedor",
            "Pago": "metodo_pago",
            "Categoria":"categoria"        
            # completen aqui su propio diccionario,

            # basandose en como se llaman las columnas 
            # en los otros 3 archivos que si coinciden
        })
print(lista_dataframes[i])



df_consolidado = pd.concat(lista_dataframes, ignore_index=True)  # Combina todos los DataFrames en uno solo
df_consolidado.to_excel("reporte_semi_ordenado.xlsx", index=False)

