import time
import sys
import serial
from serial.tools import list_ports
import docker
import requests

# Sett denne til False når du plugger inn den ekte ESP32-en senere!
SIMULATE_HARDWARE = True

# Globale innstillinger for USB
BAUD_RATE = 115200
LINK_BUDDY_VID = 0x10C4  # Standard for CP2102 (brikken på ESP32-kortet ditt)
LINK_BUDDY_PID = 0xEA60

def find_link_buddy_port():
    """Leter etter ESP32-kortet blant PC-ens USB-porter."""
    ports = list_ports.comports()
    for port in ports:
        # Sjekker enten spesifikk maskinvare-ID eller vanlige USB-navn
        if port.vid == LINK_BUDDY_VID or "CP2102" in port.description or "USB to UART" in port.description:
            return port.device
    return None

def send_to_device(ser, command):
    """Sender en kommando over USB (eller simulerer det i terminalen)."""
    if SIMULATE_HARDWARE:
        print(f"[SIMULATOR] Skjerm-tilstand endret ➔ {command}")
    else:
        if ser and ser.is_open:
            ser.write(f"{command}\n".encode('utf-8'))
            ser.flush()

def is_docker_running():
    """Sjekker om Docker Desktop kjører lokalt på PC-en."""
    try:
        client = docker.from_env()
        client.ping()
        return True
    except Exception:
        return False

def analyze_url(url):
    """
    Selve hjernen i PC-appen. 
    Sjekker om Docker kjører, velger analyse-sti, og returnerer om lenken er trygg.
    """
    print(f"\n[INFO] Starter skanning av: {url}")
    
    if is_docker_running():
        print("[STIL] Docker funnet! Kjører lokal, privat analyse...")
        # TODO: Her kobler vi på Docker-containeren din senere
        time.sleep(2) # Simulerer at analysen tar litt tid
        
        # Enkel test: Hvis lenken inneholder ordet "phishing", marker den som utrygg
        if "phishing" in url.lower():
            return False
        return True
    else:
        print("[STIL] Docker kjører IKKE. Faller tilbake på Sky-API (VirusTotal/URLScan)...")
        # TODO: Her legger vi inn requests.get() mot en sky-API senere
        time.sleep(1.5)
        
        if "bad" in url.lower():
            return False
        return True

def main():
    ser = None
    
    if not SIMULATE_HARDWARE:
        print("[INFO] Leter etter LinkBuddy på USB-portene...")
        port = find_link_buddy_port()
        if port:
            print(f"[SVARE] Fant dingsen på port: {port}")
            ser = serial.Serial(port, BAUD_RATE, timeout=1)
            time.sleep(2) # Vent på at ESP32 restarter etter tilkobling
        else:
            print("[FEIL] Fant ikke LinkBuddy. Sjekk kabelen eller sett SIMULATE_HARDWARE = True.")
            sys.exit(1)
            
    # 1. Start Onboarding/Tilkobling - Send PING til dingsen
    print("[INFO] Sender velkomst-ping til LinkBuddy...")
    send_to_device(ser, "PING_FROM_PC_APP")
    
    # 2. Test-loop for å simulere høyreklikk fra nettleseren
    print("\n--- LINKBUDDY SIMULATOR KLAR ---")
    print("Skriv inn en URL for å teste (eller 'exit' for å avslutte):")
    
    try:
        while True:
            test_url = input("\nSkriv URL: ")
            if test_url.lower() == 'exit':
                break
                
            if not test_url.strip():
                continue
                
            # Fortell dingsen at vi har startet analysen (skjermen blir stressa)
            send_to_device(ser, "CMD_ANALYZING")
            
            # Kjør selve analysen
            is_safe = analyze_url(test_url)
            
            # Send resultatet til dingsen
            if is_safe:
                print("[RESULTAT] Grønt lys! Lenken er trygg.")
                send_to_device(ser, "CMD_SAFE")
            else:
                print("[RESULTAT] ADVARSEL! Potensiell phishing oppdaget!")
                send_to_device(ser, "CMD_UNSAFE")
                
    except KeyboardInterrupt:
        print("\nAvslutter...")
    finally:
        if ser and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()
