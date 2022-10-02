JUGADOR = '@'
CAJA_SUELTA = '$'
OBJETIVO_LIBRE = '.'
PARED = "#"
ESPACIO_LIBRE = " "
CAJA_CON_OBJETIVO = "*"
JUGADOR_CON_OBJETIVO = "+"

def crear_grilla(desc):
    return _generar_grilla(desc)

def dimensiones(grilla):
    return len(grilla[0]), len(grilla)

def hay_pared(grilla, c, f):
    return _hay(grilla, c, f, PARED)

def hay_objetivo(grilla, c, f):
    return _hay(grilla, c, f, OBJETIVO_LIBRE) or _hay(grilla, c, f, CAJA_CON_OBJETIVO) or _hay(grilla, c, f, JUGADOR_CON_OBJETIVO)

def hay_caja(grilla, c, f):
    return _hay(grilla, c, f, CAJA_SUELTA) or _hay(grilla, c, f, CAJA_CON_OBJETIVO)

def hay_jugador(grilla, c, f):
    return _hay(grilla, c, f, JUGADOR) or _hay(grilla, c, f, JUGADOR_CON_OBJETIVO)

def juego_ganado(grilla):
    return CAJA_SUELTA not in [elemento for sublista in grilla for elemento in sublista]

def mover(grilla, direccion):
    copia_grilla = _generar_grilla(grilla)
    x_jugador, y_jugador = _ubicar_jugador(grilla)
    x_siguiente_jugador, y_siguiente_jugador = _posicion_siguiente(x_jugador, y_jugador, direccion)

    if hay_pared(grilla, y_siguiente_jugador, x_siguiente_jugador):
        return grilla

    if _hay_movimiento_posible(grilla, y_siguiente_jugador, x_siguiente_jugador):
        _avanzar_jugador(copia_grilla, y_siguiente_jugador, x_siguiente_jugador)
        _liberar_espacio_jugador(copia_grilla, y_jugador, x_jugador)
        return copia_grilla

    if hay_caja(grilla, y_siguiente_jugador, x_siguiente_jugador):
        x_siguiente_caja, y_siguiente_caja = _posicion_siguiente(x_siguiente_jugador, y_siguiente_jugador, direccion)

        if hay_pared(grilla, y_siguiente_caja, x_siguiente_caja) or hay_caja(grilla, y_siguiente_caja, x_siguiente_caja):
            return grilla

        if _hay_espacio_libre(grilla, y_siguiente_caja, x_siguiente_caja):
            _avanzar_jugador(copia_grilla, y_siguiente_jugador, x_siguiente_jugador)
            _colocar(copia_grilla, y_siguiente_caja, x_siguiente_caja, CAJA_SUELTA)

        if _hay_objetivo_libre(grilla, y_siguiente_caja, x_siguiente_caja):
            _avanzar_jugador(copia_grilla, y_siguiente_jugador, x_siguiente_jugador)
            _colocar(copia_grilla, y_siguiente_caja, x_siguiente_caja, CAJA_CON_OBJETIVO)

    _liberar_espacio_jugador(copia_grilla, y_jugador, x_jugador)
    return copia_grilla

def _hay(grilla, c, f, objetivo):
    return grilla[f][c] == objetivo

def _ubicar_jugador(grilla):
    for i, lista in enumerate(grilla):
        for j, valor in enumerate(lista):
            if hay_jugador(grilla, j, i):
                return i, j

def _posicion_siguiente(x, y, direccion):
    return x + direccion[1], y + direccion[0]

def _hay_espacio_libre(grilla, c, f):
    return _hay(grilla, c, f, ESPACIO_LIBRE)

def _hay_objetivo_libre(grilla, c, f):
    return _hay(grilla, c, f, OBJETIVO_LIBRE)

def _generar_grilla(desc):
    return [[desc[i][j] for j in range(len(desc[0]))] for i in range(len(desc))]

def _liberar_espacio_jugador(grilla, y_jugador, x_jugador):
    grilla[x_jugador][y_jugador] = ESPACIO_LIBRE if not hay_objetivo(grilla, y_jugador, x_jugador) else OBJETIVO_LIBRE

def _avanzar_jugador(grilla, y_jugador, x_jugador):
    _colocar(grilla, y_jugador, x_jugador,
             JUGADOR_CON_OBJETIVO if hay_objetivo(grilla, y_jugador, x_jugador) else JUGADOR)

def _colocar(grilla, y, x, pieza):
    grilla[x][y] = pieza

def _hay_movimiento_posible(grilla, y_jugador, x_jugador):
    return _hay_espacio_libre(grilla, y_jugador, x_jugador) \
            or _hay_objetivo_libre(grilla, y_jugador, x_jugador)