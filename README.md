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

4. Modifier le fichier config.ini pour renseigner les valeurs <CLIENT_ID> et <CLIENT_SECRET>, Voici la marche à suivre pour obtenir ces valeurs:
   a) Aller à l'adresse suivante: https://console.developers.google.com/apis/credentials
   b) Cliquer sur "Créer des identifiants" -> ID client OAuth
      - Si vous n'avez pas déjà configuré un écran d'autorisation, un bouton "Configurer l'écran d'autorisation" apparait, cliquer dessus, entrer une valeur dans le champ "Nom de l'application" (ex: MyApp) et cliquer sur le bouton "Enregistrer"
   c) Sélectionner "Autre"
   d) Cliquer sur "Créer"
   e) Noter les valeurs Client id et Client Secret et les mettre dans le fichier config.ini
   f) Cliquer à gauche sur "Tableau de bord"
   g) Cliquer sur "+ACTIVER DES APIS ET DES SERVICES"
   h) Chercher "sheets"
   i) Cliquer sur "Google Sheets API"
   j) Si il y a un bouton GERER, ne rien faire, si il y a un bouton "ACTIVER", cliquer dessus

5. Double cliquer sur le fichier "grant_permissions.bat" et suivre les instructions

6. Double cliquer sur le fichier "mario-maker.pyw"


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
