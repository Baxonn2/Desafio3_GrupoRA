# Desafío 3 GrupoRA: Pandemic Simulator 
## Instrucciones 
---
Requiere python 3 y pygame v1.96.

Al momento de ejecutar el código se puede utilizar el siguiente comando.

    $ python3 main.py -s <seed> -e <entities> -i <infected> -m <masks prob> -in <instance>

El código se puede ejecutar sin argumentos o con cualquiera de los presentados:
- -s --seed: semilla aleatoria para la ejecución. Por defecto 42.
- -e --entities: cantidad de entidades a utilizar. Por defecto 1000.
- -i --infected: cantidad de entidades infectadas. Por defecto 5.
- -m --masks-probability: probabilidad de que una entidad use mascarilla. Por defecto 0.
- -in --instance: ruta a archivo formato .json con valores de parámetros sobre contagios, radios de contagios, recuperación, etc. Por defecto None.
- -q --quarantine: habilita la cuarentena. Por defecto no se encuentra habilitada. 



## Descripción 
---

El programa consiste en representar una pandemia, simulando los contagios en una población en movimiento y en un espacio determinado. Estos, se ven afectados por parámetros que modifican los contagios. Entre ellos tenemos:
- Uso de mascarilla: Reduce la probabilidad de contagios para las personas sanas. Si, la persona se encuentra contagiada, además, se reduce el radio de contagio. 
- Cuarentena: Se envían las entidades contagiadas a cuarentena y de manera aislada, reduciendo a cero el riesgo de contagiar a otros de manera inmediata. 

Además, se encuentran parámetros para modificar valores sobre contagios como:
- Radio de infección (con y sin mascarilla)
- Probabilidad de inmunidad
- Probabilidad de muerte
- Duración de la enfermedad
- Tiempo que tarda en detectar la enfermedad

Y otros, que se encuentran en el documento data.json. Información más detallada en el apartado de Parámetros de contagio. 

La estructura de datos escogida para este desafío es Quadtree. Las ventajas de la estructura Quadtree es que nos permiten chequear colisiones con una parte reducida de la población. A su vez, las entidades chequeadas son las más relevantes, porque son las que se encuentran más cercanas al punto que colisiona.
Si hablamos de complejidad de ejecución, al chequear colisiones sin utilizar quadtree obtenemos una complejidad de (N CUADRADO). Por otro lado, la complejidad de chequear colisiones utilizando quadtree es de (N LOG N). Finalmente, para una población de 1000 entidades, la diferencia es de 1.000.000 a 3.000, es decir, sólo el 0,3% de chequeos son realmente efectivos.


## Estructura 
---

El código presenta 3 grandes clases: El graficador (Grapher), las entidades (Entity) y la población (Population). Se describirán brevemente estas y se mostrarán sus principales variables.

### Grapher
Esta clase se ocupa de mostrar el programa por pantalla y mantenerlo actualizado. 
Maneja la información del algoritmo utilizado, las entidades relativa a los gráficos a mostrar. Sus principales variables son:
- entity_manager: Clase tipo Population.
- algorithm: String indicando el algoritmo a utilizar. Para este caso "quadtree"

### Entity 
Esta clase es la representación de las personas dentro del programa. 
Maneja la ubicación de las personas, junto con información clave relativa a esta. Cabe mencionar, que posee una variable estática de clase, que aumenta con cada instancia generada. Sus principales variables son: 
- person_id: Integer que indica el código asignado a cada entidad, asignado en base a la variable estática de clase. 
- is_infected: Bool que indica que la persona esta infectada o no. 
- is_recovered: Bool que indica si la persona se ha recuperado o no, False por default.
- is_immune: Bool que indica si una persona se ha vuelto inmune, False por default. 
- is_alive: Bool que indica si una persona sigue viva, True por default.
- is_at_quarentine: Bool que indica si la persona se encuentra en cuarentena, False por default.
- has_mask: Bool que indica si la persona utiliza mascarilla.

