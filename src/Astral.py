import sys, os
import re
import math
from ete3 import Tree, TreeStyle, AttrFace, NodeStyle, ImgFace
from scipy.stats import chi2

def convertNHX(inNwk, ):
	def convert(line):
		last_end = 0
		patterns = []
		for match in re.compile(r"'\[(\S+?)\]':(\d+.\d+)").finditer(line):
			start = match.start()
			end = match.end()
			patterns.append( line[last_end:start] )
			branch, length = match.groups()
			new_str = ':{}[&&NHX:{}]'.format(length, branch.replace(';', ':'))
			patterns.append( new_str )
			last_end = end
		patterns.append( line[last_end:] )
		return ''.join(patterns)
	nwk = []
	for line in open(inNwk):
		nwk += [convert(line)]
	return ''.join(nwk)

class AstralTree:
	def __init__(self, astral, show=None, max_pval=0.05, tmpdir='tmp', prefix=None, collapsed=None, subset=None):
		self.treefile = astral
		self.treestr = convertNHX(self.treefile)
		self.tree = Tree(self.treestr)
		self.max_pval = max_pval
		self.tmpdir = tmpdir
		self.prefix = prefix
		self.collapsed = collapsed
		self.subset = subset
		self.show = show
		if self.prefix is None:
			self.prefix = os.path.basename(self.treefile)
		
	def check(self):
		if not re.compile(r'f1=\S+f2=\S+f3=\S+').search(self.treestr):
			raise ValueError('Keys f1, f2 and f3 are not found in {}. \
Please check...'.format(self.treefile))
	def merge_trees(self):
		for node in self.tree.traverse():
			if node.is_leaf():
				continue
			leaf_names = node.get_leaf_names()
			try:
				f1, f2, f3 = node.f1, node.f2, node.f3
			except AttributeError: continue
			anc = self.show.get_common_ancestor(leaf_names)
			anc.f1, anc.f2, anc.f3 = f1, f2, f3
		return self.show
	def number_nodes(self, tree):
		i = 0
		f_nodes = open('{}/{}.nodes.tsv'.format(self.tmpdir, self.prefix), 'w')
		for node in tree.traverse():
			if node.name:
				continue
			i += 1
			name = 'N{}'.format(i)
			node.name = name
			line = [name, ','.join(node.get_leaf_names())]
			f_nodes.write('\t'.join(line)+'\n')
		f_nodes.close()
	def process_quartet(self):
		# check f1, f2, f3
		self.check()
		# merge
		if self.show is not None:
			self.show = Tree(self.show)
			self.tree = self.merge_trees()
		# name
		self.number_nodes(self.tree)
		# subset
		if self.subset:
			self.subset_tree(self.tree, self.subset)
		# collapse
		if self.collapsed:
			self.collapse_tree(self.tree, self.collapsed)
			
		i = 0
#		f_nodes = open('{}/{}.nodes.tsv'.format(self.tmpdir, self.prefix), 'w')
		for node in self.tree.traverse():
			if node.is_leaf():
				node.sp = '{}'.format(node.name.replace('_', " "))
				N = AttrFace("sp", fsize=16, fgcolor="black", fstyle='italic')
				node.add_face(N, 0, ) #position='aligned')
			#	node.img_style["draw_descendants"] = False
				continue
			try:
				f1, f2, f3 = node.f1, node.f2, node.f3
			except AttributeError: continue
			f1, f2, f3 = map(float, [f1, f2, f3])
			n = sum([f1, f2, f3])
			q1, q2, q3 = f1/n, f2/n, f3/n
			coalescent_unit = node.dist
			#eq2 = eq3 = math.exp(-coalescent_unit) / 3	# expected
			eq2 = eq3 = (1-q1) / 2
			eq1 = 1 - eq2 - eq3
			ef1, ef2, ef3 = n*eq1, n*eq2, n*eq3
			chi_sq = (ef1-f1)**2/ef1 + (ef2-f2)**2/ef2 + (ef3-f3)**2/ef3
			pval = 1-chi2.cdf(chi_sq, 1)
			if pval > self.max_pval: # ILS
				IH_index = 0
				IH_explain = 0
				ILS_index = eq2	# (>0, <0.33)
				ILS_explain = q2+q3
				hline = eq3
			else:
				xq2, xq3 = max(q2, q3), min(q2, q3)
				IH_index = (xq2-xq3) / (q1 - xq3 + xq2-xq3)	# how many introgression (>0,<0.5)
				IH_explain = xq2-xq3
				ILS_index = xq3
				ILS_explain = xq3*2
				hline = xq3
			ILS_index = ILS_index / (1.0/3)
			IH_index = IH_index
			print(hline, pval, i, f1, f2, f3, n, [q1, q2, q3])
			pp = node.support
			# theta = 2* Lm/Lc
			i += 1
