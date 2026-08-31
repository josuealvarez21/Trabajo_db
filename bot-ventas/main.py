# ============================================
# AUTOMATIZACION - Bot de Ventas
# Vigila la carpeta de datos y procesa automaticamente
# los archivos nuevos: consolida, limpia, genera graficos y registro.
# ============================================
import time
import os
import pandas as pd
import glob
import matplotlib.pyplot as plt

CARPETA_DATOS = "datos"
CARPETA_RESULTADOS = "resultados"

os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

archivos_vistos = set(os.listdir(CARPETA_DATOS))


def procesar_todo(archivo_nuevo):
    """
    Lee todos los archivos de sucursales, consolida, limpia,
    genera graficos y guarda un registro (log) del proceso.
    """
    archivos_csv = glob.glob(os.path.join(CARPETA_DATOS, "sucursal_*.csv"))
    archivos_xlsx = glob.glob(os.path.join(CARPETA_DATOS, "sucursal_*.xlsx"))
    lista_informes = []

    for archivo in archivos_csv:
        try:
            lista_informes.append(pd.read_csv(archivo))
        except Exception as e:
            print(f"Error leyendo {archivo}: {e}")

    for archivo in archivos_xlsx:
        try:
            lista_informes.append(pd.read_excel(archivo, engine='openpyxl'))
        except Exception as e:
            print(f"Error leyendo {archivo}: {e}")

    if not lista_informes:
        print("No se encontraron archivos para procesar.")
        return

    for i, df in enumerate(lista_informes):
        if 'Fecha_Venta' in df.columns:
            lista_informes[i] = df.rename(columns={
                "Fecha_Venta": "fecha",
                "Cant": "cantidad",
                "Producto": "producto",
                "Valor_Unitario": "precio_unitario",
                "Vendedor": "vendedor",
                "Pago": "metodo_pago",
                "Categoria": "categoria"
            })

    df_consolidado = pd.concat(lista_informes, ignore_index=True)
    df_consolidado = df_consolidado.drop_duplicates()

    ruta_excel = os.path.join(CARPETA_RESULTADOS, "consolidado_limpio.xlsx")
    df_consolidado.to_excel(ruta_excel, index=False)

    ventas_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()
    ventas_categoria.plot(kind='bar', title='Ventas por Categoria')
    plt.ticklabel_format(style='plain', axis='y')
    plt.ylabel('Ventas totales (COP)')
    plt.xlabel('Categoria')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_RESULTADOS, "grafico_categoria.png"))
    plt.close()

    ventas_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()
    ventas_vendedor.plot(kind='pie', autopct='%1.1f%%', title='Participacion por Vendedor')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_RESULTADOS, "grafico_vendedor.png"))
    plt.close()

    frecuencia = df_consolidado['producto'].value_counts()
    producto_top = frecuencia.idxmax()
    total_ventas = df_consolidado['precio_unitario'].sum()

    with open(os.path.join(CARPETA_RESULTADOS, "log_automatizacion.txt"), "a", encoding="utf-8") as f:
        f.write(f"Proceso ejecutado: {pd.Timestamp.now()}\n")
        f.write(f"Archivo detectado: {archivo_nuevo}\n")
        f.write(f"Total de registros procesados: {len(df_consolidado)}\n")
        f.write(f"Ventas totales: ${total_ventas:,.0f}\n")
        f.write(f"Producto mas vendido: {producto_top}\n")
        f.write("---\n")

    print(f"  Registros consolidados: {len(df_consolidado)}")
    print(f"  Ventas totales: ${total_ventas:,.0f}")
    print(f"  Producto mas frecuente: {producto_top}")
    print("  Archivos actualizados en resultados/")


print("=" * 50)
print("  BOT DE VENTAS - MODO AUTOMATIZADO")
print("=" * 50)
print(f"Monitoreando carpeta '{CARPETA_DATOS}/'... (Ctrl+C para detener)")
print()

try:
    while True:
        archivos_actuales = set(os.listdir(CARPETA_DATOS))
        archivos_nuevos = archivos_actuales - archivos_vistos

        if archivos_nuevos:
            for archivo in archivos_nuevos:
                print(f"[+] Nuevo archivo detectado: {archivo}")
                procesar_todo(archivo)
                print()
            archivos_vistos = archivos_actuales

        time.sleep(5)
except KeyboardInterrupt:
    print("\nMonitoreo detenido por el usuario.")
