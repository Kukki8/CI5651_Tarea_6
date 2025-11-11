import numpy as np

## Seccion Arbol de Segmentos ##
class NodoASeg:
    def __init__(self):
        self.valorAnd = True
        self.valorOr = False
        self.tamano = 1
        self.promesa = False
        self.limIzq = -1
        self.limDer = -1

        self.hijoIzq = None
        self.hijoDer = None

class ArbolSegmento:
    def __init__(self, N):
        self.N = N

    def inicializar(self, valoresIniciales):
        self.raiz = self.construir(0, self.N-1 ,valoresIniciales)

    def construir(self, limIzq, limDer, valoresIniciales):
        nodoAS = NodoASeg()
        nodoAS.limIzq = limIzq
        nodoAS.limDer = limDer

        if limIzq == limDer:
            valor = valoresIniciales[limIzq]
            nodoAS.valorAnd = valor
            nodoAS.valorOr = valor
            
            return nodoAS

        mitad = (limIzq + limDer) // 2

        nodoAS.hijoIzq = self.construir(limIzq, mitad, valoresIniciales)
        nodoAS.hijoDer = self.construir(mitad + 1, limDer, valoresIniciales)

        self.actualizarNodo(nodoAS) 
        return nodoAS

    def toggle(self, nodoAS):
        
        # Verificamos que el nodo no sea una hoja
        if nodoAS.limIzq != nodoAS.limDer:
            nodoAS.promesa = not nodoAS.promesa
        
        # Invertir las propiedades resumidas: NOT(AND) = OR, NOT(OR) = AND
        nodoAS.valorAnd = not nodoAS.valorAnd
        nodoAS.valorOr = not nodoAS.valorOr

    def pasarPromesa(self, nodoAS):
        
        if nodoAS.promesa:
            # Reiniciamos promesa del padre
            nodoAS.promesa = False
            
            # Corremos promesa a los hijos
            if nodoAS.hijoIzq:
                self.toggle(nodoAS.hijoIzq)
            
            if nodoAS.hijoDer:
                self.toggle(nodoAS.hijoDer)
            
            
    def actualizarNodo(self, nodoAS):
        
        # Actualizamos valor AND
        nodoAS.valorAnd = nodoAS.hijoIzq.valorAnd and nodoAS.hijoDer.valorAnd
        
        # Actualizamos valor OR
        nodoAS.valorOr = nodoAS.hijoIzq.valorOr or nodoAS.hijoDer.valorOr

    def actualizarRango(self, x, y, nodoAS):

        if x > nodoAS.limDer or y < nodoAS.limIzq:
            return

        if x <= nodoAS.limIzq and nodoAS.limDer <= y:
            self.toggle(nodoAS)
            return

        self.pasarPromesa(nodoAS)

        mitad = (nodoAS.limIzq + nodoAS.limDer) // 2
        self.actualizarRango(x, mitad, nodoAS.hijoIzq)
        self.actualizarRango(mitad + 1, y, nodoAS.hijoDer)
        self.actualizarNodo(nodoAS)

    def consulta(self, x, y, tipoConsulta, nodoAS):
        

        if x > nodoAS.limDer or y < nodoAS.limIzq:
            # Identidad: AND=True, OR=False (neutro para la operación)
            return True if tipoConsulta == 'and' else False 
            
        if x <= nodoAS.limIzq and nodoAS.limDer <= y:

            return nodoAS.valorAnd if tipoConsulta == "and" else nodoAS.valorOr

        self.pasarPromesa(nodoAS)

        mitad = (nodoAS.limIzq + nodoAS.limDer) // 2
        resL = self.consulta(x, mitad, tipoConsulta, nodoAS.hijoIzq)
        resD = self.consulta(mitad + 1, y, tipoConsulta, nodoAS.hijoDer)
        return resL and resD if tipoConsulta == "and" else resL or resD
    
## Seccion HLD ##
class NodoHLD:
    def __init__(self, id):
        self.id = id
        self.vecinos = []       
        self.padre = -1    
        self.profundidad = 0      
        self.tamano = 1 
        self.hijoPesado = -1
        
        self.cabezaCadena = id 
        self.posArreglo = -1 

