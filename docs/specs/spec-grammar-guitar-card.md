# Spécification — Grammaire Guitar Card

> **Contexte** : `core/grammar/`
> **Rôle** : Définir la syntaxe des Guitar Cards, les règles de découpage lexical, la construction de l'AST, la gestion des diagnostics et l'expansion en occurrences pour la timeline.
>
> **Révision 2026-11-25 :** les multiplicateurs, les noms (`Punk2`), les variantes (`A^n`) et le cumul de modificateurs sont fixés par `D10`/`D15` ; les zones et familles par `D12`. Le contrat `docs/contracts/core-grammar.md` (v0.1-r2) fait foi jusqu'à l'alignement de l'EBNF par T-0004.

---

## 1. Principes généraux

Une *Guitar Card* est une partition simplifiée pour guitare sous forme d'une séquence de motifs (riffs) et de répétitions.

- Exemple développé : `AA BBBB` (« deux fois A puis quatre fois B »)
- Exemple réduit équivalent : `2A 4B` (`Ax2 Bx4`)

La grammaire est **ouverte et tolérante**. Le parser doit être extensible et **ne jamais lever d'exception** sur une entrée utilisateur, même mal formée ou contenant un token inconnu.

---

## 2. Éléments syntaxiques

| Élément              | Signification                                                                         | Exemple                                   |
|:---------------------|:--------------------------------------------------------------------------------------|:------------------------------------------|
| `A`, `B`, `C`…       | Motif (riff) de base                                                                  | `A`                                       |
| `A#`, `A~`           | Variante mélodique (`#`) ou rythmique (`~`) du motif                                  | `A#`, `B~`                                |
| `a` (minuscule)      | Variante d'intensité et/ou rythmique (pianissimo) du motif                            | `bbbb#B`                                  |
| `¦4`                 | Arpège autour de la frete 4                                                      | `¦4`                                      |
| `\|4`                | Barré / power chord sur la case 4 (éventuellement avec mélodie sur les doigts libres) | `\|4`                                     |
| `\|` (seul)          | Motif enchaînant plusieurs power chords                                               | `\|`                                      |
| `¦` (seul)           | Motif d'arpèges sans case précisée                                                    | `¦`                                       |
| `{ … }xN`            | Groupe de motifs répété $N$ fois                                                      | `{ 5A BB }x2`                             |
| `NA`, `AxN`, `\|4xN` | Répétition préfixée ou postfixée d'un motif $N$ fois                                  | `5A`, `\|4x5`                             |
| `Punk`               | Motif nommé multi-lettres (commençant par une majuscule suivie de minuscules)         | `Solo1`, `Solo2`, `Arpègge`, `Punk`       |
| `Punk x2`, `Punkx2`  | Motif nommé suivi d'un multiplicateur de répétition ($N$ fois)                        | `Punk x2` = `Punkx2` = `2×Punk` = `2Punk` |

---

## 3. Grammaire formelle (EBNF)

```ebnf
card        := item*                        # espaces = séparateurs cosmétiques, conservés pour l'affichage
item        := group | token
group       := "{" item* "}" multiplier?
token       := count? motif multiplier?
count       := INT                          # "5A" == "AAAAA"
multiplier  := "x" INT                      # "Punkx2" / "Punk x2" = jouer le motif/groupe INT fois
motif       := letter | symbol | named
letter      := [A-Za-z] modifier*           # minuscule = variante d'intensité
modifier    := "#" | "~"
symbol      := ("¦" | "|") INT?             # ¦ arpège, | barré / power chord, INT = case
named       := [A-Z][a-z]+ INT?             # Solo1, Punk (le suffixe x<INT> n'appartient jamais au nom)
```

---

## 4. Règles d'implémentation du Lexer et du Parser

### 4.1 Découpage lexical et priorités

1. **Chaque lettre isolée est un token distinct** :
* `AAA` produit 3 occurrences de `A`.
* `AA#` produit `A` suivi de `A#`.
* `bbbb#` produit `b`, `b`, `b`, `b#`.

2. **Priorité du multiplicateur postfixé `x<INT>**` :
* Le suffixe `x<ENTIER>` (`x2`, `x5`, etc.) désigne toujours un **multiplicateur de répétition** et a priorité lexicale sur la poursuite d'un identifiant `named`.
* `Punkx2` et `Punk x2` doivent produire exactement le même AST : le motif nommé `Punk` avec un multiplicateur `2` (jamais un motif nommé `Punkx` suivi de `2`).

3. **Espaces cosmétiques** :
* Les espaces servent uniquement à aérer la lecture (`¦4¦4` et `¦4 ¦4` sont équivalents sémantiquement), mais les positions (offsets début/fin) dans la chaîne source doivent être conservées pour le surlignage UI et les messages d'erreur.

### 4.2 Architecture en deux phases

1. **Lexer (`tokenize`)** : transforme la chaîne brute en flux de tokens typés avec leur `Span(start, end)` dans le texte source.
2. **Parser (`parse`)** : construit l'AST à partir des tokens et collecte les anomalies sans interrompre l'analyse. 
 - Signature attendue : `parse(source: str) -> ParseResult(ast: CardNode, diagnostics: list[Diagnostic])`.
 - Tout `Diagnostic` expose : `severity` (`info | warning | error`), `span` (`start`, `end`), `code`, `message` (en français) et une `suggestion` éventuelle.

### 4.3 Expansion de l'AST (`expand`)

* `expand(ast: CardNode) -> list[Occurrence]` déplie tous les compteurs (`5A`), multiplicateurs (`x2`) et groupes `{ … }xN` en une séquence plate ordonnée.
* Chaque `Occurrence` porte :
 - `index` : position globale dans la séquence dépliée ($0, 1, 2\dots$) ;
 - `motif_key` : identifiant normalisé du motif (ex. `A`, `A#`, `|4`, `Punk`) ;
 - `repetition_index` et `repetition_total` : ex. occurrence `2` sur `5` pour les compteurs visuels (`pips` ou badge `2/5`) ;
 - `group_path` : hiérarchie des groupes englobants (utile pour l'affichage et les chapitres YouTube) ;
 - `source_span` : position du token dans le texte de la Guitar Card.

---

## 5. Jeux de tests de référence (Golden & Property Tests)

### 5.1 Exemples golden obligatoires

Ces quatre cartes doivent passer en tests golden dans `tests/unit/grammar/` :

```text
The Wolf               : { 5A BB }x2 CC# BBB A
Reckless Paradise      : 4A {CACA DD}x2 {BBBB DD AA}x2 AA
Rusted From The Rain   : AAA ¦ {AA ¦ A# BBB C}x2 C# Solo1 BBB C B Solo2 D
Try Honesty            : AA# B# ¦4 B# {¦4¦4 |4x5 ¦4|4¦4 BBBB}x2 Punkx2 DD E AAAA# BBBB bbbb#

```

**Vérifications spécifiques sur les golden tests :**

* *The Wolf* : `{ 5A BB }x2` déplie bien `5 × A`, `2 × B`, répété 2 fois (14 occurrences avant `CC#`).
* *Try Honesty* : `Punkx2` déplie bien 2 occurrences consécutives du motif `Punk`.

### 5.2 Tests de propriété (`hypothesis`) et cas limites

* **Invariance de normalisation** : `expand(parse(s).ast) == expand(parse(normalize(s)).ast)`.
* **Robustesse** : chaînes vides, espaces multiples, retours à la ligne, accolades non fermées (`{ AA`), multiplicateurs incomplets (`Ax`, `x2` isolé), caractères inattendus (`@`, `?`) → aucun crash, diagnostic localisé en français retourné.