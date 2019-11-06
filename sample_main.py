import time
import os
import argparse
import re


def main():
    #args.studyId + ' ' + sampleName + ' ' + jobDir
    #python sample_main.py -studyId GSE122099 -sampleId SRR8146822 -jobDir GSE122099_res
    #python sample_main.py -studyId GSE122099 -sampleId SRR8146786 -jobDir GSE122099_res
    #
    parser = argparse.ArgumentParser()
    parser.add_argument("-studyId", "--studyId",  help="Proivde studyId")
    parser.add_argument("-sampleId", "--sampleId",  help="Proivde sample Id")
    parser.add_argument("-organism", "--organism",  help="Proivde organism")
    parser.add_argument("-jobDir", "--jobDir",  help="Proivde jobDir")
    args = parser.parse_args()
    print('studyId:', args.studyId)
    print('sampleId:', args.sampleId)
    print('jobDir:', args.jobDir)

    #make a dir for sample
    cmd = 'mkdir ' + args.jobDir + '/' + args.sampleId
    os.system(cmd)

    #log file
    fileName = args.studyId + '_' + args.sampleId + '_log.txt'
    logFile = open(fileName, 'w')

    if 1:
        #step 1 download the fastq files from SRR
        logFile.write('##########Step 1 started: downlaod fastq files##########' + '\n')
        cmd = 'python Step_1_download_fastq.py -sampleId ' +  args.sampleId + ' -jobDir ' + args.jobDir
        print('cmd:', cmd)
        logFile.write('cmd:' + cmd + '\n')
        startTime = time.time()
        logFile.write('start time:' + str(startTime) + '\n')
        os.system(cmd)
        endTime = time.time()
        elapsedTime = time.time() - startTime
        logFile.write('end time:' + str(endTime) + ' elapsed time:'+ str(elapsedTime) + '\n')
        logFile.write('##########Step 1 finsihed##########' + '\n')


    if 1:
        #step 2 run fastQC
        logFile.write('##########Step 2 started:run FastQC##########' + '\n')
        cmd = 'python Step_2_run_fastqQC.py -sampleId ' +  args.sampleId + ' -jobDir ' + args.jobDir
        print('cmd:', cmd)
        logFile.write('cmd:' + cmd + '\n')
        startTime = time.time()
        logFile.write('start time:' + str(startTime) + '\n')
        os.system(cmd)
        endTime = time.time()
        elapsedTime = time.time() - startTime
        logFile.write('end time:' + str(endTime) + ' elapsed time:'+ str(elapsedTime) + '\n')
        logFile.write('##########Step 2 finsihed##########' + '\n')

    if 1:
        #step 3 run STAR
        logFile.write('##########Step 3 started:run STAR##########' + '\n')
        cmd = 'python Step_3_run_STAR.py -sampleId ' +  args.sampleId + ' -jobDir ' + args.jobDir
        print('cmd:', cmd)
        logFile.write('cmd:' + cmd + '\n')
        startTime = time.time()
        logFile.write('start time:' + str(startTime) + '\n')
        os.system(cmd)
        endTime = time.time()
        elapsedTime = time.time() - startTime
        logFile.write('end time:' + str(endTime) + ' elapsed time:'+ str(elapsedTime) + '\n')
        logFile.write('##########Step 3 finsihed##########' + '\n')





    logFile.close()





main()
