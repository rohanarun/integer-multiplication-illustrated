"""Complete figure build: mathematical objects, not generic process boxes.

Earlier generators supply checked examples. This final visual layer renders
their concrete arrays, arithmetic, trajectories and geometry.
"""
from generate_foundations import *
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle, PathPatch
from matplotlib.path import Path as MPath

def clean(ax):
 for sp in ax.spines.values():sp.set_visible(False)
 ax.tick_params(length=0)

def heat(ax,a,title,cmap='Blues',vmax=None):
 a=np.asarray(a);ax.imshow(a,cmap=cmap,vmin=0,vmax=vmax or max(a.max(),1),alpha=.65)
 for (i,j),v in np.ndenumerate(a):ax.text(j,i,str(v),ha='center',va='center',fontsize=13,color=INK)
 ax.set_xticks([]);ax.set_yticks([]);ax.set_title(title,fontsize=11);clean(ax)

fig,axes=plt.subplots(1,2,figsize=(10,3.5),gridspec_kw={'width_ratios':[1,1.4]})
ax=axes[0];ax.axis('off')
for y,s in [(0.9,'23'),(.72,'× 14'),(.49,'92'),(.32,'230'),(.10,'322')]:ax.text(.75,y,s,ha='right',fontsize=23,fontfamily='DejaVu Sans Mono',color=TEAL if s=='322' else INK,transform=ax.transAxes)
ax.plot([.25,.82],[.62,.62],color=INK,transform=ax.transAxes);ax.plot([.25,.82],[.23,.23],color=INK,transform=ax.transAxes)
ax.set_title('The familiar long multiplication',fontsize=12)
ax=axes[1];pos=np.arange(3);raw=np.array([12,11,2]);carry=np.array([0,1,1])
ax.bar(pos,raw,color=BLUE,label='Convolution coefficient')
ax.bar(pos,carry,bottom=raw,color=GOLD,label='Incoming carry')
for j,(v,c,d) in enumerate(zip(raw,carry,[2,2,3])):
 ax.text(j,v+c+.4,f'{v} + {c} → digit {d}',ha='center',fontsize=10)
ax.set_xticks(pos,['Ones','Tens','Hundreds']);ax.set_ylim(0,16);ax.set_ylabel('Before carrying');ax.set_title('Convolution + one carry pass',fontsize=12)
ax.legend(fontsize=8,loc='upper right');clean(ax);fig.tight_layout();save(fig,'01-convolution')

