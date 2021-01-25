working_dir=`pwd`
matrix=$1

plotHeatmap -m $matrix -out `basename $matrix .matrix.gz`.promoter.pdf --sortUsing mean --sortRegions descend --colorMap Blues
