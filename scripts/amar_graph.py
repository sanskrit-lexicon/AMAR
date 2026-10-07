#!/usr/bin/env python3
"""H6057 — Amarakosha as a synonymy graph.

Builds an undirected co-listing graph from the CDSL-format amar.txt:
every entry (<eid>N<syns><s>lemma-gender,lemma-gender,...</s>) is a synset;
lemmas co-listed in one synset are joined by an edge (weight = shared synsets).

Metrics: connected components, degree hubs (+Gini), global transitivity,
exact diameter of the largest component (iFUB), sampled average shortest
path, MW headword coverage, and a thesaurusness block (bridge-lemma share,
synset redundancy, transitivity vs a degree-preserving rewired null).

Pure standard library; deterministic (fixed seed). Usage:

    python scripts/amar_graph.py [--amar amar.txt]
                                 [--mw /path/to/csl-orig/v02/mw/mw.txt]
                                 [--outdir analysis]
                                 [--skip-null]   # skip rewiring null model
"""

import argparse
import gzip
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict, deque

SEED = 20261004  # H6057
ASPL_SAMPLES = 200  # BFS sources for average-shortest-path estimate

# Gender suffixes of the AMAR annotation (gender_list.txt inventory, 16 tags).
GENDER_TAGS = [
    "ajYAta", "puMstrI", "puMklI", "strIklI", "strIba", "strIdvi",
    "puMba", "puMdvi", "puMdvaya", "klIdvi", "klIa", "puM", "strI",
    "klI", "tri", "a",
]
GENDER_TAGS.sort(key=len, reverse=True)  # longest-match first


def split_lemma(token):
    """'svarga-puM' -> ('svarga', 'puM'); bare token -> (token, None)."""
    for tag in GENDER_TAGS:
        if token.endswith("-" + tag):
            return token[: -(len(tag) + 1)], tag
    return token, None


def parse_synsets(amar_path):
    """Return (synsets, stats): each synset is an ordered list of (lemma, gender)."""
    syn_re = re.compile(r"<eid>\d+<syns><s>([^<]+)</s>")
    synsets = []
    n_eid = 0
    with open(amar_path, encoding="utf-8") as fh:
        for line in fh:
            if "<eid>" not in line:
                continue
            n_eid += 1
            m = syn_re.search(line)
            if not m:
                continue
            toks = [t.strip() for t in m.group(1).split(",") if t.strip()]
            synsets.append([split_lemma(t) for t in toks])
    return synsets, n_eid


def build_graph(synsets):
    """Nodes = distinct lemmas; edges = co-listing (clique per synset, deduped)."""
    node_synsets = defaultdict(set)   # lemma -> {synset idx}
    node_genders = defaultdict(set)   # lemma -> gender tags
    edge_weight = Counter()           # frozenset({u,v}) -> #synsets shared
    for i, syn in enumerate(synsets):
        lemmas = []
        for lem, gen in syn:
            node_synsets[lem].add(i)
            if gen:
                node_genders[lem].add(gen)
            lemmas.append(lem)
        uniq = sorted(set(lemmas))
        for a_i in range(len(uniq)):
            for b_i in range(a_i + 1, len(uniq)):
                edge_weight[frozenset((uniq[a_i], uniq[b_i]))] += 1
    adj = defaultdict(set)
    for e in edge_weight:
        u, v = tuple(e)
        adj[u].add(v)
        adj[v].add(u)
    return node_synsets, node_genders, edge_weight, adj


def components(adj):
    """List of components (as lists) sorted by size desc."""
    seen = set()
    comps = []
    for start in adj:
        if start in seen:
            continue
        comp, q = [], deque([start])
        seen.add(start)
        while q:
            n = q.popleft()
            comp.append(n)
            for nb in adj[n]:
                if nb not in seen:
                    seen.add(nb)
                    q.append(nb)
        comps.append(comp)
    comps.sort(key=len, reverse=True)
    return comps


def bfs_dist(adj, src):
    dist = {src: 0}
    q = deque([src])
    while q:
        n = q.popleft()
        d = dist[n] + 1
        for nb in adj[n]:
            if nb not in dist:
                dist[nb] = d
                q.append(nb)
    return dist


def ifub_diameter(adj, nodes, cap=4000):
    """Exact diameter via iFUB (Crescenzi et al. 2010) on subgraph `nodes`.
    Falls back to a certified lower bound if > cap nodes need scanning."""
    sub = {n: adj[n] & set(nodes) for n in nodes}
    start = max(nodes, key=lambda n: len(sub[n]))
    dist0 = bfs_dist(sub, start)
    ecc0 = max(dist0.values())
    levels = defaultdict(list)
    for n, d in dist0.items():
        levels[d].append(n)
    lb, scanned = ecc0, 0
    i = ecc0
    while 2 * i > lb:
        for v in levels[i]:
            lb = max(lb, max(bfs_dist(sub, v).values()))
            scanned += 1
            if scanned > cap:
                return lb, False  # certified lower bound only
        i -= 1
    return lb, True


