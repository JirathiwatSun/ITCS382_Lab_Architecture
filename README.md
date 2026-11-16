# ITCS382 Lab: Intended and Implemented Architecture

Individual lab work comparing package diagrams (intended architecture) with the real package dependencies reported by `jdeps` (implemented architecture).

- `parcelpoint-h2/` is the ParcelPoint starter project used in Parts A and B.
- `submission/` holds the quiz answers (`Q1`–`Q4`), the jdeps evidence and the rendered Mermaid diagrams.
- `Lab_Architecture_Quiz_Answers.md` is the same answers in one Markdown file.

Part C checks the Project Phase 2 code of team qwerty ([ICT-Mahidol/2026-ITCS382-Sec1-Gemini8](https://github.com/ICT-Mahidol/2026-ITCS382-Sec1-Gemini8)), commit `bd2d68c` (16 Nov 2026). That team repo is not included here.

To reproduce Part A:

```
cd parcelpoint-h2
mvn package
jdeps -verbose:package -filter:none -e "parcelpoint.*" target/classes
```
