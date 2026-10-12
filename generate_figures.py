"""Reproducible explanatory figures; toy examples are not benchmark data."""
from pathlib import Path
import os
ROOT = Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR'] = str(ROOT / 'tmp/matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np
from fractions import Fraction as F
import json

OUT = ROOT / 'figures'
INK, BLUE, TEAL, GOLD, GRAY = '#172B3A', '#245CA6', '#147C80', '#BD691B', '#687987'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,
    'axes.labelcolor':INK,'axes.edgecolor':'#CCD4DB','xtick.color':GRAY,
    'ytick.color':GRAY,'savefig.facecolor':'white','pdf.fonttype':42})

def canvas(h=3.8):
    fig, ax = plt.subplots(figsize=(10,h)); ax.set_xlim(0,10); ax.set_ylim(0,h); ax.axis('off')
    return fig,ax

def box(ax,x,y,w,h,text,color=BLUE,size=11):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.06,rounding_size=0.08',
        facecolor=color+'10',edgecolor=color,lw=1.2))
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=size,color=color)

def arrow(ax,a,b,color=GRAY):
    ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':color,'lw':1.4})

def save(fig,name):
    fig.savefig(OUT/(name+'.pdf'),bbox_inches='tight',pad_inches=.12)
    fig.savefig(OUT/(name+'.png'),dpi=160,bbox_inches='tight',pad_inches=.12)
    plt.close(fig)

# The same convolution is independently checked below.
fig,ax=canvas(3.5)
box(ax,.2,2.3,2.6,.75,'23 = 3 + 2 × 10\n14 = 4 + 1 × 10')
box(ax,3.7,2.3,2.7,.75,'(3 + 2x)(4 + x)\n= 12 + 11x + 2x²')
box(ax,7.25,2.3,2.4,.75,'12 + 110 + 200\n= 322',TEAL)
arrow(ax,(2.9,2.67),(3.6,2.67));arrow(ax,(6.5,2.67),(7.15,2.67))
for i,(raw,carry,digit) in enumerate([(12,0,2),(11,1,2),(2,1,3)]):
    x=.4+3.3*i
    box(ax,x,.45,2.7,1.05,f'Position {i}: 10^{i}\n{raw} + incoming {carry}\nwrite {digit}, carry {1 if i<2 else 0}',TEAL)
    if i<2: arrow(ax,(x+2.75,.95),(x+3.2,.95))
ax.text(5,.03,'Read the resulting digits from right to left: 3 2 2',ha='center',fontsize=10)
save(fig,'01-convolution')

fig,ax=canvas(3.5)
for j in range(12):
    x=.3+j*.78; c=[BLUE,TEAL,GOLD][j%3]
    ax.add_patch(Rectangle((x,2.5),.71,.45,facecolor=c+'22',edgecolor=c))
    ax.text(x+.355,2.725,str(j),ha='center',va='center')
ax.text(.3,3.12,'12 complete rows in tape order',fontsize=12)
for role in range(3):
    x=.4+role*3.25
    box(ax,x,.8,2.6,.9,f'Role {role}\nrows '+', '.join(map(str,range(role,12,3))),[BLUE,TEAL,GOLD][role])
    arrow(ax,(x+1.3,2.35),(x+1.3,1.8))
    ax.text(x+1.3,.35,'4B bits = V / 3',ha='center',fontsize=11)
ax.text(5,.04,'Every row retains the full suffix address set; this picture uses W = 3.',ha='center',fontsize=10)
save(fig,'02-role-volume')

fig,ax=canvas(3.6)
states=[('Start','(x, y, a)'),('Cancel old scratch','(x, y − a, a)'),('Load source','(x, y − a, a + x)'),('Read scratch','(x, y + x, a + x)'),('Restore scratch','(x, y + x, a)')]
for i,(name,state) in enumerate(states):
    x=.2+1.98*i
    box(ax,x,1.4,1.65,1.15,name+'\n\n'+state,TEAL if i==4 else BLUE,9)
    if i<4:arrow(ax,(x+1.7,1.98),(x+1.94,1.98))
ax.text(5,3.04,'An unknown scratch value can be borrowed and returned exactly',ha='center',fontsize=13)
ax.text(5,.66,'The net update is y ← y + x; x and the original a are unchanged.',ha='center',fontsize=12)
ax.text(5,.15,'Illustrative scalar identity over a ring; not the full triple-subset network.',ha='center',fontsize=10)
save(fig,'03-restoration')

