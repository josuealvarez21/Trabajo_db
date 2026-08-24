# Importación de librerías requeridas
import pandas as pd  # Manipulación y análisis de datos mediante DataFrames
import glob          # Búsqueda de patrones de nombres de archivos
import os            # Manejo de rutas
import matplotlib.pyplot as plt

# Rutas base del proyecto
CARPETA_DATOS = "datos"
CARPETA_RESULTADOS = "resultados"

os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

# 1. Buscar datos y leer archivos específicos
df_medellin = pd.read_csv(os.path.join(CARPETA_DATOS, "sucursal_medellin.csv"))
print(df_medellin.head())

df_bogota = pd.read_excel(os.path.join(CARPETA_DATOS, "sucursal_bogota.xlsx"))
print(df_bogota.head())

# Obtiene la lista de archivos de sucursales (.csv) en la carpeta datos/
archivo_csv = glob.glob(os.path.join(CARPETA_DATOS, "sucursal_*.csv"))
print(f"Archivos encontrados: {archivo_csv}")

# Obtiene la lista de archivos de sucursales (.xlsx) en la carpeta datos/
archivo_excel = glob.glob(os.path.join(CARPETA_DATOS, "sucursal_*.xlsx"))
print(f"Archivos encontrados: {archivo_excel}")

# 2. Carga masiva de archivos y almacenamiento en una lista
lista_dataframes = []

for archivo in archivo_csv:
    df = pd.read_csv(archivo)
    lista_dataframes.append(df)
    print(f"Leído: {archivo} - {len(df)} filas")

for archivo in archivo_excel:
    df = pd.read_excel(archivo)
    lista_dataframes.append(df)
    print(f"Leído: {archivo} - {len(df)} filas")

# 3. Limpieza: uno de los 4 archivos tiene columnas con nombres distintos.
# Se detecta por la columna única 'Fecha_Venta' y se renombra todo su esquema.
for i, df in enumerate(lista_dataframes):
    if 'Fecha_Venta' in df.columns:
        lista_dataframes[i] = df.rename(columns={
            "Fecha_Venta": "fecha",
            "Cant": "cantidad",
            "Producto": "producto",
            "Valor_Unitario": "precio_unitario",
            "Vendedor": "vendedor",
            "Pago": "metodo_pago",
            "Categoria": "categoria"
        })

# 4. Consolidación de todos los DataFrames en uno solo
df_consolidado = pd.concat(lista_dataframes, ignore_index=True)

# 5. Exportar el consolidado limpio a resultados/
ruta_salida = os.path.join(CARPETA_RESULTADOS, "consolidado_limpio.xlsx")
df_consolidado.to_excel(ruta_salida, index=False)
print(f"Consolidado guardado en: {ruta_salida}")

# 6a. Ventas por categoría (gráfico de barras)
ventas_por_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()
ventas_por_categoria.plot(kind='bar', title='Ventas por Categoría')
plt.ticklabel_format(style='plain', axis='y')
plt.ylabel('Ventas totales ($)')
plt.xlabel('Categoría')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(CARPETA_RESULTADOS, "grafico_categoria.png"))
plt.show()

# 6b. Participación por vendedor (gráfico de torta)
ventas_por_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()
ventas_por_vendedor.plot(kind='pie', autopct='%1.1f%%', title='Participación de Ventas por Vendedor')
plt.ylabel('')
plt.tight_layout()
plt.savefig(os.path.join(CARPETA_RESULTADOS, "grafico_vendedor.png"))
plt.show()
