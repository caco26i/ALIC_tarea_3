# Metodo de Gauss-Seidel

 
# NOTA: Para garantizar la convergencia del Metodo de Gauss-Seidel
#       hay que verificar que la matriz del sistema de ecuaciones
#       sea una matriz de diagonal estrictamente dominante.
#       Este codigo funciona para sistemas de ecuaciones
#       de tres ecuaciones por tres variables.
 
def Xval(a1, b1, c1, d1, y, z):  #
    x = (-(b1*y)-(c1*z)+d1)/a1   #
    return x                     #
                                 #
def Yval(a2, b2, c2, d2, x, z):  # Formulas para recursividad
    y = (-(a2*x)-(c2*z)+d2)/b2   #
    return y                     #
                                 #
def Zval(a3, b3, c3, d3, x, y):  #
    z = (-(a3*x)-(b3*y)+d3)/c3   #
    return z
 
def main():
    vals = [[0.0,0.0,0.0],[1.0,1.0,1.0]]
    cons = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]\
 
    print "\n\tMETODO DE GAUSS-SEIDEL\n\nA1x + B1y + C1z = D1\n\
A2x + B2y + C2z = D2\nA3x + B3y + C3z = D3\n\n"\
 
    for i in range(3):
        print " ** FILA NUMERO",i+1,"**"
        for j in range(4):
            print "Dato [",i+1,",",j+1,"] de Matriz"
            cons[i][j] = float(input("INGRESE DATO > "))
            j = j+1
        i = i+1
        print "\n"\
 
    while vals[0] != vals[1]:
        print vals[1]
        vals[0][0] = Xval(cons[0][0], cons[0][1], cons[0][2], cons[0][3],\
vals[1][1], vals[1][2])
        vals[0][1] = Yval(cons[1][0], cons[1][1], cons[1][2], cons[1][3],\
vals[0][0], vals[1][2])
        vals[0][2] = Zval(cons[2][0], cons[2][1], cons[2][2], cons[2][3],\
vals[0][0], vals[0][1])
        print vals[0]
        vals[1][0] = Xval(cons[0][0], cons[0][1], cons[0][2], cons[0][3],\
vals[0][1], vals[0][2])
        vals[1][1] = Yval(cons[1][0], cons[1][1], cons[1][2], cons[1][3],\
vals[1][0], vals[0][2])
        vals[1][2] = Zval(cons[2][0], cons[2][1], cons[2][2], cons[2][3],\
vals[1][1], vals[1][2])\
 
    raw_input("\n\nMetodo de Gauss-Seidel terminado...")
 
main()
