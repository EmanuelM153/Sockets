# Programación Concurrente: Sockets
En este repositorio se evaluan tres códigos que utilizan tres diferentes enfoques (hilos, multiprocesos, multiplexación) para lograr concurrencia en un servidor con sockets. Para ello, cada línea se argumenta a través de comentarios en el código, y en las secciones siguientes, se define de forma general que proceso hace cada código y las ventajas y desventajas de este enfoque en la programación concurrente.

## Hilos
### Visión general
En un bucle infinito:
1. Se recibe una conexión en el puerto 8080
2. Se crea un nuevo socket para la conexión
3. Se crea un nuevo hilo
4. Desde el nuevo hilo:
    1. Se reciben datos
    2. Se imprimen los datos
    3. Se envía un mensaje al cliente 
    4. Se cierra la comunicación

### Ventajas
* Menor consumo de recursos: Los hilos son ligeros en términos de memoria y recursos en comparación con procesos completos, ya que comparten el mismo espacio de memoria.
* Comunicación rápida: Dado que los hilos comparten la misma memoria, la comunicación entre ellos es rápida y eficiente.
* Adecuado para tareas de E/S: Los hilos pueden realizar operaciones de E/S sin bloquear el programa completo, permitiendo que otras tareas continúen ejecutándose en paralelo.

### Desventajas
* Problemas de seguridad y sincronización: Como los hilos comparten memoria, es necesario sincronizar el acceso a los datos compartidos, lo que puede generar condiciones de carrera y errores difíciles de depurar.
* Dependencia del GIL en Python: En Python, el Global Interpreter Lock (GIL) limita la ejecución de hilos en múltiples núcleos, afectando el rendimiento en tareas de CPU intensivas.
* Posibilidad de bloqueos: Sin una correcta gestión, los hilos pueden bloquearse o causar deadlocks.


## Multiprocesos
### Visión general
En un bucle infinito:
1. Se recibe una conexión en el puerto 8080
2. Se crea un nuevo socket para la conexión
3. Se crea un nuevo proceso
4. Desde el nuevo proceso:
    1. Se reciben datos
    2. Se imprimen los datos
    3. Se envía un mensaje al cliente 
    4. Se cierra la comunicación

### Ventajas
* Aprovecha múltiples núcleos: Cada proceso puede ejecutarse en un núcleo diferente, maximizando el uso de CPU en tareas intensivas.
* Mayor estabilidad: Al tener su propio espacio de memoria, un proceso no afecta directamente a los otros, reduciendo la posibilidad de errores de sincronización y aumentando la estabilidad.
* Evita el GIL en Python: Como cada proceso tiene su propio intérprete de Python, el multiprocesamiento evita la limitación del GIL.

### Desventajas
* Mayor consumo de recursos: Los procesos son más pesados en términos de memoria y recursos, ya que cada uno tiene su propio espacio de memoria y contexto.
* Comunicación más lenta: La comunicación entre procesos es más lenta que entre hilos, ya que se debe realizar mediante mecanismos como colas o pipes, que implican copiar datos.
* Mayor tiempo de creación: Crear y destruir procesos es más costoso en términos de tiempo comparado con los hilos.


## Multiplexación
### Visión general
En un bucle infinito:
1. Se inicializa una lista de sockets
2. Se recibe una o más conexiones en el puerto 8080
3. Se itera por cada conexión en la lista
4. Por cada conexión:
    1. Se crea un nuevo socket para cada conexión
    2. Se agregar el socket a la lista
    3. Si hay datos
        1. Se reciben datos
        2. Se imprimen los datos
        3. Se envía un mensaje al cliente
    4. Si no hay datos
        1. Se cierra la comunicación
        2. Se elimina el socket de la lista

### Ventajas
* Alta eficiencia para E/S intensiva: Es ideal para aplicaciones de red o de archivo que realizan muchas operaciones de E/S, como servidores, ya que permite que la CPU procese otras tareas mientras espera la E/S.
* Menor consumo de recursos: No requiere múltiples hilos o procesos, lo que minimiza el uso de memoria y la sobrecarga de sincronización.
* Escalabilidad: La multiplexación de E/S es eficiente para manejar muchas conexiones simultáneamente (por ejemplo, en servidores HTTP) sin saturar los recursos del sistema.

### Desventajas
* Complejidad en la programación: Manejar E/S no bloqueante puede ser más complicado y menos intuitivo, especialmente para desarrolladores nuevos en concurrencia.
* Menor rendimiento en tareas de CPU intensiva: Este enfoque es adecuado principalmente para E/S; no mejora el rendimiento de tareas que requieren mucha CPU.
* Compatibilidad limitada en algunos lenguajes: Algunos lenguajes y entornos pueden no ofrecer soporte completo para E/S no bloqueante, limitando su uso.
