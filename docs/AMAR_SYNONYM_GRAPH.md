_Created: 07-10-2026 · Last updated: 07-10-2026_

# Amarakośa as a Synonymy Graph (H6057)

The Amarakośa is a **thesaurus** where every other CDSL dictionary of this
repo's pipeline is alphabetical: its entries are synonym sets (synsets), not
headword articles. This analysis makes that structure explicit as a graph and
measures it — components, hubs, diameter, clustering — then cross-checks its
vocabulary coverage against the Monier-Williams (MW) sense network and
quantifies its "thesaurusness" against what an alphabetical dictionary can
express structurally.

All numbers below are produced by `scripts/amar_graph.py` (pure Python stdlib,
deterministic across processes, seed `20261004`; verified by two-process
byte-identical rerun); raw outputs are committed under `analysis/`.

## Reproduce

```bash
python3 scripts/amar_graph.py \
  --amar amar.txt \
  --mw   /path/to/csl-orig/v02/mw/mw.txt \
  --outdir analysis
```

MW is read locally from the sibling `csl-orig` checkout (read-only; csl-orig is
never written by this repo). Without `--mw`, coverage blocks are skipped.

## Method

- **Synsets** — every `<eid>N<syns><s>…</s>` line of `amar.txt` (5,590 synsets
  across 2,359 `<L>` entries; the *nānārtha* section packs several synonym rows
  per entry). Each token is split `lemma-genderTag` (the 15 gender tags of
  `gender_list.txt`, longest-match).
- **Nodes** — 9,027 distinct lemmas (gender stripped; gender tags are kept as
  node attributes in `analysis/amar_syngraph_nodes.tsv`).
- **Edges** — lemmas co-listed in one synset are joined (a clique per synset);
  edge weight = number of synsets the pair shares. 28,391 unique edges with
  28,741 edge instances.
- **Metrics** — components by BFS; global transitivity (3·triangles/triples,
  157,578 triangles); **exact diameter via iFUB** (Crescenzi et al.) on the
  largest component; average shortest path estimated from 200 sampled BFS
  sources; degree Gini; degree-preserving double-edge-swap null model
  (4·|E| accepted swaps) as the thesaurusness baseline.
- **MW coverage** — lemma matched against the 194,083 `<k1>` headwords of
  `mw.txt`, then unmatched lemmas probed against the full MW text (body
  attestance) and classified headword / body-only / absent.

## Headline metrics

| Metric | Value |
|---|---|
| Synsets (entries) | 5,590 (1,059 singletons) |
| Mean / median synset size | 2.51 / 2 |
| Nodes (distinct lemmas) | 9,027 |
| Unique edges (instances) | 28,391 (28,741) |
| Mean degree (max) | 6.29 (86) |
| Degree Gini | 0.595 |
| Components | 1,415 |
| Largest component | 4,955 nodes — 54.9% |
| **Diameter (largest comp., exact iFUB)** | **23** |
| Avg. shortest path (200-sample) | 7.67 |
| Global transitivity | 0.880 |
| Transitivity, rewired null | 0.0060 |
| Triangles | 157,578 |

## Components

The graph has **one giant component (4,955 nodes, 55%)** — the celestial /
divine / cosmic core of the kāṇḍas, all chained through shared synonyms —
plus 1,414 small ones (sizes 34, 25, 20, 19, 16, …): thematic vargas whose
vocabularies never overlap another varga's, and *nānārtha* singletons that no
second synset shares. This is the expected thesaurus signature: meaning-space
is one connected continent with many islands.

## Hubs (top 15 by degree)

| Lemma | Degree | Synsets |
|---|---|---|
| citraBAnu | 86 | 4 |
| viBAvasu | 86 | 4 |
| Aditya | 79 | 3 |
| puzkara | 69 | 12 |
| sarvajYa | 68 | 2 |
| viDu | 66 | 4 |
| go | 65 | **17** |
| BAnu | 64 | 4 |
| Siva | 63 | 3 |
| arka | 62 | 12 |
| Baga | 61 | 9 |
| aRqaja | 61 | 5 |
| aruRa | 61 | 6 |
| ISvara | 60 | 2 |
| BIma | 59 | 2 |

