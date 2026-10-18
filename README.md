# Quiet Weave

Read the room as cloth.

A host lays out four to twelve time bands, writes the standard that counts as quiet enough, and loads three to six observations from people or records that know the space. GenLayer validators classify every band as `QUIET`, `CONDITIONAL`, or `LOUD` with exact observation indexes. Contract code then finds the longest contiguous usable run, prefers the run containing more fully quiet bands, and returns `WINDOW` or `NO_WINDOW` without asking the model to choose the winner.

## Loom mechanics

- `set_loom` freezes the ordered bands, observation spools, minimum useful length, timezone, and standard.
- `weave_window` is permissionless. Consensus must return the complete ordered band vector.
- Deterministic code derives the selected run from those classifications.
- `pin_window` belongs to the owner and is available only for a real window.
- `unthread` lets the owner cancel before consensus.

Every observation is stored directly, attributed by its frozen index, and bound into a canonical SHA-256 input digest. No hosted fixture or raw GitHub URL is part of the visitor journey.

## Boundary

Quiet Weave coordinates ordinary community-space use. It is not a calibrated acoustic survey, accessibility guarantee, employment rule, or safety system. The bundled room observations are synthetic rehearsal material.

## Bench test

```text
python -m pytest -q
genvm-lint lint contracts/contract.py
```

StudioNet deployment and live canonical readback are recorded after release.