fig,ax=canvas(3.8)
box(ax,.3,2.6,2.1,.65,r'Logical inputs: $g_1,g_2$')
box(ax,7.1,2.6,2.5,.65,r'Logical output: $g_1+g_2$')
box(ax,.3,.65,2.1,.8,r'Stored: $Dg_1,Dg_2$')
box(ax,7.1,.65,2.5,.8,r'Stored: $D(g_1+g_2)$',TEAL)
arrow(ax,(2.5,2.92),(7,2.92));arrow(ax,(2.5,1.05),(7,1.05))
arrow(ax,(1.35,2.5),(1.35,1.55));arrow(ax,(8.35,2.5),(8.35,1.55))
ax.text(4.8,3.14,'Pointwise addition across roles',ha='center',fontsize=10)
ax.text(4.8,1.28,r'$Dg_1+Dg_2=D(g_1+g_2)$',ha='center',fontsize=13)
ax.text(1.7,2,'apply D',fontsize=10);ax.text(8.7,2,'apply D',fontsize=10)
ax.text(5,.15,r'Between vertices: $D_u g\ \longrightarrow\ (D_vD_u^{-1})D_u g = D_vg$',ha='center',fontsize=12)
save(fig,'04-common-frame')

fig,axes=plt.subplots(1,2,figsize=(10,3.7),gridspec_kw={'width_ratios':[1,1.25]})
ax=axes[0];ax.set_xlim(0,4);ax.set_ylim(0,3.7);ax.axis('off')
box(ax,.4,2.55,3.2,.65,'Parent: volume V, width mf')
box(ax,.4,.8,3.2,.85,'s children\neach: volume V/W, width f',TEAL)
arrow(ax,(2,2.45),(2,1.75));ax.text(2,.25,r'Normalized multiplier: $s/W < m$',ha='center',fontsize=11)
ax=axes[1];f=2.**np.arange(11);q=np.log2(3/2)
ax.loglog(f,f,'o-',label='Linear width cost',color=GRAY,base=2)
ax.loglog(f,f**q,'o-',label=r'Toy recurrence: $f^{\log_2(3/2)}$',color=TEAL,base=2)
ax.set(xlabel='Width f',ylabel='Normalized recursive contribution',title='Illustration: m = 2, W = 2, s = 3')
ax.grid(alpha=.18);ax.legend(fontsize=8,loc='upper left');fig.tight_layout()
save(fig,'05-recursion')

fig,ax=canvas(4)
box(ax,.25,2.35,2.25,.85,'u = 6\nv = 2')
box(ax,3.9,2.35,2.25,.85,'H₀ averages\nand differences')
box(ax,7.5,2.35,2.25,.85,'(u + v)/2 = 4\n(u − v)/2 = 2',TEAL)
arrow(ax,(2.6,2.78),(3.8,2.78));arrow(ax,(6.25,2.78),(7.4,2.78))
box(ax,.25,.45,4,.9,'Two selected address bits\n[8, 4, 2, 2]')
box(ax,5.75,.45,4,.9,'Apply H₀ on both bits\n[4, 1, 2, 1]',TEAL)
arrow(ax,(4.4,.9),(5.65,.9))
ax.text(5,1.77,'Complete normalized layer is contractive; internal scratch need not be.',ha='center',fontsize=11)
ax.text(5,.04,'Rows above are separate worked examples. The tensor output uses order 00, 01, 10, 11.',ha='center',fontsize=9)
save(fig,'06-butterfly')

fig,ax=canvas(3.1)
for row,(labs,title) in enumerate([(['a₀','a₁','a₂','a₃'],'A(y)'),(['−a₃','a₀','a₁','a₂'],'yA(y) modulo y⁴ + 1')]):
    y=2-row*1.2
    ax.text(.15,y+.26,title,va='center',fontsize=11)
    for i,lab in enumerate(labs):box(ax,4+i*1.35,y,1.05,.55,lab,GOLD if lab=='−a₃' else BLUE,13)
ax.text(5,.13,'The wrapped coefficient changes sign because y⁴ = −1.',ha='center',fontsize=12)
save(fig,'07-signed-shift')