Two hub types: **clique centres** with huge synsets (Aditya sits in synsets
of 26 and 55 members — the great sun-synonym list — giving degree 79 from
just 3 synsets) and **bridge lemmas** appearing in many small synsets (`go` —
17 synsets, the celebrated polysemy of "cow/speech/ray/water…"; `puzkara`,
`arka` — 12 each). 2,190
lemmas (24.3%) occur in ≥2 synsets: they are the cross-varga connective
tissue, exactly what an alphabetical dictionary cannot record.

## Diameter

Exact diameter of the largest component = **23** (iFUB-certified, not an
estimate). A path of length 23 chains, e.g., a solar synonym out through the
divine core to a remote technical varga term. The tail is long because the
component absorbs chains of loosely-related synonym lists; the *typical*
distance is short (ASPL ≈ 7.7).

## Coverage vs the MW sense network

| Layer | Lemmas | Share |
|---|---|---|
| MW headword (`<k1>`, exact) | 8,272 | 91.64% |
| + attested in MW body text | +136 | 93.14% |
| Absent from MW entirely | 619 | 6.86% |

The 619 absent lemmas are dominated by orthographic and lemma-form variants —
e.g. AMAR `BujaNga` where MW lemmatizes `BujaMga` (nasal-encoding variants),
sandhi-resolved stems, and AMAR-specific compounds MW never lemmatizes
(`purandara`, `mftyuYjaya`, `DanaYjaya`, `vihaNga`, …). A full 25-lemma sample
is in `analysis/amar_syngraph_metrics.json` (`uncovered_absent_sample`); the
complete per-lemma MW flag is a column of `analysis/amar_syngraph_nodes.tsv`.

## Thesaurusness vs alphabetical dictionaries

An alphabetical dictionary (MW, PW) is a *list*: its headword set, viewed as a
co-listing graph, has **no edges at all** by construction — every lemma is its
own entry, bridge share 0, no components beyond singletons. The Amarakośa
scores on three axes an alphabetical dictionary scores 0 or n/a on:

| Measure | AMAR | Alphabetical dictionary |
|---|---|---|
| Bridge-lemma share (≥2 synsets) | **0.243** | 0 (by construction) |
| Mean synset size (synonym redundancy) | **2.51** | n/a — no synsets |
| Transitivity vs degree-preserving null | **0.880 vs 0.0060 (146×)** | no graph to rewire |

The 146× transitivity lift over the rewired null is the structural signature
of onomasiological organisation: co-listed synonyms form dense, closed
communities that a random graph with the identical degree sequence cannot
reproduce. This ratio — not any raw count — is the transferable
"thesaurusness" coefficient: it can be computed for any dictionary with
synonym-set markup (e.g. any future *kośa* ingest). For alphabetical material
without synonym markup there is no co-listing graph to lift in the first
place — which is the point.

## Files

| File | Contents |
|---|---|
| `scripts/amar_graph.py` | the analysis (stdlib only, seeded, CLI above) |
| `analysis/amar_syngraph_metrics.json` | every metric, machine-readable |
| `analysis/amar_syngraph_nodes.tsv` | lemma, degree, #synsets, genders, MW flag |
| `analysis/amar_syngraph_edges.tsv.gz` | u, v, weight (28,391 rows) |

## Caveats

- Lemma identity is the SLP1 string after gender-tag stripping; homonymic
  lemmas sharing a string merge into one node (conservative: merges only
  *add* edges between true synonyms).
- Anusvāra/nasal orthography is not normalised before the MW match — the
  91.6% headword coverage is therefore a **lower bound** (see the `BujaNga`
  class above).
- Diameter is exact for the largest component only; small components are
  trees or near-trees with diameter ≤ a few steps (sizes in JSON).

_Dr. Mārcis Gasūns_
