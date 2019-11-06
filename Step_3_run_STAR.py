import time
import os
import argparse
import re
import glob


def main():
    #python Step_3_run_STAR.py -sampleId SRR3658602 -jobDir GSE83243_res
    print('Running step 3 STAR')
    parser = argparse.ArgumentParser()
    parser.add_argument("-sampleId", "--sampleId",  help="Proivde sample Id")
    parser.add_argument("-jobDir", "--jobDir",  help="Proivde jobDir")
    args = parser.parse_args()

    fastqDir = args.jobDir + '/' + args.sampleId + '/fastq_files'
    #make the STAR directory
    starResDir = args.jobDir + '/' + args.sampleId + '/STAR'
    os.system('mkdir ' + starResDir)

    #STAR cmd path
    #starPath = '/mnt/hdd/rami/tools/STAR-2.5.1b/bin/Linux_x86_64_static/'
    #genomeDir = '/mnt/hdd/rami/NGS_data/STAR_MM10'
    #gtfFileName = '/mnt/hdd/rami/NGS_data/mm10_ERCC92_tab.gtf'
    starPath = '/mnt/hdd/rami/tools/STAR-2.6.0a/bin/Linux_x86_64/'
    #organism = 'human'
    organism = 'mouse'
    if organism == 'mouse':
        genomeDir = '/mnt/hdd/rami/NGS_data/STAR_GRCm38p6_primary_overhang1'
    elif organism == 'human':
        genomeDir = '/mnt/hdd/rami/NGS_data/STAR_GRCh38p12_primary_overhang90'

    outNamePrefix = args.sampleId + '_STAR_'

    numThreads = 16
    fastqFile_1 = ''
    fastqFile_2 = ''
    c = 0
    for file in os.listdir(fastqDir):
        if re.search(r'_1.fastq', file):
            fastqFile_1 = fastqDir + '/' + file
            c += 1
        elif re.search(r'_2.fastq', file):
            fastqFile_2 = fastqDir + '/' + file
            c += 1

    print ('c:',c)
    #if it's single not paired
    if c == 0:
        fastqFile_1 = ''
        for file in os.listdir(fastqDir):
            if re.search(r'.fastq', file):
                fastqFile_1 = fastqDir + '/' + file
                c += 1

    starCmd = ''
    print ('fastq 1:', fastqFile_1,'fastq 2:', fastqFile_2)
    if c == 1:
        starCmd = starPath + 'STAR' + ' --runThreadN ' + str(numThreads) + ' --genomeDir ' + genomeDir + ' --quantMode GeneCounts ' + ' --outSAMtype BAM SortedByCoordinate --outFileNamePrefix ' +  outNamePrefix + ' --readFilesIn ' + fastqFile_1
    elif c == 2:
        starCmd = starPath + 'STAR' + ' --runThreadN ' + str(numThreads) + ' --genomeDir ' + genomeDir + ' --quantMode GeneCounts ' + ' --outSAMtype BAM SortedByCoordinate --outFileNamePrefix ' +  outNamePrefix + ' --readFilesIn ' + fastqFile_1 + ' ' + fastqFile_2
    else:
        print ('more than two fastq files')
        exit()

    #run the command
    os.system(starCmd)

    #copy results file to STAR res folder
    for file in glob.glob("*"):
        s = args.sampleId + '_STAR'
        #print('s:', s)
        if re.search(s, file):
            print('file:', file)
            cpCmd = 'mv ' + file + ' ' +  starResDir
            os.system(cpCmd)

    #get the bai
    cmd = 'samtools index ' + starResDir + '/*STAR_Aligned.sortedByCoord.out.bam'
    print ('starindex cmd:', cmd)
    os.system(cmd)


    #gzip the fastq files using pigz
    for file in os.listdir(fastqDir):
        cmd = 'pigz -p 16 ' +  fastqDir + file
        print('pigz:', cmd)
        os.system(cmd)

    #upload the fastq files to S3
    #S3 folder on amazon
    s3MainFolder='s3://sca-1/'
    s3JobFolder = s3MainFolder + args.jobDir + '/' + args.sampleId

    cmd = 'aws s3 cp ' + args.jobDir + '/' + args.sampleId +  '/fastq_files/' + ' ' + s3JobFolder + '/fastq_files/' + ' --recursive'
    print('fastq S3 cmd:', cmd)
    os.system(cmd)

    #delete the fastq files
    cmd = 'rm ' + args.jobDir + '/' + args.sampleId + '/fastq_files/*'
    print('rm cmd:', cmd)
    os.system(cmd)



main()
