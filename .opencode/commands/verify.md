---
description: Exécute une gate de qualité et consigne les preuves
agent: qa-verifier
---

Exécute la gate `$1` (G1, G2, G3, G4 ou G5) selon `docs/agents/QUALITY_GATES.md`.

Pour chaque commande : affiche la commande exacte, le résultat, la durée et le code de sortie. Ne dis pas « tests OK » sans preuve. Distingue exécuté / non exécuté (GPU, ffmpeg, OS absent).

Termine par : statut de la gate, preuves, échecs, tests flaky, prochaines actions.
