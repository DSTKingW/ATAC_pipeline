working_dir=`pwd`
ref=$1
nt=$2
sample=$3
r1=$4
r2=$5
 
bowtie2 -k 10 -p $nt --very-sensitive -X 2000 --rg-id "@RG:\tID:$sample\tSM:$sample\tPL:ILLUMINA\tCN:Euler\tLB:$sample.LIB\tPU:test_pu" -x $ref -1 $r1 -2 $r2 | samtools sort -@ $nt > $sample.bam
sambamba markdup -t $nt $sample.bam $sample.hg19.raw.bam
rm -rf $sample.bam
samtools view -b -h -f 3 -F 4 -F 8 -F 256 -F 1024 -F 2048 -q 30 $sample.hg19.raw.bam chr1 chr2 chr3 chr4 chr5 chr6 chr7 chr8 chr9 chr10 chr11 chr12 chr13 chr14 chr15 chr16 chr17 chr18 chr19 chr20 chr21 chr22 chrX chrY  > $sample.hg19.clean.bam
sambamba sort -t $nt -o $sample.hg19.bam $sample.hg19.clean.bam
sambamba index -t $nt $sample.hg19.bam
rm -f $sample.hg19.sorted.bam $sample.hg19.clean.bam $sample.hg19.clean.bam.bai $sample.hg19.sorted.bam.bai
