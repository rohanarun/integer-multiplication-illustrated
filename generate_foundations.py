"""Build the original ten figures plus concrete prerequisite illustrations.

Run this script to regenerate the complete second-edition figure set.
All numerical demonstrations are teaching examples, not performance data.
"""
from generate_figures import ROOT, OUT, canvas, box, arrow, save, BLUE, TEAL, GOLD, GRAY, INK
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from fractions import Fraction as F
import json

fig,ax=canvas(4.5)
steps=[('Split into digits','Same integer, shorter pieces'),('Compute convolution','Collect equal place values'),('Recover coefficients','Undo scales, then round'),('Propagate carries','Write the exact product')]
for j,(title,subtitle) in enumerate(steps):
 x=.12+2.5*j
 box(ax,x,3.0,2.22,.9,title+'\n'+subtitle,TEAL if j==3 else BLUE,9)
 if j<3:arrow(ax,(x+2.26,3.45),(x+2.45,3.45))
box(ax,1.5,.7,3.1,1.2,'Movement problem\nGet matching data together\nwithout too many tape scans',BLUE,11)
box(ax,5.4,.7,3.1,1.2,'Arithmetic problem\nCombine many transform axes\nwithout one pass per axis',GOLD,11)
arrow(ax,(3.85,2.9),(3.05,2.0));arrow(ax,(4.4,2.9),(6.95,2.0))
ax.text(5,.15,'Both costs must fit the final bound. A cheap arithmetic step alone is insufficient.',ha='center',fontsize=10)
save(fig,'11-proof-roadmap')

fig,axes=plt.subplots(1,2,figsize=(10,3.7))
b=np.arange(4,65,dtype=float)
for y,label,color in [(2*b,r'$n^2$',GRAY),(b+np.log2(b),r'$n\log_2n$',BLUE),(b+.75*np.log2(b),r'$n(\log_2n)^{0.75}$',TEAL)]:
 axes[0].plot(b,y,label=label,color=color,lw=2)
axes[0].set(xlabel=r'Input-length scale $b=\log_2n$',ylabel=r'$\log_2$ of the formula value',title='Compare shapes, not measured seconds')
axes[0].legend(fontsize=8);axes[0].grid(alpha=.15)
axes[1].plot(b,b**(-.25),color=TEAL,lw=2)
axes[1].set(xlabel=r'$b=\log_2n$',ylabel=r'Ratio to $n\log_2n$',title=r'Toy saving $\kappa=1/4$: ratio $b^{-1/4}$',ylim=(0,1))
axes[1].grid(alpha=.15);fig.tight_layout();save(fig,'12-growth-rates')

fig,ax=canvas(3.6)
colors=[BLUE,TEAL,GOLD]
for i,a in enumerate([3,2]):
 for j,bv in enumerate([4,1]):
  x=.8+1.6*j;y=1.7-1.05*i
  box(ax,x,y,1.3,.8,f'{a} × {bv} = {a*bv}\nposition {i+j}',colors[i+j],11)
ax.text(2.05,2.95,'Each pair of digits contributes once',ha='center',fontsize=11)
for k,value in enumerate([12,11,2]):
 box(ax,6,2.2-.85*k,3.25,.62,f'Position {k}: coefficient {value}',colors[k],11)
 for i in range(2):
  for j in range(2):
   if i+j==k:arrow(ax,(.8+1.6*j+1.35,1.7-1.05*i+.4),(5.9,2.2-.85*k+.31),colors[k])
ax.text(5,.03,'Group by the sum of the positions: i + j. Those groups are the convolution.',ha='center',fontsize=10)
save(fig,'13-convolution-groups')

fig,ax=canvas(4.3)
columns=[(.15,'Sample point x'),(2.25,'A(x) = 3 + 2x'),(4.65,'B(x) = 4 + x'),(7.1,'Product C(x)')]
for x,title in columns:ax.text(x+1.05,3.9,title,ha='center',fontsize=11)
for row,t in enumerate([0,1,-1]):
 vals=[t,3+2*t,4+t,(3+2*t)*(4+t)];y=2.9-row*.8
 for (x,_),v in zip(columns,vals):box(ax,x,y,2.05,.58,str(v),TEAL if x==7.1 else BLUE,13)
 for a,bx in [(2.25,4.65),(4.65,7.1)]:arrow(ax,(a+2.1,y+.29),(bx-.06,y+.29))
