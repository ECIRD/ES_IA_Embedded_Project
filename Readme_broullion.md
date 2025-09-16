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
