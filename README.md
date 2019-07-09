# xsplit_mario_maker

1. Télécharger et installer python 3:
https://www.python.org/downloads/

2. Installer les modules python "Pillow", "requests" et "keyboard" en tapant les commandes:
```
pip install Pillow
pip install requests
pip install keyboard
```

3. Modifier le fichier config.ini pour renseigner la clé API (la méthode pour obtenir une clé API est détaillée ici: https://github.com/ThorAsgardDev/xsplit_retrolection_extension)

4. Double cliquer sur le fichier "mario-maker.pyw"


Côté XSplit:

Ajouter des sources "text" en utilisant le custom script "Load Text from Local File".
Utiliser les file path suivants:

```
Numéro du concours: <appli mario-maker>/text-files/contest-number.txt
ID du niveau: <appli mario-maker>/text-files/level-id.txt
Nombre de vies perdues: <appli mario-maker>/text-files/lost-lives.txt
Statut: <appli mario-maker>/text-files/status.txt
Theme: <appli mario-maker>/text-files/theme.txt
Nom du viewer: <appli mario-maker>/text-files/viewer.txt
Timer du jeu: <appli mario-maker>/text-files/timer.txt
```

Pour les timers il y a un bug côté XSplit. On peut le contourner en utilisant la manip suivante:

Pour la source "text" d'un timer, au lieu d'utiliser le custom script "Load Text from Local File" il faut utiliser un "Block Template" et copier le contenu du script:
```
<appli mario-maker>/xsplit-script/update-timer-script.js
```