#			name = 'N{}'.format(i)
#			node.name = name
#			line = [name, ','.join(node.get_leaf_names())]
#			f_nodes.write('\t'.join(line)+'\n')
			name = node.name
			Pfmt = '{:.3f}' if pval > self.max_pval else '{:.2e}'
			P = Pfmt.format(pval)
			text = '$n$={:.0f}\n$P$={}\nILS-e={:.1%}\nIH-e={:.1%}\nILS-i={:.1%}\nIH-i={:.1%}'.format(
				n, P, ILS_explain, IH_explain, ILS_index, IH_index)
			outfig = '{}/{}.{}.bar.pdf'.format(self.tmpdir, self.prefix, name)
			values, labels, colors = plot_bar([q1, q2, q3], outfig=outfig, hline=hline, text=text)
			
			face = ImgFace(outfig)
			#face = faces.SVGFace(outfig)
#			face = faces.BarChartFace(values, colors=colors, labels=labels, min_value=0, max_value=1, width=100, height=100, label_fsize=2, scale_fsize=2)
			#faces.add_face_to_node(face, node, column=0)
			node.add_face(face, column=0, position="branch-right")
#		f_nodes.close()
		# write tree
		self.tree.write(format=1, outfile='{}/{}.node.tree'.format(self.tmpdir, self.prefix))
		#	node.img_style["size"] = 0
		ts = TreeStyle()
		ts.show_leaf_name = False
		ts.show_branch_support = True
		ts.scale_length = 1
		# # Set bold red branch to the root node
		style = NodeStyle()
		style["fgcolor"] = "#0f0f0f"
		style["size"] = 0
		branch_color = '#7200da'
		style["vt_line_color"] = branch_color
		style["hz_line_color"] = branch_color
		style["vt_line_width"] = 4
		style["hz_line_width"] = 4
#		style["vt_line_type"] = 0 # 0 solid, 1 dashed, 2 dotted
#		style["hz_line_type"] = 0
#		self.tree.set_style(style)
		for node in self.tree.traverse():
			node.img_style = style

		outfig = self.prefix + '.pdf'
		self.tree.render(outfig, w=1000, tree_style=ts, dpi=300)
	def collapse_tree(self, tree, cfg):
		global d_collapse
		d_collapse = {}
		keep, remove = set(tree.get_leaf_names()), set([])
		for line in open(cfg):
			temp = line.strip().split()
			mcra = temp[0]
			leaf_names = temp[1].split(',')
			if len(leaf_names) == 1:
				leaf_name = leaf_names[0]
				ancestor = tree&leaf_name
			else:
				try: ancestor = tree.get_common_ancestor(leaf_names)
				except ValueError as e:
					continue
			ancestor.name = mcra
			keep.add(mcra)
			remove = remove | set(ancestor.get_leaf_names())
#			for leaf in ancestor.get_leaves():
#				d_collapse[leaf] = mcra
#		print(self.tree.write())
#		print (self.tree.write(is_leaf_fn=collapsed_leaf))
#		self.tree = Tree( self.tree.write(is_leaf_fn=collapsed_leaf) )
		keep = keep - remove
		tree.prune(keep)
#		print(ancestor.is_leaf())
#		print(self.tree.write())
	def subset_tree(self, tree, leaf_names):
		ancestor = tree.get_common_ancestor(leaf_names)
		keep = set(ancestor.get_leaf_names())
		tree.prune(keep)

def collapsed_leaf(node):
	return node not in d_collapse


colors = ('#1f77b4', '#ff7f0e', '#2ca02c', '#d62728')
def plot_bar(qs=[1,0,0], outfig=None, hline=None, ymax=1, text=None):
	import matplotlib.pyplot as plt
	import matplotlib
	matplotlib.rcParams['ytick.minor.visible'] = True

	plt.figure(figsize=(3,3))
	x = list(range(len(qs)))
	labs = ['q{}'.format(v+1) for v in x]
	cs = colors[:len(qs)]
	print(x, qs, hline)
	plt.bar(x, qs, color=cs, tick_label=labs, align='center', width=0.67)
	if hline is not None:
		plt.axhline(y=hline, color='gray', ls='--')
	if text is not None:
		plt.text(0.3*max(x), 0.98*ymax, text, fontsize=14,
				horizontalalignment='left', verticalalignment='top')
	plt.ylim(0, ymax)
	plt.savefig(outfig, bbox_inches='tight', transparent=True, dpi=600)
	plt.close()
	return qs, labs, cs
def main():
#	print(convertNHX(sys.argv[1]))
	AstralTree(sys.argv[1]).process_quartet()

if __name__ == '__main__':
	main()
