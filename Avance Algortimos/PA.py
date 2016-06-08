import pprint

def mult_matrix(M, N):
    

                                                                                                                                                                                                       
    tuple_N = zip(*N)

    # comprension de la lista anidada para calcular el producto de matrices                                                                                                                                                                                     
    return [[sum(el_m * el_n for el_m, el_n in zip(row_m, col_n)) for col_n in tuple_N] for row_m in M]

def pivot_matrix(M):
    """Returna el pivote de la matriz  M"""
    m = len(M)

    # Crear una  matriz, identica con  valores flotantes                                                                                                                                                                                            
    id_mat = [[float(i ==j) for i in xrange(m)] for j in xrange(m)]

    # Reordenar la matriz identidad de manera que el elemento mas grande de cada columna
    # de M se coloque en la diagonal de M                                                                                                                                                                                            
    for j in xrange(m):
        row = max(xrange(j, m), key=lambda i: abs(M[i][j]))
        if j != row:
            # intercambiar filas                                                                                                                                                                                                                            
            id_mat[j], id_mat[row] = id_mat[row], id_mat[j]

    return id_mat

def lu_decomposition(A):
    """Hacer Decomposicion LU de A (debe ser cuadrada)                                                                                                                                                                                        
     PA = LU. la funcion retorna P, L y U."""
    n = len(A)

    # crear matrices nulas para L y U                                                                                                                                                                                                                 
    L = [[0.0] * n for i in xrange(n)]
    U = [[0.0] * n for i in xrange(n)]

    # Crear el pivote de la matriz P y el producto de PA                                                                                                                                                                                         
    P = pivot_matrix(A)
    PA = mult_matrix(P, A)

    # Descomposicion  LU                                                                                                                                                                                                                    
    for j in xrange(n):
        # todas las  diagonales de L son unidad                                                                                                                                                                                                   
        L[j][j] = 1.0

        # LaTeX: u_{ij} = a_{ij} - \sum_{k=1}^{i-1} u_{kj} l_{ik}                                                                                                                                                                                      
        for i in xrange(j+1):
            s1 = sum(U[k][j] * L[i][k] for k in xrange(i))
            U[i][j] = PA[i][j] - s1

        # LaTeX: l_{ij} = \frac{1}{u_{jj}} (a_{ij} - \sum_{k=1}^{j-1} u_{kj} l_{ik} )                                                                                                                                                                  
        for i in xrange(j, n):
            s2 = sum(U[k][j] * L[i][k] for k in xrange(j))
            L[i][j] = (PA[i][j] - s2) / U[j][j]

    return (P, L, U)


A = [[7, 3, -1, 2], [3, 8, 1, -4], [-1, 1, 4, -1], [2, -4, -1, 6]]
P, L, U = lu_decomposition(A)

print "A:"
pprint.pprint(A)

print "P:"
pprint.pprint(P)

print "L:"
pprint.pprint(L)

print "U:"
pprint.pprint(U)
