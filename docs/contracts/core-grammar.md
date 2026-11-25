# Contrat — `core/grammar` v0.1 (draft révisé)

> **Propriétaire :** `core-dev`
> **Consommateurs :** `core/model`, `core/sync`, `core/youtube`, `ui`, `services`
> **Statut :** draft — cible `v0.2` gelée pour W1.1
> **Spec :** `docs/specs/spec-grammar-guitar-card.md`
> **Décisions :** `D10` (multiplicateurs), `D12` (zones/familles), `D15` (noms, variantes, exposants)

---

## 1. API publique

```python
def tokenize(source: str) -> list[Token]: ...
def parse(source: str) -> ParseResult: ...
def expand(ast: CardNode) -> list[Occurrence]: ...
```

### `tokenize`

- Transforme la chaîne brute en tokens typés avec `Span`.
- Ne lève jamais d'exception sur une entrée utilisateur.
- Les caractères inconnus produisent un token `UNKNOWN` + un diagnostic.

### `parse`

- Construit l'AST et collecte les diagnostics.
- **Ne lève jamais** d'exception sur une entrée utilisateur.
- Retourne toujours un `CardNode` (éventuellement vide) + diagnostics.
- Les erreurs de syntaxe sont récupérables : le parser continue.

### `expand`

- Déplie compteurs, multiplicateurs et groupes en une liste plate ordonnée.
- Déterministe : même AST → même liste.
- Ne modifie pas l'AST.

---

## 2. Types

```python
@dataclass(frozen=True)
class Span:
    start: int   # index Python dans source (code points)
    end: int     # exclusif, start <= end

@dataclass(frozen=True)
class Diagnostic:
    severity: Literal["info", "warning", "error"]
    code: str
    message: str          # français
    span: Span
    suggestion: str | None = None

@dataclass(frozen=True)
class Token:
    kind: TokenKind
    text: str
    span: Span

@dataclass(frozen=True)
class ParseResult:
    ast: CardNode
    diagnostics: list[Diagnostic]

@dataclass(frozen=True)
class Occurrence:
    index: int
    motif_key: str                 # A, a, A^1, A^2, A^2~, Punk2, |4, ¦
    family_key: str                # A pour a/A^1/A^2 ; motif_key sinon
    repetition_index: int          # 1-based
    repetition_total: int
    group_path: tuple[GroupRef, ...]
    source_span: Span
```

`GroupRef` (à valider avec Q8) :
```python
@dataclass(frozen=True)
class GroupRef:
    group_id: int
    repetition_index: int
    repetition_total: int
```

---

## 3. Invariants

- `parse` et `tokenize` ne lèvent jamais d'exception sur une entrée utilisateur.
- `span.start <= span.end`, et `span.end <= len(source)`.
- Les spans sont des indices Python (Unicode code points), pas des bytes.
- `expand` préserve l'ordre source.
- `Punkx2` et `Punk x2` produisent le même AST et 2 occurrences de `Punk`.
- `Punk2` produit **1 occurrence** du motif nommé `Punk2` ; `Punk2x2` en produit 2.
- `A Solo1 AA Solo2` produit `A`, `Solo1`, `A`, `A`, `Solo2` (5 occurrences).
- `aaAA` produit `a`, `a`, `A`, `A` ; `family_key` vaut `A` pour les quatre.
- `A^1` ≡ `A#` et `A^2` ≡ `A##` ; l'AST normalise vers `A^1`/`A^2`.
- `A^2~` est valide ; `A~^2` produit un `warning` et est normalisé en `A^2~`.
- `A2` produit une `error` (`GC-GRAM-008`) ; aucune occurrence pour le `2`.
- `2{AA}` produit un `info` (`GC-GRAM-010`) et 4 occurrences de `A`.
- `{5A BB}x2` produit 14 occurrences avant `CC#` (5 A + 2 B, deux fois).
- `AAA` produit 3 occurrences de `A`.
- `AA#` produit `A` puis `A^1`.
- `bbbb#` produit `b`, `b`, `b`, `b^1`.
- Une entrée vide produit un AST vide + aucun diagnostic bloquant.
- Un caractère inconnu produit un diagnostic localisé, pas un crash.

---

## 4. Diagnostics (codes initiaux)

| Code | Sévérité | Cas | Message type |
|---|---|---|---|
| `GC-GRAM-001` | error | caractère inconnu | « Caractère inattendu "@". » |
| `GC-GRAM-002` | error | groupe non fermé | « Groupe non fermé : "{" sans "}". » |
| `GC-GRAM-003` | warning | multiplicateur incomplet | « Multiplicateur incomplet : "x" sans nombre. » |
| `GC-GRAM-004` | warning | multiplicateur orphelin | « "x2" n'est associé à aucun motif. » |
| `GC-GRAM-005` | warning | groupe vide | « Groupe vide "{}". » |
| `GC-GRAM-006` | warning | modificateur sans motif | « "#" n'est associé à aucun motif. » |
| `GC-GRAM-007` | warning | compteur sans motif | « "5" n'est associé à aucun motif. » |
| `GC-GRAM-008` | error | chiffre collé à un motif d'une lettre (`A2`) | « "A2" est ambigu ; écrire "2A" ou "Ax2". » |
| `GC-GRAM-009` | warning | ordre invalide `A~^2` | « Écrire "A^2~" : l'exposant porte le niveau de variante. » |
| `GC-GRAM-010` | info | compteur préfixe sur groupe (`2{AA}`) | « Préférer "{AA}x2" ou "4A". » |
| `GC-GRAM-011` | info | variante abrégée (`A##`) | « Forme normalisée : "A^2". » |

Les codes sont stables ; les messages peuvent évoluer. Toute évolution de code = décision.

---

## 5. Points ouverts

- **Q3** : `¦`/`|` sans numéro de case — motif générique ou marqueur de structure ?
- **Q8** : `group_path` et compteurs de groupe (`{5A BB}x2`).

Q4, Q5, Q6, Q7 et Q35 sont résolues (`D10`, `D12`, `D15`). Tant que Q3/Q8 ne sont pas tranchées, le contrat reste `draft` et les consommateurs ne doivent pas dépendre des cas concernés.

---

## 6. Tests de conformité

- [ ] Golden 4 cartes.
- [ ] `Punkx2` == `Punk x2` (2 occurrences de `Punk`).
- [ ] `Punk2` == 1 occurrence de `Punk2` ; `Punk2x2` == 2 occurrences.
- [ ] `A Solo1 AA Solo2` == 5 occurrences dans l'ordre.
- [ ] `aaAA` == 4 occurrences, famille `A`.
- [ ] `A^1` == `A#` ; `A^2` == `A##`.
- [ ] `A^2~` valide ; `A~^2` warning + normalisation.
- [ ] `A2` error `GC-GRAM-008`.
- [ ] `2{AA}` info `GC-GRAM-010` + 4 occurrences.
- [ ] `{5A BB}x2` == 14 occurrences.
- [ ] `AAA` == 3 × A.
- [ ] `AA#` == A, A^1.
- [ ] Entrée vide, espaces, retours ligne.
- [ ] `{ AA` non fermé.
- [ ] `Ax`, `x2` isolé.
- [ ] `@`, `?`.
- [ ] `hypothesis` : pas de crash, spans valides.
- [ ] `expand(parse(s)) == expand(parse(normalize(s)))`.

---

## 7. Versioning

- `v0.1` : draft initial.
- `v0.1-r2` : révision après `D10`/`D12`/`D15` (ce document).
- `v0.2` : gel pour W1.1 après résolution de Q3/Q8.
- Breaking change : nouvelle version + décision + mise à jour des consommateurs.
