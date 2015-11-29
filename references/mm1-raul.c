//rutinas de manejo de eventos en una cola de eventos

/*Codigo esquelo para crear un simulador M/M/1
!
Dr. Raul V. Rami≠rez-Velarde
Marzo 2009

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

//struct structUser {
//	int userId;	/*Numero de usuario*/
//	float tiempo;	/*Tiempo de entrada en el sistema*/
//	unsigned short int active;/*Indica si se debe de dar servicio al usuario*/
//} ;


struct structEvent {
    int user;
	float tiempo;	/*Tiempo en que ocurrio el evento*/
	int etype;	/*1=Salida de cuadro de buffer, 2=inicio lectura de cuadro
			   3=fin lectura de cuadro,4=Llegada de nuevo usuario
			   5=Inicio servicio nuevo usuario, 6=Buffer lleno, 7=Buffer vac√≠o*/
};

#define	LLEGACLIENTE	1
#define	TERMINACLIENTE	2


//struct structUser user[50];/*Lista de usuarios*/

/*Variables de definicion de lista de eventos*/
int head;	/*Los eventos entran por el head*/
int tail;	/*Los eventos a procesar son apuntados por tail*/
		/*Sin embargo, primero se encuentra el evento con el
		  el tiempo menor y se intercambia por el apuntado 
		  por tail*/

#define maxcola		50

float T,TMax; 	/*Tiempo maestro*/
long int NumUsers;
long int ClientesenSistema;

/*FUNCIONES PARA EL MANEJO DE VARIABLES ALEATORIAS*/
#define A	16807.0		/*Modulo*/
#define M	2147483647.0	/*Multiplicador*/


double r_seed=1.0;

struct structEvent ev[maxcola]; /*Lista circular de eventos a procesar*/

float T;
float a=5; /* Razon del tiempo entre llegadas*/
float b=6;   /*Razon del tiempo de servicio*/



/*Genera una variable aleatoria uniforma entre 1 y 0*/
double rnd() {
	r_seed=fmod(A*r_seed,M);
	return (r_seed*4.656612875e-10);
}

/*Genera una variable aleatoria exponencial con media 1/a*/
double expo(double a) {
	return(-log(rnd())/a);
}

/*Genera una variable aleatoria uniforme discreta entre i y j*/
int unifd(int i, int j) {
	j=(j-i+1)*rnd();
	return (i+j);
}

/*FUNCIONES PARA EL MANEJO DE LA COLA DE EVENTOS*/

/*Adelanta los apuntadores head y tail*/
void adelanta(int *p) {
	*p=(*p+1) % maxcola;
} 

/*Elimina un evento de la cola. Primero toma el evento al final de
la cola y lo cola en la posicion a eliminar. Despues se adelanta
el apuntador de cola para eliminar esa posicion*/

void QuitaEvento(int eventobye) {
	if (tail!=head) {
		ev[eventobye]=ev[tail];
		adelanta(&tail);
	} else {
		printf("La cola esta vacia!!!",T);
	}
}

/*Encuentra el evento con el minimo tiempo*/
/*La funcion regresa -1 si la cola esta vacia*/

int EventoTpoMin() {
	float min;
	int pos,posmin;
	pos=tail;
	if (head!=tail) {
		min=ev[pos].tiempo;
		posmin=pos;	
		adelanta(&pos);
		while (pos!=head) {
			if (ev[pos].tiempo<min) {
				posmin=pos;
				min=ev[pos].tiempo;
			}
			adelanta(&pos);
		}
	} else {
		posmin=-1;
		printf("Cola vacia, no hay evento minimo!",T);
	}
	return (posmin);
}

/*Inserta un evento en la cola de eventos
   regresa -1 si la cola esta llena*/

int InsertaEvento(float t, int etype, int user) {
	if ((head+1)%maxcola!=tail) {
		ev[head].tiempo=t;
		ev[head].etype=etype;
		ev[head].user=user;
		adelanta(&head);
		return (0);
	} else {
		printf("La cola esta llena!!",T);
		return (-1);
	}
}



/*Funciona maestra de procesamiento de eventos*/
void ProcessEvent(struct structEvent this) {
float BlockSize,BlockTime,FrameOutSize;
	switch (this.etype) {
	case (LLEGACLIENTE): 
         ClientesenSistema++;
         printf("Llegada de cliente en %f Clientes en Sistema %i\n",this.tiempo,ClientesenSistema);
         InsertaEvento(T+expo(a),LLEGACLIENTE,NumUsers++);
         if (ClientesenSistema==1)
            InsertaEvento(T+expo(b),TERMINACLIENTE,this.user);
		break;
	case (TERMINACLIENTE):
         ClientesenSistema--;
         printf("Termina cliente %i en %f Clientes en Sistema %i\n",this.user,this.tiempo,ClientesenSistema);
         if (ClientesenSistema>0)
            InsertaEvento(T+expo(b),TERMINACLIENTE,this.user);
		break;
    }

}

/*Inicializacion de eventos*/
void EventInit() {
	head=0;
	tail=0;
	T=0;
	InsertaEvento(expo(a),LLEGACLIENTE,0);
}



void Init() {
FILE * seed;
	if ((seed=fopen("seed.txt","ra"))==NULL) { 
		r_seed=1.0;		
		printf("No se abrio el archivo de semilla\n");
	} else {
		if (fscanf(seed,"%lf",&r_seed)!=1) {
			printf("No se leyo la semilla\n");
			r_seed=1.0;
		} else {
			printf("Nueva semilla es %lf\n",r_seed);
		}
		fclose(seed);
	}
}

void Bye() {
FILE * seed;
int i;
	if ((seed=fopen("seed.txt","wa"))==NULL) { 
		printf("No se abrio el archivo de semilla para cerrar\n");
	} else {
		fprintf(seed,"%lf\n",r_seed);
		fclose(seed);
	}
}


main () {
int newEventId;
struct structEvent new;
TMax=1000;
NumUsers=0;
ClientesenSistema=0;

//while (algo) {

		Init();

		EventInit();
		while (T<TMax) {

			newEventId=EventoTpoMin();
			new=ev[newEventId];

			QuitaEvento(newEventId);
			T=new.tiempo;
			ProcessEvent(new);

		}
		Bye();
		
		printf("\nresultados");
		getch();
//}

}
