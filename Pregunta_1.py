import random

class Nodo:
    def __init__(self, llave, prioridad, valor):
        self.llave = llave
        self.prioridad = prioridad
        self.valor = valor

        self.izq = None
        self.der = None

        self.tamano = 1

    def actualizarTamano(self):

        izqTam = self.izq.tamano if self.izq else 0
        derTam = self.der.tamano if self.der else 0

        self.tamano = izqTam + derTam + 1
    
class Treap:

    def __init__(self, valores):
        self.valores = valores
        self.raiz = None

        for index, n in enumerate(valores):

            n = Nodo(index + 1, random.randint(1, 1000), n)

            self.raiz = self.mezclar(self.raiz, n)

    def imprimir_treap(self):
        
        def _recorrido_in_order(nodo):

            if nodo is None:
                return []
        
            arr = _recorrido_in_order(nodo.izq)
            
            arr.append(nodo.valor) 
            
            arr.extend(_recorrido_in_order(nodo.der))
            
            return arr
            
        final_array = _recorrido_in_order(self.raiz)
        print("Arreglo resultante (Treap In-Order):", final_array)
        return final_array


    def mezclar(self, treapL, treapR):

        if treapL is None:
            return treapR
        
        if treapR is None:
            return treapL

        if treapL.prioridad < treapR.prioridad:
            treapL.der = self.mezclar(treapL.der, treapR)
            treapL.actualizarTamano()
            return treapL

        else:
            treapR.izq = self.mezclar(treapL, treapR.izq)
            treapR.actualizarTamano()
            return treapR


    def dividir(self, raiz, llaveX):
        
        if not raiz:
            return (None, None)

        if raiz.llave > llaveX:
            L, R = self.dividir(raiz.izq, llaveX)
            raiz.izq = R
            raiz.actualizarTamano()
            return (L, raiz)
        else:
            L, R = self.dividir(raiz.der, llaveX)
            raiz.der = L
            raiz.actualizarTamano()
            return (raiz, R)
        
    def multiswap(self, posA, posB):

        if self.raiz is None:
            return

        N = self.raiz.tamano
        
        # k sera el maximo de swaps que tendremos que ejecutar 
        k = min(posB - posA, N - posB)
        
        if k <= 0:
            return 

        #Vamos a segmentar nuestro Trea en 5 pedazos
        # Segmento 1
        treaInicial = self.raiz
        tPreA, tResto = self.dividir(treaInicial, posA - 1)
        
        # Segmento 2
        S1, tRestoMed = self.dividir(tResto, posA + k - 1)
        
        # Segmento 3
        T_mid, tResto_suf = self.dividir(tRestoMed, posB - posA + k - 1)
        
        # Segmento 4
        S2, tFinal = self.dividir(tResto_suf, posB + k - 1)
        
        # Mezclaremos en el nuevo orden
        tTemp1 = self.mezclar(T_mid, S1)
        
        tTemp2 = self.mezclar(S2, tTemp1)
        
        tTemp3 = self.mezclar(tPreA, tTemp2)
        
        self.raiz = self.mezclar(tTemp3, tFinal)

# Ejemplo de prueba
A = [8,7,3,4,2,1,9]
t = Treap(A)
t.multiswap(2,5)

t.imprimir_treap()
