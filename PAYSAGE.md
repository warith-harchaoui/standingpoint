# Paysage

[🇫🇷](https://github.com/warith-harchaoui/standingpoint/blob/main/PAYSAGE.md) · [🇬🇧](https://github.com/warith-harchaoui/standingpoint/blob/main/LANDSCAPE.md)

Où se situe Standpoint parmi les manières habituelles de dessiner une carte de
positionnement (carte perceptuelle) ? La façon honnête d'y répondre est d'*utiliser
Standpoint sur lui-même* — cette page est donc un tableau de comparaison passé dans
l'outil, exactement comme n'importe quel autre exemple.

La comparaison (plus haut vaut mieux, sur une échelle de 1 à 5) :

| Outil | Nommage Automatique des Axes | Sortie Multilingue | Exécution Locale | Une Seule Commande | Livrable Triple | Reproductibilité | Axes Lisibles | Simplicité d'Installation |
|---|---|---|---|---|---|---|---|---|
| Standpoint | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 4 |
| prince | 1 | 1 | 5 | 2 | 1 | 5 | 5 | 3 |
| PCA (scikit-learn) | 1 | 1 | 5 | 2 | 1 | 5 | 4 | 3 |
| factoextra + FactoMineR | 1 | 1 | 5 | 2 | 2 | 5 | 5 | 2 |
| QuadrantMaker | 1 | 2 | 2 | 4 | 1 | 1 | 2 | 5 |
| Diapositives ou tableau blanc | 1 | 3 | 5 | 2 | 1 | 1 | 2 | 4 |

![Standpoint comparé aux autres outils de cartes de positionnement](https://raw.githubusercontent.com/warith-harchaoui/standingpoint/main/assets/paysage.png)

Les en-têtes du tableau étant en français, la carte sort **entièrement en français** —
titre, noms des axes et analyse — ce qui illustre au passage le côté multilingue de
l'outil.

## Comment la lire

Deux familles se font face :

- **Les boîtes à outils ACP statistiques** (`prince`, le `PCA` de scikit-learn,
  `factoextra` + `FactoMineR`) sont fortes là où ça compte mathématiquement —
  reproductibles, scriptables, loadings lisibles — mais elles vous rendent des
  composantes et des nombres, pas une carte étiquetée, rédigée et prête à partager.
  Nommer les axes, orienter autour d'une référence, colorer et rédiger reste à votre
  charge.
- **Les faiseurs de quadrants manuels** (QuadrantMaker, ou simplement des
  diapositives / un tableau blanc) sont rapides à prendre en main et sans code, mais
  chaque point est placé à la main : rien n'est dérivé des données, rien n'est
  reproductible, et les axes signifient ce que vous décidez.

L'argument de Standpoint, c'est le coin qu'aucune des deux familles n'occupe : la
carte **dérivée** d'une boîte à outils ACP *plus* l'artéfact **fini, étiqueté et
rédigé** d'un faiseur manuel — noms d'axes, sortie multilingue et livrable en trois
volets, en une seule commande.

## Réserves honnêtes

- **Standpoint est la ligne de référence**, donc il est pivoté en haut à droite par
  construction. Cette carte est notre *lecture des compromis*, pas un classement
  objectif — les notes sont subjectives et « plus haut vaut mieux » partout. Changez
  la référence (`--reference "PCA (scikit-learn)"`) et les mêmes données se
  réorientent autour d'elle.
- Le cœur mathématique (ACP de corrélation, loadings lisibles) est **exactement ce
  que les boîtes à outils font bien** — Standpoint ne prétend pas mieux calculer. Ce
  qu'il ajoute, c'est l'automatisation et le livrable fini autour de ce calcul.

## Reproduire

```bash
python3 -m standpoint assets/paysage.csv --outdir assets --stem paysage
```

Le tableau d'entrée est dans [`assets/paysage.csv`](assets/paysage.csv) ; l'exécution
écrit aussi l'interprétation Markdown et le YAML des coordonnées à côté de la figure.

Voir le [LISEZMOI](https://github.com/warith-harchaoui/standingpoint/blob/main/LISEZMOI.md)
pour ce que fait Standpoint et comment l'installer.
