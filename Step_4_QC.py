import time
import os
import argparse
import re
import glob



def callMultiQC(jobDir, sampleIndex, studyId):
    print('call multiQC')
    print('jobDir:', jobDir, 'sampleIndex:', sampleIndex)
    #/home/rami/miniconda3/lib/python3.6/site-packages/multiqc
    cmdPath = '/home/rami/miniconda3/bin/'
    #fastqQCDir = args.jobDir + '/' + args.sampleId + '/fastQC'
    outDir = jobDir + '/multiQC'
    cmd = 'multiqc ' + jobDir + ' -o ' + outDir
    print('cmd:', cmd)
    os.system(cmd)

def callGeneBodyCov_rseqc(jobDir, sampleIndex, studyId):
    print('call rseqc gen body coverage')
    #bedFile = '/mnt/hdd/rami/NGS_data/mm10_ERCC92_tab.bed'
    #bedFile = '/mnt/hdd/rami/NGS_data/GRCm38p6_vM18.bed'
    #bedFile = '/mnt/hdd/rami/NGS_data/GRCm38_mm10_Ensembl_nochr.bed'
    bedFile = '/mnt/hdd/rami/NGS_data/GRCm38_mm10_Ensembl.bed'
    outDir = jobDir  #this is just the prefix needed
    #geneBody_coverage.py -r hg19.housekeeping.bed -i bam_path.txt  -o output
    cmdPath = ''
    ##SRR3709138_STAR_Aligned.sortedByCoord.out.bam
    #go thru the results folder and get all the bam files and write to a file
    fileList = []
    sampleIndexList = []
    for f1 in glob.glob(jobDir + "/*"):
        if re.search(sampleIndex, f1):
            print('f1:', f1)
            s = f1.split('/')
            print('s:', s)
            sampleIndexList.append(s[1])
            for f2 in glob.glob(f1 + "/STAR/*"):
                print('f2:', f2)
                if re.search('sortedByCoord.out.bam', f2):
                    if re.search('.bai',f2):
                        continue
                    fileList.append(f2)

    if len(fileList) == 0:
        print('samples:', sampleIndexList)
        s3Folder = 's3://sca-1/'
        for sampleID in sampleIndexList:
            #downlaod the bam and bai files
            downDir = jobDir + '/' + sampleID + '/STAR/'
            cmd = 'aws s3 cp ' + s3Folder + jobDir + '/' + sampleID + '/STAR/' + sampleID + '_STAR_Aligned.sortedByCoord.out.bam' + ' ' + downDir
            #print('cmd:', cmd)
            f = jobDir + '/' + sampleID + '/STAR/' + sampleID + '_STAR_Aligned.sortedByCoord.out.bam'
            fileList.append(f)
            os.system(cmd)
            cmd = 'aws s3 cp ' + s3Folder + jobDir + '/' + sampleID + '/STAR/' + sampleID + '_STAR_Aligned.sortedByCoord.out.bam.bai' + ' ' + downDir
            #print('cmd:', cmd)
            os.system(cmd)

    print('fileList:', fileList)

	#make a dir for geneBody_coverag
    resDir = jobDir + '/geneBodyCov-rseqc/'
    cmd = 'mkdir ' + resDir
    os.system(cmd)

    fileName = jobDir + '/' +studyId + '_geneBodyCov_tmpList.txt'
    #check if file exists , if not create it
    if( os.path.exists(fileName) == False):
        cmd = 'touch ' + fileName
        os.system(cmd)


    runSampleList = []
    #read the file and get list of sample in it
    with open(fileName, 'r') as handler:
        for line in handler:
            line = line.strip()
            runSampleList.append(line)
    #print('runSampleList:', runSampleList)
    outFile = open(fileName, 'a')

    maxK = 16
    k = 0
    for bamFile in fileList:
        #SRR3709138_STAR_Aligned.sortedByCoord.out.bam
        s = bamFile.split('/')
        s = s[-1]
        sampleName = s.split('_')
        sampleName = sampleName[0]
        if sampleName in runSampleList:
            continue
        print('sample:', sampleName)
        outFile.write(sampleName + '\n')
        outFileName = resDir + sampleName + '_geneBodyCov-rseqc.txt'
        nohupFileName = studyId + '_' + sampleName + '_geneBodyCov-rseqc_nohup.txt'
        #cmd = 'nohup ' + cmdPath + 'geneBody_coverage.py -i ' + bamFile + ' -r ' + bedFile + ' > ' + outFileName + ' ' + ' > ' + nohupFileName  + ' &'
        # geneBody_coverage.py -r hg19.housekeeping.bed -i test.bam -o output
        #time geneBody_coverage.py -r /mnt/hdd/rami/NGS_data/GRCm38p6_vM18.bed -i /mnt/hdd/rami/projects/sca1_portal/rna_seq/code/GSE103471_res/SRR6004714/STAR/SRR6004714_STAR_Aligned.sortedByCoord.out.bam
        #-o /mnt/hdd/rami/projects/sca1_portal/rna_seq/code/GSE103471_res/geneBodyCov-rseqc/SRR6004714
        cmd = 'nohup ' + cmdPath + 'geneBody_coverage.py -r ' + bedFile + ' -i ' + os.getcwd() + '/' + bamFile + ' -o ' + os.getcwd() +  '/' +resDir  + studyId + '_' + sampleName + ' & '
        print('cmd:', cmd)
        os.system(cmd)
        time.sleep(3)
        k = k + 1
        #if k == maxK:
        #    break


    outFile.close()

    #move files to it
    #for f1 in glob.glob(jobDir + "/*"):
    #    if re.search(r'geneBodyCoverage', f1):
    #        print('f1:', f1)
    #        cmd = 'mv ' + f1 + ' ' + resDir
    #        os.system(cmd)



