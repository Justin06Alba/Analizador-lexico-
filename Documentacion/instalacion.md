Instalacion:

##Paso 1 — Instalar dependencias Python

pip install -r requirements.txt
Instala customtkinter, pytest, hypothesis.

##Paso 2 — Compilar el lexer (flex → C → exe)
ejecutar en la carpeta 
flex -o build/lex.yy.c src/lexer.l
gcc build/lex.yy.c -o build/lexer.exe

Genera el analizador léxico ejecutable.

##Paso 3 — Empaquetar en .exe

pyinstaller MiniLexAnalyzer.spec --noconfirm

Esto genera en dist un .exe para poder ejecutar el analizador