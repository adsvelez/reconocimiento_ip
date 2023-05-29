import sys, platform, subprocess, re

def hacer_ping(ip):
    if platform.system() == 'Windows':
        proceso = subprocess.Popen(['ping', '-n', '1', ip], stdout=subprocess.PIPE)
    else:
        proceso = subprocess.Popen(['ping', '-c', '1', ip], stdout=subprocess.PIPE)

    proceso.wait()

    if proceso.returncode == 0:
        salida = proceso.stdout.read()
        print("Ping exitoso a: "+ip)
        return salida
    else:
        return None

def determinar_sistema_operativo(respuesta):
    if respuesta:
        respuesta_decodificada = respuesta.decode('latin-1')

        # Utilizar expresión regular para encontrar el valor TTL
        match_ttl = re.search(r"ttl=(\d+)", respuesta_decodificada, re.IGNORECASE)
        if match_ttl:
            ttl = int(match_ttl.group(1))

            # Inferir el sistema operativo basado en el valor TTL
            if ttl <= 64:
                sistema_operativo = "Linux/Unix/MACos"
            elif ttl <= 128:
                sistema_operativo = "Windows"
            elif ttl <= 255:
                sistema_operativo = "Windows (probablemente)/solaris-AIX"
            else:
                sistema_operativo = "Desconocido"

            return sistema_operativo

    return "No se pudo obtener respuesta"

if len(sys.argv) == 2 and sys.argv[1] == "help":
    print("Este es un script permite hacer reconocimiento de una dirección IP o dominio")
    print("Uso: python recav.py <dominio/ip>")
    print("<diominio/ip>: Objetivo del reconocimiento")
    sys.exit(0)

if len(sys.argv) < 2:
    print("Se requieren un argumento <dominio/ip>")
    sys.exit(1)

ip = sys.argv[1]
respuesta = hacer_ping(ip)

sistema_operativo = determinar_sistema_operativo(respuesta)
print("Sistema operativo inferido:", sistema_operativo)