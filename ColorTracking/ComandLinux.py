"""Codigo para automatizar y colocar los comandos de linux en el terminal para permitir la comunicacion serial"""

import subprocess

def prueba():
    # Ejecutar un comando de Linux
    comando = "ls -l"  # Por ejemplo, listar los archivos en el directorio actual
    resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Mostrar la salida del comando
    if resultado.returncode == 0:
        print("Salida del comando:")
        print(resultado.stdout)
    else:
        print("Error:")
        print(resultado.stderr)


# Reemplaza <username> y <tu_contraseña> con los valores adecuados
username = "jetsonnano"
password = "jetson123"

# Comando 1: sudo usermod -a -G dialout <username>
command1 = f'echo "{password}" | sudo -S usermod -a -G dialout {username}'

# Comando 2: sudo chmod a+rw /dev/ttyTHS1
command2 = "sudo -S chmod a+rw /dev/ttyTHS1"

# Ejecutar el comando 1
resultado1 = subprocess.run(command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Decodificar la salida del comando 1 de bytes a texto
stdout1 = resultado1.stdout.decode('utf-8')
stderr1 = resultado1.stderr.decode('utf-8')

# Mostrar la salida del comando 1
if resultado1.returncode == 0:
    print("Salida del comando 1:")
    print(stdout1)
else:
    print("Error en comando 1:")
    print(stderr1)

# Ejecutar el comando 2
resultado2 = subprocess.run(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Decodificar la salida del comando 2 de bytes a texto
stdout2 = resultado2.stdout.decode('utf-8')
stderr2 = resultado2.stderr.decode('utf-8')

# Mostrar la salida del comando 2
if resultado2.returncode == 0:
    print("Salida del comando 2:")
    print(stdout2)
else:
    print("Error en comando 2:")
    print(stderr2)

