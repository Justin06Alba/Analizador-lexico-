import customtkinter as ctk


class CodeEditor(ctk.CTkFrame):
    """Editor de código con números de línea y resaltado de errores léxicos."""

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="transparent")

        # Columna de números de línea (solo lectura)
        self.line_numbers = ctk.CTkTextbox(
            self, width=40, font=("Consolas", 11),
            wrap="none", state="disabled", activate_scrollbars=False
        )
        self.line_numbers.pack(side="left", fill="y", padx=(0, 2))

        # Área de edición de código
        self.code_text = ctk.CTkTextbox(self, font=("Consolas", 11), wrap="none")
        self.code_text.pack(side="left", fill="both", expand=True)

        self._configure_error_tag()

        self.code_text.bind("<KeyRelease>", self._on_text_change)
        self.code_text.bind("<MouseWheel>", self._on_scroll)
        self.code_text.bind("<Button-1>", self._on_text_change)

        self.update_line_numbers()

    def _configure_error_tag(self):
        try:
            if hasattr(self.code_text, '_textbox'):
                self.code_text._textbox.tag_config(
                    "error", foreground="red", font=("Consolas", 11, "bold")
                )
        except Exception:
            pass

    def get_code(self) -> str:
        return self.code_text.get("1.0", "end-1c")

    def set_code(self, code: str):
        self.code_text.delete("1.0", "end")
        self.code_text.insert("1.0", code)
        self.update_line_numbers()

    def update_line_numbers(self):
        line_count = int(self.code_text.index("end-1c").split('.')[0])
        line_numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.configure(state="disabled")

    def highlight_errors(self, error_tokens):
        try:
            if not hasattr(self.code_text, '_textbox'):
                return
            text_widget = self.code_text._textbox
        except Exception:
            return

        text_widget.tag_remove("error", "1.0", "end")
        text_widget.tag_config("error", foreground="red", font=("Consolas", 11, "bold"))

        for token in error_tokens:
            start_pos = f"{token.line}.{token.column}"
            end_pos = f"{token.line}.{token.column + len(token.lexeme)}"
            text_widget.tag_add("error", start_pos, end_pos)

    def _on_text_change(self, event=None):
        self.update_line_numbers()

    def _on_scroll(self, event=None):
        self.update_line_numbers()
