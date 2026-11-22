import json
import os
from validador import ejecutar_programa, exportar_registro_csv, exportar_reporte_txt


def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def cargar_texto(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_instancia = os.path.join(base_dir, "instancias", "grupo5.json")
    ruta_solucion = os.path.join(base_dir, "programa", "solucion.txt")
    carpeta_pruebas = os.path.join(base_dir, "programa", "prueba")

    instancia = cargar_json(ruta_instancia)

    #ejecutar solución principal
    print("=" * 60)
    print("EJECUTANDO SOLUCIÓN PRINCIPAL (grupo5.json)")
    print("=" * 60)
    texto_solucion = cargar_texto(ruta_solucion)
    res = ejecutar_programa(texto_solucion, instancia)

    print(f"Resultado: {res['resultado']}")
    print(f"Detalle:   {res['mensaje']}")
    if res["metricas"]:
        m = res["metricas"]
        print(f"Movimientos sin carga: {m['movimientos_sin_carga']}")
        print(f"Movimientos con carga: {m['movimientos_con_carga']}")
        print(f"Altura máxima de pila: {m['altura_maxima_pila']}")
        print("\nGrilla Final:\n" + m["grilla_final"])

    # exportar archivos requeridos 
    exportar_registro_csv(res["registro"], os.path.join(base_dir, "registro_solucion.csv"))
    exportar_reporte_txt(res, os.path.join(base_dir, "registro_solucion.txt"))
    print("\nArchivos 'registro_solucion.csv' y 'registro_solucion.txt' generados.\n")

    #batería de pruebas de programa/prueba/
    print("=" * 60)
    print("EJECUTANDO BATERÍA DE PRUEBAS")
    print("=" * 60)
    if os.path.exists(carpeta_pruebas):
        for archivo in sorted(os.listdir(carpeta_pruebas)):
            if archivo.endswith(".txt"):
                ruta_p = os.path.join(carpeta_pruebas, archivo)
                r_prueba = ejecutar_programa(cargar_texto(ruta_p), instancia)
                print(f"[{archivo:<24}] -> {r_prueba['resultado']}: {r_prueba['mensaje']}")

    
    casos_borde = {
        "entrada_vacia": "",
        "token_desconocido": "viaje arriba saltar agarrar abajo finviaje",
        "salida_grilla": "viaje abajo agarrar arriba soltar finviaje"
    }
    print("\n--- CASOS DE BORDE ---")
    for nombre, codigo in casos_borde.items():
        r_borde = ejecutar_programa(codigo, instancia)
        print(f"[{nombre:<24}] -> {r_borde['resultado']}: {r_borde['mensaje']}")


if __name__ == "__main__":
    main()