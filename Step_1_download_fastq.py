import time
import os
import argparse
import re


def main():
    #python Step_1_download_fastq.py -sampleId SRR3658602 -jobDirGSE83243_res
    print('Running step 1 downalod fastq')
    parser = argparse.ArgumentParser()
    parser.add_argument("-sampleId", "--sampleId",  help="Proivde sample Id")
    parser.add_argument("-jobDir", "--jobDir",  help="Proivde jobDir")
    args = parser.parse_args()
    #make a fastq dir
    fastqDir = args.jobDir + '/' + args.sampleId + '/fastq_files'
    cmd = 'mkdir ' + fastqDir
    os.system(cmd)

    cmdPath = '/home/rami/hdd/tools/sra_toolkit/sratoolkit.2.9.6-1-centos_linux64/bin/'
    #fastqdumpCmd = cmdPath + 'fastq-dump --split-files --outdir ' + fastqDir + ' ' + args.sampleId
    fastqdumpCmd = cmdPath + 'fasterq-dump --split-files --outdir ' + fastqDir + ' ' + args.sampleId
    print('cmd:', fastqdumpCmd)
    start_time = time.time()
    os.system(fastqdumpCmd)
    end_time = time.time()
    process_time = end_time - start_time
    print('time:', process_time)


main()
