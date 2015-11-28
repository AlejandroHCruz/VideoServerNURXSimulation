# VideoServerNURXSimulation

Métodos cuantitativos
Proyecto de Simulación de Transmisión de Video en la nube
	
Se desea encontrar los parámetros operativos de un sistema de distribución de video que funciona en la nube. En este sistema, un usuario entra en el sistema de la nube y solicita un video particular. El sistema lee los segmentos que conforman el video uno por uno, de forma secuencial en la capa de aplicación. De ahí, utilizando una disciplina de primeras entrada primeras salidas, el sistema envía un cuadro completo de video hasta que llega a la capa de red en donde se dividen los marcos de video en paquetes de un determinado tamaño máximo (MTU). Esto implica que marcos de video de diferentes tamaños se subdividen en paquetes más pequeños para ser cargados en un buffer de salida de tamaño n y después viajar por la red interna de la nube y el internet hasta el usuario final. 

El siguiente diagrama ilustra la situación. Hay un servidor en la nube que atiende a K clientes con archivos de video que pueden o no ser los mismos, pero que son tratados como distintos por el sistema (pues cada uno se sirve a diferente tiempo). Para que los paquetes de red viajen, antes pasan por un buffer el cual tiene un tamaño limitado n (medido en número de paquetes), el cual se comporta como una cola FIFO.  Este además rechaza paquetes entrantes cuando esta esté llena. Los paquetes viajan por un canal de red interna y externa a la nube que tiene error y pérdidas, por colisiones, interferencia, etc. La probabilidad de que un paquete que viaje por ese canal no llegue a su destino es e, el cual es variable y dependiente de la cantidad de clientes k.
 
Las peticiones de video de los clientes llegan a razón de 1/tp. En la capa de aplicación se dividen los marcos de video y se mandan a la capa de red forma round robin sin prioridad a razón de 1/r. Así mismo salen de capa de Red en forma de paquetes de forma FIFO hacia el buffer de transmisión. La comunicación entre cliente y la nube se considera  que es mediante protocolo UDP, por lo que si un paquete no llega al cliente este se considera como perdido, no hay ACK. El ancho de banda del medio es de 4,500 paquetes de red por segundo (es decir 54 Mbps, Wifi). Esto quiere decir que se elimina un paquete de alguno de los buffer cada 222 micro segundos. Adicionalmente se agrega un retraso d que tiene la nube al buscar los marcos de video y el tiempo de red interna de la nube y del internet hasta el usuario final. Este retraso d es variable y depende de la carga de la nube.

Puede darse que exista saturación en el servidor en la nube,  donde  se manden  paquetes desde el servidor de la nube a la capa de red y que estos no puedan ser enviados porque la cola este llena y se pierdan segmentos de marcos de video. La probabilidad de que esto ocurra es G. 
Asimismo, queremos que el retraso total máximo (d + tiempo en cola) sea menor a un tiempo U. Puede ser que la nube o la red tenga tiempos de retraso d muy altos en ese momento y que se exceda el tiempo máximo U.

Lo que se desea saber es lo siguiente:

1.	Dada un cierto tamaño de buffer n=50, 100, 250, 500 (paquetes) y una probabilidad  de error e=.001*k, .01*k , .1*k , ¿cuál es cantidad máxima k de usuarios que se puede atender simultáneamente manteniendo al menos un 90%, 95%, 99% de marcos de video completos entregados a cada cliente con U = 1s?
2.	Si queremos que la probabilidad de saturación G sea menor o igual a .05, .01, .001 y asumiendo k = 5, 10, 15, 20  usuarios respectivamente ¿cuál es el tamaño n (en paquetes) que debe tener el buffer de transmisión?

Algunos parámetros operativos a considerar son los siguientes:

Los paquetes en el buffer de tamano n pueden ser desde 20 hasta MTU bytes
MTU = 1500 bytes
t=222 micro segundos
r = 10 milisegundos
tp= 2 segundos

Los cuadros de video que se pueden utilizar son los que se encuentran en 
http://www-tkn.ee.tu-berlin.de/research/trace/ltvt.html

Los archivos .dat contienen la información del  tamaño del marco de video de toda la secuencia en bytes. Para obtener los tamaños de marco que se envían, utilice la versión terse de los frame traces disponibles. Por ejemplo, el primero de los enlaces de esta película y calidad escogidos (Terse_Jurassic.dat) encontrado en http://www-tkn.ee.tu-berlin.de/research/trace/pics/FrameTrace/mp4/indexaa60.html

Use los archivos .dat de la película que quiera en la calidad que desee. En este caso use el mismo archivo de marcos para cada cliente, aunque cada uno empezara a servir a distinto tiempo. Use 2000 marcos continuos seleccionados de una sección que no sea el inicio de los .dat

Para los tiempos de retraso  d de la nube use los datos de retraso ejemplo (de Amazon) proporcionados por el Profesor. Considere los renglones como el tiempo de retraso de la nube con una resolución en microsegundos. Es decir, renglón 1 es tiempo 0, renglón 2 es el retraso de la nube en el siguiente microsegundo, etc. Las unidades de los retrasos en la hoja de Excel (AmazonS3_delays) están en milisegundos. Es decir que se muestreó el retraso de Amazon casa microsegundo.

Muestre tablas y graficas  de resumen con sus resultados intermedios y responda las preguntas que se plantearon en un reporte.

Entregue el reporte, código fuente y archivos necesarios en un .ZIP

