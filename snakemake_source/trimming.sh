working_dir=`pwd`
downsample=$1
random=$2
in_r1=$3
in_r2=$4
if [ $downsample -gt 1 ] ; then
    /gpfs/users/yanghao/software/bin/seqtk sample -s $random $in_r1 $downsample |/gpfs/bin/common/pigz > $(basename $in_r1).downsample.gz &&
    /gpfs/users/yanghao/software/bin/seqtk sample -s $random $in_r2 $downsample |/gpfs/bin/common/pigz > $(basename $in_r2).downsample.gz
    fastp -V -w `nproc` -h `basename $in_r1 .R1.fastq.gz`.fastp.report.html --adapter_sequence TCGTCGGCAGCGTC --adapter_sequence_r2 GTCTCGTGGGCTCGG -i $(basename $in_r1).downsample.gz -I $(basename $in_r2).downsample.gz -o $(basename $in_r1).trimmed.gz -O $(basename $in_r2).trimmed.gz
else
    fastp -V --length_required 35 -w `nproc` -h `basename $in_r1 .R1.fastq.gz`.fastp.report.html --adapter_sequence TCGTCGGCAGCGTC --adapter_sequence_r2 GTCTCGTGGGCTCGG -i $in_r1 -I $in_r2 -o $(basename $in_r1).trimmed.gz -O $(basename $in_r2).trimmed.gz
fi
