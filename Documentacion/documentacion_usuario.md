# Documentación de Usuario — Analizador Léxico MiniLex

## Introducción

El **Analizador Léxico MiniLex** es una herramienta académica que toma código fuente escrito en el lenguaje **MiniLex** y produce una lista de **tokens**: las unidades mínimas de significado del lenguaje.
El analizador identifica cada elemento del código (palabras reservadas, variables, números, operadores, etc.) y muestra su tipo, lexema, línea y columna en una tabla interactiva. También resalta en rojo los caracteres no reconocidos directamente en el editor.
Los archivos de código MiniLex usan la extensión **`.ml`**.

---

| Botón | Acción |
|-------|--------|
| **Analizar** | Ejecuta el análisis léxico sobre el código del editor |
| **Limpiar** | Borra el editor, la tabla y la consola |
| **Cargar archivo .ml** | Abre un explorador para seleccionar un archivo `.ml` |

---

### Palabras Reservadas

MiniLex tiene exactamente **11 palabras reservadas**. No se pueden usar como nombres de variables.

| Palabra | Equivalente | Categoría |
|---------|-------------|-----------|
| `entero` | `int` | Tipo de dato |
| `decimal` | `float` | Tipo de dato |
| `texto` | `string` | Tipo de dato |
| `si` | `if` | Control de flujo |
| `sino` | `else` | Control de flujo |
| `mientras` | `while` | Control de flujo |
| `para` | `for` | Control de flujo |
| `retornar` | `return` | Control de flujo |
| `verdad` | `true` | Literal booleano |
| `falso` | `false` | Literal booleano |
| `nulo` | `null` | Literal especial |

---

### Tipos de Datos y Declaración de Variables

#### `entero` — Números enteros

```minilex
entero edad = 25;
entero contador = 0;
entero maximo = 100;
```

#### `decimal` — Números con punto flotante

```minilex
decimal precio = 9.99;
decimal pi = 3.14159;
decimal tasa = 0.15;
```

#### `texto` — Cadenas de caracteres

```minilex
texto nombre = "MiniLex";
texto saludo = "Hola mundo";
texto vacio = "";
```

#### Reasignación de variables

```minilex
edad = 30;
precio = 15.75;
nombre = "MiniLex v2";
```

---

### Literales

#### Literales enteros (`ENTERO`)

Uno o más dígitos sin punto decimal. El signo negativo **no** forma parte del literal; es el operador de resta.

```minilex
0
42
999
100
```

> `minimo = -1;` genera tres tokens: `IDENTIFICADOR(-minimo-)`, `OPERADOR_ASIG(=)`, `OPERADOR_ARIT(-)`, `ENTERO(1)`.

#### Literales decimales (`DECIMAL`)

Dígitos, un punto, más dígitos. Se requieren dígitos en ambos lados del punto.

```minilex
3.14
0.5
100.0
3.14159
```

> `3.` es **inválido** — genera `ENTERO(3)` seguido de `ERROR_LEXICO(.)`.

#### Literales de cadena (`CADENA`)

Texto entre comillas dobles. Soporta secuencias de escape estándar. No admite saltos de línea dentro de la cadena.

| Secuencia | Significado |
|-----------|-------------|
| `\n` | Nueva línea |
| `\t` | Tabulación |
| `\r` | Retorno de carro |
| `\\` | Barra invertida literal |
| `\"` | Comilla doble literal |

```minilex
texto a = "Hola mundo";
texto b = "";
texto c = "Línea1\nLínea2";
texto d = "El dijo \"hola\" ayer";
texto e = "C:\\directorio\\archivo";
texto f = "Col1\tCol2";
```

---

### Operadores

#### Operadores Aritméticos (`OPERADOR_ARIT`)

| Símbolo | Operación | Ejemplo |
|---------|-----------|---------|
| `+` | Suma | `a + b` |
| `-` | Resta | `a - b` |
| `*` | Multiplicación | `a * b` |
| `/` | División | `a / b` |
| `%` | Módulo (resto) | `a % b` |

