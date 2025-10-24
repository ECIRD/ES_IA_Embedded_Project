# ES_IA_Embedded_Project

## Modèle light 233k_80

### Description du modèle

Ce modèle possède les caractéristiques suivantes **sans compression** :

* Taille en flash : 268 Ko
* Taille en RAM : 85,7 Ko
* Environ 8,5 M d'opérations pour aboutir à un résultat
* Précision (accuracy) : 80 % (**À RETESTER AVEC LA CARTE**)

> (Parler de comment les modèles se font compresser — par exemple : compression des couches de convolution mais pas forcément des couches denses...)

### Caractéristiques après compression (compression élevée)

* Taille en flash : 235 Ko
* Taille en RAM : 85,7 Ko
* Environ 8,5 M d'opérations pour aboutir à un résultat
* Précision (accuracy) : 80 % (**À RETESTER AVEC LA CARTE**)

Nous avons choisi de poursuivre l'étude de ce modèle comme solution pour le projet. En effet, ce modèle, au vu de ses faibles besoins en mémoire (flash et RAM) et de sa précision satisfaisante, constitue un bon candidat pour notre méthode d'approche par **Ensemble Learning**. (**A évoquer avant : tableau, loi binomiale, résistances aux attaques, etc.**)

La faible place que prend le modèle en flash et en RAM — compressé ou non — nous permet de l'implanter sur des cartes ayant des caractéristiques nettement inférieures à celles de la carte d'origine. Nous pouvons donc envisager d'utiliser des cartes moins chères, mais en plus grand nombre, pour permettre un ensemble learning donnant des résultats corrects tout en gardant un coût matériel inférieur au modèle d'origine.

En compression élevée, le modèle peut tenir sur une carte possédant moins de 256 Ko de flash et un peu plus de 100 Ko de RAM, ce qui laisse de la place pour faire tourner d'autres programmes que l'IA embarquée. Nous pouvons également choisir des cartes plus puissantes pour exécuter des programmes annexes plus lourds. Il reste possible d'implémenter plusieurs IA sur une même carte si l'espace mémoire le permet, bien que cela augmente le temps d'inférence.

Dans le cadre d'un ensemble learning avec ce modèle, nous proposons trois cartes en fonction du domaine d'application du projet.

---

## Cartes proposées

### NUCLEO-G0B1RE

**Caractéristiques** :

* Flash : 256 Ko
* RAM : 144 Ko
* Cœur : ARM Cortex-M0+, 64 MHz
* Prix : < 18 €

Cette carte contient juste assez de flash pour implémenter l'IA et lui permettre d'utiliser un UART pour communiquer ses résultats. Cependant, elle coûte environ **5,3 fois moins cher** que la carte d'origine, ce qui permet d'imaginer déployer 5 modèles en ensemble learning. Cela donnerait une précision théorique (avec décision par majorité absolue) d'environ **94,5 %** (à confirmer). De plus, la carte possède un mode basse consommation.

Inconvénients : le CPU est ancien (ARM Cortex-M0+ de 2012) et la fréquence relativement basse (64 MHz) implique un temps d'inférence théorique de **132 ms**, relativement lent comparé à d'autres cartes.

---

### NUCLEO-F446RE

**Caractéristiques** :

* Flash : 512 Ko
* RAM : 128 Ko
* Cœur : Cortex-M4, 180 MHz
* Prix : < 20 €

Cette carte possède suffisamment de RAM et de flash pour installer notre modèle et d'autres programmes. Comme pour la carte précédente, elle permettrait d'atteindre une précision théorique d'environ **94,5 %** en ensemble learning. Elle coûte seulement quelques euros de plus que la carte initiale.

Avantages : fréquence d'horloge élevée, inférence théorique rapide (**66 ms**). Inconvénient : l'architecture CPU n'est pas la plus moderne et nous n'avons pas trouvé d'indication claire d'un mode low-power.

---

### NUCLEO-L452RE

**Caractéristiques** :

* Flash : 512 Ko
* RAM : 160 Ko
* Cœur : Cortex-M4, 80 MHz
* Prix indicatif : ~15 €

Cette carte offre une capacité de flash similaire à la NUCLEO-F446RE et un peu plus de RAM. Son prix attractif en fait une bonne option. Elle permettrait, comme les autres, d'embarquer 5 modèles pour un ensemble learning atteignant théoriquement **94,5 %** de précision.

Avantages : mode low-power disponible. Inconvénients : CPU un peu daté et fréquence modérée conduisant à un temps d'inférence théorique d'environ **106 ms**.

---

## Sécurité

Le modèle présente l'avantage d'être embarquable sur plusieurs cartes à faible coût, ce qui permettrait d'augmenter la robustesse et la sécurité de l'ensemble learning si le déploiement est bien réfléchi. (**À DÉVELOPPER**)

Nous avons néanmoins testé certaines attaques sur le modèle.

### Adversarial

    L'attaque par adversarial consiste bruité une image de maniére a trompé le model. Pour ce faire on peut (dans le cas "boite blanche") 
> Il est recommandé d'embarquer des modèles légèrement différents ou entraînés différemment pour réduire l'impact de ce type d'attaque sur un ensemble learning.

### Bit flip

> Le défaut de notre protocole d'évaluation actuel est que nous n'attaquons qu'un modèle à la fois ; nous ne pouvons donc pas tester pleinement la résistance de l'ensemble à une attaque laser.

---

## Conclusion (provisoire)

Le modèle *light 233k_80* apparaît comme un bon compromis entre empreinte mémoire, coût et précision. Son faible besoin en flash permet d'envisager un déploiement multi-carte en ensemble learning pour améliorer la précision globale tout en maîtrisant le coût matériel. Il faut cependant poursuivre les tests sur carte (validation de l'accuracy), diversifier les entraînements pour réduire la corrélation des erreurs et approfondir l'analyse de robustesse face aux attaques (bruit, laser, etc.).

---

*Notes : remplacer les mentions entre parenthèses (MAJUSCULES) par des sections développées dans la version finale.*
