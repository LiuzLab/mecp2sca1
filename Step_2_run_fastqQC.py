import time
import os
import argparse
import re




def main():
    #python Step_2_run_fastqQC.py -sampleId SRR6388218 -jobDir GSE108256_res
    print('Running step 2 FastQC')
    parser = argparse.ArgumentParser()
    parser.add_argument("-sampleId", "--sampleId",  help="Proivde sample Id")
    parser.add_argument("-jobDir", "--jobDir",  help="Proivde jobDir")
    args = parser.parse_args()

    fastqDir = args.jobDir + '/' + args.sampleId + '/fastq_files/'
    #make the fast QC directory
    qcDir = args.jobDir + '/' + args.sampleId + '/fastQC'
    os.system('mkdir ' + qcDir)

    fastQCCmd = '/home/rami/hdd/tools/fastqc/FastQC/fastqc '
    #get the fastq files
    for file in os.listdir(fastqDir):
        cmd = fastQCCmd + ' ' + fastqDir + file + ' -o ' + qcDir
        print('fastqQC cmd:', cmd)
        os.system(cmd)

    


main()