def callReadDist_rseqc(jobDir, sampleIndex, studyId):
    print('call rseqc read dist')
    #cmd:read_distribution.py  -i Pairend_StrandSpecific_51mer_Human_hg19.bam -r hg19.refseq.bed12
    #bedFile = '/mnt/hdd/rami/NGS_data/GRCm38p6_vM18.bed'
    #bedFile = '/mnt/hdd/rami/NGS_data/GRCm38_mm10_Ensembl_nochr.bed'
    bedFile  = '/mnt/hdd/rami/NGS_data/GRCm38_mm10_Ensembl.bed'
    cmdPath = ''
    #go thru each BAM file and call it
    #go thru the results folder and get all the bam files and write to a file
    fileList = []
    for f1 in glob.glob(jobDir + "/*"):
        if re.search(sampleIndex, f1):
            #print('f1:', f1)
            for f2 in glob.glob(f1 + "/STAR/*"):
                if re.search('sortedByCoord.out.bam', f2):
                    #print('f2:', f2)
                    if re.search('.bai',f2):
                        continue
                    fileList.append(f2)

    #make a dir for geneBody_coverag
    resDir = jobDir + '/readDist-rseqc/'
    cmd = 'mkdir ' + resDir
    os.system(cmd)


    fileName = jobDir + '/' +studyId + '_readDist_tmpList.txt'
    #check if file exists , if not create it
    if( os.path.exists(fileName) == False):
        cmd = 'touch ' + fileName
        os.system(cmd)

    runSampleList = []
    #read the file and get list of sample in it
    with open(fileName, 'r') as handler:
        for line in handler:
            line = line.strip()
            runSampleList.append(line)
    #print('runSampleList:', runSampleList)
    outFile = open(fileName, 'a')

    maxK = 16
    k = 0
    for bamFile in fileList:
        #SRR3709138_STAR_Aligned.sortedByCoord.out.bam
        s = bamFile.split('/')
        s = s[-1]
        sampleName = s.split('_')
        sampleName = sampleName[0]
        if sampleName in runSampleList:
            continue
        print('sample:', sampleName)
        outFile.write(sampleName + '\n')

        outFileName = resDir + sampleName + '_readDist-rseqc.txt'
        nohupFileName = studyId + '_' + sampleName + '_readDist-rseqc_nohup.txt'
        cmd = 'nohup ' + cmdPath + 'read_distribution.py -i ' + os.getcwd() + '/' + bamFile + ' -r ' + bedFile + ' > ' + outFileName + ' ' + ' & '
        #cmd = cmdPath + 'read_distribution.py -i ' + os.getcwd() + '/' + bamFile + ' -r ' + bedFile + ' > ' + outFileName
        print('cmd:', cmd)
        os.system(cmd)
        time.sleep(2)
        k = k + 1
        #if k == maxK:
        #    break
        #break



    outFile.close()

def main():
    print('Running QC step 1')
    #python Step_4_QC.py --studyId GSE108256 --jobDir GSE108256_res
    #python Step_4_QC.py --studyId GSE83243 --jobDir GSE83243_res
    #python Step_4_QC.py --studyId GSE103471 --jobDir GSE103471_res
    #python Step_4_QC.py --studyId GSE107915 --jobDir GSE107915_res
    #python Step_4_QC.py --studyId GSE84125 --jobDir GSE84125_res

    #python Step_4_QC.py --studyId GSE122099 --jobDir GSE122099_res
    #python Step_4_QC.py --studyId GSE78519 --jobDir GSE78519_res
    #python Step_4_QC.py --studyId GSE89952 --jobDir GSE89952_res
    parser = argparse.ArgumentParser()
    parser.add_argument("-studyId", "--studyId",  help="Proivde studyId")
    parser.add_argument("-jobDir", "--jobDir",  help="Proivde jobDir")
    args = parser.parse_args()

    #index used to find the sample results folders
    sampleIndex = 'SRR'


    #call RSeqc genebody coverage
    callGeneBodyCov_rseqc(args.jobDir, sampleIndex, args.studyId)

    #call RSeqc
    callReadDist_rseqc(args.jobDir, sampleIndex, args.studyId)

    #call multiQc provide the jobDir and the prefix or part of the sample names used
    callMultiQC(args.jobDir, sampleIndex, args.studyId)



main()
