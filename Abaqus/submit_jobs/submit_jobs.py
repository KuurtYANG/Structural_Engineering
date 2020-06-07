#!/usr/bin/env python
# coding: utf-8

from abaqus import *
from abaqusConstants import *
import job
import os

def get_jobnames(folder_list, rule='.inp'):
    job_list=[]
    path_list=[]
    for folder_name in folder_list:
        try:
            path_dir = os.getcwd()+'\\'+folder_name
            job_sub = []
            file_list = os.listdir(path_dir)
            for file_name in file_list:
                if file_name.endswith(rule) and \
                    file_name.rpartition('.')[0]+'.odb' not in file_list:
                    job_sub.append(file_name.rpartition('.')[0])
            job_list.append(job_sub)
            path_list.append(path_dir)
        except:
            pass
    return job_list, path_list

# ***************************************************** #
folder_list = ['your_folder_name', 'folder_name']

job_names, path_list = get_jobnames(folder_list)

for i, path in enumerate(path_list):
    os.chdir(path)
    for subjob in job_names[i]:
        try: 
            c_job = mdb.JobFromInputFile(name=subjob, inputFileName=path+'\\'+subjob+'.inp',
                                numCpus=6, numDomains=6, nodalOutputPrecision=FULL)
            c_job.submit()
            c_job.waitForCompletion()
        except:
            pass