ax.text(5,.45,'Recover coefficients: c₀ = 12,  c₁ = (25 − 3)/2 = 11,  c₂ = (25 + 3)/2 − 12 = 2',ha='center',fontsize=10)
ax.text(5,.05,'Three samples determine a polynomial of degree at most two.',ha='center',fontsize=10)
save(fig,'14-evaluate-recover')

components=np.array([[4,4,4,4],[3,0,-3,0],[0,1,0,-1],[1,-1,1,-1]])
fig,axes=plt.subplots(1,5,figsize=(10,3),sharey=True)
titles=['Average','Cosine pattern','Sine pattern','Alternating','Their sum']
for j,(ax,vals,title) in enumerate(zip(axes,list(components)+[components.sum(axis=0)],titles)):
 ax.axhline(0,color=GRAY,lw=.7);ax.plot(range(4),vals,'o-',color=TEAL if j==4 else BLUE,lw=1.7)
 ax.set_xticks(range(4));ax.set_title(title,fontsize=10);ax.set_xlabel('Position',fontsize=9)
 ax.set_ylim(-4,9);ax.grid(alpha=.1)
 for i,v in enumerate(vals):ax.annotate(str(v),(i,v),xytext=(0,6),textcoords='offset points',ha='center',fontsize=8)
axes[0].set_ylabel('Value');fig.tight_layout();save(fig,'15-frequency-patterns')

