## zy mod 20191030
## original: wang yujue 2019

import sys,os
import random
from os.path import join
from collections import OrderedDict
import subprocess


path = sys.path[0]
os.chdir(path)
configfile: "config.yaml"
configfile: "sample.yaml"
samples=config["samples"]
#print(samples)
os.system('mkdir -p fastq')
sample_id = samples['id']
#print(sample_id)
os.system('ln -s '+samples['fastq1']+' ./fastq/'+sample_id+'.R1.fastq.gz')
os.system('ln -s '+samples['fastq2']+' ./fastq/'+sample_id+'.R2.fastq.gz')
#os.system('speedseq align -K /gpfs/bin/scripts/somatic_pipeline/src/speedseq.config -t 20 -o '+sample_id+'.hg19 -R \"@RG:\\tID:'+sample_id+'\\tSM:'+sample_id+'\\tPL:ILLUMINA\\tCN:Euler\\tLB:'+sample_id+'.LIB\\tPU:test_pu\" /home/wangyujue/gpfs/Data/RefGenome/ucsc/hg19.fa ./fastq/'+sample_id+'.R1.fastq.gz ./fastq/'+sample_id+'.R2.fastq.gz')
rule all:
    input: 
        sample_id+'.R1.fastq.gz.trimmed.gz',
        sample_id+'.R2.fastq.gz.trimmed.gz',
        sample_id+'.hg19.raw.bam',
        sample_id+'.hg19.raw.bam.bai',
        sample_id+'.hg19.bam',
        sample_id+'.hg19.bam.bai',
        sample_id+'.hg19.bigwig',
        sample_id+'.hg19.matrix.gz',
        sample_id+'.hg19.promoter.pdf',
        sample_id+'.hg19.'+config["site"]+'.vplot.png',
        sample_id+'.macs2_BAMPE_peaks.narrowPeak',
        sample_id+'.macs2_BAMPE_peaks.xls',
        sample_id+'.macs2_BAMPE_summits.bed',
        sample_id+'.hg19.Genrich.narrowPeak',
        sample_id+'_Insertsize.pdf',
        sample_id+'_Insertsize_y_log2.pdf',
        sample_id+'_qcReport.tsv',
        'qc.bed',
        sample_id+'_PBC.tsv',
        sample_id+'_Frip.tsv',
        sample_id+'.hg19.matrix.gz.TSSscore.tsv'

rule trimming:
    input:
        r1 = 'fastq/'+sample_id+'.R1.fastq.gz',
        r2 = 'fastq/'+sample_id+'.R2.fastq.gz'
    output:
        sample_id+'.R1.fastq.gz.trimmed.gz',
        sample_id+'.R2.fastq.gz.trimmed.gz'
    threads:10
    params:
        downsample = config["downsample"]
    log:
        'logs/'+sample_id+'.trimming.log'
    run:
        random_num = random.randint(10,200) ##for downsample random seed
        command="sh trimming.sh {} {} {} {} > {} 2>&1".format(int(params.downsample), random_num, input.r1, input.r2, log)
        print(command)
        os.system(command)

rule alignment:
    input:
        r1=sample_id+'.R1.fastq.gz.trimmed.gz',
        r2=sample_id+'.R2.fastq.gz.trimmed.gz'
    output:
        sample_id+'.hg19.raw.bam',
        sample_id+'.hg19.raw.bam.bai',
        sample_id+'.hg19.bam',
        sample_id+'.hg19.bam.bai'
    params:
        ref=config["refFasta"]
    threads:20
    log:
        'logs/'+sample_id+'.alignment.log'
    run:
        command = "sh alignment.bowtie2.sh {} {} {} {} {}  > {} 2>&1".format(params.ref, threads, sample_id, input.r1, input.r2, log)
        print(command)
        os.system(command)

rule getbigwig:
    input:
        sample_id+'.hg19.bam'
    output:
        sample_id+'.hg19.bigwig'
    threads:4
    log:
        'logs/'+sample_id+'.getbigwig.log'
    run:
        command = "sh getbigwig.sh {}  > {} 2>&1".format(input, log)
        print(command)
        os.system(command)

