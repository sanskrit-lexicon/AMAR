# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AMAR** converts the *Amarakośa* (Amarasiṃha's *Nāmaliṅgānuśāsana*, a classical Sanskrit thesaurus) from its OCR source into CDSL-compatible format for integration into the Cologne Digital Sanskrit Lexicon. The processed output `amar.txt` is destined for `csl-orig/v02/amar/amar.txt`.

The Amarakośa is a Sanskrit–Sanskrit kośa (synonym dictionary) organised into three kāṇḍas (chapters), each subdivided into vargas (thematic groups). Entries list synonyms with gender markers in SLP1 transliteration.

## Architecture

| File/Dir | Purpose |
|---|---|
| `amar1.txt` | OCR source from drdhaval2785/sanskrit-lexica-ocr (Devanagari) |
| `convert.py` | Converts Devanagari (`amar1.txt`) → SLP1 (`temp_amar0.txt`) and back for invertibility check |
| `addinfo.py` | Adds CDSL markup (`<L>`, `<pc>`, `<info kvvv=...>`, `<eid>`, `<syns>`, `<LEND>`) to produce `temp_amar.txt` |
| `gender_list.py` | Generates a frequency list of gender tags from `amar.txt` |
| `gender_list.txt` | Output of `gender_list.py` — gender frequency list |
| `transcoder.py` | SLP1 ↔ Devanagari ↔ IAST transcoding engine |
| `transcoder/` | Tables for the transcoder (per-script CSV files) |
| `redo.sh` | Orchestration: convert → check invertibility → addinfo → prompt for copy |
| `amar.txt` | Processed CDSL-format output (current published version) |
| `CITATION.cff` | Academic citation metadata (CFF 1.2.0) |
| `LICENSE` | CC-BY-SA-4.0 |

## Pipeline

```bash
sh redo.sh
# Produces temp_amar.txt; then manually copy to csl-orig:
cp temp_amar.txt ../csl-orig/v02/amar/amar.txt
```

Steps inside `redo.sh`:
1. `python convert.py deva,slp1 amar1.txt temp_amar0.txt` — Devanagari → SLP1
2. `python convert.py slp1,deva temp_amar0.txt temp_amar0_deva.txt` — back-convert for round-trip check
3. `diff amar1.txt temp_amar0_deva.txt | wc -l` — must be 0
4. `python addinfo.py temp_amar0.txt temp_amar.txt` — add CDSL structural markup

## Data Format

Every dictionary entry in `amar.txt` follows this structure:

| Tag/pattern | Role | Example |
|---|---|---|
| `;METADATA` / `;CONTENT` | File-level section markers | `;CONTENT` |
| `;k{...}` | Kāṇḍa (chapter) header | `;k{<s>praTamaM kARqam</s>}` |
| `;v{...}` | Varga (thematic group) header | `;v{<s>svargavargaH</s>}` |
| `<L>N<pc>` | Entry begin with line number N | `<L>1<pc>` |
| `<info kvvv="..."/>` | Kāṇḍa/Varga/Upavarga annotation | `<info kvvv="<s>praTamaM kARqam</s>, <s>svargavargaH</s>"/>` |
| `<eid>N<syns>...` | Entry ID and synonym list with gender tags | `<eid>1<syns><s>svar-a,svarga-puM,...` |
| `<s>...</s>` | Sanskrit text in SLP1 transliteration | `<s>svargavargaH</s>` |
| `<LEND>` | Entry end | `<LEND>` |
| `;c{...}` | Commentary / section caption | `;c{<s>aTa svargavargaH .</s>}` |
| `;p{N}` | Page break marker | `;p{42}` |

Gender codes (appended to synonym with `-`): `puM` (m.), `strI` (f.), `klI` (n.), `a` (adjective/avyaya).

### Annotated example entry

```
<L>1<pc>
<info kvvv="<s>praTamaM kARqam</s>, <s>svargavargaH</s>"/>
<eid>1<syns><s>svar-a,svarga-puM,nAka-puM,...,trivizwapa-klI</s>
<s>svaravyayaM svarganAkatridivatridaSAlayAH .</s>
<s>suraloko dyodivO dve striyAM klIbe trivizwapam .. 6 ..</s>
<LEND>
```

- `<L>1<pc>` — entry 1
- `<info kvvv=.../>` — belongs to kāṇḍa "praTamaM kARqam", varga "svargavargaH"
- `<eid>1<syns>...` — entry ID 1; synonyms follow with gender (`puM`=m, `a`=adj/avyaya, `klI`=n)
- `<s>...</s>` — the verse text in SLP1

## Key Commands

```bash
# Full pipeline
sh redo.sh

# Convert Devanagari source to SLP1 only
python convert.py deva,slp1 amar1.txt temp_amar0.txt

# Add CDSL markup
python addinfo.py temp_amar0.txt temp_amar.txt

# Generate gender frequency list
python gender_list.py amar.txt gender_list.txt
```

## Dependencies

- **Python 3** (standard library only; no pip packages required)
- `amar1.txt` (Devanagari OCR source, included in repo)
- `transcoder/` directory (included in repo)
- **csl-orig** sibling repo — target for the processed `amar.txt`

## Downstream Integration

After producing `temp_amar.txt`:
1. Copy to `../csl-orig/v02/amar/amar.txt`
2. Create `csl-orig/amar/amar-meta2.txt`, `amar_hwextra.txt`, `amarheader.xml`
3. Edit `csl-pywork/dictparms.py` and `inventory.txt` to add AMAR entry
4. Edit `csl-websanlexicon/dictparms.py` and create `distinctfiles/amar/` tree

## Encoding

- Source (`amar1.txt`): UTF-8 NFC, Devanagari script
- Processed (`amar.txt`): UTF-8 NFC, SLP1 transliteration inside `<s>...</s>` tags
- Round-trip verified: `amar1.txt` → SLP1 → Devanagari produces zero diff lines

## GitHub Issue Conventions

Issues follow the Sanskrit Lexicon taxonomy (see org-level CLAUDE.md):

### Type labels (`#0075ca`)
`link-target` | `link-splitting` | `markup` | `text-correction` | `content-enhancement` | `encoding` | `scan-quality` | `bug` | `question`

### Severity labels
`minor` (`#e4e669`) | `medium` (`#fbca04`) | `hard` (`#d93f0b`)

### Milestones
| # | Title | Types |
|---|---|---|
| 1 | Dictionary to Book | `link-target`, `link-splitting` |
| 2 | Digitization Quality | `scan-quality`, `encoding`, `bug`, `text-correction` |
| 3 | Structured Data | `markup`, `question` |
| 4 | Major Enhancements | `content-enhancement` |
