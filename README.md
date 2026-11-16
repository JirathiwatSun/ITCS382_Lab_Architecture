# ITCS382 Lab: Intended and Implemented Architecture

Individual lab work comparing package diagrams (intended architecture) with the real package dependencies reported by `jdeps` (implemented architecture).

## Contents

- `parcelpoint-h2/` — ParcelPoint starter used in Parts A and B
- `submission/` — quiz answers to paste into MyCourses
  - `Q1_PartA.txt` … `Q4_AI_Declaration.txt`
  - `ITCS382_Architecture_Lab_Answers.pdf` — all answers in one PDF
  - `diagrams/` — Mermaid flowcharts rendered from jdeps
  - `evidence/` — raw jdeps logs

Part C checks team qwerty Phase 2 code ([ICT-Mahidol/2026-ITCS382-Sec1-Gemini8](https://github.com/ICT-Mahidol/2026-ITCS382-Sec1-Gemini8), commit `bd2d68c`). That team repo is not included here.

## Reproduce Part A

```
cd parcelpoint-h2
mvn package
jdeps -verbose:package -filter:none -e "parcelpoint.*" target/classes
```
