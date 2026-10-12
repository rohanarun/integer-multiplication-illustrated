INTEGER MULTIPLICATION: ILLUSTRATED READING EDITION

Deliverables
  output/pdf/illustrated-guide.pdf  - the added explanation by itself
  output/pdf/expanded-paper.pdf    - explanations interleaved with original proofs
  figures/                        - ten new vector PDF figures and PNG previews
  explanations/                   - editable LaTeX explanatory chapters
  original/                       - unchanged original manuscript source
  source-manifest.json             - upstream source hashes and source URLs
  example-checks.json              - exact checks for pedagogical calculations

This is an independent reading edition, not an official OpenAI revision.
It explains the original September 23, 2026 paper at commit
adc7f1241b42e322a6451854ab7e4b4c146bf78a. Its displayed kappa is the original
2^-182, not a claim about the newest community result. The original paper
states an unconditional theorem; this explanatory work does not independently
validate it. The CrocSwap project retains conditional all-size interfaces.

Rebuild on a machine with Python, NumPy, Matplotlib and Tectonic:
  python3 generate_figures.py
  python3 build_editions.py
  tectonic --keep-logs -o output/pdf illustrated-guide.tex
  tectonic --keep-logs -o output/pdf expanded-paper.tex

Use a mounted writable external SSD for every generated output, temporary
directory, cache and preview in the user's environment. Set TMPDIR and
XDG_CACHE_HOME to directories on that SSD before building. Do not run this
package from iCloud-synced Documents or Desktop. The figure script puts its
Matplotlib cache under tmp/ in this package.

The original manuscript requires multiple source files and a bibliography;
the build uses Tectonic for that project. The standalone-document compiler
in the app does not support additional project files.

The generated TeX wrappers omit three pdfTeX-only metadata commands for
Tectonic compatibility. Original source files, proofs, citations and constants
are unchanged. Added explanation uses unnumbered sections and E-prefixed
figures to preserve original technical numbering.

Scope of checks: original-file SHA-256 binding, example arithmetic, full PDF
compilation, and rendered-page inspection. No new all-size theorem audit,
practical performance benchmark, record claim, or Lean formalization.
