# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AMAR** converts the Amarakosha (Amarasimha's *Namalinganushasana*) from its OCR source into CDSL-compatible format for integration into the Cologne Digital Sanskrit Lexicon. The output `amar.txt` is placed in `csl-orig/v02/amar/amar.txt`.

## Architecture

| File | Purpose |
|---|---|
| `amar1.txt` | OCR source from drdhaval2785/sanskrit-lexica-ocr (Devanagari) |
| `convert.py` | Converts Devanagari (`amar1.txt`) → SLP1 (`temp_amar0.txt`) and back for invertability check |
| `addinfo.py` | Adds CDSL markup (`<L>`, `<pc>`, `<k1>`, etc.) to produce `temp_amar.txt` |
| `gender_list.py` / `gender_list.txt` | Gender information for noun entries |
| `transcoder.py` / `transcoder/` | SLP1 ↔ Devanagari transcoding tables |
| `redo.sh` | Orchestration: convert → check invertability → addinfo → prompt for copy |
| `amar.txt` | Processed CDSL-format output (copy of `temp_amar.txt`) |

### Pipeline

```bash
sh redo.sh
# Produces temp_amar.txt; then manually copy to csl-orig:
# cp amar.txt ../csl-orig/v02/amar/amar.txt
```

The pipeline verifies invertability: converting `amar1.txt` to SLP1 and back to Devanagari should produce zero diff lines.

## Dependencies

- **Python 3**
- `amar1.txt` (source OCR, included in repo)
- **csl-orig** sibling repo — target for the processed `amar.txt`
