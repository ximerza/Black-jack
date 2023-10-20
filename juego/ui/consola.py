import sys
import time
from typing import Optional

from juego.mundo.modelo import BlackJack


class UIConsola:

    def __init__(self):
        self.blackjack: Optional[BlackJack] = None
        self.opciones = {
            "1": self.iniciar_nuevo_juego,
            "0": self.salir
        }

    @staticmethod
    def mostrar_menu():
        titulo = " BLACK JACK "
        print(f"\n{titulo:_^30}")
        print("1. Iniciar nuevo juego")
        print("0. Salir")
        print(f"{'_':_^30}")

    def ejecutar_app(self):
        print("\nBIENVENIDO A UN NUEVO JUEGO DE BLACKJACK")
        self.registrar_usuario()
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ")
            accion = self.opciones.get(opcion)
            if accion:
                accion()
            else:
                print(f"{opcion} no es una opción válida")

    def registrar_usuario(self):
        nombre: str = input("¿Cuál es tu nombre?: ")
        self.blackjack = BlackJack(nombre_usuario=nombre)

    def iniciar_nuevo_juego(self):
        self.blackjack.iniciar_nuevo_juego()
        self.mostrar_manos(self.blackjack.casa.mano, self.blackjack.usuario.mano)

        if not self.blackjack.usuario_tiene_blackjack():
            self.hacer_jugada_del_jugador()
        else:
            print(f"¡¡¡BLACKJACK!!!\n!FELICITACIONES {self.blackjack.usuario.nombre.upper()}! HAS GANADO EL JUEGO\n")

    def hacer_jugada_del_jugador(self):
        while not self.blackjack.usuario_perdio():
            respuesta = input("¿Quieres otra carta? s(si), n(no): ")
            if respuesta == 's':
                self.blackjack.dar_carta_a_jugador()
                self.mostrar_manos(self.blackjack.casa.mano, self.blackjack.usuario.mano)
            elif respuesta == 'n':
                break

        if self.blackjack.usuario_perdio():
            print("\nHAS PERDIDO EL JUEGO\n")
        else:
            self.ejecutar_turno_de_la_casa()

    def ejecutar_turno_de_la_casa(self):
        print("\nAHORA ES EL TURNO DE LA CASA\n")
        self.blackjack.destapar_mano_de_la_casa()
        self.mostrar_manos(self.blackjack.casa.mano, self.blackjack.usuario.mano)

        time.sleep(3)

        while not self.blackjack.la_casa_perdio() and self.blackjack.la_casa_puede_pedir():
            print("\nLA CASA PIDE UNA CARTA\n")
            time.sleep(1)
            self.blackjack.dar_carta_a_la_casa()
            self.mostrar_manos(self.blackjack.casa.mano, self.blackjack.usuario.mano)
            time.sleep(2.5)

        print("\nLA CASA TERMINA SU JUGADA\n")
        time.sleep(1)

        print(f"{' RESULTADO ':-^20}")
        if self.blackjack.la_casa_perdio():
            print(f"\n¡FELICITACIONES {self.blackjack.usuario.nombre.upper()}! HAS GANADO EL JUEGO\n")
        else:
            if self.blackjack.casa.mano.calcular_valor() > self.blackjack.usuario.mano.calcular_valor():
                print("\nLO SENTIMOS, ¡LA CASA GANA!\n")
            else:
                print(f"\n¡FELICITACIONES {self.blackjack.usuario.nombre.upper()}! HAS GANADO EL JUEGO\n")

    @staticmethod
    def mostrar_manos(mano_casa, mano_jugador):
        print(f"\n{'MANO DE LA CASA':<15}\n{str(mano_casa):<15}")
        print(f"{'VALOR: ' + str(mano_casa.calcular_valor()):<15}\n")
        print(f"\n{'TU MANO':<15}\n{str(mano_jugador):<15}")
        print(f"{'VALOR: ' + str(mano_jugador.calcular_valor()):<15}\n")

    @staticmethod
    def salir():
        print("\nGRACIAS POR JUGAR BLACKJACK. VUELVA PRONTO")
        sys.exit(0)
