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
   1. Aller à l'adresse suivante: https://console.developers.google.com/apis/credentials
   2. Cliquer sur "Créer des identifiants" -> ID client OAuth
      - Si vous n'avez pas déjà configuré un écran d'autorisation, un bouton "Configurer l'écran d'autorisation" apparait, cliquer dessus, entrer une valeur dans le champ "Nom de l'application" (ex: MyApp) et cliquer sur le bouton "Enregistrer"
   3. Sélectionner "Autre"
   4. Cliquer sur "Créer"
   5. Noter les valeurs Client id et Client Secret et les mettre dans le fichier config.ini
   6. Cliquer à gauche sur "Tableau de bord"
   7. Cliquer sur "+ACTIVER DES APIS ET DES SERVICES"
   8. Chercher "sheets"
   9. Cliquer sur "Google Sheets API"
   10. Si il y a un bouton GERER, ne rien faire, si il y a un bouton "ACTIVER", cliquer dessus

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
Temps de jeu: <appli mario-maker>/text-files/time.txt
```

Pour les timers il y a un bug côté XSplit. On peut le contourner en utilisant la manip suivante:

Pour la source "text" d'un timer, au lieu d'utiliser le custom script "Load Text from Local File" il faut utiliser un "Block Template" et copier le contenu du script:
```
<appli mario-maker>/xsplit-script/update-timer-script.js
```
