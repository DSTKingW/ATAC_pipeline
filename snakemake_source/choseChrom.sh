working_dir=`pwd`
bam=$1
chrs=$2
sambamba view -s 0.1 -f bam -o `basename $bam .bam`.$2.bam -s 0.1 $bam $2
