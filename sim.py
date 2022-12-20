import sys, re, os, glob
from RunCmdsMP import run_cmd
from small_tools import rmdirs
def main(inPar, outTrees=sys.stdout, n=10000):
	i = 0
	
	cmd = 'fsc27 -i {} -n 10000 -c 10 -T'.format(inPar)
	outdir = os.path.splitext(inPar)[0]
	while True:
		run_cmd(cmd)
		trees = glob.glob('{}/*_mut_trees.trees'.format(outdir))[0]
		for line in open(trees):
			line = line.lstrip()
			if line.startswith('tree'):
				idx = line.find('(')
				tree = line[idx:].replace(' ', '')
				tree = re.compile(r'\.\d+').sub('', tree)
				outTrees.write(tree)
				i += 1
				if i >= n:
					break
		rmdirs(outdir)
		if i >= n:
			break

if __name__ == '__main__':
	main(inPar=sys.argv[1])
