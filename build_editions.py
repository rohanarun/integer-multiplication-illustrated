"""Assemble reading editions without modifying the frozen original sources."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent
source=(ROOT/'original/main.tex').read_text()
preamble=source.split(r'\begin{document}')[0]
preamble='\n'.join(line for line in preamble.splitlines() if not any(x in line for x in [r'\pdfinfoomitdate',r'\pdftrailerid',r'\pdfsuppressptexinfo',r'\title',r'\author',r'\date']))
preamble+=r'''
\input{explanation-style.tex}
\hypersetup{pdftitle={Integer multiplication below n log n: illustrated reading edition},pdfauthor={Explanatory edition prepared with Codex; original paper by OpenAI}}
\title{Integer multiplication below $n\log n$\\[8pt]\large An illustrated reading edition}
\author{Original manuscript: OpenAI\\[5pt]\small Added explanations and figures prepared with OpenAI Codex}
\date{Second illustrated edition, October 12, 2026\\\small Original manuscript dated September 23, 2026}
'''
chapters=sorted((ROOT/'explanations').glob('*.tex'))
foundation_before={0:['00-start'],1:['01-convolution'],2:['03-moving'],3:['04-vectors'],4:['06-recursion'],5:['02-patterns'],8:['07-errors','08-bottleneck'],9:['09-evidence']}
foundation_after={3:['05-cancellation']}
def foundation(stem):return r'\input{foundations/'+stem+'.tex}\n'
def exp(n):
 return ''.join(foundation(s) for s in foundation_before.get(n,[]))+r'\input{explanations/'+chapters[n].name+'}\n'+''.join(foundation(s) for s in foundation_after.get(n,[]))
figure_names=re.findall(r'\\explfigure\{([^}]+)\}','\n'.join(p.read_text() for folder in ['explanations','foundations'] for p in (ROOT/folder).glob('*.tex')))
assert len(figure_names)==len(set(figure_names)),'An explanatory figure was inserted twice'
figure_count=len(figure_names)
start=preamble+r'''
\begin{document}
\maketitle
\begin{abstract}
A guided explanation of the original argument, with ten new figures,
worked arithmetic examples, a map of the recursive construction, and explicit
distinctions between source theorem claims, illustrative calculations, and
conditional proof interfaces. The exposition begins with digit convolution
and builds toward frame geometry, tape recurrences, transforms, and exact
recovery. It is not a new proof or an official revision of the source paper.
\end{abstract}
'''
start=start.replace('ten new figures',f'{figure_count} explanatory figures')
guide=start+r'\tableofcontents\clearpage'+'\n'
for n in range(len(chapters)):guide+=exp(n)
guide+=r'\end{document}'+'\n'
(ROOT/'illustrated-guide.tex').write_text(guide)

full=start+r'''
\noindent\textbf{Full annotated edition.} Added explanatory chapters precede
the relevant original sections. The original proofs and numerical claims
are reproduced from the frozen source, with their original attribution.
Their reproduction is not an independent endorsement of the asserted theorem.
\tableofcontents
\clearpage
'''
def orig(name):return '\\par\\bigskip\\Needspace{8\\baselineskip}\\hrule\\medskip\\noindent{\\small\\textcolor{readerblue}{Original manuscript continues below.}}\\par\\medskip\n'+r'\input{original/sections/'+name+'}\n'
full+=exp(0)+exp(1)
abstract=source.split(r'\begin{abstract}')[1].split(r'\end{abstract}')[0]
full+=r'''\clearpage\section*{Original abstract (reproduced source claim)}
\addcontentsline{toc}{section}{Original abstract}
\noindent The following is the original author's abstract, preserved verbatim.
See the opening explanation for this edition's verification scope.
\begin{quote}
'''+abstract+r'\end{quote}'+'\n'
full+=orig('00-introduction.tex')
for i,name in [(2,'02-streams.tex'),(3,'03-motifs.tex'),(4,'04-swap.tex'),(5,'05-layers.tex'),(6,'06-transforms.tex'),(7,'07-resampling.tex'),(8,'08-assembly.tex')]:full+=exp(i)+orig(name)
full+=exp(9)+orig('09-exact-arithmetic.tex')+orig('10-transposition.tex')
full+=r'\appendix'+'\n'+orig('11-grouped-rectangles.tex')+exp(10)
full+=r'''\clearpage
\bibliographystyle{plain}
\bibliography{original/references}
\end{document}
'''
(ROOT/'expanded-paper.tex').write_text(full)
manifest=json.loads((ROOT/'source-manifest.json').read_text())
for name,meta in manifest['files'].items():
 if name.startswith('build/'):
  assert hashlib.sha256((ROOT/'original'/name[6:]).read_bytes()).hexdigest()==meta['sha256'],name
(ROOT/'figure-manifest.json').write_text(json.dumps({'count':figure_count,'figures':sorted(figure_names)},indent=2)+'\n')
print(f'Assembled guide and expanded paper with {figure_count} figures; original LaTeX sources unchanged.')
