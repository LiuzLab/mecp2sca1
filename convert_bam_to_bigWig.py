import time
import os
import argparse
import re
import glob


def main():
    #python Step_4_QC.py --jobDir GSE122099_res
    #python Step_4_QC.py --jobDir GSE83243_res
    #python Step_4_QC.py --jobDir GSE103471_res
    #python Step_4_QC.py --jobDir GSE107915_res
    #python Step_4_QC.py --jobDir GSE108256_res
    #python Step_4_QC.py --jobDir GSE78519_res
    #python Step_4_QC.py --jobDir GSE84125_res
    #python Step_4_QC.py --jobDir GSE89952_res
    parser = argparse.ArgumentParser()
    parser.add_argument("-jobDir", "--jobDir",  help="Proivde jobDir")
    args = parser.parse_args()

    #make a big wig directory
    outDirName = args.jobDir + '/bigwig'
    cmd = 'mkdir ' + outDirName
    print('cmd:', cmd)
    os.system(cmd)

    sampleIndex = 'SRR'
    #loop and get the bam files
    fileList = []
    sampleIndexList = []
    for f1 in glob.glob(args.jobDir + "/*"):
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



    #/home/rami/miniconda3/bin/bamCoverage
    cmdPath = '/home/rami/miniconda3/bin/'
    for fileName in fileList:
        print('fileName:', fileName)
        s1 = fileName.split('/')
        print('s1:', s1)
        s2 = s1[-1]
        s2 = s2.split('_')
        sampleId = s2[0]
        print('sampleId:', sampleId)
        #sampleIndexList.append(s[1])
        cmd = 'nohup ' + cmdPath + 'bamCoverage -b ' + fileName + ' -bs 10 -of bigwig -o ' + outDirName + '/' + sampleId + '.bw &'
        print('cmd:', cmd)
        os.system(cmd)



#cmd = 'nohup /mnt/hdd/atrostle/miniconda2/envs/py3/bin/bamCoverage -b' + starResDir + '/*STAR_Aligned.sortedByCoord.out.bam' + ' -bs 10 -of bigwig -o' + args.sampleId + '.bw &'
#   print ('bw creation cmd:', cmd)
#   os.system(cmd)

main()
