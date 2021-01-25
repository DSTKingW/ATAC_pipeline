working_dir=`pwd`
shifts=$1
bam=$2

## zy mod 20191123: Genrich *NEEDS* a raw output bam from bowtie2 that includes secondary mapping results. Hence clean bam is not suitable. 
## zy mod 20191201: changed back into original bam to check

rawbam=`basename $bam .hg19.bam`.hg19.raw.bam
sample=`basename $bam .bam`

/home/changluyuan/.pyenv/versions/3.6.2/bin/macs2 callpeak -t $bam -f BAMPE -n `basename $bam .hg19.bam`.macs2_BAMPE

sambamba sort -n -t 20 -o $sample.sortedByName.bam $bam; 

Genrich -t $sample.sortedByName.bam -o $sample.Genrich.narrowPeak -r -E /gpfs/genomedb/atac/hg19_blacklist.merge.bed -m 1 -j