fig,ax=canvas(3.8)
order=list(range(9));transposed=[0,3,6,1,4,7,2,5,8]
for row,(arr,title) in enumerate([(order,'Rows stored consecutively'),(transposed,'Columns stored consecutively')]):
 y=2.5-row*1.4
 ax.text(.2,y+.72,title,fontsize=12)
 for i,v in enumerate(arr):
  box(ax,.2+i*1.07,y,.88,.48,str(v),[BLUE,TEAL,GOLD][v//3],12)
for i in [0,1,2]:
 arrow(ax,(.64+1.07*i,2.4),(.64+1.07*transposed.index(i),1.68),BLUE)
ax.text(5,.36,'Numbers name records, not their contents. Each colored record must actually move.',ha='center',fontsize=10)
ax.text(5,.03,'Only the first row’s routes are drawn; the same permutation routes all nine records.',ha='center',fontsize=9)
save(fig,'16-tape-order')

fig,axes=plt.subplots(1,2,figsize=(10,3.9))
for ax,vecs,title in zip(axes,[[(1,1),(2,2)],[(1,0),(0,1)]],['Rank 1: two arrows, one independent direction','Rank 2: two independent directions']):
 ax.axhline(0,color=GRAY,lw=.8);ax.axvline(0,color=GRAY,lw=.8)
 for j,(x,y) in enumerate(vecs):
  ax.quiver(0,0,x,y,angles='xy',scale_units='xy',scale=1,color=[BLUE,GOLD][j],width=.012,zorder=3-j)
  ax.text(x+.07,y+.05,f'v{j+1} = ({x}, {y})',fontsize=10)
 ax.set(xlim=(-.4,3.2),ylim=(-.4,2.6),aspect='equal');ax.set_title(title,fontsize=11);ax.grid(alpha=.15)
fig.tight_layout();save(fig,'17-rank-directions')

fig,ax=canvas(4)
box(ax,.25,2.6,2.5,.8,'Input vectors\nx = (1, 0), y = (0, 1)',BLUE,11)
box(ax,3.8,2.6,2.5,.8,'Add first, rotate\nx + y = (1, 1)',BLUE,11)
box(ax,7.35,2.6,2.4,.8,'Correct result\nD(x + y) = (−1, 1)',TEAL,11)
arrow(ax,(2.85,3),(3.7,3));arrow(ax,(6.4,3),(7.25,3))
box(ax,.25,.8,4.35,1.0,'Same frame on both inputs\nDx + Dy = (0, 1) + (−1, 0) = (−1, 1)',TEAL,11)
box(ax,5.35,.8,4.35,1.0,'Rotate only one input\nDx + y = (0, 1) + (0, 1) = (0, 2)',GOLD,11)
ax.text(5,.15,'D is a quarter-turn counterclockwise. A mixed representation gives the wrong sum.',ha='center',fontsize=10)
save(fig,'18-frame-example')

fig,ax=canvas(4)
headers=['Depth j','Calls at this depth','Volume of each call','Total volume visited']
for j,title in enumerate(headers):ax.text(.2+j*2.5+1.1,3.6,title,ha='center',fontsize=10)
for depth in range(4):
 vals=[str(depth),str(3**depth),f'V / {2**depth}',f'{F(3,2)**depth} × V'];y=2.7-depth*.65
 for j,val in enumerate(vals):box(ax,.2+j*2.5,y,2.2,.43,val,TEAL if j==3 else BLUE,11)
ax.text(5,.32,'Calls can run sequentially and reuse storage; visited volume is work, not peak memory.',ha='center',fontsize=10)
ax.text(5,.02,'Toy model m = 2, W = 2, s = 3. A naive width cost grows by 2 per level; here it grows by 3/2.',ha='center',fontsize=9)
save(fig,'19-recursion-ledger')

fig,ax=plt.subplots(figsize=(10,3.6))
vals=[.01,.03,.24,.96];labels=['Initial bound','Add local error 0.02','Then rescale by 8','Alternative: rescale by 32']
ax.barh(range(4),vals,color=[BLUE,BLUE,TEAL,GOLD],height=.5);ax.invert_yaxis()
ax.axvline(.5,color=INK,ls='--',label='Strict rounding threshold: 1/2')
for j,v in enumerate(vals):ax.text(v+.018,j,f'{v:.2f}',va='center',fontsize=10)
ax.set_yticks(range(4),labels);ax.set_xlim(0,1.1);ax.set_xlabel('Certified upper bound on absolute error (toy example)')
ax.legend(loc='lower center',bbox_to_anchor=(.5,1.02),fontsize=9,frameon=False);fig.tight_layout();save(fig,'20-error-budget')

fig,axes=plt.subplots(1,2,figsize=(10,3.5))
q=np.arange(4);central=[-.5,0,.5,1];side=[.5,0,-.5,0]
ax=axes[0]
ax.bar(q-.24,central,width=.24,label='Central contribution',color=BLUE)
ax.bar(q,side,width=.24,label='Side correction',color=GOLD)
ax.bar(q+.24,np.array(central)+side,width=.24,label='Net coefficient',color=TEAL)
ax.set_xticks(q,['0','1','2','3 (self)']);ax.axhline(0,color=GRAY,lw=.8)
ax.set(xlabel='Intersection size of two triples',ylabel='Coefficient',title='Complex construction: cancel unwanted terms')
ax.legend(fontsize=7,loc='upper left');ax.set_ylim(-.65,1.6)
axes[1].axis('off')
cells=[['0','0','0','0'],['1','1','1','0'],['2','0','0','0'],['3 (self)','1','0','1']]
tab=axes[1].table(cellText=cells,colLabels=['Overlap','Central','Side XOR','Net'],loc='center',cellLoc='center');tab.auto_set_font_size(False);tab.set_fontsize(10);tab.scale(1,1.7)
axes[1].set_title('Bit construction: arithmetic modulo two',fontsize=11)
fig.tight_layout();save(fig,'21-intersection-cancellation')

fig,ax=plt.subplots(figsize=(10,3.5));profiles=np.array([[.20,.03,.10],[.40,.03,.10],[.20,.08,.10]])
names=['Starting toy profile','Improve an easy term','Improve the limiting term'];colors=[BLUE,GOLD,TEAL]
for i in range(3):ax.barh(np.arange(3)+(i-1)*.22,profiles[:,i],height=.22,label=['Margin A','Margin B','Margin C'][i],color=colors[i])
ax.set_yticks(range(3),names);ax.invert_yaxis();ax.set_xlim(0,.48)
for row,profile in enumerate(profiles):ax.text(.42,row,f'min = {min(profile):.2f}',va='center',fontsize=10)
ax.set_xlabel('Toy margins: larger is better');ax.legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=3,fontsize=9,frameon=False);fig.tight_layout();save(fig,'22-bottleneck')

fig,ax=canvas(4.4)
labels=[('Finite algebra','Does the circuit do the\nclaimed thing, including cleanup?'),('Physical implementation','Can one fixed tape machine\nexecute it at the charged cost?'),('Accuracy and scaling','Do bounds survive resampling,\nrounding, and every input size?')]
for i,(title,sub) in enumerate(labels):
 x=.25+i*3.3;box(ax,x,2.3,2.9,1.35,title+'\n\n'+sub,BLUE,10);arrow(ax,(x+1.45,2.2),(5,1.35))
box(ax,2.2,.35,5.6,.9,'All contracts together support the final conclusion.\nA check of one box does not establish the others.',TEAL,11)
save(fig,'23-proof-obligations')

fig,ax=plt.subplots(figsize=(7.8,4.0));ax.set_aspect('equal')
theta=np.linspace(0,2*np.pi,200);ax.plot(np.cos(theta),np.sin(theta),color='#CCD4DB')
ax.plot([-1.45,1.45],[0,0],color=GRAY,lw=.7);ax.plot([0,0],[-1.45,1.45],color=GRAY,lw=.7)
for j,(x,y,label) in enumerate([(1,0,'1'),(0,1,'i'),(-1,0,'−1'),(0,-1,'−i')]):
 ax.plot(x,y,'o',color=BLUE);ax.text(1.16*x,1.16*y,label,ha='center',va='center',fontsize=14)
 a=j*np.pi/2+.18;b=(j+1)*np.pi/2-.18
 ax.annotate('',xy=(np.cos(b),np.sin(b)),xytext=(np.cos(a),np.sin(a)),arrowprops={'arrowstyle':'->','color':TEAL,'connectionstyle':'arc3,rad=.3'})
ax.text(1.6,.25,'Multiply by i:\nturn a quarter-circle\ncounterclockwise',fontsize=12,va='center')
ax.set(xlim=(-1.6,4),ylim=(-1.5,1.5));ax.axis('off');fig.tight_layout();save(fig,'24-complex-turns')

# Exact checks bind the explanatory numbers to their displayed identities.
A=[3,2];B=[4,1];C=[12,11,2]
samples={str(x):(A[0]+A[1]*x)*(B[0]+B[1]*x) for x in [0,1,-1]}
assert samples=={'0':12,'1':25,'-1':3}
assert [samples['0'],F(samples['1']-samples['-1'],2),F(samples['1']+samples['-1'],2)-samples['0']]==C
assert list(components.sum(axis=0))==[8,4,2,2]
fourth_roots=[1,-1j,-1,1j]
sample=[8,4,2,2]
dft=[sum(sample[j]*fourth_roots[(j*k)%4] for j in range(4)) for k in range(4)]
assert dft==[16,6-2j,4,6+2j]
D=np.array([[0,-1],[1,0]]);x=np.array([1,0]);y=np.array([0,1])
assert np.array_equal(D@(x+y),D@x+D@y)
assert not np.array_equal(D@(x+y),D@x+y)
assert [F(q-1,2)+(F(1-q,2) if q in [0,2] else 0) for q in range(4)]==[0,0,0,1]
assert [(q%2)^(1 if q==1 else 0) for q in range(4)]==[0,0,0,1]
assert (F(1,100)+F(2,100))*8==F(24,100)<F(1,2)
assert (F(1,100)+F(2,100))*32==F(96,100)>F(1,2)
assert [min(map(F,map(str,row))) for row in profiles]==[F(3,100),F(3,100),F(8,100)]
checks={'evaluation_samples':samples,'recovered_coefficients':C,'pattern_sum':[8,4,2,2],
 'four_sample_dft':[str(z) for z in dft],
 'shared_frame_result':[-1,1],'mixed_frame_result':[0,2],
 'intersection_net':[0,0,0,1],'toy_error_bounds':['1/100','3/100','6/25','24/25'],
 'toy_profile_minima':['3/100','3/100','2/25'],
 'scope':'Exact pedagogical examples, not the original asymptotic theorem.'}
(ROOT/'foundation-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print('Generated 24 explanatory figures; new prerequisite examples checked exactly.')
