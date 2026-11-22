import csv
from errores import ErrorLexico, RechazoAP, ErrorFisico
from motor_AP import AutomataPila, LAMBDA
from mundo import Mundo

PALABRAS_RESERVADAS = {"viaje", "finviaje", "arriba", "abajo", "izquierda", "derecha", "agarrar", "soltar"}

def tokenizar_y_validar(texto):
    """verifica que cada palabra pertenezca a PALABRAS_RESERVADAS, si no pertenece, lanza ErrorLexico y devuelve su ubicacion"""
    tokens = []
    indice = 1
    for num_linea, linea in enumerate(texto.splitlines(), start=1):
        for num_palabra, palabra in enumerate(linea.split(), start=1):
            if palabra not in PALABRAS_RESERVADAS:
                raise ErrorLexico(indice, palabra,num_linea, num_palabra)
            tokens.append(palabra)
            indice += 1
    return tokens

def ejecutar_programa(texto_programa, instancia_json):
    """Devuelve lo solicitado por el enunciado"""

    mundo = Mundo(instancia_json)
    grilla_inicial = mundo.grilla_texto()
    ap = AutomataPila()

    #validacion

    try:
        tokens = tokenizar_y_validar(texto_programa)
    except ErrorLexico as e:
        return {
            "resultado": "ERROR LEXICO",
            "mensaje": str(e),
            "registro": [],
            "metricas": None

        }

    #validacion d sintaxis con AP

    try: 
        traza_ap = ap.procesar(tokens)
    except RechazoAP as e:
        return {
            "resultado": "RECHAZO DEL AP",
            "mensaje": str(e),
            "registro": [],
            "metricas": None
        }

    # simulacion del mundo y registro por token

    registro_completo = []
    try:
        for paso_ap in traza_ap:
            idx = paso_ap["indice"]
            token = paso_ap["token"]

            #transicion lambda final hacia q5
            if token != LAMBDA:
                mundo.aplicar(idx,token)

            registro_completo.append({
                "indice": idx,
                "orden": token,
                "estado_ap": paso_ap["estado"],
                "pila": paso_ap["pila"],
                "posicion": f"({mundo.robot[0]}, {mundo.robot[1]})",
                "carga": "con carga" if mundo.cargando else "vacia"
            })
    except ErrorFisico as e:
        return {
            "resultado": "ERROR FISICO",
            "mensaje": str(e),
            "registro": registro_completo,
            "metricas": None
        }

    #verificacion meta final

    metricas = {
        "grilla_inicial": grilla_inicial,
        "grilla_final": mundo.grilla_texto(),
        "movimientos_sin_carga": mundo.movimientos_sin_carga,
        "movimientos_con_carga": mundo.movimientos_con_carga,
        "altura_maxima_pila":ap.altura_maxima
    }

    if mundo.cumple_meta():
        return {
            "resultado": "MISION RESUELTA",
            "mensaje": "Todas las cajas estan en destino, robot esta en posicion final y la pinza esta vacia",
            "registro": registro_completo,
            "metricas": metricas
        }
    else:
        return {
        "resultado": "OBJETIVO NO ALCANZADO",
        "mensaje":f"Objetivo no alcanzado: {mundo.motivo_meta()}",
        "registro": registro_completo,
        "metricas": metricas
        }

def exportar_registro_csv(registro, ruta_csv):
    "guarda el registro de la secuencia paso a paso en formato CSV"
    if not registro:
        return
    columnas = ["indice","orden", "estado_ap", "pila", "posicion", "carga"]
    with open(ruta_csv, mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=columnas)
        writer.writeheader()
        writer.writerows(registro)


def exportar_reporte_txt(res, ruta_txt):
    "genera reusmen en txt con registro anterior y metricas pedidas"
    with open(ruta_txt, mode="w", encoding="utf-8") as f:
        f.write(f"RESULTADO: {res['resultado']}\n")
        f.write(f"DETALLE: {res['mensaje']}\n\n")

        if res["metricas"]:
            m = res["metricas"]
            f.write("=== MÉTRICAS DE EJECUCIÓN ===\n")
            f.write(f"Movimientos sin carga: {m['movimientos_sin_carga']}\n")
            f.write(f"Movimientos con carga: {m['movimientos_con_carga']}\n")
            f.write(f"Máxima altura de pila (sin Z): {m['altura_maxima_pila']}\n\n")
            f.write("--- GRILLA INICIAL ---\n")
            f.write(m["grilla_inicial"] + "\n\n")
            f.write("--- GRILLA FINAL ---\n")
            f.write(m["grilla_final"] + "\n\n")

        if res["registro"]:
            f.write("=== REGISTRO POR TOKEN ===\n")
            f.write(f"{'Índice':<7} | {'Orden':<10} | {'Estado':<6} | {'Pila':<10} | {'Posición':<10} | {'Carga'}\n")
            f.write("-" * 65 + "\n")
            for fila in res["registro"]:
                f.write(
                    f"{fila['indice']:<7} | {fila['orden']:<10} | {fila['estado_ap']:<6} | "
                    f"{fila['pila']:<10} | {fila['posicion']:<10} | {fila['carga']}\n"
                )