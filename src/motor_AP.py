

from errores import RechazoAP

MOVIMIENTOS = ["arriba", "abajo", "izquierda", "derecha"]


SIMBOLO_PILA = {"arriba": "D", "abajo": "U", "izquierda": "R", "derecha": "L"}


OPUESTO = {"U": "arriba", "D": "abajo", "L": "izquierda", "R": "derecha"}

SIMBOLOS_PILA = ["U", "D", "L", "R", "Z"]
ESTADO_INICIAL = "q0"
LAMBDA = "λ"
FONDO = "Z"
ESTADOS_FINALES = {"q5"}


def construir_transiciones():
    t = {}

    # q0: movimientos libres antes del primer viaje
    for m in MOVIMIENTOS:
        t[("q0", m, "Z")] = ("q0", "Z")

    # q0 / q4: abrir un viaje
    t[("q0", "viaje", "Z")] = ("q1", "Z")
    t[("q4", "viaje", "Z")] = ("q1", "Z")

    # q1: ida -> apila el símbolo del movimiento
    for m in MOVIMIENTOS:
        for tope in SIMBOLOS_PILA:
            t[("q1", m, tope)] = ("q1", SIMBOLO_PILA[m] + tope)

    # q1: agarrar -> empieza la vuelta (no toca la pila)
    for tope in SIMBOLOS_PILA:
        t[("q1", "agarrar", tope)] = ("q2", tope)

    # q2: vuelta -> solo el movimiento que coincide con el tope desapila
    for simbolo, movimiento in OPUESTO.items():
        t[("q2", movimiento, simbolo)] = ("q2", "")

    # q2: soltar solo si la vuelta terminó (pila en Z)
    t[("q2", "soltar", "Z")] = ("q3", "Z")

    # q3: cerrar el viaje
    t[("q3", "finviaje", "Z")] = ("q4", "Z")

    # q4: movimientos libres entre viajes o al final
    for m in MOVIMIENTOS:
        t[("q4", m, "Z")] = ("q4", "Z")

    # q4: transición λ hacia el estado final (no consume entrada)
    t[("q4", LAMBDA, "Z")] = ("q5", "Z")

    return t


def explicar_rechazo(estado, token, tope):
    if estado in ("q0", "q4"):
        if token in ("agarrar", "soltar", "finviaje"):
            return f"'{token}' fuera de un viaje"
    if estado == "q1":
        if token == "soltar":
            return "soltar sin haber agarrado una caja"
        if token in ("viaje", "finviaje"):
            return f"'{token}' durante el camino de ida"
    if estado == "q2":
        if token == "agarrar":
            return "segundo agarrar en el mismo viaje"
        if token == "soltar":
            return "soltar antes de terminar el regreso"
        if token in MOVIMIENTOS:
            esperado = OPUESTO.get(tope)
            if esperado is None:
                return f"'{token}' después de completar el regreso (se esperaba soltar)"
            return f"el regreso no es el camino inverso: se esperaba '{esperado}'"
        return f"'{token}' durante el camino de regreso"
    if estado == "q3":
        return "se esperaba finviaje después de soltar"
    return "no hay transición definida"


class AutomataPila:
    def __init__(self):
        self.transiciones = construir_transiciones()
        self.reiniciar()

    def reiniciar(self):
        self.estado = ESTADO_INICIAL
        self.pila = [FONDO]          # último elemento = tope
        self.altura_maxima = 0       # sin contar el fondo Z

    def pila_texto(self):
        return "".join(reversed(self.pila))

    def paso(self, indice, token):
        tope = self.pila[-1]
        clave = (self.estado, token, tope)
        if clave not in self.transiciones:
            raise RechazoAP(indice, token, self.estado, self.pila_texto(),
                            explicar_rechazo(self.estado, token, tope))

        nuevo_estado, reemplazo = self.transiciones[clave]
        self.pila.pop()
        for simbolo in reversed(reemplazo):   # el primero del texto queda como tope
            self.pila.append(simbolo)
        self.estado = nuevo_estado
        self.altura_maxima = max(self.altura_maxima, len(self.pila) - 1)

    def procesar(self, tokens):
        self.reiniciar()
        traza = []
        for indice, token in enumerate(tokens, start=1):
            self.paso(indice, token)
            traza.append({
                "indice": indice,
                "token": token,
                "estado": self.estado,
                "pila": self.pila_texto(),
            })

      
        clave_lambda = (self.estado, LAMBDA, self.pila[-1])
        if clave_lambda in self.transiciones:
            self.paso(len(tokens) + 1, LAMBDA)
            traza.append({
                "indice": len(tokens) + 1,
                "token": LAMBDA,
                "estado": self.estado,
                "pila": self.pila_texto(),
            })

        if self.estado not in ESTADOS_FINALES:
            motivos = {
                "q0": "la entrada no contiene ningún viaje",
                "q1": "viaje sin agarrar ni cierre",
                "q2": "viaje sin terminar el regreso",
                "q3": "viaje sin cierre finviaje",
            }
            raise RechazoAP(len(tokens), "fin de entrada", self.estado,
                            self.pila_texto(), motivos[self.estado])
        return traza

    def acepta(self, tokens):
        """True/False sin lanzar excepciones."""
        try:
            self.procesar(tokens)
            return True
        except RechazoAP:
            return False
