# ES_IA_Embedded_Project

## 1. Analyse du modèle existant (Model0)

Le modèle étudié est une version simplifiée du **VGG11**, adaptée au jeu de données **CIFAR-10**.
Il s’agit d’un **réseau de neurones convolutionnel profond (CNN)** construit de manière séquentielle, comprenant trois blocs convolutionnels suivis de couches entièrement connectées.

### Structure du modèle

Chaque bloc convolutionnel comporte :

* une couche **Conv2D (3×3)**,
* une fonction d’activation **ReLU**,
* une **Batch Normalization** pour stabiliser l’apprentissage,
* une seconde couche **Conv2D (3×3)**,
* une fonction d’activation **ReLU**,
* une **Batch Normalization**,
* un **Dropout** pour régulariser,
* un **MaxPooling(2×2)** pour réduire la taille des cartes de caractéristiques.

Le nombre de filtres appliqués à la première couche de convolution est de 32 et est **multiplié par 2 à chaque bloc**.
Cela permet de conserver un bon ratio entre le nombre de filtres et la taille des données (chaque MaxPooling(2×2) divisant la taille par 4), limitant ainsi la perte d’information.

La partie finale du réseau comprend :

* deux couches denses (1024 et 512 neurones) avec **Dropout(0.3)**,
* une couche de sortie **Softmax** à 10 neurones (correspondant aux classes de CIFAR-10).

Ce type d’architecture atteint généralement **81 % de précision** sur le jeu de test CIFAR-10 et possède **2 916 394 paramètres**.
Cela correspond à un besoin mémoire d’environ **2 Mo 39**, supérieur à la limite de **1 Mo 99**, ce qui **ne le rend pas embarquable** sur notre carte actuelle.

---

## 2. Ensemble Learning

Une de nos idées pour réduire les coûts, augmenter la précision du système et améliorer la robustesse face aux attaques consiste à utiliser une approche **d’Ensemble Learning**.

### Principe

L’Ensemble Learning consiste à faire travailler **plusieurs modèles en parallèle** sur un même input (ici une image de CIFAR-10).
Chaque modèle produit sa propre prédiction, puis un **système de décision** fusionne ces résultats pour produire la classification finale.

Nous envisageons un système composé de **plusieurs petites IA embarquées sur des cartes distinctes**, chacune transmettant son résultat à une carte centrale responsable de la décision finale.

> **Schéma à insérer ici**

Nous avons choisi un **vote à majorité absolue** :
l’image est classée dans le label le plus fréquemment proposé.
En cas d’égalité (peu probable si le nombre de modèles est impair), un tirage aléatoire ou une nouvelle analyse peut être effectué.

Les modèles embarqués seront **similaires**, avec de légères variations (poids initiaux, paramètres d’entraînement ou architecture).

### Objectif

L’objectif est de déterminer **combien de modèles** d’une certaine précision individuelle sont nécessaires pour atteindre une **accuracy globale satisfaisante**, tout en **minimisant le coût matériel**.

La probabilité que la majorité des modèles aient raison correspond à :

[
P(X > n/2), \text{ avec } X \sim \text{Binom}(n, p)
]

où :

* *n* = nombre de modèles,
* *p* = précision individuelle du modèle,
* *X* = nombre de modèles donnant la bonne prédiction.


<p align="center">
  <img src="Loi%20binomiale.png" alt="Probabilité pour la Loi Binomiale" width="500">
</p>

Le graphique montre qu’il est préférable d’utiliser un **nombre impair de modèles** pour éviter les égalités.
Des modèles avec une précision individuelle de **plus de 75 %** permettent d’atteindre une précision globale **supérieure à 90 %** dès **4 modèles**.

---

## 3. Modèle 19

La fonction Resnet_block définit un bloc résiduel, : elle applique plusieurs convolutions successives avec normalisation et activation ReLU, puis ajoute une connexion directe (shortcut) entre l’entrée et la sortie du bloc. 

Le modèle débute par une couche de convolution initiale, suivie de plusieurs blocs résiduels à différentes profondeurs (8, 16, puis 32 et 64 filtres), intercalés avec des couches de MaxPooling et de Dropout pour la régularisation.
Enfin, une couche de GlobalAveragePooling et deux couches denses assurent la classification finale en 10 classes via une activation softmax.

Le fait de commencer par une convolution de 8 filtre nous permet d'une part de diminuer l'espace mémoire flash mais cela peremt surtout d'avoir un besoin en mémoire RAM relativement bas car elle stocke le résidus 
### Caractéristiques sans compression

* **Flash** : 268 Ko
* **RAM** : 85,7 Ko
* **Opérations** : ~8,5 M
* **Précision** : 80 % (**à revalider sur carte**)

### Caractéristiques avec compression élevée

* **Flash** : 235 Ko
* **RAM** : 85,7 Ko
* **Opérations** : ~8,5 M
* **Précision** : 80 % (**à revalider sur carte**)

