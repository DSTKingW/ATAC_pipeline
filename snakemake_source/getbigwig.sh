working_dir=`pwd`
bam=$1

bamCoverage -b $bam -o `basename $bam .bam`.bigwig -bs=20 --minFragmentLength 35 --normalizeUsing RPKM -p=max
