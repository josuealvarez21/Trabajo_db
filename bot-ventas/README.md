# Bot de Ventas 🤖📊

Bot de análisis de ventas desarrollado en Python que consolida automáticamente los datos de ventas de **4 sucursales** (Medellín, Bogotá, Cali y Barranquilla), limpia y unifica la información, genera reportes en Excel y gráficos estadísticos.

---

## 📁 Estructura del Proyecto

```
bot-ventas/
├── datos/
│   ├── sucursal_medellin.csv        # Datos CSV - Sucursal Medellín
│   ├── sucursal_bogota.xlsx         # Datos Excel - Sucursal Bogotá
│   ├── sucursal_cali.csv            # Datos CSV - Sucursal Cali
│   └── sucursal_barranquilla.xlsx   # Datos Excel - Sucursal Barranquilla
├── resultados/
│   ├── consolidado_limpio.xlsx      # Reporte final consolidado y limpio
│   ├── grafico_categoria.png        # Gráfico de barras: ventas por categoría
│   └── grafico_vendedor.png         # Gráfico de torta: participación por vendedor
├── main.py                          # Script principal del bot
└── README.md                        # Este archivo
```

---

## 📋 Descripción General

Este proyecto resuelve el problema típico de tener información de ventas **dispersa en múltiples archivos con formatos distintos** (CSV y Excel) e incluso con **nombres de columnas diferentes** entre archivos. El bot automatiza todo el flujo de trabajo:

1. **Descubrimiento de archivos**: Busca automáticamente todos los archivos `sucursal_*.csv` y `sucursal_*.xlsx` dentro de la carpeta `datos/`.
2. **Carga masiva**: Lee cada archivo con la función adecuada según su formato (`pd.read_csv` o `pd.read_excel`) y lo almacena como DataFrame en una lista.
3. **Limpieza y estandarización**: Detecta el archivo con columnas renombradas (uno de los 4 usa nombres distintos) y aplica un diccionario de renombrado para unificar todos los esquemas.
4. **Consolidación**: Une todos los DataFrames en uno solo con `pd.concat()`.
5. **Generación de reportes**: Exporta el consolidado limpio a `resultados/consolidado_limpio.xlsx`.
6. **Análisis visual**: Genera gráficos estadísticos y los guarda como imágenes PNG en `resultados/`.

---

## 🔧 Tecnologías Utilizadas

| Librería | Uso |
|----------|-----|
| **pandas** | Lectura, manipulación y consolidación de datos (DataFrames) |
| **matplotlib** | Generación de gráficos de barras y torta |
| **glob** | Búsqueda de archivos por patrón de nombre |
| **openpyxl** | Motor para leer/escribir archivos `.xlsx` |

### Requisitos

- Python 3.9 o superior
- pip actualizado

---

## ⚙️ Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/josuealvarez21/Trabajo_db.git
cd Trabajo_db/bot-ventas

# 2. Instalar las dependencias
pip install pandas matplotlib openpyxl
```

---

## ▶️ Uso

```bash
python main.py
```

Al ejecutar el script, la consola mostrará:

```
Archivos encontrados: ['datos/sucursal_medellin.csv', ...]
Leído: datos/sucursal_medellin.csv - N filas
Leído: datos/sucursal_cali.csv - N filas
...
```

Los resultados se generan automáticamente en la carpeta `resultados/`.

---

## 📊 Estructura de los Datos

Tras la limpieza, todas las tablas comparten el mismo esquema:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `fecha` | fecha | Fecha de la venta |
| `producto` | texto | Nombre del producto vendido |
| `cantidad` | numérico | Unidades vendidas |
| `precio_unitario` | numérico | Valor unitario del producto |
| `vendedor` | texto | Vendedor responsable |
| `metodo_pago` | texto | Medio de pago utilizado |
| `categoria` | texto | Categoría del producto |

> **Nota**: El archivo de Barranquilla originalmente usaba nombres distintos (`Fecha_Venta`, `Cant`, `Valor_Unitario`, `Pago`). El bot lo detecta mediante la columna única `Fecha_Venta` y renombra sus columnas con un diccionario antes de consolidar.

---

## 📈 Análisis Realizados

1. **Ventas por categoría** → Gráfico de barras (`grafico_categoria.png`)
2. **Participación por vendedor** → Gráfico de torta con porcentajes (`grafico_vendedor.png`)
3. **Producto más vendido** → Frecuencia de aparición usando `value_counts()` sobre la columna `producto`

### Funciones clave de pandas utilizadas

| Función | Propósito |
|---------|-----------|
| `pd.read_csv()` | Leer archivos CSV |
| `pd.read_excel()` | Leer archivos Excel |
| `df.rename(columns={...})` | Renombrar columnas con un diccionario |
| `pd.concat()` | Unir múltiples DataFrames en uno solo |
| `df.groupby()` + `.sum()` | Agrupar ventas por categoría/vendedor y sumarlas |
| `df['col'].value_counts()` | Contar frecuencia de valores únicos |
| `.idxmax()` | Obtener el valor con mayor frecuencia |
| `df.to_excel()` | Exportar resultados a Excel |

---

## 🖼️ Ejemplos de Resultados

- **Gráfico de barras**: Compara el total de ventas ($) entre categorías de productos.
- **Gráfico de torta**: Muestra qué porcentaje del total vendido aporta cada vendedor al equipo.

---

## 👨‍💻 Autor

- **Josué Álvarez** — [GitHub](https://github.com/josuealvarez21)

## 📄 Licencia

Proyecto educativo desarrollado para fines académicos.