```minilex
entero suma     = 10 + 5;
entero resta    = 20 - 3;
entero producto = 4 * 7;
entero cociente = 100 / 4;
entero modulo   = 17 % 5;
```

#### Operadores Relacionales (`OPERADOR_REL`)

Comparan dos valores y producen un resultado booleano.

| Símbolo | Significado | Ejemplo |
|---------|-------------|---------|
| `==` | Igual a | `a == b` |
| `!=` | Diferente de | `a != b` |
| `<` | Menor que | `a < b` |
| `>` | Mayor que | `a > b` |
| `<=` | Menor o igual | `a <= b` |
| `>=` | Mayor o igual | `a >= b` |

```minilex
si (edad == 18) { retornar verdad; }
si (nota != 10) { retornar falso; }
si (x < 100)    { x = x + 1; }
si (y > 0)      { y = y - 1; }
si (valor <= 50){ retornar falso; }
si (saldo >= 0) { retornar verdad; }
```

#### Operadores Lógicos (`OPERADOR_LOG`)

| Símbolo | Operación | Descripción |
|---------|-----------|-------------|
| `&&` | AND | Verdadero si **ambas** condiciones son verdaderas |
| `\|\|` | OR | Verdadero si **al menos una** condición es verdadera |
| `!` | NOT | Invierte el valor booleano |

```minilex
si (x > 0 && x < 100)  { retornar verdad; }
si (a == 0 || b == 0)  { producto = 0; }
si (!falso)            { retornar verdad; }
```

#### Operador de Asignación (`OPERADOR_ASIG`)

| Símbolo | Uso |
|---------|-----|
| `=` | Asigna el valor de la derecha a la variable de la izquierda |

```minilex
entero contador = 0;
contador = contador + 1;
```

> `=` es asignación; `==` es comparación. Son tokens distintos.

---

### Delimitadores

Los delimitadores estructuran el código. Todos generan el token `DELIMITADOR`.

| Símbolo | Nombre | Uso |
|---------|--------|-----|
| `(` `)` | Paréntesis | Condiciones, listas de argumentos |
| `{` `}` | Llaves | Bloques de código |
| `[` `]` | Corchetes | Índices de arreglo |
| `;` | Punto y coma | Fin de sentencia |
| `,` | Coma | Separador de argumentos |

```minilex
si (x > 0) {
    numeros[i] = 42;
    func(a, b, c);
}
```

---

### Comentarios

MiniLex soporta únicamente comentarios de **una sola línea**, iniciados con `//`. El analizador los reconoce como tokens `COMENTARIO` (no los descarta).

```minilex
// Comentario al inicio de la línea
entero x = 42; // Comentario al final de la sentencia

// Los comentarios pueden estar en cualquier posición de la línea
// Cada línea necesita su propio //
```

> Los comentarios **sí aparecen** en la tabla de tokens con tipo `COMENTARIO`.

---

### Identificadores

Un identificador es un nombre definido por el programador (variables, funciones, etc.).

**Reglas de formación:**
- Debe comenzar con una **letra** (`a-z`, `A-Z`) o **guión bajo** (`_`)
- El resto puede ser letras, dígitos o guiones bajos
- Distingue mayúsculas y minúsculas

```minilex
// Identificadores válidos
entero miVariable;
decimal _temporal;
texto nombre123;
entero CONSTANTE_MAX;
entero _x1_y2;
```

```minilex
// Identificadores INVÁLIDOS (generan ERROR_LEXICO)
entero 1variable;  // No puede empezar con dígito
entero mi-var;     // Guión no permitido
```

---

### Errores Léxicos

Cualquier carácter no reconocido genera un token `ERROR_LEXICO`. El analizador **no se detiene** — continúa procesando el resto del código y resalta la posición del error en rojo en el editor.

Caracteres que producen error léxico:

| Carácter | Por qué es error |
|----------|-----------------|
| `@` | No pertenece al lenguaje |
| `#` | No pertenece al lenguaje |
| `$` | No pertenece al lenguaje |
| `?` | No pertenece al lenguaje |
| `^` | No pertenece al lenguaje |
| `~` | No pertenece al lenguaje |
| `&` (solo) | Solo `&&` es válido |
| `á`, `ñ`, `€` | Caracteres Unicode no ASCII |

