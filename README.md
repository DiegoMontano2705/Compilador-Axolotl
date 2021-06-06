![Axoltol++](https://github.com/DiegoMontano2705/Compilador-Axolotl/blob/main/axolotl%2B%2B.JPG?rar=true)
# Compilador-Axolotl++
Axolotl++ es un lenguaje de programación hecho en español basado de C++, creado para el manejo de objetos.

# Como ejecutarlo.
unix:
chmod +x run.sh
1. ./run.sh (NombrePrograma)
Sin unix:
1. python3 Axolotl++.py (NombrePrograma).ax
2. python3 MaquinaVirtual.py (NombrePrograma).obj

# Manual de Usuario
Axolotl++ es un lenguaje de programación totalmente en español creado por Diego Montaño y Jose Gonzalez para el proyecto final del curso de Diseño de Compiladores(TC 3048.1) y está dirigido para personas que están empezando a programar y buscan una opción en su lengua materna. Es un lenguaje interpretado originalmente programado en Python, gran parte de sus sintaxis está basada en C. El lenguaje abarca dos paradigmas de programación:
Programación Orientada a Objetos
Programación Estructurada

# Estructura de un programa
En Axolotl++ la primera línea de código que siempre debe estar es la de 
programa <Nombre del Programa> ;  esto es requerido para tener una compilación correcta.

La segunda parte más importante es el bloque donde se tendrá el código principal y está siempre al final del programa, para diferenciar esta con las funciones y clases que soporta el lenguaje es necesario que siempre se empiece con la siguiente palabra tal y como se muestra:  principal() seguido de dos corchetes { } que abren y cierran en los cuales dentro de ellos se escriben los bloques de sentencia a programar.

Otra parte fundamental es el manejo de comentarios los cuales no tienen ningún efecto en el comportamiento del programa y ayudan a los programadores para incluir explicaciones o declaraciones dentro del código fuente. Los comentarios empiezan con los signos %% seguidos del mensaje a escribir.

Para darnos una idea  de como se ve un programa se dejará el siguiente ejemplo:

programa holaMundo;

%% Primer Hola Mundo en Axolotl++
principal() {
    escribe("Hola Mundo");
}

Un programa más complejo puede incluir clases, funciones, declaraciones de variable y sentencias, todos estos se explican a más a detalle en el resto del documento.

Un ejemplo de un programa más completo:


programa test;
clase creando {
    atributos
            entero : a;
            flotante : b;
            entero : c[2];
            flotante : f[4,4];
            flotante : d, e;
    metodos
            entero funcion regresaValores(entero k, flotante h){
                    variables entero : a;
                    a = 8 * 2 + 2;
                    b = 10.5;
            }
};
entero funcion pruebaUno(){
    variables char : hola;
    lee(hola);
    regresa(hola);
}
flotante funcion pruebaDos(char i){
    pruebaUno();
    lee(i);
    escribe("probando codigo", 1+2);
}

variables entero : j, a;
principal() {
    a = 0;
    j = 4;
    y = 3 * 2 / pruebaUno();
    si(j > y) entonces {
            mientras (a < 5) hacer {
            escribe(a);
                    a = a + 1;
            }
    } sino {
            desde j = 1; hasta j == 10; hacer j = j +1; {
                          escribe(j);
            }  
         }
}
                            
# Variables y tipos de datos
Una variable es un espacio en memoria que es reservado para contener valores los cuales pueden ser modificados, estas variables tiene tipos de datos los cuales son asignados cuando se declaran, en este lenguaje los tipos no pueden ser modificados y si reciben valores que no sean de su tipo no serán aceptados. 
Las variables se pueden presentar de dos diferentes maneras dentro de un programa, como variables locales y variables globales.
Las variables locales son definidas en un solo bloque de sentencias y no pueden ser usadas fuera de este.
Mientras que las variables globales se definen fuera de los bloques de sentencias y pueden ser usados en cualquier parte del programa.

Los tipos de datos que se usan en Axolotl++ son muy importantes de comprender pues las operaciones sólo funcionan con variables o datos del mismo tipo pero pueden resolver variables de otros tipos.

En la siguiente tabla se mostrara los tipos de datos que existen y cómo estos se deben declarar en un programa:

Tipo
Declaración
Ejemplo
Int
entero
 A = 10;
Float
flotante
B = 40.234;
Caracter
char
C = ‘c’;
void
void
void prueba()


Para declarar variables en Axolotl++ es importante seguir la siguiente sintaxis, según el contexto en donde se declaren dependerá si las variables son locales o globales.

variables <tipo> : <Nombre de Variables>; 

Es posible declarar más de una variable, para esto es necesario agregar comas entre ellas.
Axolotl++ no permite asignar valores dentro de este contexto, a diferencia de lenguajes más avanzados como C + +, Java, etc. que si lo permiten.
  
# Bloque de sentencias
Las sentencias son los elementos que permiten dar instrucciones al programa de qué hacer, en otras palabras las líneas de código con instrucciones. Estas sentencias vienen acompañadas de expresiones y operaciones que se ejecutan secuencialmente, en caso de que haya un error de sintaxis, lógica o compilación el programa mostrará el respectivo error. Las sentencias  siempre se encuentran dentro de bloques  
Operaciones aritméticas
El lenguaje soporta las operaciones aritméticas básicas: suma (+), resta (-), multiplicación (*)  y división (/). Cuando se hacen operaciones se sigue un orden lógico en el cual las multiplicaciones y divisiones se hacen antes que las sumas y restas. Se pueden agrupar operaciones entre paréntesis dando aún más prioridad, siendo esto lo primero en resolverse.

( operando <operacion> operando ) 

Ejemplos:
5 + 5 → 10
8 - 2 → 6
60 * 10 → 600
20.0 / 2.0 → 10.0
(2 * 4  - 1) + 2 → 9
  
# Operaciones de Comparaciones y Lógicas
Las operaciones de comparación y lógicas permiten determinar si se ha cumplido o no una condición, estas operaciones regresan valores booleanos. Se cuentan con siete operadores que permiten hacer estas operaciones: mayor (>), mayor igual (>=), menor (<), menor igual (<=), es igual (==), diferente (!=), or (|) y and (&). Estos operadores necesitan dos operaciones de cada lado para que funcionen.

operando <operacion> operando
operando <operacion> operando <OR y AND> operando <operacion> operando

Ejemplos:
a == b
c > d
e < f
g <= h
i >= j
k != l
a < b | a > b
b == d & x != z

# Asignación de variables
Para hacer una asignación de variables es necesario que estas estén declaradas de la manera correcta, las variables globales se pueden asignar en cualquier bloque del programa, mientras que las locales solo pueden ser asignadas en el bloque donde se declararon.
La asignación se hace mediante el uso del operador igual (=) y la variable a asignar debe estar del lado izquierdo. A las variables solo se le puede asignar operaciones que cumplan con el tipo de dato con el que fueron declarados, por lo tanto, a una variable entero no se le puede asignar un valor flotante.

variable < = > operando ;

Ejemplos de asignaciones: 
variables entero : a;
variables flotante : b;
variables char : ejemplo;

a = 10 + 5;
b = 5.5 - 3.5;
ejemplo = 'e';
  
# Sentencia IF/Else(Si/Sino)
La sentencia si es lo equivalente a un if en otro lenguajes de programación, el cual ayuda elegir entre diferentes alternativas que puede seguir el programa. Para hacer estas sentencias se requiere un valor o expresión booleana en la cual dependiendo de su resultado se seguirá el camino correcto. Se tiene la siguiente sintaxis para hacer de forma correcta la sentencia:

si (<expresión booleana>) entonces {
    <Bloque y/o sentencias a ejecutar en caso de que se cumpla la expresión dada > 
}

Se puede hacer el uso de la opción sino si se requiere que se siga un camino en caso de que el valor o la expresión booleana sea negativa. No es necesario agregar esta opción para que el programa funcione pero en caso de que se agregue debe estar hecho de la siguiente manera seguido del último corchete.

sino {
    <Bloque y/o sentencias a ejecutar en caso de que no se cumpla la expresión dada > 
}




Ejemplo:

si (a > 1) entonces {
c = a * d;
} sino {
        c = d + a;
}
      
# Sentencia While(Mientras)
La sentencia Mientras implementa un bucle la cual sirve para repetir un bloque de expresiones y/o sentencias cierta cantidad de veces hasta que se cumpla una condición.
Para poder declarar esta sentencia es necesario usar la palabra reservada mientras seguido de un paréntesis que en su interior tendrá la condición.
Cada que termine una iteración del bucle se volverá a revisar si la condición se cumple, en caso de que no la sentencia se dará por terminada y se continuará la siguiente.

mientras ( <condición> ) hacer {
    <Bloque a realizar en caso de que  la condición se cumpla>
}

Ejemplo:

mientras (a < 10) hacer {
    escribe(a);
    a = a +1;
}
                 
# Sentencia For(Desde)
La sentencia Desde es otra implementación de un bucle para repetir un bloque de expresiones y/o sentencias cierta cantidad de veces hasta que se cumpla una condición. En este bucle se tiene más control de cómo se manejan las iteraciones, lo primero que se hace es inicializar una variable con cierto valor, después se hará un condición que dirá hasta cuando terminará el bucle y por último se debe asignar el cómo se irá incrementando/decrementando el valor que se inicializó. Cada que termine una iteración se revisará si la condición se sigue cumpliendo y si se hará el respectivo incremento o decremento puesto para la variable.



desde <asignación a variable> ; hasta <condición> ; hacer <operación> ; {
    <Bloque a realizar en caso de que la condición se cumpla>
}

Ejemplo : 

desde i = 1; hasta i == 10; hacer i = i +1; {
            escribe(i);
 }
      
# Sentencia Escribe/Lee
La sentencias escribe y lee son fundamentales para que el programa pueda tener interacción con el usuario. Son funciones integradas para leer datos ingresados por el usuario y asignarlos a una variable y para mostrar resultados de variables o mensajes puestos por el programador.

Ejemplo de funcionamiento:

lee(<variable>)
lee(a);

Cuando se ejecute el programa y se llegue a esa instrucción, se le pedirá al usuario que teclee el valor correspondiente para ‘a’, en caso de que valor dado no corresponda al tipo de variable que tiene asignado se marcara un error, de lo contrario el programa guardará el dato en memoria para su futuro uso.

escribe(<variable o mensaje>);

Esta instrucción muestra en consola el valor dado entre paréntesis, se pueden mostrar más de un resultado o mensaje siempre y cuando estén separados entre comillas dentro del paréntesis. Esta sentencia no guarda datos al menos que se haga una operación dentro de él pero será mostrada y borrada inmediatamente.

escribe(“Resultado de a :”, a);
      
# Sentencia Regresa
La sentencia regresa solo funciona para salir de una función la cual permite regresar un valor, al hacer esto se regresa el valor al lugar donde se llamó a la función. En Axolotl++ para hacer un regreso con operaciones dentro del paréntesis es requerido poner otro paréntesis entre la operación para que funcione adecuadamente.


Ejemplos:
 regresa(<operación o variable>);
 regresa((10 +5));


# Funciones
Las funciones en Axolotl++ son subrutinas que pueden ser invocadas desde otras partes del código. Son bloques de código que suelen funcionar para hacer operaciones las cuales se usarán múltiples veces y así ya no se tendrán que declarar todas las veces usadas.
Las funciones declaradas deben tener diferentes nombres y pueden regresar datos o no, los tipos de datos a regresar son: entero, flotantes o char. Cuando la función no regresa ningún valor se declaran como ‘void’.

Ejemplo de cómo declarar una función:

<tipo de retorno> funcion <nombre de función>(<parámetros>){
    <Bloque con sentencias/declaraciones>
    <**regresa> 
}

**Solo si el tipo de función es diferente a void

void funcion prueba1() {
    variables entero : a,;
    a = 10;
    escribe(a);
}
entero funcion prueba2(entero x) {
    x =  x + 1;
    regresa(x);
}



# Manejo de Objetos
Axolotl++ es un lenguaje de programación orientado a objetos, para crear objetos es necesario crear una estructura necesaria. Estas estructuras son muy parecidas a un programa completo de Axolotl++ pero son declaradas dentro de la misma. Estas estructuras pueden ser asignadas a una variable del programa original y obtener funciones que solo la estructura maneja pero el programa principal no. Para hacer las estructuras se maneja la palabra reservada clase seguido de un nombre para esta misma, dentro del bloque de la clase se deben declarar los atributos que son las variables que se usarán y los métodos que son las funciones propias que tiene la clase.
Para entender mejor todo esto se dará un ejemplo:

clase <Nombre de clase>{
    atributos
        <Declaración variables>

    metodos
        <Funciones>
};

clase Producto {
    atributos
        enteros: a, b;

    metodos
        entero funcion prueba(){
                regresa(a);
        }
};

Para hacer uso de las clases hechas es necesario declarar variables del tipo de clase.

variables <ID de la funcion> : <variables> ; 

Una vez que se tenga declarada una variable con el tipo de la clase se podrá acceder a los atributos y métodos únicos que ésta tiene. Para acceder a los atributos o asignarles un valor es necesario poner la variable seguida de un punto(.) seguido del atributo al que se quiere acceder. Para los métodos es muy parecido pero en vez de un punto se requiere poner una flecha(->).


Ejemplos:

variables carros : carro1, carro2;

carro1.añoDelModelo = 2010;
carro2.numeroDeAsiento = 4;
carro1->imprimirCaracteristicas();


# Video Demo de como correr un programa Axolotl++
Link: https://drive.google.com/file/d/10m-JskTQ-i_jTmZXD9vHaWgsGPTvfumL/view?usp=sharing