class HeavyLightDecomposition:
    def __init__(self, N, aristas, predicadosIniciales):
        self.N = N
        self.nodos = [NodoHLD(i) for i in range(N)]
        self.construirAdjacencias(aristas)
        
        self.posAct = 0
        self.predicados = {} 
        
        self.construirPredicados(aristas, predicadosIniciales)
        
        self.asignarHijoPesado(0, -1, 0)
        self.descomponer(0, 0)
        
        # Inicializar el Segment Tree
        self.st = ArbolSegmento(self.N)
        self.inicializarAS()

    def construirAdjacencias(self, aristas):
        for u, v in aristas:
            self.nodos[u].vecinos.append(v)
            self.nodos[v].vecinos.append(u)
            
    def construirPredicados(self, aristas, predicadosIniciales):
        
        for i, (u, v) in enumerate(aristas):
            primero = min(u, v)
            segundo = max(u, v)

            self.predicados[(primero, segundo)] = predicadosIniciales[i]

    # Raíz u, Padre p, Profundidad d
    def asignarHijoPesado(self, u, p, d):
        self.nodos[u].padre = p
        self.nodos[u].profundidad = d
        tamanoMaximo = -1
        
        for v in self.nodos[u].vecinos:
            if v != p:
                self.asignarHijoPesado(v, u, d + 1)
                self.nodos[u].tamano += self.nodos[v].tamano
                
                if self.nodos[v].tamano > tamanoMaximo:
                    tamanoMaximo = self.nodos[v].tamano
                    self.nodos[u].hijoPesado = v
                    
    def descomponer(self, u, cabeza):
        self.nodos[u].cabezaCadena = cabeza
        self.nodos[u].posArreglo = self.posAct
        self.posAct += 1
        # Procesamos hijo pesado
        if self.nodos[u].hijoPesado != -1:
            self.descomponer(self.nodos[u].hijoPesado, cabeza)
            
        # Procesamos aristas livianas
        for v in self.nodos[u].vecinos:
            if v != self.nodos[u].padre and v != self.nodos[u].hijoPesado:
                self.descomponer(v, v)


    def inicializarAS(self):
        valoresIniciales = [False] * self.N 

        for u in range(self.N):
            nodo = self.nodos[u]
            p = nodo.padre
            
            if p != -1: 
                primero = min(u, p)
                segundo = max(u, p)

                predicado = self.predicados.get((primero, segundo))

                if predicado is not None:
                    pos = nodo.posArreglo
                    valoresIniciales[pos] = predicado
 
        self.st.inicializar(valoresIniciales)

    def consultasCamino(self, u, v, tipoConsulta):
        # Elemento neutro
        res = True if tipoConsulta == 'and' else False 
        
        while self.nodos[u].cabezaCadena != self.nodos[v].cabezaCadena:
            
            if self.nodos[self.nodos[u].cabezaCadena].profundidad > self.nodos[self.nodos[v].cabezaCadena].profundidad:
                u, v = v, u
            
            cabeza = self.nodos[v].cabezaCadena
            
            x = self.nodos[cabeza].posArreglo
            y = self.nodos[v].posArreglo
            
            segRes = self.st.consulta(x, y, tipoConsulta, self.st.raiz)
            
            if tipoConsulta == 'and': 
                res = res and segRes

            else: 
                res = res or segRes
            
            v = self.nodos[cabeza].padre

        if self.nodos[u].profundidad > self.nodos[v].profundidad:
            u, v = v, u 

        x = self.nodos[u].posArreglo
        y = self.nodos[v].posArreglo
        
        if x <= y:
            segRes = self.st.consulta(x, y, tipoConsulta, self.st.raiz)
            if tipoConsulta == 'and': 
                res = res and segRes
            else: 
                res = res or segRes
        
        return res

    def forall(self, u, v):
        return self.consultasCamino(u, v, 'and')

    def exists(self, u, v):
        return self.consultasCamino(u, v, 'or')

    def toggle(self, u, v):

        while self.nodos[u].cabezaCadena != self.nodos[v].cabezaCadena:
            if self.nodos[self.nodos[u].cabezaCadena].profundidad < self.nodos[self.nodos[v].cabezaCadena].profundidad:
                u, v = v, u 
        
            cabeza = self.nodos[u].cabezaCadena
            
            x = self.nodos[cabeza].posArreglo
            y = self.nodos[u].posArreglo
            
            self.st.actualizarRango(x, y, self.st.raiz)
            
            u = self.nodos[cabeza].padre

        if self.nodos[u].profundidad > self.nodos[v].profundidad:
            u, v = v, u 
            
        x = self.nodos[self.nodos[u].hijoPesado].posArreglo 
        y = self.nodos[v].posArreglo
        
        self.st.actualizarRango(x, y, self.st.raiz)


        
N = 6
aristas = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5)] 
predicadosIniciales = [True, False, True, True, False] 
hld = HeavyLightDecomposition(N, aristas, predicadosIniciales)

while(True):

    print("FORALL X Y")
    print("EXISTS X Y")
    print("TOGGLE X Y")
    print("SALIR")

    op = input()
    partes = op.split()

    if(op.lower()[0]  == 'f'):

        print(hld.forall(int(partes[1]),int(partes[2])))

    elif(op.lower()[0]  == 'e'):

        print(hld.exists(int(partes[1]),int(partes[2])))

    elif(op.lower()[0] == 't'):
        hld.toggle(int(partes[1]),int(partes[2]))

    elif(op.lower()[0]  == 's'):
        print("Hasta luego!")
        break
