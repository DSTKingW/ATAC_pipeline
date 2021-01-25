working_dir=`pwd`
bigwig=$1

computeMatrix reference-point -S $bigwig -R /gpfs/output/20191002_Nova/ATAC/bed/hg19_promoter.for.ATAC_qc.bed -o `basename $bigwig .bigwig`.matrix.gz  -a 2000 -b 2000 --binSize 1 -p max
