'''Comprobador de Conectividad de Sitios Web

La idea de este proyecto es crear un programa que compruebe
si una página web está funcionando. El usuario introduce una dirección web 
y el programa devuelve su código HTTP. Si el código es 200 significa que 
la página está disponible.

Utilizaremos:
- urllib para conectarnos a páginas web.
- tkinter para crear la interfaz gráfica.

Estructura:

ComprobadorWeb:
    Se encarga de comprobar la conexión.

App:
    Crea la ventana y recoge los datos del usuario.
'''

import tkinter as tk
from urllib.request import urlopen

class ComprobadorWeb:

    # Esta clase contiene la lógica del programa.
    # No sabe nada de ventanas.
    # Solo recibe una dirección y comprueba si funciona.

    def comprobar(self, url):

        try:

            # urlopen abre una conexión con la página.
            respuesta = urlopen(url)

            # getcode() devuelve el código HTTP.
            codigo = respuesta.getcode()

            if codigo == 200:

                return "La página funciona correctamente"

            else:

                return f"La página no está disponible. Código: {codigo}"

        # Si ocurre algún error de conexión entra aquí.
        except:

            return "No se pudo conectar con la página"

class App:

    # Esta clase controla la interfaz gráfica.
    # Aquí creamos:
    # - caja donde escribir la URL.
    # - botón para comprobar.
    # - etiqueta con el resultado.

    def __init__(self, comprobador):

        # Conectamos las clases.
        # App recibe un objeto ComprobadorWeb
        # y puede utilizar sus métodos.
        self.comprobador = comprobador

        self.ventana = tk.Tk()

        self.ventana.title("Comprobador de páginas web")

        self.crear_ventana()

    def crear_ventana(self):

        etiqueta = tk.Label(
            self.ventana,
            text="Introduce una página web:"
        )

        etiqueta.pack()

        self.entrada = tk.Entry(
            self.ventana,
            width=40
        )

        self.entrada.pack()

        boton = tk.Button(
            self.ventana,
            text="Comprobar",
            command=self.comprobar
        )

        boton.pack()

        self.resultado = tk.Label(
            self.ventana,
            text=""
        )

        self.resultado.pack()

    def comprobar(self):

        # Obtenemos el texto escrito por el usuario.

        url = self.entrada.get()

        # Llamamos al método de la otra clase.

        mensaje = self.comprobador.comprobar(url)

        # Mostramos el resultado en la ventana.

        self.resultado.config(text=mensaje)


def main():

    # Creamos el objeto que sabe comprobar páginas.

    comprobador = ComprobadorWeb()

    # Creamos la aplicación y le pasamos
    # el comprobador.

    app = App(comprobador)

    # Mantiene abierta la ventana.

    app.ventana.mainloop()


if __name__ == "__main__":

    main()