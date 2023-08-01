On serait intéressés par un mini crawler sur Scrapy (Librairie Python) avec comme URL d'entrée : https://www.flightradar24.com/data/airports/dxb

Ici il faut imaginer que tu ne connais pas cette URL de base, c'est une URL que ton script récupère quelque part, doit visiter, et indexer la donnée brute des pages

Plusieurs points :

On souhaite récupérer toutes les pages des vols dans la partie "Arrivals", "Departures"  et "On Ground"– dans les onglets.

- https://www.flightradar24.com/data/airports/dxb/departures
- https://www.flightradar24.com/data/airports/dxb/arrivals
- https://www.flightradar24.com/data/airports/dxb/ground

Il faut visiter chaque URL des vols, exemple : https://www.flightradar24.com/data/flights/ek238 et stocker dans un fichier la donnée brute des pages.

Le point le plus important est de pouvoir récupérer sur chacune de ces pages l'historique des vols, le tableau que l'on voit sur la page. Si tu y arrives, – encore une fois sans passer par l'analyse du réseau du site au préalable –, tu peux éventuellement parser la donnée pour la restituer mais ce n'est pas le point important ici.
