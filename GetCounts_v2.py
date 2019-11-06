import os, sys, glob, argparse, re
#this will make the counts for all the samples in the right format from the STAR counts file

def get_counts_1(countFile, sampleId, jobDir):
    #files=glob.glob("*ReadsPerGene.out.tab")
    fileName = countFile.replace("ReadsPerGene.out.tab","ReadCounts_v2.txt")
    outFile=open(fileName,"w")

    lines = open(countFile,"r").readlines()[4:]
    for line in lines:
        data=line.strip().split("\t")
        count=int(data[2])+int(data[3])
        outFile.write(data[0]+"\t"+str(count)+"\n")
        #print('count:', count)
        #break

    outFile.close()

def main():
    #python GetCounts_v2.py -jobDir GSE122099_res
    #python GetCounts_v2.py -jobDir GSE108256_res
    parser = argparse.ArgumentParser()
    parser.add_argument("-jobDir", "--jobDir",  help="Proivde jobDir")
    args = parser.parse_args()

    #loop thru samples
    for f1 in glob.glob(args.jobDir + "/*"):
        if re.search('SRR', f1):
            #print('f1:', f1)
            sampleId = f1.split('/')
            sampleId = sampleId[-1]
            print('sample:', sampleId)
            #get the STAR dir
            countFile = f1 + '/STAR/' + sampleId + '_STAR_ReadsPerGene.out.tab'
            print('countFile:', countFile)
            get_counts_1(countFile, sampleId, args.jobDir)
            #break




main()


#for file in inFile:
#	out=file.replace("ReadsPerGene.out.tab","ReadCounts_v2.txt")
#	filewrite=open(out,"w")
#	lines=open(file,"r").readlines()[4:]
#	for line in lines:
#		data=line.strip().split("\t")
#		count=int(data[2])+int(data[3])
#		filewrite.write(data[0]+"\t"+str(count)+"\n")
