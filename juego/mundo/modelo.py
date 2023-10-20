from dataclasses import dataclass
import random
from typing import Optional, ClassVar, Union

CORAZON = "\u2764\uFE0F"
TREBOL = "\u2663\uFE0F"
DIAMANTE = "\u2666\uFE0F"
ESPADA = "\u2660\uFE0F"
OCULTA = "\u25AE\uFE0F"


@dataclass
class Carta:
    VALORES: ClassVar[list[str]] = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    PINTAS: ClassVar[list[str]] = [CORAZON, TREBOL, DIAMANTE, ESPADA]
    pinta: str
    valor: str
    visible: bool = True

    def mostrar(self):
        self.visible = True

    def ocultar(self):
        self.visible = False

    def calcular_valor(self, as_como_11=True) -> int:
        if self.valor == "A":
            if as_como_11:
                return 11
            else:
                return 1
        elif self.valor in ["J", "Q", "K"]:
            return 10
        else:
            return int(self.valor)

    def es_letra(self) -> bool:
        return self.valor in ["A", "J", "Q", "K"]

    def __str__(self) -> str:
        if not self.visible:
            return f"{OCULTA}"
        else:
            return f"{self.valor}{self.pinta}"


class Baraja:

    def __init__(self):
        self.cartas = []
        self.reiniciar()

    def reiniciar(self):
        for pinta in Carta.PINTAS:
            for valor in Carta.VALORES:
                self.cartas.append(Carta(pinta, valor))

    def revolver(self):
        random.shuffle(self.cartas)

    def repartir(self, oculta=False) -> Optional[Carta]:
        if len(self.cartas) > 0:
            carta = self.cartas.pop()
            if oculta:
                carta.ocultar()
            return carta
        else:
            return None

    def tiene_cartas(self) -> bool:
        return len(self.cartas) > 0


class Mano:

    def __init__(self):
        self.cartas: list[Carta] = []
        self.cantidad_ases = 0

    def limpiar(self):
        self.cartas.clear()

    def agregar_carta(self, carta: Carta):
        if carta.valor == "A":
            self.cartas.append(carta)
            self.cantidad_ases += 1
        else:
            self.cartas.insert(0, carta)

    def calcular_valor(self) -> Union[int, str]:

        for carta in self.cartas:
            if not carta.visible:
                return "--"

        valor = 0

        for carta in self.cartas[:-self.cantidad_ases]:
            valor += carta.calcular_valor()

        for carta in self.cartas[-self.cantidad_ases:]:
            valor += carta.calcular_valor(valor < 11)

        return valor

    def es_blackjack(self):
        if len(self.cartas) > 2:
            return False
        else:
            return self.cartas[0].valor == "A" and self.cartas[1].valor in ["J", "Q", "K"] \
                   or self.cartas[1].valor == "A" and self.cartas[0].valor in ["J", "Q", "K"]

    def __str__(self) -> str:
        str_mano = ""
        for carta in self.cartas:
            str_mano += f"{str(carta):^5}"

        return str_mano


class Jugador:

    def __init__(self, nombre: str):
        self.nombre: str = nombre
        self.mano: Mano = Mano()

    def recibir_carta(self, carta: Carta):
        self.mano.agregar_carta(carta)


class BlackJack:

    def __init__(self, nombre_usuario: str):
        self.baraja: Baraja = Baraja()
        self.usuario: Jugador = Jugador(nombre_usuario)
        self.casa: Jugador = Jugador("La Casa")

    def iniciar_nuevo_juego(self):
        self.usuario.mano.limpiar()
        self.casa.mano.limpiar()
        self.baraja.reiniciar()
        self.repartir_manos()

    def repartir_manos(self):
        self.baraja.revolver()

        # Repartir la mano del usuario
        self.usuario.recibir_carta(self.baraja.repartir())
        self.usuario.recibir_carta(self.baraja.repartir())

        # Repartir la mano de la casa
        self.casa.recibir_carta(self.baraja.repartir())
        self.casa.recibir_carta(self.baraja.repartir(oculta=True))

    def dar_carta_a_jugador(self):
        self.usuario.recibir_carta(self.baraja.repartir())

    def usuario_perdio(self) -> bool:
        return self.usuario.mano.calcular_valor() > 21

    def la_casa_perdio(self) -> bool:
        return self.casa.mano.calcular_valor() > 21

    def la_casa_puede_pedir(self) -> bool:
        valor_mano_casa = self.casa.mano.calcular_valor()
        return valor_mano_casa <= self.usuario.mano.calcular_valor() and valor_mano_casa < 21

    def destapar_mano_de_la_casa(self):
        for carta in self.casa.mano.cartas:
            carta.mostrar()

    def dar_carta_a_la_casa(self):
        self.casa.recibir_carta(self.baraja.repartir())

    def usuario_tiene_blackjack(self) -> bool:
        return self.usuario.mano.es_blackjack()
