# Step 1
-> Lecture des insctructions

-> Création du dossier de travail

-> Lecture de la doc de Scrap

-> Création du projet Scrap

-> Création du spider

-> Test du spider sur la home page

### Observation du résultat:
Le site semble être dinamique (javascript) et le spider ne récupère pas les liens du menu.

On va utiliser Playwright (https://github.com/scrapy-plugins/scrapy-playwright).

# Step 2
-> Lecture de la doc de Scrapy Playwright

-> Test du spider sur la home page

### Observation du résultat:
"Rien" ne change, on va essayer de cliquer sur le burger menu.

On récupère enfin les liens présents dans le menu.

# Step 3
-> On créé une boucle pour récupérer les liens de chaque page puis naviguer sur chaque page.

-> On récupère les données de chaque page ? (ça me semble un peu compliqué en terme de stockage / parsing).

Je suis un peu bloqué sur cette étape, je ne suis pas sûr de comprendre
à 100% les insctructions. J'ai beau relire le mail, je n'arrive pas à savoir
si je dois tout stocker (ce qui me semble le plus logique en partant du principe que nous ne connaissons "rien" du site) ou si je dois juste récupérer les données de "arrivals", "departures"... et les stocker dans un fichier. Ce dernier cas me semble plus "logique" en terme d'objectif mais je ne vois pas comment faire si nous ne connaissons ni les urls, ni les données à récupérer.

En relisant le premier mail, je me dis que je dois peut-être commencer par l'url donnée, et non par la home page. Je pense avoir mal interprété "Ici il faut imaginer que tu ne connais pas cette URL de base".

Dans le doute, je vais continuer sur la base de la home page mais en incluant une condition pour ne récupérer que les données souhaitées.
