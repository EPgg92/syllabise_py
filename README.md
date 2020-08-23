# Syllabise_py
Pour un usage spécifique de la fonction de syllabise_word du PAM

## Pre-requis

L'environnement de cette fonction est `python3`. Le module `yaml` est nécessaire pour l'exécution ; il faut dont installer le package `PyYAML` :
```
pip install PyYAML
```
ou
```
pip3 install PyYAML
```

## Lancement

Rendez votre fichier exécutable:
```
chmod +x syllabise.py
```
Lancez le script avec l'une des commandes suivantes :
```
./syllabise.py syllabation
```
ou
```
python3 syllabise.py syllabation
```

## Exemple

Deux exemples de retours :

```
$> ./syllabise.py syllabation
syllabation => ['syl', 'la', 'ba', 'ti', 'on']
$> ./syllabise.py syllabation "je suis une phrase"
syllabation => ['syl', 'la', 'ba', 'ti', 'on']
je => ['je']
suis => ['suis']
une => ['u', 'ne']
phrase => ['phra', 'se']
```

## Utilisation des exceptions

Changez le fichier `constants.yaml` à votre convenance :
```
vowel:
  - /
  - à
  [...]
exeption:
  [...]
  on: V
  ll: C
  ion: V
  gn: C

```
Cela vous donnera :
```
$> ./syllabise.py syllabation/
syllabation/ => ['sy', 'lla', 'ba', 'tion', '/']

```

Toute amélioration est bienvenue pour une syllabation générique.

__N'hésitez pas à soumettre des issues.__

---
# Théorie de la syllabation des groupes de consonnes

## Introduction : types de groupes de consonnes
Un groupe de deux consonnes doit être (1) ou (2) :
1. tautosyllabique (=homo-organique)
2. hétérosyllabique (=hétéro-organique)

Cela signifie que dans la suite CC, la coupure syllabique ('.') peut tomber entre C et C : (C.C), après les deux CC (CC.) ou avant celle-ci (.CC).

>À noter : la syllabation CC. n'est pas possible en termes phonologiques, elle n'est pas attestée. En revanche, dans les langues comme le français qui notent, dans leur variété écrite, des consonnes qu'elles ne prononcent plus, on peut/pourrait trouver cette syllabation CC. Pour l'instant, on considère que CC. n'existe pas ; s'il existe il faudra le gérer.

## Groupes tautosyllabiques .CC
En français, sont tautosyllabiques les groupes dont la seconde consonne est un 'r' ou un 'l' et dont la première consonne est un :
- p
- b
- t
- d
- q
  - qu
  - c
  - k
- g
- f
  - ph
  - fh
- ch
  - sh
  - sch
- z
- s
- j

### Groupes tautosyllabiques .CCC
Ils sont rares, mais existent, comme dans _scribe_ ou _druide_ (/drɥidə/). _Druide_ ne sera a priori par traité par le syllabeur du PAM (parce que l'appoximante /ɥ/ n'est pas reconnue par le PAM), mais pour le type _scribe_, les règles sont les suivantes :
- le premier élément doit être un "s"
- le second et le troisième élément doivent former ensemble un groupe .CC autonome.
Mais en fait il semble que ce soit une exception, qui ne s'applique pas sur la base d'une règle... **À ne pas appliquer !**

## Groupes hétérosyllabiques C.C
Tous les groupes de deux consonnes qui ne sont pas .CC sont C.C. Donc tous ceux qui ne répondent pas aux test de .CC (et .CCC) sont traités C.C

## Cyclicité et linéarité
Quand on a plus de deux consonnes, il faut les analyses de droite à gauche :
- STR
  - T+R = .CC
  - S+(TR) = C.C
    - **Donc** STR = C.CC
