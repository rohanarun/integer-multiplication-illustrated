# Integer multiplication, illustrated

An independent illustrated reading edition of OpenAI's *Integer multiplication below n log n* (September 23, 2026).

## Read the documents

- **[Illustrated guide (17 pages)](output/pdf/illustrated-guide.pdf)** — ten new figures, worked examples, explanations of the main ideas, and a notation glossary.
- **[Expanded paper (92 pages)](output/pdf/expanded-paper.pdf)** — the explanations interleaved with the original proofs and bibliography.
- **[Download the editable package](output/integer-multiplication-editable-package.zip)** — LaTeX sources, figures, and example checks.

The guide starts with ordinary multiplication and explains convolution, data movement, borrowed workspace, common frames, recursive savings, transform layers, and exact recovery. It is an introductory technical guide: the later sections still require mathematical effort and are not a complete prerequisite-free explanation for a general reader.

![Borrowing and restoring an unknown scratch value](figures/03-restoration.png)

## Scope

This edition explains the original paper at commit [`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Integer-multiplication-below-n-log-n-September-23-2026). Its displayed exponent saving is the original `2^-182`; this is not a live record of later community improvements.

The original paper states its result as a theorem. This edition does not independently validate that theorem. It distinguishes source claims, pedagogical calculations, and the conditional interfaces retained by the [community research repository](https://github.com/CrocSwap/integer-mult-bounds). It is not an official OpenAI revision or endorsement, a practical multiplication benchmark, or a full Lean formalization.

## Contents

| Location | Contents |
| --- | --- |
| `explanations/` | Editable explanatory chapters |
| `figures/` | Ten vector PDF figures and PNG previews |
| `original/` | Unmodified original manuscript sources |
| `illustrated-guide.tex` | Guide entry point |
| `expanded-paper.tex` | Annotated-paper entry point |
| `source-manifest.json` | Pinned upstream URLs and hashes |
| `example-checks.json` | Exact pedagogical calculations |
| `verification.json` | PDF integrity and rendering checks |

## Rebuild

Use Python with NumPy and Matplotlib, plus Tectonic. The optional renderer also uses PyMuPDF and Pillow.

```sh
python3 generate_figures.py
python3 build_editions.py
tectonic --keep-logs -o output/pdf illustrated-guide.tex
tectonic --keep-logs -o output/pdf expanded-paper.tex
python3 verify_and_render.py
```

All outputs, temporary directories, caches, and previews should stay on the mounted writable external SSD in the author's local environment. See [README.txt](README.txt) for build details and storage guidance.

The original source hashes, convolution and carry example, restoration identity on 343 integer triples, two-axis butterfly, and seven original rational margins were checked. All pages of both PDFs were rendered and visually reviewed. These checks concern the documents and illustrative calculations, not the full asymptotic theorem.

## Attribution and license

Original manuscript: OpenAI, September 23, 2026. Its bibliography and source attribution are preserved. Added explanations, figures, and scripts were prepared with substantial OpenAI Codex assistance on October 12, 2026. See [NOTICE](NOTICE) and the [Apache-2.0 license](LICENSE).
