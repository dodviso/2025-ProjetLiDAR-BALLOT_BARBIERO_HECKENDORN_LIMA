import os
import requests
from tqdm import tqdm
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

# Définition de la fonction principale de téléchargement
def download_tile(url, output_dir, max_retries=5, timeout=60, pause_between_retries=5):
    """Télécharge un fichier à partir de son URL avec gestion des erreurs et retries."""
    nom_fichier = url.split("/")[-1]  
    chemin_fichier = os.path.join(output_dir, nom_fichier)

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, stream=True, timeout=timeout)
            total_size = int(response.headers.get("content-length", 0))  

            if response.status_code == 200:
                with open(chemin_fichier, "wb") as f:
                    with tqdm(
                        total=total_size, 
                        unit="B", 
                        unit_scale=True, 
                        unit_divisor=1024, 
                        desc=nom_fichier,
                        ascii=True,  
                        dynamic_ncols=True  
                    ) as bar:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                bar.update(len(chunk))  

                return f"✅ {nom_fichier} téléchargé avec succès !"

            else:
                return f"⚠️ Erreur {response.status_code} pour {nom_fichier}"

        except requests.exceptions.Timeout:
            print(f"⏳ Timeout pour {nom_fichier}, tentative {attempt}/{max_retries}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur lors du téléchargement de {nom_fichier} : {e}")

        if attempt < max_retries:
            print("🔄 Nouvelle tentative après 5 secondes...")
            sleep(pause_between_retries)
        else:
            return f"🚨 Échec définitif après {max_retries} tentatives pour {nom_fichier}"

def parallel_download(urls, output_dir, max_workers=4, max_retries=5, timeout=60, pause_between_retries=5):
    """Télécharge plusieurs fichiers en parallèle."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(download_tile, url, output_dir, max_retries, timeout, pause_between_retries): url 
            for url in urls
        }
        for future in as_completed(future_to_url):
            print(future.result())  # Affiche le statut de chaque téléchargement

# Traitement
if __name__ == "__main__":

    # Fichier contenant la liste de liens de téléchargement des tuiles
    TILES_LIST = "liste_dalle.txt"

    # Dossier de téléchargement des tuiles
    OUT_DIR = "/Users/d.ballot/Documents/PROJETS_SIGMA/tuto_lidar/QGIS/dalles_lidar"
    
    MAX_WORKERS = 4  # Nombre de téléchargements en parallèle
    MAX_RETRIES = 5  # Nombre maximal de tentatives par fichier
    TIMEOUT = 60  # Temps d'attente avant timeout
    PAUSE_BETWEEN_RETRIES = 5  # Pause entre chaque tentative en cas d'échec

    os.makedirs(OUT_DIR, exist_ok=True)

    # Lecture des URLs depuis le fichier
    with open(TILES_LIST, "r") as file:
        urls = [line.strip() for line in file if line.strip()]

    print("📡 Lancement des téléchargements en parallèle...")

    # 🚀 Lancer les téléchargements en parallèle
    parallel_download(urls, OUT_DIR, MAX_WORKERS, MAX_RETRIES, TIMEOUT, PAUSE_BETWEEN_RETRIES)

    print("🎉 Téléchargement terminé !")