fig,ax=plt.subplots(figsize=(10,4));ax.set_xlim(-.8,12);ax.set_ylim(-.7,3.7);ax.axis('off')
palette=[BLUE,TEAL,GOLD]
for j in range(12):
 col=palette[j%3];ax.add_patch(Rectangle((j,2.7),.75,.45,facecolor=col+'30',edgecolor=col));ax.text(j+.375,2.925,str(j),ha='center',va='center',fontsize=10)
 rx=1+(j%3)*4+(j//3)*.62;ry=.65
 ax.add_patch(Rectangle((rx,ry),.55,.45,facecolor=col+'30',edgecolor=col));ax.text(rx+.275,ry+.225,str(j),ha='center',va='center',fontsize=9)
 ax.plot([j+.375,rx+.275],[2.62,1.2],color=col,alpha=.45,lw=1)
for k in range(3):ax.text(1.95+k*4,.15,f'Role {k}: 4B = V/3',ha='center',color=palette[k],fontsize=11)
ax.text(5.5,3.5,'Whole rows are dealt cyclically; each row keeps its entire suffix',ha='center',fontsize=13)
ax.text(5.5,-.45,'12 rows × B bits = V bits total. All three role streams have matching local shapes.',ha='center',fontsize=10)
save(fig,'02-role-volume')

fig,ax=plt.subplots(figsize=(10,3.8));t=np.arange(5)
for vals,label,col in [([3]*5,'Source x',BLUE),([5,-2,-2,8,8],'Target y',TEAL),([7,7,10,10,7],'Scratch a',GOLD)]:
 ax.plot(t,vals,'o-',lw=2,color=col,label=label)
 for i,v in enumerate(vals):ax.annotate(str(v),(i,v),xytext=(0,-15 if label=='Source x' or (label=='Scratch a' and i==4) else 7),textcoords='offset points',ha='center',fontsize=9,color=col)
ax.set_xticks(t,['Start','y ← y − a','a ← a + x','y ← y + a','a ← a − x']);ax.set_ylim(-4,13)
ax.axhline(7,color=GOLD,ls=':',alpha=.6);ax.annotate('Scratch returns to 7',xy=(4,7),xytext=(2.8,11.8),arrowprops={'arrowstyle':'->','color':GOLD},color=GOLD)
ax.set_ylabel('Actual register value');ax.set_title('Borrow a register containing 7: add x = 3 to y = 5, then return the 7')
ax.legend(loc='lower right',fontsize=9);ax.grid(axis='y',alpha=.12);fig.tight_layout();save(fig,'03-restoration')

fig,axes=plt.subplots(2,3,figsize=(8,5.2))
aa=np.array([[1,2],[3,4]]);bb=np.array([[5,6],[7,8]])
for j,(a,title) in enumerate([(aa,'Array A'),(bb,'Array B'),(aa+bb,'A + B')]):
 heat(axes[0,j],a,title,vmax=12)
 heat(axes[1,j],np.rot90(a),'D(A)' if j==0 else 'D(B)' if j==1 else 'D(A + B) = D(A) + D(B)',vmax=12)
fig.suptitle('A common frame can be a quarter-turn of the address grid',fontsize=13)
fig.tight_layout(rect=(0,.02,1,.94));save(fig,'04-common-frame')

fig,axes=plt.subplots(1,2,figsize=(10,3.7));f=2.**np.arange(11);q=np.log2(1.5)
axes[0].loglog(f,f,'o-',label='Linear width cost',color=GRAY,base=2)
axes[0].loglog(f,f**q,'o-',label=r'Toy cost: $f^{\log_2(3/2)}$',color=TEAL,base=2)
axes[0].set(xlabel='Width f',ylabel='Cost per unit volume',title='Doubling width multiplies cost by 1.5');axes[0].legend(fontsize=8);axes[0].grid(alpha=.15)
axes[1].plot(np.arange(11),(.75)**np.arange(11),'o-',color=TEAL)
axes[1].set(xlabel='Number of doublings',ylabel='Toy cost / linear cost',title='The gap compounds at every scale',ylim=(0,1.05));axes[1].grid(alpha=.15)
fig.tight_layout();save(fig,'05-recursion')

fig,ax=plt.subplots(figsize=(9.5,3.4));ax.set_xlim(0,10);ax.set_ylim(0,3);ax.axis('off')
for yy,val in [(2.4,'6'),(.6,'2')]:ax.text(.45,yy,val,ha='center',va='center',fontsize=24)
for yy,sign,val in [(2.4,'+','4'),(.6,'−','2')]:
 ax.add_patch(Circle((4.2,yy),.22,facecolor='white',edgecolor=BLUE,lw=1.5));ax.text(4.2,yy,sign,ha='center',va='center',fontsize=16)
 for start in [2.4,.6]:
  ax.annotate('',xy=(3.96,yy),xytext=(1,start),arrowprops={'arrowstyle':'->','color':BLUE,'alpha':.6})
 ax.text(6,yy+.16,'divide by 2',ha='center',fontsize=11)
 ax.annotate('',xy=(8.6,yy),xytext=(4.5,yy),arrowprops={'arrowstyle':'->','color':TEAL})
 ax.text(9,yy,val,ha='center',va='center',fontsize=24,color=TEAL)
ax.text(5,1.5,'Upper branch: (6 + 2)/2\nLower branch: (6 − 2)/2',ha='center',va='center',fontsize=11)
save(fig,'06-butterfly')

fig,ax=plt.subplots(figsize=(9,3.7));theta=np.pi/2-np.arange(4)*np.pi/2
xy=np.stack([np.cos(theta),np.sin(theta)],axis=1)
for j,(x,y) in enumerate(xy):
 ax.text(x*1.1,y*1.1,f'slot {j}\na{j}',ha='center',va='center',fontsize=12,color=BLUE)
 k=(j+1)%4;tx,ty=xy[k]
 ax.annotate('',xy=(tx*.8,ty*.8),xytext=(x*.8,y*.8),arrowprops={'arrowstyle':'->','connectionstyle':'arc3,rad=-.35','color':GOLD if j==3 else TEAL,'lw':2})
ax.text(-1.55,1.4,'wrap: negate a₃',color=GOLD,fontsize=11)
ax.text(1.8,.45,'Multiply by y modulo y⁴ + 1',fontsize=13)
ax.text(1.8,-.02,'[a₀, a₁, a₂, a₃]\n          ↓\n[−a₃, a₀, a₁, a₂]',fontsize=15,va='center')
ax.set(xlim=(-1.8,5),ylim=(-1.45,1.5),aspect='equal');ax.axis('off');fig.tight_layout();save(fig,'07-signed-shift')

fig,axes=plt.subplots(2,3,figsize=(10,4.5));a=np.array([2,5,1,4]);b=np.array([3,2,6,1]);p=[0,2,1,3]
for row,perm in enumerate([list(range(4)),p]):
 for j,(v,title) in enumerate([(a,'A'),(b,'B'),(a*b,'A × B entry by entry')]):
  axes[row,j].bar(range(4),v[perm],color=[palette[k%3] for k in perm]);axes[row,j].set_xticks(range(4),[f'freq {k}' for k in perm],fontsize=8);axes[row,j].set_ylim(0,12)
  axes[row,j].set_title(title if row==0 else title+' in order P',fontsize=10);clean(axes[row,j])
fig.suptitle('Reorder both inputs the same way: each frequency still meets its partner',fontsize=12)
fig.tight_layout(rect=(0,0,1,.93));save(fig,'08-permutations')

fig,axes=plt.subplots(1,2,figsize=(10,3.6));ax=axes[0]
for j in range(8):
 dest=[0,4,2,6,1,5,3,7][j];ax.plot([0,1],[j,dest],color=palette[j%3],lw=1.3,alpha=.7);ax.scatter([0,1],[j,dest],color=palette[j%3],s=30)
ax.set_xticks([0,1],['Stored order','Required order']);ax.set_yticks([]);ax.set_title('Move records to their partners',fontsize=12);clean(ax)
ax=axes[1]
for layer in range(3):
 for i in range(8):
  for dest in [i,i^(1<<layer)]:ax.plot([layer,layer+1],[i,dest],color=TEAL,alpha=.28)
for layer in range(4):ax.scatter([layer]*8,range(8),color=TEAL,s=22)
ax.set_xticks(range(4),['Input','Bit 0','Bit 1','Bit 2']);ax.set_yticks([]);ax.set_title('Mix matching values through butterfly layers',fontsize=11);clean(ax)
fig.tight_layout();save(fig,'11-proof-roadmap')

fig,axes=plt.subplots(1,2,figsize=(10,3.6));ax=axes[0]
ax.imshow([[0,1],[1,2]],cmap=ListedColormap([BLUE+'45',TEAL+'45',GOLD+'45']),vmin=0,vmax=2)
for i,a in enumerate([3,2]):
 for j,bv in enumerate([4,1]):ax.text(j,i,f'{a} × {bv} = {a*bv}\nposition {i+j}',ha='center',va='center',fontsize=12)
ax.set_xticks([0,1],['4 ones','1 ten']);ax.set_yticks([0,1],['3 ones','2 tens']);ax.set_title('Same color = same output position');clean(ax)
ax=axes[1];ax.bar([0,1,2],[12,3,2],color=palette);ax.bar([1],[8],bottom=[3],color=TEAL,alpha=.55)
for x,y,t in [(0,6,'12'),(1,1.5,'3'),(1,7,'8'),(2,1,'2')]:ax.text(x,y,t,ha='center',va='center',fontsize=12,color='white' if x!=2 else INK)
ax.text(1,11.7,'3 + 8 = 11',ha='center',fontsize=11);ax.set_xticks([0,1,2],['Ones','Tens','Hundreds']);ax.set_ylim(0,14);ax.set_ylabel('Coefficient before carrying');ax.set_title('Add along each colored diagonal');clean(ax)
fig.tight_layout();save(fig,'13-convolution-groups')

fig,axes=plt.subplots(1,2,figsize=(10,3.8));xx=np.linspace(-1.3,1.3,200)
axes[0].plot(xx,3+2*xx,label='A(x) = 3 + 2x',color=BLUE);axes[0].plot(xx,4+xx,label='B(x) = 4 + x',color=GOLD)
for t in [-1,0,1]:axes[0].plot([t,t],[3+2*t,4+t],':',color=GRAY);axes[0].scatter([t,t],[3+2*t,4+t],color=[BLUE,GOLD])
axes[0].set(xlabel='Sample point x',ylabel='Value',title='Evaluate each input at the same points');axes[0].legend(fontsize=9)
axes[1].plot(xx,12+11*xx+2*xx**2,color=TEAL)
for t,val in [(-1,3),(0,12),(1,25)]:
 axes[1].scatter([t],[val],s=55,color=TEAL);axes[1].annotate(f'({t}, {val})',(t,val),xytext=(5,7),textcoords='offset points',fontsize=10)
axes[1].set(xlabel='Sample point x',ylabel='Product A(x)B(x)',title='Three products determine this quadratic')
for ax in axes:ax.grid(alpha=.15)
fig.tight_layout();save(fig,'14-evaluate-recover')

fig,axes=plt.subplots(1,2,figsize=(10,4),gridspec_kw={'width_ratios':[1,1.7]})
heat(axes[0],np.arange(9).reshape(3,3),'A 3 × 3 array',vmax=9)
ax=axes[1];perm=[0,3,6,1,4,7,2,5,8]
for i in range(9):
 dest=perm.index(i);col=palette[i//3]
 ax.plot([i,dest],[1,0],color=col,lw=1.5,alpha=.55)
 ax.scatter([i,dest],[1,0],s=180,color=col,zorder=3)
 ax.text(i,1,str(i),color='white',ha='center',va='center',fontsize=9)
 ax.text(dest,0,str(i),color='white',ha='center',va='center',fontsize=9)
ax.text(4,1.3,'Read rows: 0 1 2 | 3 4 5 | 6 7 8',ha='center',fontsize=11)
ax.text(4,-.3,'Read columns: 0 3 6 | 1 4 7 | 2 5 8',ha='center',fontsize=11)
ax.annotate('One tape head scans positions',xy=(8,1.65),xytext=(0,1.65),arrowprops={'arrowstyle':'->','color':INK},va='center',fontsize=10)
ax.set(xlim=(-.4,8.4),ylim=(-.65,1.85));ax.axis('off');fig.tight_layout();save(fig,'16-tape-order')

fig,axes=plt.subplots(1,3,figsize=(10,3.8))
for ax,vectors,title in zip(axes,[[(1,0),(0,1),(1,1)],[(0,1),(-1,0),(-1,1)],[(0,1),(0,1),(0,2)]],['Add x and y','Rotate both, then add','Rotate only x: wrong sum']):
 ax.axhline(0,color=GRAY,lw=.7);ax.axvline(0,color=GRAY,lw=.7)
 for j,(x,y) in reversed(list(enumerate(vectors))):
  ax.quiver(0,0,x,y,angles='xy',scale_units='xy',scale=1,color=[BLUE,GOLD,TEAL][j],width=.015,zorder=4-j,alpha=.8)
 ax.text(vectors[2][0]-.05,vectors[2][1]+.15,str(tuple(vectors[2])),ha='center',fontsize=11,color=TEAL)
 ax.set(xlim=(-1.6,1.6),ylim=(-.5,2.5),aspect='equal');ax.set_title(title,fontsize=11);ax.grid(alpha=.1)
fig.tight_layout();save(fig,'18-frame-example')

fig,axes=plt.subplots(1,2,figsize=(10,3.8));ax=axes[0];levels=[[4],[1,4,7],list(np.linspace(0,8,9))]
for d in range(2):
 for j,x in enumerate(levels[d]):
  for child in levels[d+1][3*j:3*j+3]:ax.plot([x,child],[2-d,1-d],color=GRAY,alpha=.5)
for d,xs in enumerate(levels):
 ax.scatter(xs,[2-d]*len(xs),s=500/(2**d),color=[BLUE,TEAL,GOLD][d],zorder=3)
 ax.text(9,2-d,f'{3**d} calls\nV/{2**d} each',va='center',fontsize=10)
ax.set(xlim=(-.6,11.5),ylim=(-.5,2.5));ax.axis('off');ax.set_title('Circle area = volume of one call',fontsize=12)
ax=axes[1];depth=np.arange(6)
ax.plot(depth,2.**depth,'o-',color=GRAY,label='Naive doubling: 2ʲ')
ax.plot(depth,1.5**depth,'o-',color=TEAL,label='Total visited: (3/2)ʲ')
ax.set(xlabel='Depth j',ylabel='Volume visited / V',title='More calls, but each call is smaller');ax.legend(fontsize=9);ax.grid(alpha=.15)
fig.tight_layout();save(fig,'19-recursion-ledger')

fig,ax=plt.subplots(figsize=(10,3.7));ax.axis('off')
rows=[['Algebra example','Concrete tape program','All-size proof'],['Circuit outputs the intended values','Heads, copies, routing, cleanup are charged','Every size meets cost and error bounds'],['Finite replay can check this instance','A scalar identity does not price movement','A finite run does not prove this quantifier']]
table=ax.table(cellText=rows[1:],colLabels=rows[0],cellLoc='left',loc='center',colWidths=[.32,.34,.34]);table.auto_set_font_size(False);table.set_fontsize(10);table.scale(1,2.8)
for (r,c),cell in table.get_celld().items():
 cell.set_edgecolor('#D7E0E5');cell.set_facecolor('#EAF0F5' if r==0 else 'white')
 cell.get_text().set_wrap(True)
 # Explicit line wrapping is governed by the explanatory content, not image fitting.
text_rows=[['Outputs match, and scratch\nreturns to its starting value','Head movement, copies, routing,\nand cleanup are charged','Every input size satisfies\nthe cost and error bounds'],['Finite replay checks\na concrete instance','A scalar identity alone\ndoes not price movement','A finite run alone\ndoes not prove every size']]
for r,row in enumerate(text_rows,1):
 for c,text in enumerate(row):table[r,c].get_text().set_text(text)
ax.set_title('Three different claims require three different kinds of evidence',fontsize=13)
save(fig,'23-proof-obligations')

assert np.array_equal(np.rot90(aa+bb),np.rot90(aa)+np.rot90(bb))
# Separate exact binding for the concrete frequency-order illustration.
freq_a=np.array([2,5,1,4]);freq_b=np.array([3,2,6,1]);perm=[0,2,1,3]
assert list(freq_a*freq_b)==[6,10,6,4]
assert np.array_equal(freq_a[perm]*freq_b[perm],(freq_a*freq_b)[perm])
checks=json.loads((ROOT/'foundation-checks.json').read_text())
checks['array_rotation_commutes_with_addition']=True
checks['permutation_example_product']=[6,10,6,4]
checks['register_trajectory']={'x':[3,3,3,3,3],'y':[5,-2,-2,8,8],'a':[7,7,10,10,7]}
(ROOT/'foundation-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print('Rendered concrete mathematical diagrams for all core illustrations.')
