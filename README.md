
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
