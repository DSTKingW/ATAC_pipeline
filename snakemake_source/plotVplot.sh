working_dir=`pwd`
bed=$1
bam=$2
chrs=$3

python /home/wangyujue/gpfs/ATAC/scr/feature2vplot_mid_strand.py $bed /gpfs/output/20191002_Nova/ATAC/bed/chromosome.for.vplot $bam False `basename $bam .bam`.ctcf.vplot
