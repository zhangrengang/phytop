import sys,os
import copy
import argparse
import shutil
import json
import math
import multiprocessing
from collections import OrderedDict, Counter
from .Astral import AstralTree
from .RunCmdsMP import logger
from .small_tools import mkdirs
from .__version__ import version


bindir = os.path.dirname(os.path.realpath(__file__))

def makeArgparse():
	parser = argparse.ArgumentParser( 
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description='Visualizing ILS/HI signals on species tree from ASTRAL.',
		)
	# input
	parser.add_argument("astral", metavar='NEWICK',
					help="Species tree output by ASTRAL (using option `-u 2` for C++ versions and `-t 2` for JAVA versions) [required]")
	parser.add_argument('-alter', default=None, type=str, dest='alter',  metavar='NEWICK',
                    help="Show the tree (e.g. a timetree) instead of the ASTRAL tree (their topologies MUST be identical) [default=%(default)s]")
	parser.add_argument('-g', '-genetrees', default=None, type=str, dest='genetrees',  metavar='NEWICK',
                    help="gene trees for branch lengths [default=%(default)s]")

	# clade operateion
	parser.add_argument('-clades', default=None, type=str,  dest='clades',  metavar='FILE',
                    help="Difinition of clades [default=%(default)s]")

	parser.add_argument('-collapse', default=None, type=str, nargs='*', dest='collapsed',  metavar='TAXON/FILE',
					help="Collapse clades [default=%(default)s]")
	parser.add_argument('-onshow', default=None, type=str, nargs='+', dest='onshow',  metavar='TAXON/FILE',
                    help="Only show barcharts on these inner nodes [default=%(default)s]")
	parser.add_argument('-noshow', default=None, type=str, nargs='+', dest='noshow',  metavar='TAXON/FILE',
                    help="Don't show barcharts on these inner nodes [default=%(default)s]")


	parser.add_argument('-subset', default=None, type=str, nargs='+', dest='subset',  metavar='TAXON/FILE',
                    help="Show a subset clade with their MCRA [default=%(default)s]")

	# test
	parser.add_argument('-test', default=None, type=str,  nargs='*', dest='test_clades',  metavar='TAXON/FILE',
                    help="Test four-taxon (the first is outgroup and others are sampled for three ingroups) [default=%(default)s]")
	parser.add_argument('-astral_bin', default='astral-pro', type=str,  metavar='STR',
                    help="ASTRAL command ('astral-pro', 'astral-hybrid', ...) [default=%(default)s]")
	parser.add_argument('-outgroup', default=None, type=str, metavar='STR',
                    help="Outgroup [default: the first of `-test`]")

	# output
	parser.add_argument('-pre', '-prefix', default=None, type=str, dest='prefix', metavar='STR',
					help="Prefix for output [default=%(default)s]")
	parser.add_argument('-tmp', '-tmpdir', default='tmp', dest='tmpdir', type=str, metavar='DIR',
					help="Temporary directory [default=%(default)s]")

	# set barcharts
	parser.add_argument('-sort', action="store_true", default=False, 
                    help="Sort q1, q2 and q3, which will miss the directionality [default=%(default)s]")
	parser.add_argument('-notext', action="store_true", default=False, 
                    help="Do not draw text on the barcharts [default=%(default)s]")
	parser.add_argument('-figsize', default=3, type=float, 
					help="Figure size of barcharts [default=%(default)s]")
	parser.add_argument('-fontsize', default=13, type=float,
                    help="Font size of text in barcharts [default=%(default)s]")

	# pie
	parser.add_argument('-pie', '-pie_chart', action="store_true", default=False, dest='pie',
                    help="Use piechart instead of barchart [default=%(default)s]")
	parser.add_argument('-cp', '-concordance_percent', action="store_true", default=False,
                    help="Show gene-species trees concordance percent at inner nodes instead of PP [default=%(default)s]")

	args = parser.parse_args()
	return args

def plot(**kargs):
	mkdirs(kargs['tmpdir'])
	AstralTree(**kargs).run()
def main():
	args = makeArgparse()
	logger.info('Command: {}'.format(' '.join(sys.argv)))
	logger.info('Version: {}'.format(version))
	logger.info('Arguments: {}'.format(args.__dict__))
	pipeline = plot(**args.__dict__)

if __name__ == '__main__':
	main()
