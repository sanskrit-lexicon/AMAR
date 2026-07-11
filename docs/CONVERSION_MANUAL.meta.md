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

## Related documents

- [README.md](https://github.com/sanskrit-lexicon/AMAR/blob/main/README.md) — repo overview, timeline, issue taxonomy
- [CLAUDE.md](https://github.com/sanskrit-lexicon/AMAR/blob/main/CLAUDE.md) — code contract: data-format tag table, downstream integration, issue conventions
- [csl-orig correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md) — canonical post-publish correction procedure
- [changelog.md](https://github.com/sanskrit-lexicon/AMAR/blob/main/changelog.md) — dated maintenance snapshots

## Revision history

| Date | Change | By |
|---|---|---|
| 11-07-2026 | Initial manual + this metadoc authored (H531); pipeline re-run and all numbers verified live | Fable 5 (`claude-fable-5`) |

_Dr. Mārcis Gasūns_
