import os
import sys
import subprocess
from tkinter import filedialog, ttk

import customtkinter as ctk

from src.gui import CodeEditor, TokenTable, ConsoleOutput
from src.lexer_compiler import LexerCompiler
from src.lexer_executor import LexerExecutor
from src.token_parser import TokenParser
from src.ast_nodes import ASTNode, ProgramaNode
from src.parser_sintatico import SintacticoParser, ParseResult, ErrorSintactico


def _get_base_dir() -> str:
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MiniLexGUI(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("MiniLexAnalyzer")
        self.geometry("1280x900")

        base = _get_base_dir()
        self.compiler = LexerCompiler(os.path.join(base, "src", "lexer.l"), os.path.join(base, "build"))
        self.executor: LexerExecutor | None = None
        self.parser = TokenParser()

        self.create_widgets()
        self.check_and_compile_lexer()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=3)
        ctk.CTkLabel(self, text="Editor de Codigo", font=("Consolas", 12, "bold"), anchor="w").grid(
            row=0, column=0, sticky="nw", padx=10, pady=(10, 0)
        )
        self.editor = CodeEditor(self)
        self.editor.grid(row=0, column=0, sticky="nsew", padx=10, pady=(28, 4))

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

        self.grid_rowconfigure(2, weight=2)
        nb_frame = ctk.CTkFrame(self, fg_color="transparent")
        nb_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(4, 4))
        nb_frame.grid_columnconfigure(0, weight=1)
        nb_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(nb_frame, text="Resultados del Analisis", font=("Consolas", 12, "bold"), anchor="w").grid(
            row=0, column=0, sticky="nw", pady=(4, 0)
        )

        self.notebook = ttk.Notebook(nb_frame)
        self.notebook.grid(row=1, column=0, sticky="nsew")

        tab_tokens = ctk.CTkFrame(self.notebook, fg_color="transparent")
        self.notebook.add(tab_tokens, text="Tokens")
        tab_tokens.grid_columnconfigure(0, weight=1)
        tab_tokens.grid_rowconfigure(0, weight=1)
        self.token_table = TokenTable(tab_tokens)
        self.token_table.grid(row=0, column=0, sticky="nsew")

        tab_ast = ctk.CTkFrame(self.notebook, fg_color="transparent")
        self.notebook.add(tab_ast, text="Arbol Sintactico")
        tab_ast.grid_columnconfigure(0, weight=1)
        tab_ast.grid_rowconfigure(0, weight=1)
        self._crear_ast_treeview(tab_ast)

        tab_errores = ctk.CTkFrame(self.notebook, fg_color="transparent")
        self.notebook.add(tab_errores, text="Errores Sint.")
        tab_errores.grid_columnconfigure(0, weight=1)
        tab_errores.grid_rowconfigure(0, weight=1)
        self._crear_errores_sint_treeview(tab_errores)

        self.grid_rowconfigure(3, weight=1)
        ctk.CTkLabel(self, text="Consola de Estado", font=("Consolas", 12, "bold"), anchor="w").grid(
            row=3, column=0, sticky="nw", padx=10, pady=(4, 0)
        )
        self.console = ConsoleOutput(self)
        self.console.grid(row=3, column=0, sticky="nsew", padx=10, pady=(22, 10))

    def _crear_ast_treeview(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        self.ast_tree = ttk.Treeview(frame, columns=("nodo",), show="tree headings", height=15)
        self.ast_tree.heading("#0", text="Estructura")
        self.ast_tree.heading("nodo", text="Nodo")
        self.ast_tree.column("#0", width=300, stretch=True)
        self.ast_tree.column("nodo", width=250, anchor="w", stretch=True)

        sb_y = ctk.CTkScrollbar(frame, command=self.ast_tree.yview)
        sb_x = ctk.CTkScrollbar(frame, command=self.ast_tree.xview, orientation="horizontal")
        self.ast_tree.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        self.ast_tree.grid(row=0, column=0, sticky="nsew")
        sb_y.grid(row=0, column=1, sticky="ns")
        sb_x.grid(row=1, column=0, sticky="ew")

    def _crear_errores_sint_treeview(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        self.errores_sint_tree = ttk.Treeview(
            frame,
            columns=("num", "linea", "col", "mensaje"),
            show="headings",
            height=15,
        )
        self.errores_sint_tree.heading("num", text="N°")
        self.errores_sint_tree.heading("linea", text="Linea")
        self.errores_sint_tree.heading("col", text="Col")
        self.errores_sint_tree.heading("mensaje", text="Mensaje")

        self.errores_sint_tree.column("num", width=50, anchor="center", stretch=False)
        self.errores_sint_tree.column("linea", width=80, anchor="center", stretch=False)
        self.errores_sint_tree.column("col", width=60, anchor="center", stretch=False)
        self.errores_sint_tree.column("mensaje", width=600, anchor="w", stretch=True)

        self.errores_sint_tree.tag_configure("error_sint", foreground="#FF8C00")
        self.errores_sint_tree.tag_configure("sin_errores", foreground="#4EC9B0")

        sb = ctk.CTkScrollbar(frame, command=self.errores_sint_tree.yview)
        self.errores_sint_tree.configure(yscrollcommand=sb.set)

        self.errores_sint_tree.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")

    def on_analyze(self):
        code = self.editor.get_code()
        if not code or not code.strip():
            self.console.write("No hay codigo para analizar", "error")
            return

        if self.executor is None:
            self.console.write("Lexer no compilado.", "error")
            return

        self.console.write("Iniciando analisis lexico...", "info")

        try:
            success, stdout, stderr = self.executor.execute(code)

            if success:
                tokens = self.parser.parse(stdout)
                self.token_table.display_tokens(tokens)

                error_tokens = [t for t in tokens if t.is_error()]
                self.editor.highlight_errors(error_tokens)

                token_count = len([t for t in tokens if not t.is_error()])
                error_lexico_count = len(error_tokens)

                self.console.write("Ejecutando analisis sintactico...", "info")
                sint_parser = SintacticoParser(tokens)
                parse_result = sint_parser.parsear()
                self._mostrar_resultado_sintatico(parse_result)

                err_lex_str = f"{error_lexico_count} error{'es' if error_lexico_count != 1 else ''}"
                self.console.write(
                    f"LEXICO:      {token_count} tokens | {err_lex_str}",
                    "success" if error_lexico_count == 0 else "info",
                )

                sint_errores = len(parse_result.errores)
                sint_err_str = f"{sint_errores} error{'es' if sint_errores != 1 else ''}"
                sint_estado = "valido" if parse_result.exitoso else "invalido"
                self.console.write(
                    f"SINTACTICO:  {sint_err_str} | programa {sint_estado}",
                    "success" if parse_result.exitoso else "error",
                )
            else:
                self.console.write(stderr or "Error al ejecutar el lexer.", "error")

        except FileNotFoundError as e:
            self.console.write(f"Archivo no encontrado: {e}", "error")
        except subprocess.CalledProcessError as e:
            self.console.write(f"Error al ejecutar el lexer: {e.stderr or str(e)}", "error")
        except Exception as e:
            self.console.write(f"Error: {e}", "error")

    def on_clear(self):
        self.editor.set_code("")
        self.editor.highlight_errors([])
        self.editor.highlight_errors_sint([])
        self.token_table.clear()
        self.ast_tree.delete(*self.ast_tree.get_children())
        self.errores_sint_tree.delete(*self.errores_sint_tree.get_children())
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
            self.console.write(f"Archivo no encontrado: {filepath}", "error")
        except Exception as exc:
            self.console.write(f"Error al cargar: {exc}", "error")

    def _mostrar_resultado_sintatico(self, result: ParseResult) -> None:
        if result.ast is not None:
            self._poblar_ast_treeview(result.ast)
        else:
            self.ast_tree.delete(*self.ast_tree.get_children())
            self.ast_tree.insert("", "end", text="Sin arbol (errores criticos)", values=("",))

        self._poblar_tabla_errores_sint(result.errores)
        self.editor.highlight_errors_sint(result.errores)

        if result.errores:
            self.notebook.select(2)
        else:
            self.notebook.select(1)

    def _poblar_ast_treeview(self, ast: ProgramaNode) -> None:
        self.ast_tree.delete(*self.ast_tree.get_children())

        def insertar_nodo(parent_id, nodo_dict, profundidad):
            etiqueta = nodo_dict.get("etiqueta", "")
            tipo = nodo_dict.get("tipo", "")
            hijos = nodo_dict.get("hijos", [])
            icono = "▶ " if hijos else "• "
            iid = self.ast_tree.insert(
                parent_id, "end",
                text=icono + (etiqueta or tipo),
                values=(tipo,),
                open=(profundidad <= 2),
            )
            for hijo in hijos:
                if hijo is not None:
                    insertar_nodo(iid, hijo, profundidad + 1)

        try:
            insertar_nodo("", ast.to_dict(), 0)
        except Exception:
            self.ast_tree.insert("", "end", text="Error al generar el arbol", values=("",))

    def _poblar_tabla_errores_sint(self, errores: list) -> None:
        self.errores_sint_tree.delete(*self.errores_sint_tree.get_children())

        if not errores:
            self.errores_sint_tree.insert(
                "", "end",
                values=("", "", "", "Sin errores sintacticos"),
                tags=("sin_errores",),
            )
            return

        for i, err in enumerate(errores, start=1):
            self.errores_sint_tree.insert(
                "", "end",
                values=(i, err.line, err.column, err.mensaje),
                tags=("error_sint",),
            )

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
                self.console.write(f"Herramienta faltante: '{tool}'.", "error")
            return

        self.console.write("Compilando lexer...", "info")
        success, message = self.compiler.compile()

        if success:
            self.executor = LexerExecutor(exe_path)
            self.console.write(message, "success")
        else:
            self.console.write(f"Error de compilacion: {message}", "error")


def main():
    app = MiniLexGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