def transitivity(adj):
    """Global clustering: 3*triangles / connected triples.
    The loop below counts each triangle once per each of its 3 vertices,
    i.e. `triangles` = 3T, so triangles/triples = 3T/triples directly."""
    triangles = triples = 0
    for v in adj:
        nbs = list(adj[v])
        k = len(nbs)
        if k < 2:
            continue
        triples += k * (k - 1) // 2
        for i in range(k):
            ni = adj[nbs[i]]
            for j in range(i + 1, k):
                if nbs[j] in ni:
                    triangles += 1
    return (triangles / triples) if triples else 0.0, triangles // 3, triples


def gini(values):
    v = sorted(values)
    n, s = len(v), sum(v)
    if n == 0 or s == 0:
        return 0.0
    cum = 0.0
    for i, x in enumerate(v, 1):
        cum += i * x
    return (2 * cum) / (n * s) - (n + 1) / n


def rewire_null(adj, n_swaps_mult=4):
    """Degree-preserving double-edge-swap null model (simple graph)."""
    rng = random.Random(SEED)
    edges = [tuple(e) for e in adj_to_edges(adj)]
    eset = set(frozenset(e) for e in edges)
    n_adj = {n: set(adj[n]) for n in adj}
    accepted, target = 0, n_swaps_mult * len(edges)
    attempts = 0
    max_attempts = 200 * target
    while accepted < target and attempts < max_attempts:
        attempts += 1
        (a, b), (c, d) = edges[rng.randrange(len(edges))], edges[rng.randrange(len(edges))]
        if len({a, b, c, d}) < 4:
            continue
        e1, e2 = frozenset((a, d)), frozenset((c, b))
        if e1 in eset or e2 in eset:
            continue
        eset.remove(frozenset((a, b)))
        eset.remove(frozenset((c, d)))
        eset.add(e1)
        eset.add(e2)
        n_adj[a].discard(b); n_adj[a].add(d)
        n_adj[b].discard(a); n_adj[b].add(c)
        n_adj[c].discard(d); n_adj[c].add(b)
        n_adj[d].discard(c); n_adj[d].add(a)
        edges[edges.index((a, b))] = (a, d)
        edges[edges.index((c, d))] = (c, b)
        accepted += 1
    return n_adj


def adj_to_edges(adj):
    seen = set()
    for u in adj:
        for v in adj[u]:
            e = frozenset((u, v))
            if e not in seen:
                seen.add(e)
                yield tuple(e)


