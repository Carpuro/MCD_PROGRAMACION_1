Algoritmo Comparacion_De_Dos_Numeros
	// Declaraci�n de variables
	Definir num1, num2 Como Real
	// Entrada de datos
	Escribir 'Introduce el primer n�mero: '
	Leer num1
	Escribir 'Introduce el segundo n�mero: '
	Leer num2
	// Mostrar los valores introducidos
	Escribir 'Primer n�mero: ', num1
	Escribir 'Segundo n�mero: ', num2
	// Comparaci�n de los n�meros
	Si num1=num2 Entonces
		Escribir 'Ambos n�meros son iguales.'
	SiNo
		Si num1<num2 Entonces
			Escribir 'El primer n�mero es menor que el segundo.'
		SiNo
			Escribir 'El primer n�mero es mayor que el segundo.'
		FinSi
	FinSi
FinAlgoritmo
