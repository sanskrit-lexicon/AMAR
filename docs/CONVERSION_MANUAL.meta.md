# CONVERSION_MANUAL.md — metadoc

_Created: 11-07-2026 · Last updated: 11-07-2026_


Companion record for
[docs/CONVERSION_MANUAL.md](https://github.com/sanskrit-lexicon/AMAR/blob/main/docs/CONVERSION_MANUAL.md)
— purpose, provenance, improvement backlog, and revision history of the manual
itself (not of the pipeline it documents).

## Purpose

Give a new operator/contributor everything needed to re-run, verify, and extend
the AMAR OCR→CDSL conversion pipeline **without reading the source code**. The
acceptance test is operational: a newcomer runs the repo from the manual alone
and can interpret every console line the pipeline prints.

## Audience

- **Operators** re-running the conversion after a source or script change
  (cheat-sheet, walkthrough, symptom table);
- **Maintainers** modifying the scripts (appendix: per-script breakdown,
  invariants, latent defects);
- **CDSL integrators** wiring `amar.txt` downstream (stage 4 checklist).

## Provenance

- Authored 11-07-2026 by Fable 5 (`claude-fable-5`) executing handoff
  [H531-Fable_AMAR_conversion_pipeline_manual_10.07.26.md](https://github.com/gasyoun/Uprava/blob/main/handoffs/H531-Fable_AMAR_conversion_pipeline_manual_10.07.26.md)
  (manual-coverage census batch H501–H531).
- Modelled on the gold-standard operator manual
  [RussianRamayana Litpam-Indexator MANUAL.md](https://github.com/gasyoun/RussianRamayana/blob/main/Litpam-Indexator/docs/indesign-pipeline/MANUAL.md).
- All quoted numbers were measured on a live `sh redo.sh` run against commit
  `8af150e` data on 11-07-2026: round-trip diff 0; `1155 changes in info_1`;
  13,455 → 15,814 lines; 2,359 `<L>` entries; output reproduces the committed
  [amar.txt](https://github.com/sanskrit-lexicon/AMAR/blob/main/amar.txt) with
  0 content-diff lines. The CRLF phantom-diff counts (26,912 / 31,630) were
  observed on a `core.autocrlf true` Windows checkout the same day.

## Ranked improvement backlog

| # | Item | Status |
|---|---|---|
| 1 | Fix the latent `info_1` silent line drop (`newlines.append` → `newlines.append(line)`) in [addinfo.py](https://github.com/sanskrit-lexicon/AMAR/blob/main/addinfo.py), plus the mislabelled `info_2` print in `info_3` — then simplify manual §defects 1–2 to "fixed" | open |
| 2 | Add `set -e` (or per-step exit checks) to [redo.sh](https://github.com/sanskrit-lexicon/AMAR/blob/main/redo.sh) so a failed stage aborts the run, and make the round-trip check fail loudly on non-zero | open |
| 3 | A one-command selftest (script or CI job) asserting the four numeric invariants of manual §Invariants, so regressions surface without a human reading console output | open |
| 4 | Decide `;p{N}` page-break handling (`info_2`) with the XML build, or remove the dead pass — tracked in spirit by issue [#1](https://github.com/sanskrit-lexicon/AMAR/issues/1)-adjacent Structured Data work | open |
| 5 | Modernise `codecs.open()` → `open(..., encoding='utf-8')` across the four scripts to silence DeprecationWarnings | open |
| 6 | Fix `gender_list.py` name-table typos ("kIba", "musculine"), fill the `'?'` glosses, and regenerate [gender_list.txt](https://github.com/sanskrit-lexicon/AMAR/blob/main/gender_list.txt) | open |

## Known limitations

- The manual documents the pipeline as-is, including deliberately unfixed
  defects (appendix list); it does not cover the historical 2024 one-time
  import steps that produced `amar1.txt`.
- Stage 4's first-time CDSL wiring checklist is summarised from
  [CLAUDE.md](https://github.com/sanskrit-lexicon/AMAR/blob/main/CLAUDE.md) and
  has not been re-executed (AMAR is already integrated); treat it as a pointer,
  not a verified walkthrough.
- Verified on Windows (Git Bash) only, 11-07-2026; the CRLF section is
  inapplicable on LF-native systems.

## Intended use / known misuse

- **For:** an operator or maintainer who needs to re-run
  [redo.sh](https://github.com/sanskrit-lexicon/AMAR/blob/main/redo.sh)
  end-to-end, verify its console output against the checkpoint table, diagnose
  a failure via the symptom table, or extend `addinfo.py` with a new `info_N`
  pass — all without reading the four pipeline scripts first. It is also the
  reference for a CDSL integrator confirming what `amar.txt`'s tags mean before
  wiring stage 4 downstream.
- **Known/likely misuse:**
  - Treating stage 4's "first-time CDSL wiring checklist" as a verified,
    re-executable runbook — it is a summary pointer to
    [CLAUDE.md](https://github.com/sanskrit-lexicon/AMAR/blob/main/CLAUDE.md)
    for a step that has not been re-run since AMAR's original onboarding (see
    Known limitations above).
  - Reading the manual as documentation of the *editorial content* of the
    Amarakośa itself, or of `amar1.txt`'s 2024 one-time import steps — it
    documents only the mechanical OCR→CDSL conversion pipeline that runs on
    top of that already-imported source.
  - Assuming the "Observed defects and latent traps" list describes bugs that
    corrupt current output — invariant 3 in the appendix proves zero net loss
    on present data; the list flags *latent* risk for future data shapes, not
    an active defect.
  - Skipping `--strip-trailing-cr` on a Windows/`core.autocrlf true` checkout
    and concluding the round-trip or reproducibility checks failed — that is
    the documented CRLF phantom-diff, not a real regression.
  - Using this manual as a substitute for the
    [csl-orig correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)
    when a *published* text error needs fixing — this manual covers re-running
    the conversion pipeline, not the change-file correction process for
    already-published CDSL text.

## Maintenance & sunset plan

The manual is kept alive by whoever next touches the AMAR conversion pipeline
(`redo.sh`, `convert.py`, `addinfo.py`, `gender_list.py`, or the
`transcoder/` tables) in the `sanskrit-lexicon/AMAR` repo — there is no
separate owning process or scheduled job; it updates opportunistically when a
script changes or a documented number (line counts, change counts) drifts.
The six items in the Ranked improvement backlog above are the concrete
maintenance queue; item 1 (the `info_1` silent-line-drop fix) and item 2
(`set -e` in `redo.sh`) are the ones most likely to force a manual update if
picked up. "Archived/ended" for this document means one of: the AMAR pipeline
itself is retired (the dictionary is fully migrated to a different conversion
path and `redo.sh` no longer runs), or the manual is superseded by a newer
document covering the same pipeline — in either case this metadoc's
Deprecation status below should flip and the file should move under an
`archive/` folder per the org's `/handoff-archive`-style convention. No sunset
is currently scheduled or anticipated.

## Deprecation status

`active`

## Related documents

- [README.md](https://github.com/sanskrit-lexicon/AMAR/blob/main/README.md) — repo overview, timeline, issue taxonomy
- [CLAUDE.md](https://github.com/sanskrit-lexicon/AMAR/blob/main/CLAUDE.md) — code contract: data-format tag table, downstream integration, issue conventions
- [csl-orig correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md) — canonical post-publish correction procedure
- [changelog.md](https://github.com/sanskrit-lexicon/AMAR/blob/main/changelog.md) — dated maintenance snapshots

## Revision history

| Date | Change | By |
|---|---|---|
| 11-07-2026 | Initial manual + this metadoc authored (H531); pipeline re-run and all numbers verified live | Fable 5 (`claude-fable-5`) |
| 11-07-2026 | template v2 backfill (H663) | Sonnet 5 (`claude-sonnet-5`) |

_Dr. Mārcis Gasūns_
