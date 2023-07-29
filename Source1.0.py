import wmi
import tkinter as tk
import pyperclip
import psutil
import os
import urllib.request
import shutil
import ctypes
import win32process
import win32api
import win32con

# Définir un dictionnaire pour stocker les noms d'utilisateur, mots de passe et HWIDs
user_info = {
    'mattfr48': {'password': 'mattfr48', 'hwid': 'SN210208963813'},
}

# Fonction pour vérifier si l'HWID correspond au nom d'utilisateur et mot de passe
def check_credentials(username, password, hwid):
    if username in user_info:
        if password == user_info[username]['password'] and hwid == user_info[username]['hwid']:
            return True
    return False

# Fonction pour obtenir l'HWID de l'ordinateur
def get_hwid():
    c = wmi.WMI()
    for disk in c.Win32_DiskDrive():
        if disk.Index == 0:
            return str(disk.SerialNumber)

# Fonction pour copier l'HWID dans le presse-papiers
def copy_hwid():
    hwid = get_hwid()
    pyperclip.copy(hwid)

# Fonction pour vérifier si le processus "csgo.exe" est en cours d'exécution
def check_process():
    for proc in psutil.process_iter():
        if proc.name() == "csgo.exe":
            return True
    return False

# Fonction pour télécharger le fichier DLL à partir de l'URL donnée
def download_dll(url):
    download_dir = os.path.expanduser("~/AppData/")  # Chemin absolu du dossier "Downloads"
    filename = os.path.join(download_dir, "gamesense.dll")  # Chemin absolu du fichier de sortie
    urllib.request.urlretrieve(url, filename)
    return filename

# Fonction pour supprimer le fichier DLL
def remove_dll(filename):
    os.remove(filename)

# Fonction pour lancer le processus "csgo.exe"
def launch_csgo():
    os.startfile("steam://rungameid/730")

# Fonction pour injecter le fichier DLL dans CS:GO
def inject_dll():
    if check_process():
        print("Injecting DLL...")
        dll_filename = os.path.join(os.path.expanduser("~/AppData/"), "gamesense.dll")
        pid = None
        for proc in psutil.process_iter():
            if proc.name() == "csgo.exe":
                pid = proc.pid
                break
        if pid is not None:
            try:
                kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                dll_handle = ctypes.windll.kernel32.LoadLibraryW(dll_filename)
                process_handle = kernel32.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
                kernel32.CreateRemoteThread(process_handle, None, 0, ctypes.windll.kernel32.GetProcAddress(dll_handle, 'DLL_ENTRY_POINT'), None, 0, None)
                kernel32.CloseHandle(process_handle)
                print("DLL injected successfully.")
            except Exception as e:
                print(f"Error injecting DLL: {e}")
        else:
            print("CSGO process not found.")
    else:
        print("CSGO is not running.")

# Fonction pour se connecter et afficher le menu principal
def login():
    username = username_entry.get()
    password = password_entry.get()
    hwid = get_hwid()
    if check_credentials(username, password, hwid):
        root.destroy()  # Fermer la fenêtre de connexion
        # Afficher le menu principal
        main_window = tk.Tk()
        main_window.title("Napo.cc")
        main_window.geometry("400x200")

        # Ajouter des widgets pour le menu principal ici
        label = tk.Label(main_window, text="Welcome, " + username + " in Napo.cc CS:GO !")
        label.pack(pady=20)

        # Ajouter le bouton "Load" pour vérifier si le processus "csgo.exe" est en cours d'exécution
        load_button = tk.Button(main_window, text="Load CS:GO", command=load_csgo)
        load_button.pack(pady=10)

        # Ajouter le bouton "Inject" pour injecter le fichier DLL dans CS:GO
        inject_button = tk.Button(main_window, text="Inject DLL in CS:GO", command=inject_dll)
        inject_button.pack(pady=10)

        # Crédits
        label = tk.Label(main_window, text="Made By mattfr48")
        label.pack(pady=10)

        main_window.mainloop()
    else:
        error_label.config(text="Username, password or HWID are wrong.")

# Fonction pour charger le processus "csgo.exe" si nécessaire
def load_csgo():
    if check_process():
        print("CSGO is already running.")
    else:
        print("Launching CSGO...")
        # Télécharger le fichier DLL
        dll_filename = download_dll("https://github.com/MaSa5251/4776848963/raw/main/gamesense.dll")
        # Lancer CSGO
        launch_csgo()
        # Supprimer le fichier DLL
        remove_dll(dll_filename)

# Créer la fenêtre principale
root = tk.Tk()
root.title("Napo.cc")
root.geometry("400x320")

# Ajouter des widgets pour la fenêtre principale ici

# Ajouter des widgets pour la fenêtre de connexion ici
username_label = tk.Label(root, text="Username:")
username_label.pack(pady=10)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)
password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)
login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=10)
error_label = tk.Label(root, fg="red")
error_label.pack(pady=5)
hwid_label = tk.Label(root, text="HWID: " + get_hwid())
hwid_label.pack(pady=10)

copy_button = tk.Button(root, text="Copy HWID", command=copy_hwid)
copy_button.pack(pady=10)

root.mainloop()
