# Bot de Ventas

Bot de analisis de ventas desarrollado en Python con **sistema de automatizacion** que vigila la carpeta de datos y procesa automaticamente los reportes nuevos que van llegando.

---

## Estructura del Proyecto

```
bot-ventas/
├── datos/                          # Carpeta vigilada (aqui se colocan los reportes)
│   ├── sucursal_medellin.csv       # Datos CSV - Sucursal Medellin
│   ├── sucursal_bogota.xlsx        # Datos Excel - Sucursal Bogota
│   ├── sucursal_cali.csv           # Datos CSV - Sucursal Cali
│   └── sucursal_barranquilla.xlsx  # Datos Excel - Sucursal Barranquilla
├── resultados/                     # Salidas generadas
│   ├── consolidado_limpio.xlsx     # Reporte final consolidado y limpio
│   ├── grafico_categoria.png       # Grafico de barras: ventas por categoria
│   ├── grafico_vendedor.png        # Grafico de torta: participacion por vendedor
│   └── log_automatizacion.txt      # Registro de cada proceso automatizado
├── prueba/                         # Archivos de prueba para la demo
│   ├── sucursal_medellin_reporte2.csv
│   └── sucursal_cali_reporte2.csv
├── main.py                         # Script principal (vigilancia + proceso)
├── requirements.txt                # Dependencias del proyecto
└── README.md                       # Este archivo
```

---

## Descripcion General

El proyecto resuelve el problema de tener la informacion de ventas **dispersa en multiples archivos con formatos distintos** (CSV y Excel) e incluso con **nombres de columnas diferentes** entre archivos. El bot automatiza todo el flujo de trabajo y, con el nuevo sistema de automatizacion, ya no es necesario ejecutar nada manualmente: basta con dejar caer un reporte nuevo en la carpeta `datos/` y el bot hace el resto.

---

## Como Funciona la Automatizacion

Este sistema convierte al bot en un **vigilante automatico**. No necesitas correr el proceso cada vez que llega un reporte: el bot se queda "mirando" la carpeta y reacciona solo.

### 1. La vigilancia (deteccion de archivos)

Cuando el script arranca toma una **fotografia inicial** de los archivos que ya existen en `datos/` y los guarda en un conjunto (set) llamado `archivos_vistos`:

```python
archivos_vistos = set(os.listdir("datos/"))
```

Despues entra en un **bucle infinito** que, cada **5 segundos**, vuelve a listar la carpeta y compara el resultado con lo que ya habia visto:

```python
while True:
    archivos_actuales = set(os.listdir("datos/"))
    archivos_nuevos = archivos_actuales - archivos_vistos  # diferencia de conjuntos
    if archivos_nuevos:
        ...  # hay reportes nuevos, procesar
    time.sleep(5)
```

- Se usa la **diferencia de conjuntos** (`-`): todo lo que este en `archivos_actuales` pero no en `archivos_vistos` es un **archivo nuevo**.
- Si la diferencia no esta vacia, significa que **llego un reporte**.
- El `time.sleep(5)` hace que el bot "descanse" 5 segundos entre revisiones, sin saturar la maquina.

### 2. Que pasa cuando encuentra un archivo nuevo

Al detectar un reporte, el bot llama a la funcion `procesar_todo(archivo_nuevo)`, que ejecuta el proceso completo:

1. **Relee todos** los reportes CSV y Excel de la carpeta `datos/`.
2. **Unifica los esquemas**: si aparece el archivo de Bogota (que usa nombres distintos como `Fecha_Venta`), lo renombra con un diccionario para que todas las tablas tengan las mismas columnas.
3. **Consolida** todo en un unico DataFrame y **elimina duplicados** con `drop_duplicates()`.
4. **Actualiza el Excel** `resultados/consolidado_limpio.xlsx` con todos los datos.
5. **Genera los graficos** de ventas por categoria (barras) y participacion por vendedor (torta).
6. **Escribe en el log** `resultados/log_automatizacion.txt` un registro con la fecha, el archivo detectado y el total de registros.

### 3. El registro (log)

Cada vez que detecta y procesa un archivo, deja una **huella** en `resultados/log_automatizacion.txt`:

```
Proceso ejecutado: 2026-08-31 14:30:15
Archivo detectado: sucursal_medellin_reporte2.csv
Total de registros procesados: 86
---
```

Asi queda evidencia de **cada automatizacion** que se ejecuto.

### Modelo mental

```
[Reporte llega a datos/]
        │
        ▼
[Loop revisa cada 5s -> detecta archivo nuevo]
        │
        ▼
[procesar_todo() lee + consolida + limpia]
        │
        ├──> actualiza consolidado_limpio.xlsx
        ├──> actualiza grafico_categoria.png / grafico_vendedor.png
        └──> escribe en log_automatizacion.txt
```

---

## Uso (Automatizacion)

```bash
pip install -r requirements.txt
python main.py
```

Al ejecutar el script, la consola muestra que el bot **queda vigilando** la carpeta de datos:

```
==================================================
  BOT DE VENTAS - MODO AUTOMATIZADO
==================================================
Monitoreando carpeta 'datos/'... (Ctrl+C para detener)
```

Cuando se **agrega un archivo nuevo** a `datos/`, el bot lo detecta y lo procesa:

```
[+] Nuevo archivo detectado: sucursal_medellin_reporte2.csv
  Registros consolidados: 86
  Ventas totales: $7,XXX,XXX
  Producto mas frecuente: Jean clasico
  Archivos actualizados en resultados/
```