Ce modèle, de par sa **faible empreinte mémoire** et sa précision satisfaisante, est un **bon candidat pour l’approche Ensemble Learning**.

Sa taille réduite permet son déploiement sur des **cartes à bas coût**, tout en laissant de la mémoire disponible pour d’autres fonctions.
Plusieurs IA peuvent éventuellement être implantées sur une même carte, au prix d’un temps d’inférence plus élevé.

---

## 4. Cartes proposées

### a) NUCLEO-G0B1RE

* **Flash** : 256 Ko
* **RAM** : 144 Ko
* **Cœur** : ARM Cortex-M0+, 64 MHz
* **Prix** : < 18 €

Assez de mémoire pour embarquer le modèle et communiquer via UART.
Son coût environ **5,3 fois inférieur** à la carte d’origine permettrait d’utiliser **5 modèles en ensemble learning**, pour une précision théorique d’environ **94,5 %**.
Mode basse consommation disponible.

**Inconvénients** : CPU ancien et fréquence limitée (64 MHz), donnant un **temps d’inférence estimé à 132 ms**.

---

### b) NUCLEO-F446RE

* **Flash** : 512 Ko
* **RAM** : 128 Ko
* **Cœur** : ARM Cortex-M4, 180 MHz
* **Prix** : < 20 €

Carte plus rapide tout en restant abordable.
Précision théorique similaire : **94,5 %** en ensemble learning.
**Avantages** : inférence rapide (~66 ms).
**Inconvénient** : absence de mode basse consommation documenté.

---

### c) NUCLEO-L452RE

* **Flash** : 512 Ko
* **RAM** : 160 Ko
* **Cœur** : ARM Cortex-M4, 80 MHz
* **Prix indicatif** : ~15 €

Bon rapport performance/prix.
Permet d’embarquer plusieurs modèles pour atteindre **94,5 %** de précision.
**Avantages** : présence d’un mode basse consommation.
**Inconvénients** : fréquence modérée, **temps d’inférence ≈ 106 ms**.

---

## 5. Sécurité

L’utilisation de plusieurs modèles à faible coût renforce la **résilience globale du système**.
Cependant, chaque modèle reste individuellement vulnérable, d’où la nécessité d’étudier leur robustesse face à différentes attaques.

### a) Attaques adversariales

Une **attaque adversariale** consiste à **ajouter un bruit subtil** à une image pour provoquer une mauvaise classification.
Nous avons testé deux types d’attaques : **FGSM** et **PGD** (en boîte blanche).

**Masques obtenue pour un budget de 0,01 et un step de 0,001**
<p align="center">
  <img src="./Securite/Model19/adv_attack_mask_exemple_001_step0001.png" alt="GProbabilité pour la Loi Binomiale" width="400">
</p>

<p align="center">
  <img src="./Securite/Model19/analyse_courbe_adv.png" alt="GProbabilité pour la Loi Binomiale" width="700">
</p>

Les tests montrent que :

* l’attaque **PGD** est plus efficace que **FGSM** à budget égal ;
* la perturbation visuelle reste à peine perceptible pour l’humain ;
* la précision chute de **90 % à environ 35 %**.

Ainsi, le modèle n’est **pas robuste** à ces attaques.
De plus, la similarité entre modèles rend l’ensemble learning **également vulnérable**, car une même perturbation affectera plusieurs modèles.

#### Protection

Nous avons ensuite testé une **adversarial training**, en introduisant des images bruitées dans les batches d’entraînement.
Cette méthode rallonge le temps d’entraînement, mais améliore la résistance du modèle.

> (**Résultats à développer et illustrer**)

---

### b) Bit Flip

Le protocole actuel n’attaque qu’un seul modèle à la fois ; nous ne pouvons donc pas encore évaluer la résistance de **l’ensemble complet** à une attaque physique (type laser). Cependant nous pouvons évaluer la résistance d'un seul modèle face à ce type d'attaque.

Pour protéger un modèle contre les perturbations de type bit-flip deux stratégies complémentaires peuvent être employées : RandBET et Clipping.

RandBET (Randomized Bit Error Training) consiste à introduire aléatoirement des erreurs de bits simulées dans les poids du réseau pendant l’entraînement. Cette approche expose le modèle à des perturbations similaires à celles qu’il pourrait subir en conditions réelles, ce qui le rend plus robuste aux erreurs matérielles. En apprenant à tolérer ces perturbations, le réseau développe une meilleure stabilité de ses prédictions face à des modifications accidentelles de ses paramètres.

Clipping vise à limiter la plage de valeurs des poids du réseau après chaque mise à jour. En contraignant les poids à rester dans un intervalle borné (par exemple entre −1 et 1), on évite que de petites erreurs de bits produisent des variations trop importantes dans les valeurs numériques. Cette méthode améliore donc la résilience numérique du modèle et réduit la sensibilité aux erreurs binaires.


