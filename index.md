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
4. [Production d'un MNT](#production-dun-mnt-avec-whitebox-tools)

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

![Zoom sur la carte des tuiles LiDAR](/images/zoom_carte_select_tuiles.png){: .fig #fig-2}  
_Figure 2 : Zoom sur la carte des tuiles LiDAR._

Avec l'outil Polygone ou Rectangle, tracez l'emprise sur laquelle vous souhaitez télécharger les dalles LiDAR.

![Sélection des tuiles LiDAR](/images/select_tuiles.png){: .fig #fig-3}  
_Figure 3 : Sélection des tuiles LiDAR._

Téléchargez le fichier .txt contenant la liste des liens de téléchargement pour toutes les tuiles.

![Téléchargement de la liste des tuiles](/images/download_tuiles.png){: .fig #fig-4}  
_Figure 4 : Téléchargement de la liste des tuiles._

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
![Tuiles téléchargées](/images/dalles_telechargees.png){: .fig #fig-5}  
_Figure 5 : Tuiles téléchargées après le téléchargement._


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

A l'issue de cette étape, toutes vos dalles sont fusionnées !
Le fichier résultant devrait faire plusieurs dizaines de Go.


## Installer le plug-in QGIS Whitebox Tools

Cette étape n'est pas la plus facile, le plug-in Whitebox Tools ne fonctionne pas tout à fait comme les autres plug-in QGIS.
Il s'agit d'un outil initialement en ligne de commande, et pour s'en servir dans QGIS il faut d'abord l'installer en ligne de commande.

Commencez par installer le plug-in sur QGIS
![plug-in qgis](/images/download_whitebox.png){: .fig #fig-6}  
_Figure 6 : Téléchargement du plug-in Whitebox Tools sur QGIS._

Vous pouvez essayer de lancer n'importe quel traitement, vous verrez que cela ne fonctionne pas.

Installons donc l'exécutable Whitebox Tools.

Rendez-vous sur le site de la [Whitebox Geospatial Incorporated](https://www.whiteboxgeo.com/download-whiteboxtools/).

Vous allez croire en premier lieu que c'est payant, mais en fait n'ayez crainte, vous pouvez bien le télécharger pour 0$.

![site whitebox](/images/download_exe_whitebox.png){: .fig #fig-7}  
_Figure 7 : Téléchargement de l'outil WhiteboxTools._

En cliquant sur download, vous serez ensuite invités à télécharger la version compilée de l'outil dans le format adapté à votre système d'exploitation. 
Choisissez celle qui convient, et suivez les instructions suivantes qui correpondent.

### Installation pour Windows

Décompressez l'archive zip dans un dossier comme `C:\WhiteboxTools\`.

Ensuite, aller dans QGIS.  
Onglet "Préférences" > "Options"  
Option "Traitements" > "Fournisseur de traitement" > "WhiteboxTools executable"

Dans la zone prévue à cet effet, renseignez le chemin d'accès à l'exécutable WhiteboxTools.

![exe whitebox](/images/path_exe_whitebox.png){: .fig #fig-8}  
_Figure 8 : Paramétrage du chemin d'accès de l'exécutable WhiteboxTools dans QGIS._

Faites 'ok' et redémarrez QGIS.

Le plug-in WhiteboxTools est prêt à fonctionner sur QGIS !

### Installation pour MacOS/Linux

Dans votre répertoire utilisateur, exécutez :
```bash
mkdir -p ~/WhiteboxTools
```
Pour créer un dossier associé à l'outil.


Ensuite, exécutez :
```bash
unzip ~/Downloads/WhiteboxTools_darwin_amd64.zip -d ~/WhiteboxTools/
```
A adapter avec le nom de votre version.


Ensuite, il faut rendre l'outil exécutable :
```bash
chmod +x ~/WhiteboxTools/WhiteboxTools_darwin_amd64/WBT/whitebox_tools
```

Vérifiez que l'outil est bien installé en tapant :
```bash
 ~/WhiteboxTools/WhiteboxTools_darwin_amd64/WBT/whitebox_tools --version
```

Si cela vous affiche la version, c'est que c'est bon !

Sur mac, ce popup risque de s'afficher :

![gatekeeper](/images/mac_gatekeeper.png){: .fig #fig-9}  
_Figure 9 : Blocage sur MacOS de l'utilisation d'un logiciel extérieur._

Pour contourner ce problème, allez dans "Réglages Système" > "Confidentialité et Sécurité"

Et en bas de la page, vous trouverez :
![contourner autorisation](/images/mac_autorisation.png){: .fig #fig-10}  
_Figure 10 : Contourner le blocage d'un logiciel extérieur._

Cliquez sur "Autoriser quand même".

Ensuite, relancez
```bash
 ~/WhiteboxTools/WhiteboxTools_darwin_amd64/WBT/whitebox_tools --version
```

Et cette fois vous aurez :
![gatekeeper autorisé](/images/mac_autorise.png){: .fig #fig-11}  
_Figure 11 : Blocage d'un logiciel extérieur avec possibilité de contournement._
Et vous pouvez cliquer sur "Ouvrir quand même".

Les informations relatives à la version s'afficheront enfin dans votre terminal.


Ensuite, aller dans QGIS.  
Onglet "Préférences" > "Options"  
Option "Traitements" > "Fournisseur de traitement" > "WhiteboxTools executable"

Dans la zone prévue à cet effet, renseignez le chemin d'accès à l'exécutable WhiteboxTools.

![exe whitebox](/images/path_exe_whitebox.png){: .fig #fig-12}  
_Figure 12 : Paramétrage du chemin d'accès de l'exécutable WhiteboxTools dans QGIS._

Faites 'ok' et redémarrez QGIS.

Le plug-in WhiteboxTools est prêt à fonctionner sur QGIS !

---

Maintenant, tout est prêt pour produire un MNT dans de bonnes conditions.

## Production d'un MNT avec Whitebox Tools

Dans la boîte à outils QGIS, cherchez l'outil `LidarTINGridding`.

![lidartingridding](/images/tingridding_parametres.png){: .fig #fig-13}  
_Figure 13 : Paramètres du traitement LidarTINGridding._

Sélectionnez votre couche Lidar fusionnée précédemment.

On souhaite produire un MNT, c’est-à-dire une surface qui représente uniquement le terrain,
sans la végétation ni les bâtiments. Pour cela, il faut interpoler les altitudes des points LiDAR,
c’est pourquoi on garde l’option `elevation` dans `interpolation parameter`.
Cette option indique à l’algorithme qu’il doit construire la surface en fonction des valeurs d’altitude des points.

Ensuite, pour l’option `points returns included`, on choisit `last`. Un signal LiDAR peut être réfléchi plusieurs fois
avant d’atteindre le sol. Le premier retour (first) correspond à la première surface rencontrée,
souvent la cime des arbres ou le toit des bâtiments. Le dernier retour (last), lui,
correspond à la surface la plus basse touchée, donc généralement le sol. Comme on cherche à produire un MNT et non un MNS,
on sélectionne uniquement les last returns afin d’exclure les objets en hauteur et ne garder que le relief du terrain.

Enfin, pour obtenir un MNT précis, il est important de filtrer les points qui ne correspondent pas au sol.
Les données LiDAR sont classifiées selon différents types d’objets, et certaines classes doivent être exclues
pour éviter d’intégrer des éléments indésirables dans le modèle.
Ici, on exclut les classes :
```
1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18
```

Qui correspondent notamment aux points non classifiés, à la végétation de différentes hauteurs, aux bâtiments,
aux ponts ou encore aux objets artificiels. En filtrant ces classes, on s’assure de ne conserver que les points
réellement situés au niveau du sol, ce qui permet d’obtenir un MNT fidèle à la réalité topographique.

---

Une fois ces paramètres configurés, vous pouvez lancer le traitement en créant une couche temporaire, ou bien en indiquant directement
l'emplacement de sauvegarde du fichier de résultat. Nous vous conseillons de l'enregistrer directement car le traitement va être
un peu long, et de cette manière vous vous assurez de ne pas perdre le résultat en fermant QGIS par inadvertance à la fin.