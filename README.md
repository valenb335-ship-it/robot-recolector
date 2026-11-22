 Robot recolector — TP de Promoción
 
Fundamentos Teóricos de la Informática — Facultad de Ingeniería, UNPSJB
 
**Integrantes:** Benitez Valentina, Guzman Katya, Villegas Catalina
 
**Instancia asignada:** Grupo 05 · Escalera
 
Reconocedor de programas para un robot recolector: un análisis léxico, un autómata de pila (AP) que verifica el protocolo de los viajes y un simulador del mundo que verifica los movimientos y la distribución final de las cajas.
 

 
## Requisitos
- **Python 3.10 o superior.** Para verificarlo: `python --version` (en Windows también puede ser `py --version`).

## Estructura del proyecto
 
```
robot-recolector/
├── README.md
├── instancias/
│   └── grupo5.json            ← grilla: robot, cajas, obstáculos y destinos
├── programa/
│   ├── solucion.txt           ← programa que resuelve la instancia
│   └── prueba/                ← programas de prueba (uno por archivo .txt)
├── src/
│   ├── main.py                ← programa principal
│   ├── validador.py           ← análisis léxico, ejecución por fases y exportación
│   ├── motor_AP.py            ← autómata de pila con pila explícita
│   ├── mundo.py               ← simulador de la grilla y verificación de la meta
│   └── errores.py             ← excepciones: léxico, AP y físico
├── registro_solucion.csv      ← registro por token de la solución (se genera)
└── registro_solucion.txt      ← resumen, métricas, grillas y registro (se genera)
```

## Cómo reproducir la ejecución
 
1. Descargar o clonar el repositorio:
```
git clone <url-del-repositorio>
cd robot-recolector
```
2. Ejecutar el programa principal desde la carpeta raíz del proyecto:
```
python src/main.py
```
### Qué hace la ejecución
 
En una sola corrida:
 
1. **Ejecuta la solución** (`programa/solucion.txt`) sobre la instancia `instancias/grupo5.json` y muestra el resultado, los movimientos con y sin carga, la altura máxima de pila y la grilla final.
2. **Genera los archivos de registro** en la carpeta raíz:
   - `registro_solucion.csv`: registro por token con las columnas `indice`, `orden`, `estado_ap`, `pila`, `posicion` y `carga`.
   - `registro_solucion.txt`: resultado, métricas, grillas inicial y final, y el mismo registro en formato de tabla.
3. **Ejecuta todas las pruebas** de la carpeta `programa/prueba/` y muestra el resultado de cada una.
4. **Ejecuta los casos de borde**: entrada vacía, token desconocido y salida de la grilla.
### Resultado esperado de la solución
 
```
Resultado: MISION RESUELTA
Movimientos sin carga: 28
Movimientos con carga: 14
Altura máxima de pila: 5
```
 
### Resultados esperados de las pruebas
 
| Prueba | Archivo / caso | Resultado esperado |
|---|---|---|
| 1 | `programa/solucion.txt` | MISION RESUELTA |
| 2 | `vuelta_incorrecta.txt` | RECHAZO DEL AP |
| 3 | `soltar_antes.txt` | RECHAZO DEL AP |
| 4 | `sin_finviaje.txt` | RECHAZO DEL AP |
| 5 | `agarrar_doble.txt` | RECHAZO DEL AP |
| 6 | `obstaculo.txt` | ERROR FISICO |
| 7 | `agarrar_vacia.txt` | ERROR FISICO |
| 8 | `meta_no_alcanzada.txt` | OBJETIVO NO ALCANZADO |
| Borde | entrada vacía | RECHAZO DEL AP |
| Borde | token desconocido | ERROR LEXICO |
| Borde | salida de la grilla | ERROR FISICO |
 
## Cambiar las entradas
 
Las entradas se cambian sin modificar el reconocedor ni el simulador:
 
- **Otro programa:** reemplazar el contenido de `programa/solucion.txt`, o agregar un archivo `.txt` en `programa/prueba/` (se ejecuta automáticamente junto con las demás pruebas). Las órdenes se separan con espacios o saltos de línea. Palabras válidas: `arriba`, `abajo`, `izquierda`, `derecha`, `agarrar`, `soltar`, `viaje`, `finviaje`.
- **Otra grilla:** editar `instancias/grupo5.json`, respetando el formato. Las coordenadas son `[fila, columna]`, empezando en 1; la fila 1 está arriba y la columna 1 a la izquierda.
```json
{
  "filas": 6,
  "columnas": 6,
  "robot": [6, 1],
  "robot_final": [6, 1],
  "cajas": [[1, 1], [1, 5], [2, 3], [3, 6]],
  "obstaculos": [[2, 2], [2, 4], [3, 4], [5, 3]],
  "destinos": [[3, 2], [4, 3], [5, 4], [6, 5]]
}
```
 
## Resultados posibles
 
Cada programa se procesa en fases y se detiene en la primera que falla:
 
1. **ERROR LEXICO:** hay una palabra que no es reservada. Se informa el índice del token, la línea y la posición de la palabra en la línea.
2. **RECHAZO DEL AP:** el programa no respeta el protocolo de los viajes. Se informa el token, el estado y la pila.
3. **ERROR FISICO:** una orden no se puede ejecutar en la grilla (obstáculo, salida de la grilla, agarrar sin caja, etc.).
4. **OBJETIVO NO ALCANZADO:** el programa se ejecuta completo pero no deja todo en su lugar.
5. **MISION RESUELTA:** las cajas están en los destinos, el robot en su posición final y la pinza vacía.
Primero se valida toda la sintaxis (análisis léxico y AP) y solo si el AP acepta se ejecuta el programa en el mundo. Por eso el registro por token se genera únicamente para las entradas aceptadas por el AP.