```minilex
entero x = 42;
entero y = x @ 2;       // '@' → ERROR_LEXICO
texto msg = "ok" # 1;   // '#' → ERROR_LEXICO
decimal z = 3.14 $ 1.0; // '$' → ERROR_LEXICO
```

---

## Tipos de Tokens Reconocidos

La tabla completa de tipos de tokens que produce el analizador:

| Tipo de Token | Descripción | Ejemplos de lexemas |
|---------------|-------------|---------------------|
| `PALABRA_RESERVADA` | Palabras con significado fijo | `si`, `entero`, `verdad` |
| `IDENTIFICADOR` | Nombres definidos por el usuario | `contador`, `_temp`, `x1` |
| `ENTERO` | Número sin punto decimal | `0`, `42`, `999` |
| `DECIMAL` | Número con punto decimal | `3.14`, `0.5`, `100.0` |
| `CADENA` | Texto entre comillas dobles | `"Hola"`, `""`, `"a\nb"` |
| `OPERADOR_ARIT` | Cálculo numérico | `+`, `-`, `*`, `/`, `%` |
| `OPERADOR_REL` | Comparación | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| `OPERADOR_ASIG` | Asignación | `=` |
| `OPERADOR_LOG` | Operación booleana | `&&`, `\|\|`, `!` |
| `DELIMITADOR` | Puntuación estructural | `(`, `)`, `{`, `}`, `[`, `]`, `;`, `,` |
| `COMENTARIO` | Texto ignorado por el compilador | `// texto...` |
| `ERROR_LEXICO` | Carácter no reconocido | `@`, `#`, `$` |

---

## Casos de Prueba por Categoría

Esta sección proporciona código listo para copiar en el editor y verificar el comportamiento del analizador.

### Prueba 1 — Declaraciones y Asignaciones Básicas

Verifica el reconocimiento de palabras reservadas de tipo, identificadores, literales y el operador de asignación.

```minilex
entero edad = 25;
entero contador = 0;
decimal precio = 9.99;
decimal pi = 3.14159;
texto nombre = "MiniLex";
texto vacio = "";

edad = 30;
precio = 15.75;
nombre = "MiniLex v2";
```

**Tokens esperados (muestra):**

| Línea | Col | Tipo | Lexema |
|-------|-----|------|--------|
| 1 | 1 | `PALABRA_RESERVADA` | `entero` |
| 1 | 8 | `IDENTIFICADOR` | `edad` |
| 1 | 13 | `OPERADOR_ASIG` | `=` |
| 1 | 15 | `ENTERO` | `25` |
| 1 | 17 | `DELIMITADOR` | `;` |

---

### Prueba 2 — Operadores Aritméticos

Verifica todos los operadores aritméticos y su precedencia léxica.

```minilex
entero a = 10;
entero b = 3;

entero suma     = a + b;
entero resta    = a - b;
entero producto = a * b;
entero cociente = a / b;
entero modulo   = a % b;

decimal x = 5.5;
decimal y = 2.0;
decimal resultado = x + y * 2.0 - 1.0 / y % 3.0;
```

---

### Prueba 3 — Operadores Relacionales

Verifica que los operadores de dos caracteres (`==`, `!=`, `<=`, `>=`) se reconocen correctamente antes que los de un carácter.

```minilex
entero a = 10;
entero b = 3;

si (a == 10) { retornar verdad; }
si (b != 0)  { retornar verdad; }
si (a > b)   { retornar verdad; }
si (b < a)   { retornar verdad; }
si (a >= 10) { retornar verdad; }
si (b <= 3)  { retornar verdad; }
```

---

### Prueba 4 — Operadores Lógicos

Verifica AND, OR y NOT, incluyendo combinaciones.

```minilex
entero p = verdad;
entero q = falso;

si (p && q)   { retornar falso; }
si (p || q)   { retornar verdad; }
si (!q)       { retornar verdad; }
si (!falso)   { retornar verdad; }

si (p && !q || verdad) {
    retornar verdad;
}
```

---

### Prueba 5 — Estructuras de Control

