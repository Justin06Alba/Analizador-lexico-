import os
import sys
import subprocess
from tkinter import filedialog

import customtkinter as ctk

from src.gui import CodeEditor, TokenTable, ConsoleOutput
from src.lexer_compiler import LexerCompiler
from src.lexer_executor import LexerExecutor
from src.token_parser import TokenParser


def _get_base_dir() -> str:
    """Retorna el directorio base del proyecto.

    Cuando la aplicación corre empaquetada con PyInstaller (frozen),
    los recursos están en sys._MEIPASS.  En desarrollo normal es la
    carpeta donde vive este archivo (src/), un nivel arriba del proyecto.
    """
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MiniLexGUI(ctk.CTk):
    """Ventana principal del Analizador Léxico MiniLex."""

    def __init__(self):
        super().__init__()
        self.title("Analizador Léxico MiniLex")
        self.geometry("1200x800")

        base = _get_base_dir()
        lexer_l   = os.path.join(base, "src", "lexer.l")
        build_dir = os.path.join(base, "build")

        self.compiler = LexerCompiler(lexer_l, build_dir)
        self.executor: LexerExecutor | None = None
        self.parser = TokenParser()

        self.create_widgets()
        self.check_and_compile_lexer()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)

        # Editor de código
        self.grid_rowconfigure(0, weight=3)
        ctk.CTkLabel(self, text="Editor de Código", font=("Consolas", 12, "bold"), anchor="w").grid(
            row=0, column=0, sticky="nw", padx=10, pady=(10, 0)
        )
        self.editor = CodeEditor(self)
        self.editor.grid(row=0, column=0, sticky="nsew", padx=10, pady=(28, 4))

        # Botones
        self.grid_rowconfigure(1, weight=0)
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=4)

        self.btn_analyze = ctk.CTkButton(button_frame, text="Analizar", command=self.on_analyze, width=120)
        self.btn_analyze.pack(side="left", padx=(0, 8))

        self.btn_clear = ctk.CTkButton(
            button_frame, text="Limpiar", command=self.on_clear,
            width=120, fg_color="#555555", hover_color="#444444"
        )
        self.btn_clear.pack(side="left", padx=(0, 8))

        self.btn_load = ctk.CTkButton(
            button_frame, text="Cargar archivo .ml", command=self.on_load_file,
            width=160, fg_color="#555555", hover_color="#444444"
        )
        self.btn_load.pack(side="left")

        # Tabla de tokens
        self.grid_rowconfigure(2, weight=2)
        ctk.CTkLabel(self, text="Tabla de Tokens", font=("Consolas", 12, "bold"), anchor="w").grid(
            row=2, column=0, sticky="nw", padx=10, pady=(4, 0)
        )
        self.token_table = TokenTable(self)
        self.token_table.grid(row=2, column=0, sticky="nsew", padx=10, pady=(22, 4))

        # Consola de estado
        self.grid_rowconfigure(3, weight=1)
        ctk.CTkLabel(self, text="Consola de Estado", font=("Consolas", 12, "bold"), anchor="w").grid(
            row=3, column=0, sticky="nw", padx=10, pady=(4, 0)
        )
        self.console = ConsoleOutput(self)
        self.console.grid(row=3, column=0, sticky="nsew", padx=10, pady=(22, 10))

    def on_analyze(self):
        code = self.editor.get_code()
        if not code or not code.strip():
            self.console.write("No hay código para analizar", "error")
            return

        if self.executor is None:
            self.console.write("Lexer no compilado. No se puede ejecutar el análisis.", "error")
            return

        self.console.write("Iniciando análisis léxico...", "info")

        try:
            success, stdout, stderr = self.executor.execute(code)

            if success:
                tokens = self.parser.parse(stdout)
                self.token_table.display_tokens(tokens)

                error_tokens = [t for t in tokens if t.is_error()]
                self.editor.highlight_errors(error_tokens)

                token_count = len([t for t in tokens if not t.is_error()])
                error_count = len(error_tokens)
                self.console.write(
                    f"Análisis completado — Tokens reconocidos: {token_count}, "
                    f"Errores encontrados: {error_count}",
                    "success" if error_count == 0 else "info",
                )
            else:
                self.console.write(stderr or "Error desconocido al ejecutar el lexer.", "error")

        except FileNotFoundError as e:
            self.console.write(f"Archivo no encontrado: {e}", "error")
        except subprocess.CalledProcessError as e:
            self.console.write(f"Error al ejecutar el lexer: {e.stderr or str(e)}", "error")
        except Exception as e:
            self.console.write(f"Error inesperado: {e}", "error")

    def on_clear(self):
        self.editor.set_code("")
        self.editor.highlight_errors([])
        self.token_table.clear()
        self.console.clear()

    def on_load_file(self):
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo MiniLex",
            filetypes=[("MiniLex files", "*.ml"), ("All files", "*.*")],
        )
        if not filepath:
            return
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            self.editor.set_code(content)
            filename = filepath.split("/")[-1].split("\\")[-1]
            self.console.write(f"Archivo cargado: {filename}", "info")
        except FileNotFoundError:
            self.console.write(f"Error: Archivo no encontrado — {filepath}", "error")
        except Exception as exc:
            self.console.write(f"Error al cargar el archivo: {exc}", "error")

    def check_and_compile_lexer(self):
        exe_path = self.compiler.executable_path

        if os.path.exists(exe_path):
            self.executor = LexerExecutor(exe_path)
            self.console.write(f"Lexer encontrado: {exe_path}", "success")
            return

        self.console.write("Verificando dependencias (flex, gcc)...", "info")
        deps_ok, missing = self.compiler.check_dependencies()

        if not deps_ok:
            for tool in missing:
                self.console.write(
                    f"Herramienta faltante: '{tool}'. Instálala y reinicia la aplicación.", "error"
                )
            return

        self.console.write("Compilando lexer (flex + gcc)...", "info")
        success, message = self.compiler.compile()

        if success:
            self.executor = LexerExecutor(exe_path)
            self.console.write(message, "success")
        else:
            self.console.write(f"Error de compilación: {message}", "error")


def main():
    app = MiniLexGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
