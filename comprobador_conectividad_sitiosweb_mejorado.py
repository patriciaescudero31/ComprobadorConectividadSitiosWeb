"""Comprobador de Conectividad de Sitios Web (versión mejorada)

Versión mejorada que:
- Normaliza el esquema (añade http:// si falta)
- Añade timeout y manejo de errores explícito
- Ejecuta la comprobación en un hilo para no bloquear la interfaz
- Mejora la experiencia de usuario (estado, deshabilita botón, Enter para enviar)

Archivo creado aparte para no sustituir el original.
"""

import tkinter as tk
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import threading

class ComprobadorWeb:
    """Lógica independiente de la interfaz."""

    def comprobar(self, url, timeout=10):
        """Devuelve un mensaje con el resultado de la comprobación.

        Parámetros:
        - url: cadena introducida por el usuario (puede faltar http/https)
        - timeout: segundos antes de agotar la espera
        """
        # Normalizar esquema si falta
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        try:
            respuesta = urlopen(url, timeout=timeout)
            codigo = respuesta.getcode()
            if codigo == 200:
                return f"La página funciona correctamente (HTTP {codigo})"
            else:
                return f"La página respondió con código: {codigo}"
        except HTTPError as e:
            return f"Error HTTP: {e.code}"
        except URLError as e:
            # e.reason puede ser una tupla o un mensaje
            return f"No se pudo conectar con la página: {e.reason}"
        except Exception as e:
            return f"Error inesperado: {e}"

class App:
    def __init__(self, comprobador):
        self.comprobador = comprobador
        self.ventana = tk.Tk()
        self.ventana.title("Comprobador de páginas web — Mejorado")
        self.crear_ventana()

    def crear_ventana(self):
        etiqueta = tk.Label(self.ventana, text="Introduce una página web:")
        etiqueta.pack(padx=8, pady=(8, 0))

        self.entrada = tk.Entry(self.ventana, width=50)
        self.entrada.pack(padx=8, pady=6)
        self.entrada.insert(0, "https://")  # ayuda al usuario
        self.entrada.bind("<Return>", lambda e: self.comprobar())

        self.boton = tk.Button(self.ventana, text="Comprobar", command=self.comprobar)
        self.boton.pack(padx=8, pady=6)

        self.resultado = tk.Label(self.ventana, text="", wraplength=400, justify="left")
        self.resultado.pack(padx=8, pady=(0, 8))

    def comprobar(self):
        url = self.entrada.get().strip()
        if not url:
            self.resultado.config(text="Escribe una URL primero")
            return

        # UX: desactivar botón y mostrar estado
        self.boton.config(state="disabled")
        self.resultado.config(text="Comprobando...")

        # Ejecutar la comprobación en un hilo para no bloquear la GUI
        thread = threading.Thread(target=self._thread_comprobar, args=(url,), daemon=True)
        thread.start()

    def _thread_comprobar(self, url):
        mensaje = self.comprobador.comprobar(url)
        # Actualizar la GUI desde el hilo principal
        self.ventana.after(0, lambda: self._mostrar_resultado(mensaje))

    def _mostrar_resultado(self, mensaje):
        self.resultado.config(text=mensaje)
        self.boton.config(state="normal")


def main():
    comprobador = ComprobadorWeb()
    app = App(comprobador)
    app.ventana.mainloop()


if __name__ == "__main__":
    main()
