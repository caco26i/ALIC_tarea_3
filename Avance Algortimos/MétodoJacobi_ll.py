from __future__ import division                

import sys                                     

class InvalidSizeError(Exception):
  """Excepcion en caso que las matrices tengan un tamnio no adecuado"""
  pass

def printM(m):                                 
  
  for j in m:
    for elem in j:
      print "%3d" % elem, 
    print ""
  print ""

def readM():                                   
  
   matriz = []                                 
   lastsize = 0                                ## Guarda  tamanio de la ultima fila leida 
                                               

   print ">> Ingrese MATRIZ:  (fila  en blanco para terminar):"
   while 1:
      r = sys.stdin.readline()                 
      if r.strip():                            
        l = r.split()                         
                                               ##.. '1 2   32 1 2' --> ['1', '2', '32', '1', '2']
        s = len(l)                             
        if lastsize and  s != lastsize:        
          raise InvalidSizeError, "As linhas devem ter todas o mesmo numero de colunas." 
        matriz.append([float(elem) for elem in l]) ## Convierte los elementos de la fila a enteros
                                                 ##.. e coloca la matriz
        lastsize = s                           
      else:
        break                     
   return matriz                  


##### Inicio de la funcion que aplica los metodos  ######

def jacobi_reg(mat, Error, MaX): 
  columnas = 0
  numIT = 1                  
  switchh = False  

##### Aplica  metodo Gauss-Jacobi ######

  filas = len(mat)                              
  for C in mat[0]:
    columnas += 1                                 

  print ">> Dimension de la Matriz: [%d][%d]\n" %(filas, columnas)  ## Imprime numero de filas x columnas
  if ((columnas - filas) != 1):
    print ">> *** Existen mas filas  que columnas ***\n"
    sys.exit(1)

  ###### Primer iteracion ######
  B = list(zip(*mat)[-1])                        ## B[] Vector que guarda la ultima columna de la matriz
  X0 = [B[i]/mat[i][i] for i in xrange(filas)]  ## Guarda  resultado de X[i]= b1/a11 , X[i]=b2/a22 etc..
  X1 = list(X0)                                  ## X1(actual) = X0(anterior)

  ###### Segunda iteracion ######
  numIT += 1                  
  while not switchh:
    sup = 0
    div = 0

    for i in xrange(filas):
      X1[i] = B[i]
      for j in xrange(columnas-1):
        if ( i != j):
          X1[i]=  (X1[i] - (mat[i][j] * X0[j]))
      X1[i] =  (1/mat[i][i] * X1[i])
      aux = X1[i] - X0[i]
      if (aux < 0) :
        aux = aux * -1
      aux2 = X1[i]
      if (aux2 < 0):
        aux2 = aux2 * -1
      if (aux > sup):
        sup = aux
      if (aux2 > div):
        div = aux2
    X0 = list(X1)
    if (sup / div) <= Error:
      switchh = True 
      numIT += 1
    if int(numIT) > int(MaX):
      print ">> **Imposible** encontrar resultado en %s *iteraciones*.\n" % MaX   
      sys.exit(0)
 
  printM(mat)                                       
  my_cont = 0
  print "*** GauSS-JaCoBi ***"
  for i in X0:                                     ## Imprime  X, resultados de gauss-jacobi
    print "X%d = %f" % ((my_cont+1), i)
    my_cont += 1
  print "\n>> Numero de iteraciones: %d " % numIT
  print ">> Valor do error: %s" % Error

####### Fin de Gauss-Jacobi #########
#

  

  for a in xrange(1, filas):                      ## Checar a a triangular inferior  
    for b in xrange(0, columnas):                 
      if (int(a) != int(b)):
        if (int(mat[a][b]) != 0):
          print ">> **Imposible** calcular  triangular inferior * debe ser diferente de 0*\n" 
          sys.exit(0)
      elif (int(a) == int(b)):
          break
        
  switchh = False
  i = filas-1
  j = i 
  B[j] = B[j] / mat[i][j]
  i -= 1
  j = i
  t = 0
  numIT = 1
  columnas -= 1

  while not (switchh):
    div = 0
    numIT += 1
    for t in xrange(j+1, columnas):
      div = div + (mat[i][t] * B[t])
    B[j] = (B[j] - div) / mat[i][j]
    if int(i) == 0:
      switchh = True
    i -= 1
    j = i

  my_cont = 0
  for i in B:                                 ## Imprime B, vetor que guarda resultados retornados
    print "B%d = %f" % ((my_cont+1), i)
    my_cont += 1





def main():
  error = raw_input("\n>> Defina el margen de error: ")               
  maxx = raw_input(">> MAX iteraciones: ")                

  if int(maxx) <= 0:
    print "\n>> *** Maximo de iteraciones debe ser > 0 ***\n"
    sys.exit(0)

                       

  matriz = readM()
  

   
  #matriz = [1, 0, 0, 0, 2], [0, 4, 0, 0, 15], [0, 0, 10, 0, 10], [0, 0, 0, 1, 1]
  matriz = [1, 0, 0, 2], [0, 5, 0, 15], [0, 0, 10, 10]

  print "\n************************************************"
  jacobi_reg(matriz, error, maxx)                      
  print "\n-=*********************************************=-"
 
if __name__ == '__main__':
  main()
