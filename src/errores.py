

class RechazoAP(Exception):
    def __init__(self, indice, token, estado, pila, motivo):
        self.indice = indice
        self.token = token
        self.estado = estado
        self.pila = pila
        self.motivo = motivo
        super().__init__(
            f"Rechazo del AP en token {indice} ('{token}'), estado {estado}, "
            f"pila {pila}: {motivo}"
        )

class ErrorFisico(Exception):
    def __init__(self, indice, token, motivo):
        self.indice = indice
        self.token = token
        self.motivo = motivo
        super().__init__(f"Error físico en token {indice} ('{token}'): {motivo}")


class ErrorLexico(Exception):
    def __init__(self, indice, token, linea, columna):
        self.indice = indice
        self.token = token
        self.linea = linea
        self.columna = columna
        super().__init__(f"Error lexico en token {indice} (linea {linea}, palabra {columna }): "
                         f"'{token}' no es una palabra reservada valida.")