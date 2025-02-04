---
layout: default
title: Tutoriel LiDAR
description: "Génération d'un MNT avec Whitebox Tools sur QGIS"
---

# Tutoriel LiDAR : Génération d'un MNT avec Whitebox Tools sur QGIS

Bienvenue dans ce tutoriel LiDAR !
Nous allons voir comment traiter une grosse quantité de dalles LiDAR, pour pouvoir générer un MNT à une échelle communale.
Dans ce tutoriel, nous allons nous placer sur la commune de [Valdrôme](https://www.google.fr/maps/place/26310+Valdr%C3%B4me/@44.4966869,5.5400527,13z/data=!4m6!3m5!1s0x12cae603804a2bcb:0x408ab2ae4bfb590!8m2!3d44.504108!4d5.571565!16s%2Fm%2F03mhlq1?entry=ttu&g_ep=EgoyMDI1MDEyOS4xIKXMDSoASAFQAw%3D%3D), un petit village entouré de colines au coeur de la Drôme.

Tous les matériaux nécéssaires à ce tutoriel sont disponibles sur le dépôt Github associé à cette page, mais vous pouvez très bien le reproduire en sélectionnant vos propres tuiles LiDAR.

---

## Table des matières

1. [Télécharger les données LiDAR](#télécharger-les-données-lidar)
2. [Fusionner toutes les dalles LiDAR](#fusionner-toutes-les-dalles-lidar)
3. [Installer le plug-in QGIS Whitebox Tools](#installer-le-plug-in-qgis-whitebox-tools)

---

## Télécharger les données LiDAR

L'IGN produit et diffuse une cartographie 3D de l'intégralité du sol et du sursol en données LiDAR.
La couverture est presque complète, et vous pouvez suivre l'état d'avancement de l'acquisition de données LiDAR [sur cette page](https://macarte.ign.fr/carte/322ea69dab4c7e5afabc6ec7043b5994/acquisitionslidarhd).

Pour télécharger des données, rendez-vous sur la [page LiDAR](https://geoservices.ign.fr/lidarhd) de l'IGN.

Descendez jusqu'à **Nuages de points classés et modèles numériques**.
Vous trouverez l'interface de sélection des tuiles comme indiqué en [Figure 1](#fig-1).

![Carte de sélection des tuiles LiDAR](/images/carte_select_tuiles.png){: .fig #fig-1}
_Figure 1 : Carte de sélection des tuiles LiDAR._

Cherchez la zone sur laquelle vous souhaitez récupérer des données LiDAR

![zoom carte tuiles](/images/zoom_carte_select_tuiles.png)

Avec l'outil Polygone ou Rectangle, tracez l'emprise sur laquelle vous souhaitez télécharger les dalles LiDAR.

![selection tuiles](/images/select_tuiles.png)

Téléchargez le fichier .txt contenant la liste des liens de téléchargement pour toutes les tuiles.

![télécharger tuiles](/images/download_tuiles.png)

L'IGN conseille d'utiliser une extension de notre navigateur pour télécharger des fichiers en masse.
Toutefois, ce genre d'outil n'est pas toujours très modulable ou facile d'utilisation, alors nous mettons à votre disposition [ce script python](https://github.com/dodviso/tuto_lidar/blob/master/download_tiles.py) pour télécharger toutes vos tuiles à partir du fichier `liste_dalle.txt` dans le dossier de votre choix.

Pour l'utiliser, il vous suffit de le télécharger, dans le bloc `if __name__ == "__main__":` de modifier les paramètres :

```python
# Fichier contenant la liste de liens de téléchargement des tuiles
TILES_LIST = "liste_dalle.txt"

# Dossier de téléchargement des tuiles
OUT_DIR = "/QGIS/dalles_lidar"
```

Par vos propres chemins d'accès, absolus ou relatifs à l'emplacement auquel vous avez téléchargé le script.

Ensuite, exécutez le script selon vos habitudes, VS Code, Spyder, terminal ..

Le processus de téléchargement peut être un peu long selon la quantité de tuiles téléchargées.

Vos dalles sont téléchargées dans votre dossier !
![tuiles téléchargées](/images/dalles_telechargees.png)


## Fusionner toutes les dalles LiDAR

Pour traiter toutes ces dalles, on ne va pas s'amuser à les traiter une par une.

Il va falloir les fusionner.

Sur QGIS, il existe plusieurs outils qui traitent des données LiDAR : Whitebox Tools que nous allons voir après, LAStools, PDAL...

LAStools a une limitation sur MacOS, et en plus n'est pas open-source. Donc nous allons utiliser PDAL qui est un outil open-source en ligne de commande.

Pour installer PDAL, nous recommandons de passer par Anaconda.

Dans un terminal (PowerShell ou bash), exécutez:
```bash
# Vérifier si Conda est bien installé
conda --version
```

```bash
# Activer l'environnement de base de Conda
conda activate base
```

```bash
# Installer PDAL
conda install -c conda-forge pdal
```

Ensuite, il va falloir créer un fichier de pipeline pour opérer la fusion.
Rendez-vous dans votre répertoire de travail et créez un fichier `merge_pipeline.json` qui devra contenir ceci :

```json
{
    "pipeline": [
        "dalles_lidar/*.laz",
        {
            "type": "writers.las",
            "filename": "data/valdrome_lidar.laz",
            "compression": "laszip"
        }
    ]
}
```

Bien entendu, les chemins renseignés dans "pipeline" et "filename" doivent être relatifs à l'emplacement de votre fichier `merge_pipeline.json`.

Exemple dans notre cas :

```
└── 📁QGIS
    └── 📁dalles_lidar
        └── LHD_FXX_0899_6379_PTS_C_LAMB93_IGN69.copc.laz
        └── ...
    └── 📁data
    └── merge_pipeline.json
    └── tuto_lidar.qgz
```

Avec une aussi grosse quantité de tuiles, il est important de rester en format compressé .laz, car si on essaie d'enregistrer le fichier fusionné en format .las (non compressé et donc plus rapide à lire par QGIS par la suite) le fichier résultant fera plusieurs centaines de Go, ce qui, sur la plupart des ordinateurs, risque de saturer complètement l'espace de stockage.

Ensuite, une fois que tout est mis en place, on peut procéder la fusion des tuiles en exécutant la commande suivante dans le terminal dans lequel conda a précédemment été activé.
Bien entendu, il faut avoir navigué dans le terminal pour rejoindre le dossier dans lequel se trouve `merge_pipeline.json`.

```
pdal pipeline merge_pipeline.json
```


## Installer le plug-in QGIS Whitebox Tools

Aller dans le menu extensions de QGIS

Installer l'extension Whitebox Tools

Ouvrir lidar tin gridding
![image](/images/lidar_tin_gridding.png)

