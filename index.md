---
layout: default
title: Tutoriel LiDAR
description: "Génération d'un MNT avec Whitebox Tools sur QGIS"
---


# Tutoriel LiDAR : Génération d'un MNT avec Whitebox Tools sur QGIS

Bienvenue dans ce tutoriel LiDAR !
Nous allons voir comment traiter une grosse quantité de dalles LiDAR, pour pouvoir générer un MNT (Modèle Numérique de Terrain) à une échelle communale.

Un Modèle Numérique de Terrain est une représentation du relief sous forme de données altimétriques. Contrairement à un modèle qui inclurait les bâtiments ou la végétation, un MNT ne représente que le sol nu. Il peut est utilisé pour l'analyse du relief, la gestion des risques naturels, la modélisation hydraulique ou encore la planification d’aménagements.

Dans ce tutoriel, nous allons nous placer sur la commune de [Valdrôme](https://www.google.fr/maps/place/26310+Valdr%C3%B4me/@44.4966869,5.5400527,13z/data=!4m6!3m5!1s0x12cae603804a2bcb:0x408ab2ae4bfb590!8m2!3d44.504108!4d5.571565!16s%2Fm%2F03mhlq1?entry=ttu&g_ep=EgoyMDI1MDEyOS4xIKXMDSoASAFQAw%3D%3D), un petit village entouré de colines au coeur de la Drôme.

![valdrome](/images/valdrome.jpeg)
_Village de Valdrôme au milieu des colines_


Tous les matériaux nécéssaires à ce tutoriel sont disponibles sur le dépôt Github associé à cette page, mais vous pouvez très bien le reproduire en sélectionnant vos propres tuiles LiDAR.

---

## Table des matières


- [Tutoriel LiDAR : Génération d'un MNT avec Whitebox Tools sur QGIS](#tutoriel-lidar--génération-dun-mnt-avec-whitebox-tools-sur-qgis)
  - [Table des matières](#table-des-matières)
  - [Télécharger les données LiDAR](#télécharger-les-données-lidar)
  - [Fusionner toutes les dalles LiDAR](#fusionner-toutes-les-dalles-lidar)
  - [Installer le plug-in QGIS Whitebox Tools](#installer-le-plug-in-qgis-whitebox-tools)
    - [Installation pour Windows](#installation-pour-windows)
    - [Installation pour MacOS/Linux](#installation-pour-macoslinux)
  - [Production d'un MNT avec Whitebox Tools](#production-dun-mnt-avec-whitebox-tools)

---

## Télécharger les données LiDAR

L'IGN produit et diffuse une cartographie 3D de l'intégralité du sol et du sursol en données LiDAR.
La couverture est presque complète, et vous pouvez suivre l'état d'avancement de l'acquisition de données LiDAR [sur cette page](https://macarte.ign.fr/carte/322ea69dab4c7e5afabc6ec7043b5994/acquisitionslidarhd).

Pour télécharger des données, rendez-vous sur la [page LiDAR](https://geoservices.ign.fr/lidarhd) de l'IGN.

Descendez jusqu'à **Nuages de points classés et modèles numériques**.
Vous trouverez l'interface de sélection des tuiles comme indiqué en [Figure 1](#fig-1).

![Carte de sélection des tuiles LiDAR](/images/carte_select_tuiles.png){: .fig #fig-1}
_Figure 1 : Carte de sélection des tuiles LiDAR_

Cherchez la zone sur laquelle vous souhaitez récupérer des données LiDAR

![Zoom sur la carte des tuiles LiDAR](/images/zoom_carte_select_tuiles.png){: .fig #fig-2}  
_Figure 2 : Zoom sur la carte des tuiles LiDAR_

Avec l'outil Polygone ou Rectangle, tracez l'emprise sur laquelle vous souhaitez télécharger les dalles LiDAR.

![Sélection des tuiles LiDAR](/images/select_tuiles.png){: .fig #fig-3}  
_Figure 3 : Sélection des tuiles LiDAR_

Téléchargez le fichier .txt contenant la liste des liens de téléchargement pour toutes les tuiles, en cliquant sur le bouton représenté en [Figure 4](#fig-4).

![Téléchargement de la liste des tuiles](/images/download_tuiles.png){: .fig #fig-4}  
_Figure 4 : Téléchargement de la liste des tuiles_

L'IGN conseille d'utiliser une extension de votre navigateur pour télécharger des fichiers en masse.
Toutefois, ce genre d'outil n'est pas toujours très modulable ou facile d'utilisation, alors nous mettons à votre disposition [ce script python](https://github.com/dodviso/2025-ProjetLiDAR-BALLOT_BARBIERO_HECKENDORN_LIMA/blob/master/download_tiles.py) pour télécharger toutes vos tuiles à partir du fichier `liste_dalle.txt` dans le dossier de votre choix.

Pour l'utiliser, il vous suffit de le télécharger, dans le bloc `if __name__ == "__main__":` de modifier les paramètres :

```python
# Fichier contenant la liste de liens de téléchargement des tuiles
TILES_LIST = "liste_dalle.txt"

# Dossier de téléchargement des tuiles
OUT_DIR = "/QGIS/dalles_lidar"
```

Par vos propres chemins d'accès, absolus ou relatifs à l'emplacement depuis lequel vous allez exécuter le script.

Ensuite, exécutez le script selon vos habitudes, VS Code, Spyder, terminal ...

Le processus de téléchargement peut être un peu long selon la quantité de tuiles téléchargées (plusieurs dizaines de minutes, voire plus d'une heure).

---

Vos dalles sont téléchargées dans votre dossier !

![Tuiles téléchargées](/images/dalles_telechargees.png){: .fig #fig-5}  
_Figure 5 : Dalles téléchargées après le téléchargement_


## Fusionner toutes les dalles LiDAR

Dans l'optique de produire un MNT à l'échelle du village, on ne va pas faire les traitements individuellement pour chacune des dalles.

Il va falloir les fusionner.

Sur QGIS, il existe plusieurs outils qui traitent des données LiDAR : Whitebox Tools que nous allons voir après, LAStools, PDAL...

LAStools a une limitation sur MacOS, et en plus n'est pas open-source.  
Whitebox Tools ne permet malheuresement pas de fusionner des dalles LiDAR.  
Donc nous allons utiliser PDAL qui est un outil open-source en ligne de commande.  

Pour installer PDAL, nous recommandons de passer par Anaconda.

Dans un terminal (PowerShell ou bash), exécutez:

```bash
# Vérifier si Conda est bien installé
conda --version
```

Si Conda n'est pas installé dans votre environnement, vous pouvez vous référer à [cette documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) pour procéder à l'installation.  

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

Vous pouvez également récupérer le fichier [directement ici](https://github.com/dodviso/2025-ProjetLiDAR-BALLOT_BARBIERO_HECKENDORN_LIMA/blob/master/merge_pipeline.json).

Cette pipeline va indiquer à PDAL de charger toutes vos dalles, puis de les écrire dans un nouveau fichier (filename) en format compressé.

Bien entendu, les chemins renseignés dans "pipeline" et "filename" doivent être relatifs à l'emplacement de votre fichier `merge_pipeline.json`.

Exemple dans notre cas :

```
└── 📁TUTO_LiDAR
    └── 📁dalles_lidar
        └── LHD_FXX_0899_6379_PTS_C_LAMB93_IGN69.copc.laz
        └── ...
    └── 📁data
    └── merge_pipeline.json
```

Avec une aussi grosse quantité de tuiles, il est important de rester en format compressé .laz, car si on essaie d'enregistrer le fichier fusionné en format .las (non compressé et donc plus rapide à lire par QGIS par la suite) le fichier résultant fera plusieurs centaines de Go, ce qui, sur la plupart des ordinateurs, risque de saturer complètement l'espace de stockage.
C'est pour cette raison que l'on passe par un pipeline, car si on passait directement par une commande dans le terminal avec `pdal merge`, on n'aurait pas pu contrôler le mode d'écriture en compression laszip.

Ensuite, une fois que tout est mis en place, on peut procéder à la fusion des tuiles en exécutant la commande suivante dans le terminal dans lequel conda a précédemment été activé.
Bien entendu, il faut avoir navigué dans le terminal pour rejoindre le dossier dans lequel se trouve `merge_pipeline.json`.

```
pdal pipeline merge_pipeline.json
```

A l'issue de cette étape, toutes vos dalles sont fusionnées !
Le fichier résultant devrait faire plusieurs dizaines de Go.


## Installer le plug-in QGIS Whitebox Tools

Cette étape n'est pas la plus facile, le plug-in Whitebox Tools ne fonctionnant pas tout à fait comme les autres plug-in QGIS.
Il s'agit d'un outil initialement en ligne de commande, et pour s'en servir dans QGIS il faut d'abord l'installer en ligne de commande.

Commencez par installer le plug-in sur QGIS :
![plug-in qgis](/images/download_whitebox.png){: .fig #fig-6}  
_Figure 6 : Téléchargement du plug-in Whitebox Tools sur QGIS_

Vous pouvez essayer de lancer n'importe quel traitement, vous verrez que cela ne fonctionne pas.

Installons donc l'exécutable Whitebox Tools.

Rendez-vous sur le site de la [Whitebox Geospatial Incorporated](https://www.whiteboxgeo.com/download-whiteboxtools/).

Vous allez croire en premier lieu que c'est payant, mais en fait n'ayez crainte, vous pouvez bien le télécharger pour 0$, comme indiqué en [Figure 7](#fig-7).

![site whitebox](/images/download_exe_whitebox.png){: .fig #fig-7}  
_Figure 7 : Téléchargement de l'outil WhiteboxTools_

En cliquant sur download, vous serez ensuite invités à télécharger la version compilée de l'outil dans le format adapté à votre système d'exploitation. 
Choisissez celle qui convient, et suivez les instructions suivantes qui vous correspondent.

### Installation pour Windows

Décompressez l'archive zip dans un dossier comme `C:\WhiteboxTools\`.

Ensuite, allez dans QGIS.  
Onglet "Préférences" > "Options"  
Option "Traitements" > "Fournisseur de traitement" > "WhiteboxTools executable"

Dans la zone prévue à cet effet, renseignez le chemin d'accès à l'exécutable WhiteboxTools, comme indiqué en [Figure 8](#fig-8).

![exe whitebox](/images/path_exe_whitebox_windows.jpeg){: .fig #fig-8}  
_Figure 8 : Paramétrage du chemin d'accès de l'exécutable WhiteboxTools dans QGIS_

Faites 'OK' et redémarrez QGIS.

Le plug-in WhiteboxTools est prêt à fonctionner sur QGIS !

### Installation pour MacOS/Linux

Dans votre répertoire utilisateur, exécutez :
```bash
mkdir -p ~/WhiteboxTools
```
Pour créer un dossier associé à l'outil.


Ensuite, exécutez :
```bash
unzip ~/Downloads/WhiteboxTools_[version].zip -d ~/WhiteboxTools/
```
A adapter avec le nom de votre version, et éventuellement votre emplacement de téléchargement si celui-ci n'était pas `Downloads`.


Ensuite, il faut rendre l'outil exécutable :
```bash
chmod +x ~/WhiteboxTools/WhiteboxTools_[version]/WBT/whitebox_tools
```

Vérifiez que l'outil est bien installé en tapant :
```bash
 ~/WhiteboxTools/WhiteboxTools_[version]/WBT/whitebox_tools --version
```

Si cela vous affiche la version, c'est que c'est bon !

Sur MacOS, le popup de la [Figure 9](#fig-9) risque de s'afficher.

![gatekeeper](/images/mac_gatekeeper.png){: .fig #fig-9}  
_Figure 9 : Blocage sur MacOS de l'utilisation d'un logiciel extérieur_

Pour contourner ce problème, allez dans "Réglages Système" > "Confidentialité et Sécurité".

Et en bas de la page, vous trouverez :

![contourner autorisation](/images/mac_autorisation.png){: .fig #fig-10}  
_Figure 10 : Contourner le blocage d'un logiciel extérieur._

Cliquez sur "Autoriser quand même".

Ensuite, relancez
```bash
 ~/WhiteboxTools/WhiteboxTools_[version]/WBT/whitebox_tools --version
```

Et cette fois vous aurez le popup indiqué en [Figure 11](#fig-11).

![gatekeeper autorisé](/images/mac_autorise.png){: .fig #fig-11}  
_Figure 11 : Blocage d'un logiciel extérieur avec possibilité de contournement_

Et vous pouvez cliquer sur "Ouvrir quand même".

Les informations relatives à la version s'afficheront enfin dans votre terminal.


Ensuite, allez dans QGIS.  
Onglet "Préférences" > "Options"  
Option "Traitements" > "Fournisseur de traitement" > "WhiteboxTools executable"

Dans la zone prévue à cet effet, renseignez le chemin d'accès à l'exécutable WhiteboxTools, comme indiqué en [Figure 12](#fig-12).

![exe whitebox](/images/path_exe_whitebox.png){: .fig #fig-12}  
_Figure 12 : Paramétrage du chemin d'accès de l'exécutable WhiteboxTools dans QGIS_

Faites 'OK' et redémarrez QGIS.

Le plug-in WhiteboxTools est prêt à fonctionner sur QGIS !

---

Maintenant, tout est prêt pour produire un MNT dans de bonnes conditions.

## Production d'un MNT avec Whitebox Tools

Dans la boîte à outils QGIS, cherchez l'outil `LidarTINGridding`.

![lidartingridding](/images/tingridding_parametres.png){: .fig #fig-13}  
_Figure 13 : Paramètres du traitement LidarTINGridding_

Suivez les paramètres indiqués sur la [Figure 13](#fig-13).

Commencez donc par sélectionner votre couche LiDAR fusionnée précédemment.

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
réellement situés au niveau du sol (classe 2, la seule non exclue), ce qui permet d’obtenir un MNT fidèle à la réalité topographique.

Vous pouvez consulter les correpondances entre les codes et les classe sur [ce document](https://geoservices.ign.fr/sites/default/files/2024-09/DC_LiDAR_HD_1-0.pdf).

---

Une fois ces paramètres configurés, vous pouvez exécuter le traitement en créant une couche temporaire, ou bien en indiquant directement l'emplacement de sauvegarde du fichier de résultat. Nous vous conseillons de l'enregistrer directement car le traitement va être un peu long (1h30 pour 36 dalles, fichier .laz global de 14 Go), et de cette manière vous vous assurez de ne pas perdre le résultat en fermant QGIS par inadvertance à la fin.

---

Une fois le traitement terminé, QGIS vous affichera probablement le message indiqué en [Figure 14](#fig-14)

![erreur reproj](/images/erreur_reproj.png){: .fig #fig-14}  
_Figure 14 : Erreur de reprojection du MNT_

Whitebox Tools ne conserve pas le système de projection initial des données LiDAR, et donc le MNT en sortie est sans projection, d'où le terme 'unnamed'.

Pour résoudre ce problème définitivement, commencez par assigner la projection que vous souhaitez au MNT (ici 2154).

![assigner proj](/images/reproj_2154.png){: .fig #fig-15}  
_Figure 15 : Assigner la projection 2154_

Ensuite, exportez le MNT projecté dans un nouveau fichier.

![export 1](/images/export.png){: .fig #fig-16}  
_Figure 16 : Exporter le MNT reprojeté_

De cette manière, le fichier est enregistré avec la bonne projection, et le message ne s'affichera plus à chaque ouverture de QGIS.

![export 2](/images/export2.png){: .fig #fig-17}  
_Figure 17 : Sauvegarder le MNT reprojeté_

---

Voilà ! Vous avez un beau MNT.  

Pour finir ce tutoriel, on peut ajouter un peu de symbologie à notre MNT pour le rendre plus joli.

Avec le mode `ombrage`, on obtient avec les réglages par défaut ce genre de visualisation :

![ombrages](/images/mnt_ombrages.png){: .fig #fig-18}  
_Figure 18 : Symbologie en ombrages_


Avec quelques paramétrages, on obtient une carte très jolie du MNT fusionné avec le fond de plan OSM :

![ombages osm](/images/mnt_fusion_plan.png){: .fig #fig-19}  
_Figure 19 : Symbologie en fusion avec le fond de plan_

Et voilà, à vous de jouer !

---
**Auteurs** : Doris Ballot, Audrey Barbiero, Robin Heckendorn, Lucas Lima.

*Ce tutoriel a été réalisé dans le cadre de l'UE 901_22 : introduction au traitement de données LiDAR, M2 SIGMA 2024-2025.*
