# Importación de librerías requeridas
import pandas as pd  # Manipulación y análisis de datos mediante DataFrames
import glob       # Búsqueda de patrones de nombres de archivos en el sistema
import matplotlib.pyplot as plt
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


# Obtiene la lista de los archivos de sucursales (.csv) en la carpeta actual
archivo_csv = glob.glob("sucursal_*.csv")
print(f"Archivos encontrados: {archivo_csv}")

# Obtiene la lista de los archivos de sucursales (.xlsx) en la carpeta actual
archivo_excel = glob.glob("sucursal_*.xlsx")
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

# 6a. EJEMPLO RESUELTO: ventas por categoría (gráfico de barras)
ventas_por_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()  # Agrupa y suma por categoría
ventas_por_categoria.plot(kind='bar', title='Ventas por Categoria')  # Crea el gráfico de barras
plt.ticklabel_format(style='plain', axis='y')  # Evita notación científica (1e6)
plt.ylabel('Ventas totales ($)')
plt.xlabel('Categoría')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("grafico_ventas_categoria.png")
plt.show()

# 6b. EJEMPLO RESUELTO: participación por vendedor (gráfico de torta)
ventas_por_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()  # Agrupa y suma por vendedor
ventas_por_vendedor.plot(kind='pie', autopct='%1.1f%%', title='Participacion de Ventas por Vendedor')  # Grafico de torta con porcentajes
plt.ylabel('')  # No aplica en gráficos de torta
plt.tight_layout()
plt.savefig("grafico_ventas_vendedor.png")
plt.show()

# 6c. AHORA USTEDES: ¿cuál es el producto que aparece más veces 
# en las ventas? Investiguen la función value_counts() y 
# apliquenla a la columna 'producto'
frecuencia_productos = df_consolidado['producto'].value_counts()
print("Frecuencia de productos vendidos:")
print(frecuencia_productos)
print(f"El producto que mas aparece es: {frecuencia_productos.idxmax()}")


#rta// el producto que mas aparece es electronica 

"""La función value_counts() (utilizada principalmente en la librería pandas 
de Python) sirve para contar cuántas 
veces aparece cada valor único dentro de una columna o serie de datos."""


