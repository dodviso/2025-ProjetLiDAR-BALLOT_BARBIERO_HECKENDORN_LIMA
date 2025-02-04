# Tutoriel LiDAR : Génération d'un MNT avec Whitebox Tools sur QGIS

Ce tutoriel permet d'apprendre comment traiter plusieurs tuiles lidar.
Comment les télécharger en lot, comment les fusionner pour pouvoir les traiter d'un seul tenant ensuite sur QGIS.

## Etape 1 : télécharger les données LiDAR

[Etat d'avancement de l'acquisition de données LiDAR](https://macarte.ign.fr/carte/322ea69dab4c7e5afabc6ec7043b5994/acquisitionslidarhd)

Rendez-vous sur la [page LiDAR](https://geoservices.ign.fr/lidarhd) de l'IGN

Descendez jusqu'à **Nuages de points classés et modèles numériques**

![carte tuiles](/images/carte_select_tuiles.png)

cherchez sur la zone sur laquelle vous souhaitez récupérer des données LiDAR

![zoom carte tuiles](/images/zoom_carte_select_tuiles.png)

Selectionner toutes les tuiles qui vous souhaitez
(bon 118 c'est peut-être un peu beaucoup, mais en même temps ça peut servir)

![selection tuiles](/images/select_tuiles.png)

téléchargez la liste des liens de téléchargement pour toutes les tuiles

![télécharger tuiles](/images/download_tuiles.png)

Téléchargez [ce script](https://github.com/dodviso/tuto_lidar/blob/master/download_tiles.py) pour télécharger toutes vos tuiles dans le dossier de votre choix


## Etape 2 : installer le plug-in QGIS Whitebox Tools

aller dans le menu extensions de QGIS

installer l'extension Whitebox Tools

ouvrir lidar tin gridding
![image](/images/lidar_tin_gridding.png)

## Etape 3 : Fusionner toutes les dalles lidar en une 

installer pdal 
```
conda install -c conda-forge pdal
```

créer un fichier de pipeline pour exécuter la fusion
```json
{
    "pipeline": [
        "dalles_lidar/*.laz",
        {
            "type": "writers.las",
            "filename": "data/valdrome_lidar.las"
        }
    ]
}
```

Executer le fusion
```
pdal pipeline merge_pipeline.json
```