Verifica `si`/`sino`, `mientras` y `para`.

```minilex
entero x = 10;
entero resultado = 0;

si (x > 5) {
    resultado = x * 2;
} sino {
    resultado = x + 1;
}

mientras (x > 0) {
    x = x - 1;
    resultado = resultado + x;
}

para (entero i = 0; i < 5; i = i + 1) {
    resultado = resultado + i;
}

retornar resultado;
```

---

### Prueba 6 — Cadenas y Secuencias de Escape

Verifica todos los tipos de cadenas válidas.

```minilex
texto simple   = "Hola mundo";
texto vacio    = "";
texto escape_n = "Linea1\nLinea2";
texto escape_t = "Columna1\tColumna2";
texto escape_r = "Retorno\r";
texto comillas = "El dijo \"hola\" ayer";
texto ruta     = "C:\\directorio\\archivo";
```

---

### Prueba 7 — Comentarios

Verifica que los comentarios se tokenicen correctamente.

```minilex
// Comentario al inicio del archivo
entero x = 42; // Comentario al final de la línea

// Comentario de bloque (una línea por vez)
// Segunda línea del bloque
// Tercera línea del bloque

decimal y = 3.14; // Operaciones después del comentario
```

---

### Prueba 8 — Errores Léxicos Intencionales

Verifica que los errores se detectan y el análisis continúa.

```minilex
entero x = 42;
entero y = x @ 2;
texto msg = "ok" # invalido;
decimal z = 3.14 $ 1.0;
entero w = 10 ? 5;
```

**Resultado esperado:** Los tokens `@`, `#`, `$` y `?` aparecen con tipo `ERROR_LEXICO` y se resaltan en rojo en el editor. El resto de los tokens se analizan normalmente.

---

### Prueba 9 — Programa Completo (Mixta)

Combina todos los tipos de tokens del lenguaje.

```minilex
// Declaraciones de variables
entero contador = 0;
entero limite   = 100;
decimal promedio = 0.0;
decimal tasa     = 3.14159;
texto saludo     = "Hola, MiniLex!";

// Arreglos y acceso con corchetes
entero numeros[10];
numeros[0] = 42;
numeros[1] = 7;

// Estructura si / sino
si (contador < limite) {
    contador = contador + 1;
} sino {
    retornar falso;
}

// Estructura mientras
mientras (contador != limite) {
    promedio = promedio + tasa;
    contador = contador + 1;
}

// Estructura para
para (entero i = 0; i < 10; i = i + 1) {
    numeros[i] = i * 2;
}

// Operadores logicos combinados
si (verdad && !falso) {
    contador = contador + 1;
}

// Expresion compleja
decimal formula = (tasa * 2.0 + promedio) / (tasa - 1.0);

// Uso de nulo
texto vacio = nulo;

si (promedio > 50.0) {
    retornar verdad;
} sino {
    retornar falso;
}
```

---

## Archivos de Prueba Incluidos

El proyecto incluye cinco archivos `.ml` en la carpeta `tests/` listos para cargar:

| Archivo | Contenido | Propósito |
|---------|-----------|-----------|
| `test_simple.ml` | Variables, estructuras básicas, un error intencional | Prueba rápida inicial |
| `prueba_basica.ml` | Declaraciones de los tres tipos, operaciones aritméticas | Verificar tipos y literales |
| `prueba_expresiones.ml` | Todos los operadores aritméticos, relacionales y lógicos | Verificar operadores |
| `prueba_cadenas.ml` | Cadenas con escapes, comentarios múltiples | Verificar cadenas y comentarios |
| `prueba_mixta.ml` | Programa completo con todos los tokens | Prueba de integración |

Para usarlos: clic en **Cargar archivo .ml** → navegar a la carpeta `tests/` → seleccionar el archivo → clic en **Analizar**.

---

## Cómo Cargar y Analizar un Archivo

**Opción A — Escribir directamente en el editor:**

1. Haz clic en el área del editor
2. Escribe o pega código MiniLex
3. Clic en **Analizar**

**Opción B — Cargar un archivo `.ml`:**

