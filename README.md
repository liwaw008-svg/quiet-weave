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

## StudioNet release

- App: [quiet-weave.pages.dev](https://quiet-weave.pages.dev/)
- Contract: [`0xeEC7e5Ff9071Ac62e07ab7aC562e6C6774f2EF2e`](https://explorer-studio.genlayer.com/address/0xeEC7e5Ff9071Ac62e07ab7aC562e6C6774f2EF2e)
- Deployment: [`0xd013c832d30455272edde7d02ffa208059c95d8d1cecff80574785dcba82c2d3`](https://explorer-studio.genlayer.com/transactions/0xd013c832d30455272edde7d02ffa208059c95d8d1cecff80574785dcba82c2d3)

The exact source digest and canonical lifecycle readback are recorded in `deployment.json` and `evidence/live-run.json`.