rule getmatrix:
    input:
        sample_id+'.hg19.bigwig'
    output:
        sample_id+'.hg19.matrix.gz'
    threads:20
    log:
        'logs/'+sample_id+'.getmatrix.log'
    run:
        command = "sh getmatrix.sh {}  > {} 2>&1".format(input, log)
        print(command)
        os.system(command)

rule plotHeatmap:
    input:
        sample_id+'.hg19.matrix.gz'
    output:
        sample_id+'.hg19.promoter.pdf'
    threads:10
    log:
        'logs/'+sample_id+'.plotHeatmap.log'
    run:
        command = "sh plotHeatmap.sh {}  > {} 2>&1".format(input, log)
        print(command)
        os.system(command)

rule plotVplot:
    input:
        sample_id+'.hg19.bam'
    output:
        sample_id+'.hg19.'+config["site"]+'.vplot.png'
    params:
        bed = config["bed"],
        chrs = config["chrs"]
    threads:1
    log:
        'logs/'+sample_id+'.plotVplot.log'
    run:
        command = "sh plotVplot.sh {} {} {}  > {} 2>&1".format(params.bed, input, params.chrs, log)
        print(command)
        os.system(command)

rule callpeak:
    input:
        sample_id+'.hg19.bam'
    output:
        sample_id+'.macs2_BAMPE_peaks.narrowPeak',
        sample_id+'.macs2_BAMPE_peaks.xls',
        sample_id+'.macs2_BAMPE_summits.bed',
        sample_id+'.hg19.Genrich.narrowPeak'
    params:
        shifts = config["shift"]
    threads:1
    log:
        'logs/'+sample_id+'.callpeak.log'
    run:
        command = "sh callpeak.sh {} {}  > {} 2>&1".format(params.shifts, input, log)
        print(command)
        os.system(command)

rule insertSize:
    input:
        sample_id+'.hg19.raw.bam'
    output:
        sample_id+'_Insertsize.pdf',
        sample_id+'_Insertsize_y_log2.pdf'
    threads:1
    log:
        'logs/'+sample_id+'.insertsize.log'
    run:
        command = "sh insertSize.sh {}  > {} 2>&1".format(input, log)
        print(command)
        os.system(command)

rule qcReport:
    input:
        bam = sample_id+'.hg19.raw.bam'
    output:
        sample_id+'_qcReport.tsv'
    threads:10
    log:
        'logs/'+sample_id+'.qcReport.log'
    run:
        command = "sh qcReport.sh {}  > {} 2>&1".format(input.bam, log)
        print(command)
        os.system(command)
## zy mod 20191123: qcReport.sh error without inserting peak parameter. Rewrote MACS2 peak and did not correctly output. 
rule get_QC:
    input:
        sample_id+'.hg19.raw.bam'
    output:
        'qc.bed',
        sample_id+'_PBC.tsv'
    threads:10
    log:
        'logs/'+sample_id+'.get_QC.log'
    run:
        command = "sh get_QC.sh {}  > {} 2>&1".format(input, log)
        print(command)
        os.system(command)

rule Frip:
    input:
        bed = 'qc.bed',
        sample_id+'.macs2_BAMPE_peaks.narrowPeak'
    output:
        sample_id+'_Frip.tsv'
    threads:1
    log:
        'logs/'+sample_id+'.Frip.log'
    run:
        command = "sh Frip.sh {} {}  > {} 2>&1".format(input.bed, input.peak, log)
        print(command)
        os.system(command)

rule TSSscore:
    input:
        sample_id+'.hg19.matrix.gz'
    output:
        sample_id+'.hg19.matrix.gz.TSSscore.tsv'
    threads:1
    log:
        'logs/'+sample_id+'.TSSscore.log'
    run:
        command = "sh TSSscore.sh {}  > {} 2>&1".format(input, log)
        print(command)
        os.system(command)

## 20191127: add Frip TSSscore as single shell
