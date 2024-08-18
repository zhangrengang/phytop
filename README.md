
### Quick install and start ###
```
git clone https://github.com/zhangrengang/phytop
cd phytop

# install
conda env create -f phytop.yaml
conda activate phytop
python setup.py install

# start
cd example_data

# barcharts
phytop astral.tree

# barcharts with collapse for clades
phytop astral.tree -clades setcladefile -collapse

# piecharts
phytop astral.tree -pie -cp
```

### INPUT ###
When runing ASTRAL, please use `-u 2` (for [C++ version](https://github.com/chaoszhang/ASTER), including `astral`, `astral-pro` and `astral-hybrid` etc.) or 
`-t 2` (for [JAVA version](https://github.com/smirarab/ASTRAL/), including ASTRAL-III and ASTRAL-MP) option. Then, the output species tree from ASTRAL can be used as input to `phytop`.

### Usage ###
```
usage: phytop [-h] [-alter NEWICK] [-g NEWICK] [-align] [-cp] [-branch_size BRANCH_SIZE] [-leaf_size LEAF_SIZE] [-sort]
              [-notext] [-figsize FIGSIZE] [-fontsize FONTSIZE] [-figfmt FIGFMT] [-polytomy_test] [-pie] [-pie_size PIE_SIZE]
              [-pie_fold PIE_FOLD] [-bl] [-test [TAXON/FILE [TAXON/FILE ...]]] [-astral_bin STR] [-outgroup STR]
              [-clades FILE] [-collapse [TAXON/FILE [TAXON/FILE ...]]] [-onshow TAXON/FILE [TAXON/FILE ...]]
              [-noshow TAXON/FILE [TAXON/FILE ...]] [-subset TAXON/FILE [TAXON/FILE ...]] [-pre STR] [-tmp DIR]
              NEWICK

Visualizing ILS/IH signals on species tree from ASTRAL.

optional arguments:
  -h, --help            show this help message and exit

Input:

  NEWICK                Species tree output by ASTRAL (using option `-u 2` for C++ versions and `-t 2` for JAVA versions)
                        [required]
  -alter NEWICK         Show the tree (e.g. a timetree) instead of the ASTRAL tree (their topologies MUST be identical)
                        [default=None]
  -g NEWICK, -genetrees NEWICK
                        gene trees for branch lengths in TEST mode [default=None]

Tree options:

  -align                Align tips [default=False]
  -cp, -concordance_percent
                        Show gene-species trees concordance percent at inner nodes instead of PP [default=False]
  -branch_size BRANCH_SIZE
                        Font size of text in branch [default=48]
  -leaf_size LEAF_SIZE  Font size of leaf name [default=60]

Barcharts options:

  -sort                 Sort q1, q2 and q3, which will miss the directionality [default=False]
  -notext               Do not draw text on the barcharts [default=False]
  -figsize FIGSIZE      Figure size of barcharts [default=3]
  -fontsize FONTSIZE    Font size of text in barcharts [default=13]
  -figfmt FIGFMT        Figure format of barcharts in tmpdir [default=png]
  -polytomy_test        Test for polytomies [default=False]

Piecharts options:

  -pie, -pie_chart      Use piechart instead of barchart [default=False]
  -pie_size PIE_SIZE    Size of Piecharts [default=30]
  -pie_fold PIE_FOLD    Fold of font size between Barcharts and Piecharts [default=6]
  -bl                   Branch lengths to check [default=False]

Branch length (BL) options:

Test mode:

  -test [TAXON/FILE [TAXON/FILE ...]]
                        Test four-taxon (the first is outgroup and others are sampled for three ingroups) [default=None]
  -astral_bin STR       ASTRAL command ('astral-pro', 'astral-hybrid', ...) [default=astral-pro]
  -outgroup STR         Outgroup [default: the first of `-test`]

Clade operateion:

  -clades FILE          Difinition of clades [default=None]
  -collapse [TAXON/FILE [TAXON/FILE ...]]
                        Collapse clades [default=None]
  -onshow TAXON/FILE [TAXON/FILE ...]
                        Only show charts on these inner nodes [default=None]
  -noshow TAXON/FILE [TAXON/FILE ...]
                        Don't show charts on these inner nodes [default=None]
  -subset TAXON/FILE [TAXON/FILE ...]
                        Show a subset clade with their MCRA [default=None]

Output:

  -pre STR, -prefix STR
                        Prefix for output [default=None]
  -tmp DIR, -tmpdir DIR
                        Temporary directory [default=tmp]
```