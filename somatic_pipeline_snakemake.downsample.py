#coding=utf-8
import argparse
import os,sys
from collections import OrderedDict
print("Usage: python " + sys.argv[0] + ' sample.conf')
print("sample.conf 包含四列：第一列为sampleid，第二列为eulerid，第三列为R1_fastq，第四列为R2_fastq")
parser = argparse.ArgumentParser(description='')
parser.add_argument('--conf')
parser.add_argument('--down')
args = parser.parse_args()
conffile = args.conf
downsample = args.down
Sample = OrderedDict()
with open(conffile) as conf:
    for line in conf:
        list1 = line.strip().split('\t')
        if len(list1) != 4:
            print('sample.conf must 4 columns!!!!')
            exit(-1)

        sampleid = list1[0]
        eulerid= list1[1]
        fastq1 = list1[2]
        fastq2 = list1[3]
        Sample[eulerid] = fastq1+'\t'+fastq2
scriptpath  = os.path.dirname(sys.argv[0])
for sampleid in Sample:
    dirname = sampleid
    os.system('mkdir -p {}'.format(dirname))
    os.system('cp {}/snakemake_source/* {}'.format(scriptpath,dirname))
    outfile = open("{}/sample.yaml".format(dirname),'w')
    outfile.write('samples:\n  fastq1: '+Sample[sampleid].split('\t')[0]+'\n  fastq2: '+Sample[sampleid].split('\t')[1]+'\n  id: '+sampleid)
    outfile.close()
    cmd0 = 'unset PYTHONPATH;/home/changluyuan/.pyenv/versions/3.6.2/bin/snakemake -p -s %s/Snakefile_2.py  --cluster "corvidrun-cnf 1 {threads}" -j 1000 --latency-wait 3600 --unlock' % dirname
    cmd = 'corvidrun-gpun 1 1 \'unset PYTHONPATH;nohup /home/changluyuan/.pyenv/versions/3.6.2/bin/snakemake --config downsample='+downsample+' -p -s %s/Snakefile_2.py  --cluster "corvidrun-cnm 1 {threads}" -j 1000 --latency-wait 7200 > %s.log 2>&1 &\'' %(dirname,dirname)
    print cmd0
    print cmd
    os.system(cmd0)
    os.system(cmd)
