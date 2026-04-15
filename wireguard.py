import subprocess
ruta = "/etc/wireguard"

def menu_principal():
    
    print("""
1. Activar/Desactivar
    2. Estado y Diagnosticos
        3. SYSTEMD (cuidado con esto!)
            4. Limpiar Pantalla
    """)
    
    try:
        opcion_principal = int(input("> "))
        if opcion_principal == 1:
            menu_one()
        elif opcion_principal == 2:
            menu_two()
        elif opcion_principal == 3:
            menu_tree()
        elif opcion_principal == 4:
            clear()
            menu_principal()
    except:  
        print("no seleccionaste una opcion valida!!")


# una funcion global para saberque vpn se esta usando
def obtener_vpn():

    resultado = subprocess.run(
    ["find", ruta, "-maxdepth", "1", "-type", "f", "-name", "*.conf"],
    capture_output=True,
    text=True,
    check=True,
    )
    vpn = [linea.rsplit("/", 1)[-1] for linea in resultado.stdout.splitlines() if linea]
    
    for i, v in enumerate(vpn, 1):
        print(f"{i}. {v}")
    
    print("eligue el numero de la vpn que te quieres conectar")
    numero_vpn = int(input("> "))
    
    
    reemplazar = vpn[numero_vpn - 1]
    nombre = reemplazar.replace(".conf", "")
    return nombre
    


# esta es la configuracion del menu de avtivar y desactivar     
def activar(nombre_vpn):
    clear()
    print(f"activando... {nombre_vpn}")
    subprocess.run(["wg-quick", "up", nombre_vpn])
    menu_principal()

def desactivar():
    nombre_vpn = subprocess.run(
        ["wg", "show", "interfaces"],
        capture_output=True,
        text=True).stdout.strip().split()
    
    if not nombre_vpn:
        menu_one()
    for i in nombre_vpn:
        print(f"desactivando...{i}")
        subprocess.run(["wg-quick", "down", i])
    menu_principal()

def menu_one():
    clear()
    print("""
1. Activar
    2. Desactivar
        3. Atras
    """)
    try:
        opcion_one = int(input("> "))
        if opcion_one == 1: 
             nombre_vpn = obtener_vpn()
             activar(nombre_vpn)
        elif opcion_one == 2:
            desactivar()
        else:
            menu_principal()
    except:
        menu_one()

    
    
    
# todas las funciones de la opcion 2 estan lista
def estado_actual():
    clear()
    estado = subprocess.run(["wg", "show"], capture_output=True, text=True).stdout
    if not estado:
        print("no estas conectado a una vpn")
    else:
        print(estado)
    menu_two()

def interfaz_especifica():
    clear()
    interfaz = subprocess.run(["wg", "show", "interfaces"], capture_output=True, text=True).stdout
    print(f"estas conectado a la vpn {interfaz.upper()}")
    menu_two()

def ip_actual():

    resultado = subprocess.run(
        ["ip", "-4", "addr", "show"],
        capture_output=True,
        text=True
    )

    ip_privada = None
    ip_vpn = None
    interfaz_actual = ""

    for linea in resultado.stdout.splitlines():
        # detectar interfaz
        if ":" in linea and not linea.startswith(" "):
            interfaz_actual = linea.split(":")[1].strip()

        if "inet " in linea:
            ip = linea.strip().split()[1].split("/")[0]

            if interfaz_actual == "lo":
                continue
            elif interfaz_actual == "usa":  # tu VPN
                ip_vpn = ip
            else:
                ip_privada = ip

    # 🌍 IP pública FORZANDO IPv4
    ip_publica = subprocess.run(
        ["curl", "-4", "-s", "ifconfig.me"],
        capture_output=True,
        text=True
    ).stdout.strip()

    clear()
    print(f"🌍 IP pública: {ip_publica}")
    print(f"🏠 IP privada: {ip_privada}")
    
    if ip_vpn:
        print(f"🔐 IP VPN: {ip_vpn}")
    else:
        print("🔐 VPN: no activa")
    menu_two()

def menu_two():
    
    print("""
1. Ver estado actual
    2. Ver interfaz específica
        3. Ver tu IP actual
            4. Atras
    """)
    try:
        opcion_two = int(input("> "))
        if opcion_two == 1:
            estado_actual()
        elif opcion_two == 2:
            interfaz_especifica()
        elif opcion_two == 3:
            ip_actual()
        elif opcion_two == 4:
            clear()
            menu_principal()
    
    except:
        print("opcion no valida")
        menu_two()
    
    
    
    
    
    
    
    
    
    
    
def menu_tree():
    clear()
    print("""
1. Activar/Desactivar
  2. Estado y Diagnosticos
    3. SYSTEMD (cuidado con esto!)
    """)

def clear():
    subprocess.run(["clear"])



# el inicio de todo
while True:
    menu_principal()
    break
