#!/usr/bin/env python
import subprocess
import sys


if __name__ == '__main__':
   
    action = ""

    # Recoge el primer argumento
    if ( len(sys.argv) > 1 ):
        # recoge el primer parametro que le pasamos al script
        action = sys.argv[1]

    # Si la acción es get
    if (action == "get"):

        # Mira que el segundo argumento exista 
        # ->Si no termina el programa y devuelve "Debe introducir el nombre de la cartera"
        if ( len(sys.argv) > 2 ):
            # recoge el segundo parámetro que le pasamos al script (Nombre de la cartera)
            walletName = sys.argv[2]
        else:
            print("\n\tDebe introducir el nombre de la cartera")
            exit()

        # Mira si el dispositivo esta autorizado (0: autorizado, 1: no autorizado, 2: no se ha emparejado)
        authorized = subprocess.call("autorizacion.py", shell=True) 
        
        # Si no está emparejado terminamos el programa
        if (authorized == 2):
            print("\n\tDebe estar emparejado para para poder usar el comando \"get <nombre_cartera>\" ")
            print("\n\tPara emparejarse use el comando \"set <llave_privada> <nombre_cartera>\" ")
            exit()

        # No esta autorizado
        if (authorized == 1):
            # Terminamos el programa
            print("\n\tLo sentimos. Debe estar autorizado. ")
            exit()
       
        # Esta autorizado
        if (authorized == 0):
   
            # Mira si se ha creado un archivo de texto con el nombre de la cartera
            # -> Si no para el programa y devuelve "No existe ninguna cartera con ese nombre"
            try:
                open("./BBDD_wallets/" + walletName + '.bin', 'rb')
            except:
                print(f"\n\tNo existe ninguna cartera con el nombre: {walletName} ")
                exit()

            # LLama al módulo de cifrado/descifrado
            # devuelva por pantalla la llave de la cartera descifrada
            subprocess.call("cifrador_AES_PUF.py " + walletName, shell=True)
            


    # Si es un set
    elif (action == "set"):

        # Mira que el segundo argumento exista 
        # ->Si no termina el programa y devuelve "Debe introducir la llave de la cartera"
        if ( len(sys.argv) > 2 ):
            # recoge el segundo parámetro que le pasamos al script (Llave de la cartera)
            walletKey = sys.argv[2]
        else:
            print("\n\tDebe introducir la llave de la cartera")
            exit()

        # Mira que el tercer argumento exista
        # ->Si no termina el programa y devuelve "Debe introducir el nombre de la cartera"
        if ( len(sys.argv) > 3 ):
            # recoge el segundo parámetro que le pasamos al script (Nombre de la cartera)
            walletName = sys.argv[3]
        else:
            print("\n\tDebe introducir el nombre de la cartera")
            exit()

        # Mira si el dispositivo esta autorizado (0: autorizado, 1: no autorizado, 2: no se ha emparejado)
        authorized = subprocess.call("autorizacion.py", shell=True) 

        # Si no está emparejado, lo emparejamos
        if (authorized == 2):
            
            print("\n\tEmparejando... ")
            authorized = subprocess.call("emparejamiento.py", shell=True)

        # No está autorizado
        if (authorized == 1):
            # Terminamos el programa
            print("\n\tLo sentimos. Debe estar autorizado. ")
            exit()

        # Si esta autorizado 
        # Está autorizado
        if (authorized == 0):
            print("\n\tDispositivo autorizado")
        
        # Si se acaba de emparejar o está autorizado:
        # cifra y almacena la llave de la cartera
        subprocess.call("cifrador_AES_PUF.py " + walletKey + " " + walletName, shell=True)
        print("\n\tSu llave se ha guardado correctamente en la cartera " + walletName)   




    # No se ha introducido correctamente el primer parametro (action)
    else:
        print("\n\tEl primer argumento debe ser \"get\" o \"set\"")
        exit()

    