fig,ax=canvas(3.6)
for x,title,vals in [(.2,'Frequencies in canonical order',['0','1','2','3']),(5.5,'Same frequencies, common order P',['0','2','1','3'])]:
    ax.text(x+2,3.2,title,ha='center',fontsize=11)
    for row,prefix in enumerate(['A','B','A·B']):
        for i,v in enumerate(vals):box(ax,x+i*1.02,2.35-row*.78,.86,.5,prefix+'['+v+']',TEAL if row==2 else BLUE,9)
arrow(ax,(4.4,2.6),(5.3,2.6));arrow(ax,(4.4,1.82),(5.3,1.82));arrow(ax,(4.4,1.04),(5.3,1.04))
ax.text(5,.17,r'$(PA)\odot(PB)=P(A\odot B)$: matching entries remain matched.',ha='center',fontsize=13)
save(fig,'08-permutations')

fig,ax=plt.subplots(figsize=(10,2.6));ax.set_xlim(10.8,13.2);ax.set_ylim(-.4,1)
ax.axvspan(11.5,12.5,color=TEAL,alpha=.12)
ax.axvline(11.5,color=GOLD,ls='--');ax.axvline(12.5,color=GOLD,ls='--')
ax.plot([11,12,13],[0,0,0],'o',color=INK);ax.plot([12.27],[.38],'o',color=TEAL,ms=9)
ax.annotate('Example approximation: 12.27',xy=(12.27,.38),xytext=(11.1,.75),arrowprops={'arrowstyle':'->','color':TEAL},fontsize=11)
ax.text(12,-.25,'Correct integer: 12',ha='center',fontsize=11)
ax.set_xticks([11,11.5,12,12.5,13]);ax.set_yticks([]);ax.set_title('After every scale is undone: absolute error must be strictly below 1/2')
for s in ['left','right','top']:ax.spines[s].set_visible(False)
fig.tight_layout();save(fig,'09-rounding')

eps=F(1,2**75);c=F(1,2**56);tau=1-F(1,2**50);lp=1-F(1,2**54);delta=F(1,16);k=F(1,2**182)
gs=[1-eps*(1+c),eps*c*(1-tau),eps*(1-lp),1-tau-eps*(2-tau),F(1,4)-delta-F(3,2)*eps,1-delta-eps,eps]
assert min(gs)==2*k
fig,ax=plt.subplots(figsize=(10,4.1))
labels=['Prefix moves','Chunk exchanges','Butterfly rounds','CRT / axis layouts','Gaussian maps','Chirps / products','Packed products']
x=-np.log2([float(g) for g in gs]);yy=np.arange(7)
ax.barh(yy,x,color=[GOLD if g==min(gs) else BLUE for g in gs],height=.58)
ax.axvline(182,color=TEAL,ls='--',label=r'Target $\kappa=2^{-182}$')
ax.set_yticks(yy,labels);ax.invert_yaxis();ax.set_xlim(0,206)
ax.set_xlabel(r'$-\log_2(g_i)$: farther right means a smaller margin (worse)')
for i,v in enumerate(x):ax.text(v+2,i,f'{v:.2f}',va='center',fontsize=9)
ax.legend(loc='lower right',fontsize=9);fig.tight_layout();save(fig,'10-margins')

# Independent exact computations for the pedagogical examples.
digits_a=[3,2];digits_b=[4,1];conv=[sum(digits_a[i]*digits_b[j] for i in range(2) for j in range(2) if i+j==k) for k in range(3)]
assert conv==[12,11,2] and sum(v*10**i for i,v in enumerate(conv))==23*14==322
for a in range(-3,4):
 for x in range(-3,4):
  for y in range(-3,4):
   old=(x,y,a);y-=a;a+=x;y+=a;a-=x
   assert (x,y,a)==(old[0],old[1]+old[0],old[2])
H=np.array([[F(1,2),F(1,2)],[F(1,2),F(-1,2)]])
assert list(np.kron(H,H)@np.array([8,4,2,2]))==[4,1,2,1]
audit={'source_commit':'adc7f1241b42e322a6451854ab7e4b4c146bf78a','margins':[str(g) for g in gs],
       'minimum_margin':str(min(gs)),'kappa':str(k),'min_equals_two_kappa':True,
       'convolution':conv,'product':322,'restoration_examples':343,'tensor_butterfly':[4,1,2,1],
       'scope':'Pedagogical examples and original margin arithmetic only; not a theorem audit.'}
(ROOT/'example-checks.json').write_text(json.dumps(audit,indent=2)+'\n')
print('Generated 10 vector PDF figures and 10 PNG previews; exact example checks passed.')