<p align="center">
  <img src="./Securite/Model19/Result_bfa.png" alt="Résultat de l'attaque BFA du model 19" width="700">
</p>

# Interprétation

On observe que la **courbe rouge (nominale)** chute très rapidement : la précision tombe fortement dès quelques bit-flips, indiquant une forte vulnérabilité aux erreurs matérielles.

Les méthodes **clipping** et **RandBET + clipping**  maintiennent une meilleure précision pour un même nombre d’erreurs, surtout dans les **10 premiers bit-flips**. Cela montre qu’elles améliorent la robustesse du modèle.

Les valeurs de clipping différentes (**0.1 vs 0.2**) montrent des variations modestes : un clipping plus fort (**0.2**) semble légèrement plus stable, mais au prix d’une petite perte initiale.

Globalement, les modèles protégés conservent une précision autour de **10–15 %** même après de nombreux bit-flips, contrairement au modèle nominal qui s’effondre presque complètement.

## Conclusion

Ce graphique démontre que les techniques de **RandBET** et **Clipping** améliorent significativement la résilience du modèle face aux erreurs binaires. La combinaison **RandBET + Clipping** offre un compromis efficace entre **stabilité et performance**, limitant la dégradation de la précision lorsque le nombre de bit-flips augmente.



## 6. Conclusion (provisoire)

Le **modèle light 233k_80** constitue un **excellent compromis** entre taille mémoire, coût et précision.
Il est adapté à un **déploiement multi-carte** en ensemble learning, permettant d’améliorer la précision globale tout en réduisant les coûts.

Des tests complémentaires sont nécessaires :

* validation sur carte réelle,
* diversification des entraînements pour réduire la corrélation des erreurs,
* évaluation approfondie de la robustesse (bruit, laser, bit flip, etc.).

---

## 7. Modèle 5 compressé

Ce modèle est plus lourd, il est composé de 3 couche de 2 convolution simple de 32, 64, 128 filtres, avec pour fonction d'activation Relu. Il termine sur une couche de 128 neuronnes.

### Caractéristiques (compression élevée)

* **Flash** : 1,25 Mo
* **RAM** : 147,87 Ko
* **Opérations** : ~39,3 M
* **Précision** : 88 % (**à revalider sur carte**)

Ce modèle présente une **excellente précision** et reste **intégrable sur la carte STM32L4R9** après compression, tout en laissant suffisamment de mémoire disponible pour d’autres fonctions.

---

### Carte NUCLEO-L4R9

> Détails à compléter.

---

### Sécurité

Comme pour le modèle précédent, nous avons testé la robustesse face à des attaques adversariales et appliqué des techniques de protection.

#### Attaques adversariales

> **Graphiques et masques à insérer ici**

Le modèle reste sensible à ce type d’attaque : une petite perturbation (invisible à l’œil humain) peut réduire fortement l’accuracy.

#### Protection

> **Image avec masques à insérer**

#### Bit Flip

<p align="center">
  <img src="./Securite/Model5/Result_bfa.png" alt="Résultat de l'attaque BFA du model 5" width="700">
</p>
# Interprétation

Pour une perturbation maximale d'environ **30 bit-flips**, les résultats montrent une différence nette de robustesse entre le **modèle nominal** et les **modèles protégés**. Le modèle nominal (sans protection) chute à **20 % de précision**, ce qui indique une dégradation quasi totale des performances due aux inversions de bits.

En revanche, les modèles utilisant le **clipping seul** résistent nettement mieux :  

- Avec un seuil de **0.1**, on obtient encore **60 % de précision**.  
- Avec un seuil plus large (**0.2**), la précision descend à **45 %**.  

Cela suggère qu’un clipping plus strict (**0.1**) limite mieux les effets des erreurs en restreignant la variation des poids, au prix d’une légère contrainte sur la capacité d’apprentissage.

## Combinaison RandBET + Clipping

Les combinaisons **RandBET + Clipping** donnent les meilleures performances globales :  

- Avec **clipping = 0.1**, la précision atteint **75 %**, soit une amélioration considérable. Cela montre que l’entraînement sous perturbation (**RandBET**) permet au réseau de s’adapter à la présence d’erreurs binaires.  
- Avec **clipping = 0.2**, la précision reste bonne (**50 %**), mais inférieure, ce qui confirme qu’un clipping trop permissif réduit l’effet protecteur.

## Conclusion

Ces résultats montrent que la combinaison **RandBET + Clipping** améliore fortement la tolérance aux bit-flips, surtout lorsque le seuil de clipping est modéré (**0.1**). Cette stratégie permet au modèle de conserver une performance élevée même en présence d’erreurs matérielles importantes, prouvant son efficacité en **robustesse numérique et matérielle**.



---

## Conclusion (provisoire)

Le **modèle 5 compressé** offre un bon compromis entre performance et compatibilité embarquée.
Combiné à l’approche **Ensemble Learning**, il pourrait constituer une base robuste et scalable pour le projet.

---

