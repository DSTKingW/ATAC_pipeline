working_dir=`pwd`
bam=$1

sambamba view -t 10 -f bam -F "not supplementary" $bam | sambamba sort -t 10 -n -o qc.bam /dev/stdin
bedtools bamtobed -bedpe -i qc.bam |grep -v '\.' > qc.bed
python /home/wangyujue/gpfs/ATAC/scr/PBC.py $bam