def load_mw_keys(mw_path):
    """MW headwords: <k1>KEY<k2> ... on head lines. Returns (raw, normalized)."""
    k1_re = re.compile(r"<k1>([^<]*)<k2>")
    strip = str.maketrans("", "", "/\\^~%\"'|")
    raw = set()
    with open(mw_path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if "<k1>" not in line:
                continue
            m = k1_re.search(line)
            if m:
                raw.add(m.group(1))
    norm = {k.translate(strip) for k in raw}
    return raw, norm


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--amar", default="amar.txt")
    ap.add_argument("--mw", default="/Users/mac/Documents/GitHub/csl-orig/v02/mw/mw.txt")
    ap.add_argument("--outdir", default="analysis")
    ap.add_argument("--skip-null", action="store_true")
    args = ap.parse_args()

    rng = random.Random(SEED)
    synsets, n_eid = parse_synsets(args.amar)
    sizes = [len(s) for s in synsets]
    singletons = sum(1 for s in sizes if s == 1)

    node_synsets, node_genders, edge_weight, adj = build_graph(synsets)
    nodes = sorted(adj)
    n_nodes, n_edges = len(nodes), len(edge_weight)
    degrees = {n: len(adj[n]) for n in nodes}

    comps = components(adj)
    comp_sizes = [len(c) for c in comps]
    largest = set(comps[0])

    hubs = sorted(nodes, key=lambda n: (-degrees[n], n))[:25]

    trans, n_tri, n_tri_trip = transitivity(adj)
    diam, exact = ifub_diameter(adj, largest)

    # sampled average shortest path length over the largest component
    sub = {n: adj[n] & largest for n in largest}
    aspl_vals = []
    for src in rng.sample(sorted(largest), min(ASPL_SAMPLES, len(largest))):
        d = bfs_dist(sub, src)
        aspl_vals.append(sum(d.values()) / len(d))
    aspl = sum(aspl_vals) / len(aspl_vals)

    # MW coverage
    mw_exact = mw_norm = None
    covered_exact = covered_norm = 0
    uncovered = []
    if args.mw:
        try:
            mw_raw, mw_normalized = load_mw_keys(args.mw)
            mw_exact, mw_norm = mw_raw, mw_normalized
        except OSError as exc:
            print(f"WARN: cannot read MW ({exc}); coverage skipped", file=sys.stderr)
    if mw_exact is not None:
        strip = str.maketrans("", "", "/\\^~%\"'|")
        for n in nodes:
            if n in mw_exact:
                covered_exact += 1
            elif n.translate(strip) in mw_norm:
                covered_norm += 1
            else:
                uncovered.append(n)

    # Secondary pass: do the uncovered lemmas at least occur anywhere in the
    # MW text (attested in body/compounds) or are they absent from MW entirely?
    uncovered_in_body, uncovered_absent = [], []
    if mw_exact is not None and uncovered:
        with open(args.mw, encoding="utf-8", errors="replace") as fh:
            mw_text = fh.read()
        for n in uncovered:
            (uncovered_in_body if n in mw_text else uncovered_absent).append(n)
        del mw_text

    # thesaurusness
    bridge = [n for n in nodes if len(node_synsets[n]) >= 2]
    bridge_share = len(bridge) / n_nodes

    null_trans = None
    if not args.skip_null:
        null_adj = rewire_null(adj)
        null_trans, _, _ = transitivity(null_adj)

    metrics = {
        "handoff": "H6057",
        "seed": SEED,
        "source": args.amar,
        "entries_total": n_eid,
        "synsets": len(synsets),
        "synsets_singleton": singletons,
        "synset_size": {
            "mean": sum(sizes) / len(sizes),
            "median": sorted(sizes)[len(sizes) // 2],
            "max": max(sizes),
        },
        "nodes": n_nodes,
        "edges_unique": n_edges,
        "edge_multiplicity_total": sum(edge_weight.values()),
        "components": {
            "count": len(comps),
            "sizes_top10": comp_sizes[:10],
            "largest_share": comp_sizes[0] / n_nodes,
        },
        "degree": {
            "max": max(degrees.values()),
            "mean": 2 * n_edges / n_nodes,
            "gini": gini(list(degrees.values())),
            "top25": [[h, degrees[h], len(node_synsets[h])] for h in hubs],
        },
        "transitivity": trans,
        "triangles": n_tri,
        "connected_triples": n_tri_trip,
        "diameter_largest": diam,
        "diameter_exact": exact,
        "aspl_largest_sampled": round(aspl, 4),
        "aspl_samples": len(aspl_vals),
        "mw_coverage": None if mw_exact is None else {
            "mw_headwords": len(mw_exact),
            "covered_exact": covered_exact,
            "covered_after_accent_strip": covered_norm,
            "uncovered": len(uncovered),
            "uncovered_in_mw_body": len(uncovered_in_body),
            "uncovered_absent_from_mw": len(uncovered_absent),
            "uncovered_absent_sample": sorted(uncovered_absent, key=lambda n: -degrees[n])[:25],
            "share_exact": covered_exact / n_nodes,
            "share_normalized": (covered_exact + covered_norm) / n_nodes,
            "share_headword_or_body": (covered_exact + covered_norm + len(uncovered_in_body)) / n_nodes,
        },
        "thesaurusness": {
            "bridge_lemma_share": bridge_share,
            "bridge_lemmas": len(bridge),
            "mean_synset_size": sum(sizes) / len(sizes),
            "transitivity": trans,
            "transitivity_null_rewired": null_trans,
            "transitivity_lift_vs_null": (trans / null_trans) if null_trans else None,
        },
    }
    import os
    os.makedirs(args.outdir, exist_ok=True)

    with open(f"{args.outdir}/amar_syngraph_metrics.json", "w", encoding="utf-8") as fh:
        json.dump(metrics, fh, ensure_ascii=False, indent=2, sort_keys=False)
        fh.write("\n")

    with open(f"{args.outdir}/amar_syngraph_nodes.tsv", "w", encoding="utf-8") as fh:
        fh.write("lemma\tdegree\tn_synsets\tgenders\tmw_exact\n")
        for n in sorted(nodes, key=lambda x: (-degrees[x], x)):
            mw_flag = "" if mw_exact is None else ("1" if n in mw_exact else "0")
            fh.write(f"{n}\t{degrees[n]}\t{len(node_synsets[n])}\t"
                     f"{'|'.join(sorted(node_genders[n]))}\t{mw_flag}\n")

    with gzip.open(f"{args.outdir}/amar_syngraph_edges.tsv.gz", "wt", encoding="utf-8") as fh:
        fh.write("u\tv\tweight\n")
        for e, w in sorted(edge_weight.items(), key=lambda kv: -kv[1]):
            u, v = sorted(e)
            fh.write(f"{u}\t{v}\t{w}\n")

    print(json.dumps({k: metrics[k] for k in
                      ("nodes", "edges_unique", "components", "diameter_largest",
                       "diameter_exact", "transitivity", "mw_coverage",
                       "thesaurusness")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
