import socket
import sys
import signal
import threading

# Variable pour contrôler l'exécution
running = True

# Gestionnaire de signal pour l'interruption
def signal_handler(sig, frame):
    global running
    running = False
    print("\nScan is stopping....")

# ========================================
# Fonction : scan_port
# Description : Scanne un port TCP spécifique pour vérifier s'il est ouvert ou fermé
# Entrées :
#   - host : l'adresse IP ou le nom de domaine de la machine cible
#   - port : le port à scanner
#   - open_ports : liste pour stocker les ports ouverts
# ========================================
def scan_port(host, port, open_ports):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Définir un timeout pour éviter les blocages
            result = s.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
                print(f"--> Port {port}/TCP est ouvert.")
    except socket.error:
        pass  # Ignorer les erreurs de connexion

# ========================================
# Fonction : scan_ports
# Description : Scanne une gamme de ports (0 à 1023) sur l'hôte donné
# Entrées :
#   - host : l'adresse IP ou le nom de domaine de la machine cible
# Sortie :
#   - Liste des ports ouverts
# ========================================
def scan_ports(host):
    print(f"Scanning ports on {host}...")
    open_ports = []
    threads = []

    for port in range(0, 1023):  # Scanner les ports de 0 à 1023
        if not running:
            break  # Arrêter le scan si interrompu
        thread = threading.Thread(target=scan_port, args=(host, port, open_ports))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Attendre que tous les threads se terminent

    return open_ports

# ========================================
# Fonction principale
# Description : Gère l'entrée utilisateur, la résolution de l'adresse, et lance le scan des ports
# ========================================
def main():
    signal.signal(signal.SIGINT, signal_handler)  # Attacher le gestionnaire de signal
    if len(sys.argv) != 2:
        print("Usage : python scanner.py <target ip or hostname>")
        sys.exit(0)

    host = sys.argv[1]

    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"Le nom d'hôte {host} n'a pas pu être résolu : [ERREUR 110] échec.")
        sys.exit(1)

    # Lancer le scan des ports
    open_ports = scan_ports(target_ip)

    # Résumé des résultats : afficher les ports ouverts
    if open_ports:
        #sa nous indique le port es ouvert dans quel domaine en donnant son adresse ip es le port en question.
        print(f"Ports ouverts sur {host} ({target_ip}) : {', '.join(map(str, open_ports))}")
    else:
         #le cas ou le port n'est pas ouvert . mais dans notre cas sa nous interesse pas tellement.
        print(f"Aucun port ouvert trouvé sur {host} ({target_ip}).")
    print("Scan completed successfully.")

# ========================================
# Point d'entrée du programme
# ========================================
if __name__ == "__main__":
    main()