### Population
Clase que se ocupa de manejar todas las entidades, además de la cuarentena en caso de encontrarse activa. Sus principales variables son: 
- entities: Listado con todas las entidades.
- sick_entities: Diccionario que contiene las entidades presentes en el listado de entidades que estén contagias.
- healthy_entities: Diccionario que contiene las entidades presentes en el listado de entidades que no estén contagias. 
- quarantien_enabled: Bool que indica si la cuarentena esta activa. 

## Parametros de contagio
---

- MASK_FACTOR_SICK: Valor entre 0 y 1, mientras más cercano a cero, menor será la probabilidad de contagiar a otra entidad
- MASK_FACTOR_HEALTHY: Valor entre 0 y 1, mientras más cercano a cero, menor será la probabilidad de ser contagiado
- RECOVERED_FACTOR: Valor entre 0 y 1, indica la probabilidad de recontagio de una persona luego de su periodo de inmunidad

Cuando una enfermedad es mortal, se define su tasa de mortalidad y un factor de modificación a la curva de mortalidad. Esta curva sigue el comportamiento de una curva de agnesi, está alterada de acuerdo a la duración de la enfermedad y el factor de modificación

- DEATH_PROB: valor entre 0 y 1 que representa la tasa de mortalidad de una enfermedad. Importante, aunque tome valor 1, los contagiados pueden sobrevivir si se recuperan en periodos tempranos del contagio.

- DIFF_PROB: Valor numérico, modificador de la curva de mortalidad haciéndola más abierta o cerrada en el centro.

- SICKNESS_DURATION: Valor entero, representa la duración de la enfermedad en iteraciones.

- IMMUNITY_DURATION: Duración del periodo de inmunidad luego de que la entidad se haya recuperado

- IMMUNITY_PROB_AFTER_TIME: Valor entre 0 y 1, representa la probabilidad de extender el periodo de inmunidad adquirida

- INFECT_RADIUS: Valor entero, indica el radio por defecto en el cual una entidad puede infectar a otras
- MASK_RADIUS_INFECTION: Valor entre 0 y 1. Es un factor que reduce el radio de infección cuando la entidad infectada porta mascarilla

- INFECT_PROB: Probabilidad de contagio base de la enfermedad
- IMMUNITY_FAIL: Probabilidad de que la inmunidad de una entidad falle

### Probabilidades de recuperacion
RECOVERY_AFTER_TIME: Probabilidad de superar la infección cuando ha acabado la duración base ésta.
RECOVERY_BEFORE_TIME: Probabilidad de que la entidad supere la infección antes del periodo determinado.

DETECTION_DELAY: Tiempo en el que una entidad es puesta en cuarentena luega de ser contagiada.



## Algoritmo
---
El algoritmo consiste en un ciclo perpetuo en la clase Grapher que mantiene la gráfica corriendo. Al iniciar agrega las entidades a la clase Grapher. Para esto, la clase Population completa su arreglo, diccionarios e indicadores con la información entregada. Luego, comienza con la constante actualización de las ubicaciones de cada entidad. 
Al momento de actualizar la ubicación de cada entidad, se comprueba primero, si esta se encuentra viva y de ser así, se calcula el nuevo movimiento de esta entidad. Junto con esto, se comprueba si continúa enfermo, ha fallecido, se ha recuperado o si ha desarrollado inmunidad. Después, se actualizan los diccionarios de entidades. Finalmente, realiza la búsqueda en el QuadTree, se actualiza la gráfica y se repite el ciclo. 


### QuadTree 

Dentro del Quadtree se guardan todas las entidades que representan a las personas sanas. Para cada entidad contagiada, se hace una consulta al Quadtree con la posición de la entidad contagiada y el radio de contagio. El resultado de la consulta son todas las personas sanas que se encontraban dentro del radio de contagio del infectado.