1. Clic en **Cargar archivo .ml**
2. Navega hasta el archivo deseado
3. Selecciona el archivo y confirma
4. Clic en **Analizar**

**Opción C — Limpiar y empezar de nuevo:**

1. Clic en **Limpiar** para borrar el editor, la tabla y la consola
2. Escribe nuevo código o carga otro archivo

---

## Interpretación de Resultados

### Tabla de Tokens

Cada fila de la tabla corresponde a un token reconocido:

| Columna | Descripción |
|---------|-------------|
| **N°** | Número secuencial del token |
| **Línea** | Número de línea en el código fuente |
| **Columna** | Posición de inicio dentro de la línea |
| **Tipo** | Categoría del token (ver tabla de tipos) |
| **Lexema** | El texto exacto del token en el código |

### Indicadores en la Consola

| Mensaje | Significado |
|---------|-------------|
| `Análisis completado — Tokens reconocidos: N, Errores encontrados: 0` | Análisis exitoso sin errores |
| `Análisis completado — Tokens reconocidos: N, Errores encontrados: M` | Análisis completado con M errores léxicos |
| `Lexer no compilado. No se puede ejecutar el análisis.` | Falta compilar el lexer (necesita flex y gcc) |
| `No hay código para analizar` | El editor está vacío |

### Resaltado de Errores

Cuando el análisis encuentra tokens `ERROR_LEXICO`, el analizador resalta en **rojo** la posición exacta del carácter inválido en el editor. El análisis **continúa** después del error y procesa el resto del código normalmente.

---

## Errores Frecuentes y Soluciones

### El botón "Analizar" no hace nada y la consola dice "Lexer no compilado"

**Causa:** El ejecutable del lexer (`build/lexer.exe`) no está compilado.  
**Solución:** Instala `flex` y `gcc` (disponibles con MSYS2 o MinGW en Windows) y reinicia la aplicación. Al iniciar, la app intenta compilar automáticamente.

---

### Un número como `3.` genera un error léxico en el punto

**Causa:** MiniLex requiere dígitos en **ambos lados** del punto decimal.  
**Solución:** Usa `3.0` en lugar de `3.`.

---

### Una palabra reservada aparece como IDENTIFICADOR

**Causa:** Probablemente está escrita con mayúscula inicial. `Entero` es un identificador; `entero` es la palabra reservada.  
**Solución:** Verifica que las palabras reservadas estén en minúsculas.

---

### Una cadena no se cierra y el resto del código aparece mal analizado

**Causa:** Falta la comilla de cierre `"`, o hay un salto de línea dentro de la cadena (no permitido).  
**Solución:** Asegúrate de cerrar cada cadena en la misma línea. Usa `\n` dentro de la cadena para representar un salto de línea.

---

### El operador `&` solo genera un ERROR_LEXICO

**Causa:** En MiniLex, el AND lógico se escribe con **dos** ampersands: `&&`. Un solo `&` no es válido.  
**Solución:** Usa `&&` para AND lógico y `||` para OR lógico.

---

## Referencia Rápida

```
PALABRAS RESERVADAS (11):
  Tipos:    entero   decimal   texto
  Flujo:    si   sino   mientras   para   retornar
  Valores:  verdad   falso   nulo

OPERADORES:
  Aritméticos:   +   -   *   /   %
  Relacionales:  ==   !=   <   >   <=   >=
  Lógicos:       &&   ||   !
  Asignación:    =

DELIMITADORES:    (   )   {   }   [   ]   ;   ,

LITERALES:
  Entero:   solo dígitos           → 42, 0, 999
  Decimal:  dígitos.dígitos        → 3.14, 0.5, 100.0
  Cadena:   "texto con escapes"    → "Hola\nMundo"
  Booleano: verdad  /  falso
  Nulo:     nulo

COMENTARIOS:      // texto hasta fin de línea

IDENTIFICADORES:  [a-zA-Z_][a-zA-Z0-9_]*
  Válidos:   miVar, _temp, x1, CONSTANTE
  Inválidos: 1var, mi-var

ERRORES LÉXICOS:  @ # $ ? ^ ~ & (solo) | (solo)
```

---
