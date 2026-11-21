from errores import ErrorFisico

# Cuánto cambia (fila, columna) con cada movimiento
DESPLAZAMIENTOS = {
    "arriba": (-1, 0),
    "abajo": (1, 0),
    "izquierda": (0, -1),
    "derecha": (0, 1),
}


class Mundo:
    def __init__(self, instancia):
        """'instancia' es el diccionario leído del archivo .json"""
        self.filas = instancia["filas"]
        self.columnas = instancia["columnas"]
        self.robot = tuple(instancia["robot"])
        self.robot_final = tuple(instancia["robot_final"])
        self.cajas = {tuple(c) for c in instancia["cajas"]}          # cambia
        self.obstaculos = {tuple(o) for o in instancia["obstaculos"]}  # fijo
        self.destinos = {tuple(d) for d in instancia["destinos"]}      # fijo
        self.cargando = False            # pinza vacía al empezar

        # Contadores que pide la consigna
        self.movimientos_sin_carga = 0
        self.movimientos_con_carga = 0

 
    def aplicar(self, indice, token):
        """Ejecuta UNA orden. Si no se puede hacer, lanza ErrorFisico."""
        if token in DESPLAZAMIENTOS:
            self._mover(indice, token)
        elif token == "agarrar":
            self._agarrar(indice, token)
        elif token == "soltar":
            self._soltar(indice, token)
       

    def _mover(self, indice, token):
        df, dc = DESPLAZAMIENTOS[token]
        nueva = (self.robot[0] + df, self.robot[1] + dc)

        if not (1 <= nueva[0] <= self.filas and 1 <= nueva[1] <= self.columnas):
            raise ErrorFisico(indice, token,
                              f"desde {self.robot} el robot sale de la grilla")
        if nueva in self.obstaculos:
            raise ErrorFisico(indice, token,
                              f"desde {self.robot} intenta atravesar el obstáculo {nueva}")

        self.robot = nueva
        if self.cargando:
            self.movimientos_con_carga += 1
        else:
            self.movimientos_sin_carga += 1

    def _agarrar(self, indice, token):
        if self.cargando:
            raise ErrorFisico(indice, token, "la pinza ya tiene una caja")
        if self.robot not in self.cajas:
            raise ErrorFisico(indice, token, f"no hay caja en {self.robot}")
        self.cajas.remove(self.robot)
        self.cargando = True

    def _soltar(self, indice, token):
        if not self.cargando:
            raise ErrorFisico(indice, token, "la pinza está vacía")
        if self.robot in self.cajas:
            raise ErrorFisico(indice, token, f"ya hay una caja en {self.robot}")
        self.cajas.add(self.robot)
        self.cargando = False

    def ejecutar(self, tokens):
        """Ejecuta todo el programa. Devuelve una lista con el estado
        del mundo después de cada token (para el registro CSV)."""
        registro = []
        for indice, token in enumerate(tokens, start=1):
            self.aplicar(indice, token)
            registro.append({
                "indice": indice,
                "posicion": self.robot,
                "carga": "con carga" if self.cargando else "vacia",
            })
        return registro


    def cumple_meta(self):
        return (self.cajas == self.destinos
                and self.robot == self.robot_final
                and not self.cargando)

    def motivo_meta(self):
        """Explica qué falta, si la meta no se cumple."""
        problemas = []
        if self.cajas != self.destinos:
            faltan = sorted(self.destinos - self.cajas)
            sobran = sorted(self.cajas - self.destinos)
            problemas.append(f"destinos sin caja: {faltan}; cajas fuera de destino: {sobran}")
        if self.robot != self.robot_final:
            problemas.append(f"el robot terminó en {self.robot} y debía terminar en {self.robot_final}")
        if self.cargando:
            problemas.append("la pinza terminó con una caja")
        return "; ".join(problemas)

  
    def grilla_texto(self):
        """R robot, C caja, X obstáculo, T destino vacío, * caja en destino."""
        lineas = ["    " + " ".join(str(c) for c in range(1, self.columnas + 1))]
        for f in range(1, self.filas + 1):
            fila = []
            for c in range(1, self.columnas + 1):
                celda = (f, c)
                if celda == self.robot:
                    fila.append("R")
                elif celda in self.obstaculos:
                    fila.append("X")
                elif celda in self.cajas and celda in self.destinos:
                    fila.append("*")
                elif celda in self.cajas:
                    fila.append("C")
                elif celda in self.destinos:
                    fila.append("T")
                else:
                    fila.append(".")
            lineas.append(f"{f}   " + " ".join(fila))
        return "\n".join(lineas)