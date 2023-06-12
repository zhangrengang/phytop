
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

# piecharts
phytop astral.tree -pie -cp
```

### INPUT ###
When runing ASTRAL, please use `-u 2` (for [C++ version](https://github.com/chaoszhang/ASTER), including `astral`, `astral-pro` and `astral-hybrid` etc.) or 
`-t 8` (for [JAVA version](https://github.com/smirarab/ASTRAL/), including ASTRAL-III and ASTRAL-MP) option. Then, the output species tree from ASTRAL can be used as input to `phytop`.