El bot **no se detiene**: continua vigilando por si llegan mas reportes. Para detenerlo usa `Ctrl+C`.

---

## Prueba Manual (demo)

Para probar la automatizacion:

1. Abre una terminal y ejecuta `python main.py`.
2. Abre otra ventana con la carpeta `prueba/` del proyecto.
3. **Arrastra** `sucursal_medellin_reporte2.csv` dentro de `datos/`.
4. Observa la consola: aparecera el mensaje `[+] Nuevo archivo detectado: ...` y el proceso se ejecutara solo.
5. Haz lo mismo con `sucursal_cali_reporte2.csv`.
6. Verifica que `resultados/log_automatizacion.txt` registro ambos procesos, y que el consolidado y los graficos se actualizaron.

---

## Tecnologias Utilizadas

| Libreria | Uso |
|----------|-----|
| **pandas** | Lectura, manipulacion y consolidacion de datos (DataFrames) |
| **matplotlib** | Generacion de graficos de barras y torta |
| **glob** | Busqueda de archivos por patron de nombre |
| **openpyxl** | Motor para leer/escribir archivos `.xlsx` |

### Requisitos

- Python 3.9 o superior
- pip actualizado

---

## Instalacion

```bash
git clone https://github.com/josuealvarez21/Trabajo_db.git
cd Trabajo_db/bot-ventas
pip install -r requirements.txt
```

---

## Estructura de los Datos

Tras la limpieza, todas las tablas comparten el mismo esquema:

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| `fecha` | fecha | Fecha de la venta |
| `producto` | texto | Nombre del producto vendido |
| `cantidad` | numerico | Unidades vendidas |
| `precio_unitario` | numerico | Valor unitario del producto |
| `vendedor` | texto | Vendedor responsable |
| `metodo_pago` | texto | Medio de pago utilizado |
| `categoria` | texto | Categoria del producto |

> **Nota**: El archivo de **Bogota** originalmente usaba nombres distintos (`Fecha_Venta`, `Producto`, `Categoria`, `Cant`, `Valor_Unitario`, `Vendedor`, `Pago`). El bot lo detecta mediante la columna unica `Fecha_Venta` y renombra sus columnas con un diccionario antes de consolidar.

---

## Analisis Realizados

1. **Ventas por categoria** -> Grafico de barras (`grafico_categoria.png`)
2. **Participacion por vendedor** -> Grafico de torta con porcentajes (`grafico_vendedor.png`)
3. **Producto mas vendido** -> Frecuencia de aparicion usando `value_counts()` sobre la columna `producto`

### Funciones clave de pandas utilizadas

| Funcion | Proposito |
|---------|-----------|
| `pd.read_csv()` | Leer archivos CSV |
| `pd.read_excel()` | Leer archivos Excel |
| `df.rename(columns={...})` | Renombrar columnas con un diccionario |
| `pd.concat()` | Unir multiples DataFrames en uno solo |
| `df.drop_duplicates()` | Eliminar registros duplicados |
| `df.groupby()` + `.sum()` | Agrupar ventas por categoria/vendedor y sumarlas |
| `df['col'].value_counts()` | Contar frecuencia de valores unicos |
| `.idxmax()` | Obtener el valor con mayor frecuencia |
| `df.to_excel()` | Exportar resultados a Excel |

---

## Ejemplos de Resultados

- **Grafico de barras**: compara el total de ventas ($) entre categorias de productos.
- **Grafico de torta**: muestra que porcentaje del total vendido aporta cada vendedor.

### Ventas por categoria

![Ventas por Categoria](resultados/grafico_categoria.png)

### Participacion de ventas por vendedor

![Participacion por Vendedor](resultados/grafico_vendedor.png)

---

## Resultados Obtenidos (datos iniciales)

Al procesar los datos de las 4 sucursales se obtienen:

| Metrica | Valor |
|---------|-------|
| Registros consolidados | **66 ventas** (Medellin 18 · Cali 17 · Barranquilla 16 · Bogota 15) |
| Ventas totales | **$6,037,900** |
| Unidades vendidas | 294 |
| Productos unicos | 10 |

### Ventas por categoria

| Categoria | Ventas ($) | Participacion |
|-----------|-----------:|--------------:|
| Electronica | $3,412,700 | 56.5% |
| Ropa | $2,625,200 | 43.5% |

### Participacion por vendedor

| Vendedor | Ventas ($) | Participacion |
|----------|-----------:|--------------:|
| Camila Ruiz | $1,935,800 | 33.1% |
| Andres Gomez | $1,361,700 | 23.3% |
| Sofia Mena | $1,322,300 | 22.6% |
| Felipe Torres | $651,200 | 11.1% |
| Laura Diaz | $580,200 | 9.9% |

### Producto mas vendido

El producto que **mas aparece** en las ventas es el **Jean clasico**, con **11 apariciones**:

| # | Producto | Apariciones |
|---|----------|------------:|
| 1 | Jean clasico | 11 |
| 2 | Cargador USB-C | 10 |
| 3 | Camiseta basica | 9 |
| 4 | Medias deportivas | 7 |
| 5 | Audifonos Bluetooth | 6 |

> **Hallazgo clave**: aunque Electronica es la categoria que mas dinero genera ($3.4M, 56.5%), el producto mas frecuente pertenece a Ropa (Jean clasico), lo que sugiere que las prendas se venden en mayor volumen pero con precios unitarios mas bajos.

---

## Autor

- **Josue Alvarez** - [GitHub](https://github.com/josuealvarez21)

## Licencia

Proyecto educativo desarrollado para fines academicos.
