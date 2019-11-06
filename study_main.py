#run a study through the pipeline
#this is the first script to run which calls the other steps
import os
import argparse
import re
import pandas as pd
import psutil
import time



def process_metaFile(metaFile, outFileName):
    #with open()
    print('test')
    df = pd.read_csv(metaFile, sep='\t')
    #print(df.head())
    filtColNames = ['genotype', 'age', 'cell_line', 'tissue', 'Organism', 'Experiment', 'Run', 'Sample_Name', 'LibraryLayout', 'strain','sex']
    colNameList = []
    notList = []
    filtColNames_2 = []
    for filtName in filtColNames:
        flag = 0
        for colName in df.columns:
            if filtName in colName:
                colNameList.append(colName)
                filtColNames_2.append(filtName)
                flag = 1
        #if column not found in the sra meta table
        if flag == 0:
            notList.append(filtName)
    print('colNameList:', colNameList)
    #filter the meta files
    filtDf = df[colNameList]
    #change the column names
    filtDf.columns = filtColNames_2
    #add the notList if exists:
    if len(notList) != 0:
        for colName in notList:
            filtDf[colName] = 'NA'
    #
    print(filtDf)
    filtDf.to_csv(outFileName, sep='\t', index=False)


def checkIfProcessRunning(processName):
    #https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def findProcessIdByName(processName, username):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    username if we want to filter the users
    '''

    listOfProcessObjects = []

    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['username', 'pid', 'name' ])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass

    filterObjList = []
    #filter based on user name
    for obj in listOfProcessObjects:
        #print('obj:', obj, 'name:', obj['name'])
        if obj['username'] == username:
            #print('found')
            filterObjList.append(obj)
    return filterObjList
    #return listOfProcessObjects;


def main():
    #python study_main.py -studyId GSE84125 -metaFile ../GEO_sra_runtables/GSE84125_SraRunTable.txt
    #python study_main.py -studyId GSE83243 -metaFile ../GEO_sra_runtables/GSE83243_SraRunTable.txt
    #python study_main.py -studyId GSE103471 -metaFile ../GEO_sra_runtables/GSE103471_SraRunTable.txt
    #python study_main.py -studyId GSE107915 -metaFile ../GEO_sra_runtables/GSE107915_SraRunTable.txt
    #python study_main.py -studyId GSE108256 -metaFile ../GEO_sra_runtables/GSE108256_SraRunTable.txt
	#python study_main.py -studyId GSE122099 -metaFile ../GEO_sra_runtables/GSE122099_SraRunTable.txt
    #python study_main.py -studyId GSE78519 -metaFile ../GEO_sra_runtables/GSE78519_SraRunTable.txt   ##HUMAN
    #python study_main.py -studyId GSE89952 -metaFile ../GEO_sra_runtables/GSE89952_SraRunTable.txt

    parser = argparse.ArgumentParser()
    parser.add_argument("-studyId", "--studyId",  help="Provide studyId or GSE ID")
    parser.add_argument("-metaFile", "--metaFile",  help="Provide the study/GSE meta file")
    args = parser.parse_args()
    print('study id:', args.studyId)
    print('metafile:', args.metaFile)

    #create a job folder
    jobDir = args.studyId + '_res'
    if not os.path.isdir(jobDir) :
        cmd = 'mkdir ' + args.studyId + '_res'
        os.system(cmd)

    #log file
    fileName = args.studyId + '_log.txt'
    logFile = open(fileName, 'w')

    #process the meta file to a standard format
    processMetaFileName = jobDir + '/' + args.studyId + '_process_meta_file.txt'
    process_metaFile(args.metaFile, processMetaFileName)

    #read the processed meta file and run for each sample the sample_main.py script
    metaDf = pd.read_csv(processMetaFileName, sep='\t')
    #get the Organism
    organism = metaDf.at[1,'Organism']
    print('organism:', organism)
    organism = 'Musmusculus'


    #exit()
    #get the SRR names column
    #outFile =open('out.txt', 'w')

    maxJobs = 2 #don't forget the running script counts as well so 2 + 1
    k = 0
    for sampleName in metaDf['Run']:
        continue
        print('sample:', sampleName)
        continue
        processObjList = findProcessIdByName('python', 'rami')
        print('len of idList:', len(processObjList))
        #nohup sh your-script.sh > /path/to/custom.out &
        if len(processObjList) > maxJobs:
            while 1:
                print('waiting')
                time.sleep(30)
                processObjList = findProcessIdByName('python', 'rami')
                if len(processObjList) < maxJobs:
                    print('\n\nstart running sample:', sampleName)
                    logFile.write('processing sample:' + sampleName + '\n')
                    finalResFile = jobDir + '/' + sampleName + '_final_res_file.txt'
                    nohupFileName = args.studyId + '_' + sampleName + '_nohup.out'
                    #call the sample_main script
                    cmd = 'nohup python sample_main.py -studyId ' + args.studyId + ' -sampleId ' + sampleName + ' -organism ' + organism  + ' -jobDir ' + jobDir + ' > ' + nohupFileName  + ' &'
                    print ('sample_main cmd:',cmd)
                    os.system(cmd)
                    break
        else:
            print('start running sample:', sampleName)
            logFile.write('processing sample:' + sampleName + '\n')
            finalResFile = jobDir + '/' + sampleName + '_final_res_file.txt'
            nohupFileName = args.studyId + '_' + sampleName + '_nohup.out'
            #call the sample_main script
            cmd = 'nohup python sample_main.py -studyId ' + args.studyId + ' -sampleId ' + sampleName + ' -organism ' + organism  +' -jobDir ' + jobDir + ' > ' + nohupFileName  + ' &'
            #python sample_main.py -studyId GSE83243 -sampleId SRR3658602 -jobDir GSE83243_res
            print ('\n\nsample_main cmd:',cmd)
            #check how many samples are Running
            os.system(cmd)
        k = k + 1
        #if k == 2:
        #    break
            #check if final res file exist or not
            #restart
            #k = 0


    #calling sample_main above will do processing per each sample, let that finsih first then call quality control
    #the call quality control and
    if 0:
        #step 4 QC
        logFile.write('##########Step 4 started:run QC##########' + '\n')
        cmd = 'python Step_4_QC.py -studyId ' +  args.studyId + ' -jobDir ' + jobDir
        print('cmd:', cmd)
        logFile.write('cmd:' + cmd + '\n')
        startTime = time.time()
        logFile.write('start time:' + str(startTime) + '\n')
        os.system(cmd)
        endTime = time.time()
        elapsedTime = time.time() - startTime
        logFile.write('end time:' + str(endTime) + ' elapsed time:'+ str(elapsedTime) + '\n')
        logFile.write('##########Step 4 finsihed##########' + '\n')

    #uplaod to S3 if needed
    if 0:
        #upload results to S3 and delete big files from local machine
        logFile.write('##########Step 5 started:uplaod to S3##########' + '\n')
        cmd = 'python upload_S3.py -studyId ' +  args.studyId + ' -jobDir ' + jobDir
        print('cmd:', cmd)
        logFile.write('cmd:' + cmd + '\n')
        startTime = time.time()
        logFile.write('start time:' + str(startTime) + '\n')
        os.system(cmd)
        endTime = time.time()
        elapsedTime = time.time() - startTime
        logFile.write('end time:' + str(endTime) + ' elapsed time:'+ str(elapsedTime) + '\n')
        logFile.write('##########Step 5 finsihed##########' + '\n')

    logFile.close()




main()
