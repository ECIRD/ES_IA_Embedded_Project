# Broullion

## Analyse du modele
Ce readme est temporaire:

Le nombre d opration effectuer est de **32,997,984** ce qui prend: **0,2749832s**\
C**Conv2d_1** et **Conv2d_2** prennent chacun >**9,000,000** d'opération et les zutres Conv sont dans cette ordre de grandeur (>**1,000,000** opération) cependant ce sont les couche **dense_dense** et **dense_1_dense** qui prenne le plus de place en memoire (**39,1% chacune**)


Le modéle prend **5,14Mb** en Flash et **148,56Kb** en RAM.\
Detaille:

| Catégorie            | Taille (B) | Taille (human readable) | Segments | Remarques         |
| -------------------- | ---------- | ----------------------- | -------- | ----------------- |
| **weights (ro)**     | 5 372 584  | 5.12 MiB                | 1        | Lecture seule     |
| **activations (rw)** | 143 468    | 140.11 KiB              | 1*        | Lecture/écriture  |
| **RAM (total)**      | 143 468    | 140.11 KiB              | –        | = 143 468 + 0 + 0 |


*Pour tester le model il faut faire un load sur le programme python avec tensor flow*

### Resultat de l'analyse 📊
Exactitude (accuracy): 0.8320

Matrice de confusion :\
[[861   9  18  12   9   2   7   3  57  22]\
 [  5 908   2   4   1   1   6   0  13  60]\
 [ 54   0 705  38  59  44  76  10   7   7]\
 [ 17   2  43 636  46 122  95  16  15   8]\
 [ 12   1  31  28 854  14  40  15   4   1]\
 [  8   2  30 117  35 753  31  19   1   4]\
 [  6   1  14  17  19   6 927   2   6   2]\
 [  8   0  18  30  55  33   6 843   3   4]\
 [ 32  12   3   9   1   1   6   5 920  11]\
 [ 16  33   2   3   2   3   8   5  15 913]]

Rapport de classification :
              precision    recall  f1-score   support

           0     0.8449    0.8610    0.8529      1000
           1     0.9380    0.9080    0.9228      1000
           2     0.8141    0.7050    0.7556      1000
           3     0.7114    0.6360    0.6716      1000
           4     0.7900    0.8540    0.8208      1000
           5     0.7692    0.7530    0.7610      1000
           6     0.7712    0.9270    0.8420      1000
           7     0.9183    0.8430    0.8790      1000
           8     0.8838    0.9200    0.9015      1000
           9     0.8847    0.9130    0.8986      1000

    accuracy                         0.8320     10000
   macro avg     0.8326    0.8320    0.8306     10000
weighted avg     0.8326    0.8320    0.8306     10000


	Le modèle prend en entrée des images de taille 32x32 sur trois niveau de couleur (RGB) et après une série de calcul, renvoie un label parmi 10. Pour toutes les couches de conv2D la fonction d'activation ReLu est utilisée pour un linéarité du gradient. Enfin pour la dernière couche la fonction softmax est utilisée ce qui permet de choisir 1 sortie parmi 10.
    
	Le model temps à réduire le nombre de pixel/neurone par filtre mais à augmenter le nombre de filtre (max poll 2.2 into conv2D nb filtre x2). On perds en information spatiale mais on gagne en information en profondeur (moins de où mais plus de quoi). De plus le ratio polling/filtre reste quasi constant ce que permet de ne pas faire exploser les coûts. Ça permet au réseau de conserver sa capacité de représentation malgré la compression spatiale.

   ## Idée

Mettre plusieur carte en parrallele pour peu qu'elles ne coutent pas cher (par rapport a l initial)

L'idée est de mettre un modele ayant une accuracy >75% sur plusieur carte peut couteuse en ressource (financiére, en flash ect) pour que le cout soit reduit par rapport au projet de base mais que les performance reste au moins similaire. Plusieur IA donne un resultat et on essaye de determiner un resultat. Peut etre envisager d'entrainer les IA de maniére différente ou faire legerment varier le modele.

## Etude du microcontrôleur cible

Pour embarquer un programme sur un microcontrôleur, il faut s’assurer non seulement qu’il dispose d’assez de mémoire ROM (mémoire Flash) pour stocker le programme et les poids du réseau de neurones, mais aussi qu’il possède suffisamment de mémoire RAM (mémoire volatile) pour exécuter le programme sans saturer ses capacités de calcul. Ces deux paramètres sont cruciaux en IA embarquée, car les modèles modernes sont de plus en plus volumineux et nécessitent un grand nombre d’opérations.

En pratique :

La ROM contient les poids du modèle et le code de l’application. Si la taille du réseau dépasse la capacité de la Flash interne (souvent limitée à quelques Mo sur STM32), il devient impossible de le déployer sans compression (quantization, pruning) ou ajout de mémoire externe.

La RAM est sollicitée lors de l’inférence pour stocker les activations intermédiaires (sorties de chaque couche), les buffers temporaires et les variables nécessaires aux calculs. Même si le modèle rentre en ROM, il peut être inutilisable si les activations dépassent la capacité RAM disponible.

Enfin, au-delà de la mémoire, il faut tenir compte de la puissance de calcul du microcontrôleur. Les opérations de convolution et de multiplication matricielle sont coûteuses, et leur exécution doit rester compatible avec les contraintes temps réel. Des optimisations logicielles (ex. CMSIS-NN) ou matérielles (NPU embarqué) sont souvent nécessaires.

Ainsi, la combinaison ROM + RAM + puissance de calcul constitue la principale limite dans l’IA embarquée. Dans le cas d’un modèle comme VGG11 simplifié (~5 Mo), la taille est trop importante pour la ROM et la RAM risque aussi d’être fortement sollicitée à cause des couches fully connected. Cela montre la nécessité d’utiliser des modèles plus compacts (MobileNet, SqueezeNet) ou d’appliquer des techniques de compression pour les rendre réellement exploitables sur STM32.

Nous utilisons dans un premier temps la STM32L4R9I-DISCO qui est une carte de démo de STMicroelectronics. Elle 