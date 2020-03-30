# divideDICOM.py
# This script takes an input directory where DICOM files are stored, and saves them divided into a directories schema mimicing Osirix
# as follows: PatientName/StudyDescription_StudyDate/SeriesDescription/IM-SeriesNumber-InstanceNumber.dcm


# Prerrequisites: pydicom library needs to be installed - Note: for older versions you might need to replace pydicom with dicom
# To run, just change the input_list name, providing a list of directories you want to use the script on, and 'python/python3 divideDICOM.py' 

# ATTN: Not working fully for MRI, when there are SeriesDescription fields like '(13371/900/18)-(13371/800/18)' etc

import glob
import os
import pydicom as dicom
import shutil

# *************************************************************************************************************************************
# MAIN 
# *************************************************************************************************************************************

# Input list containing the list of directories where the DICOM files are stored
inputList = 'list_directories_to_divide.txt' 

with open(inputList, 'r') as file:
    line = file.readline()
    
    while line:
       oldpath  = [line.strip()]    
       upstream = os.path.dirname(oldpath[0])
       files    = glob.glob(oldpath[0] + '/*')

       for filename in files:
            dicominfo    = dicom.read_file(filename)
            
            # New path will be: PatientName/StudyDescription_StudyDate/SeriesDescription
            newDir          = dicominfo.PatientName
            newSubDir       = dicominfo.StudyDescription + '_' + dicominfo.StudyDate
            newSubSubDir    = dicominfo.SeriesDescription

            # Clean the path names of undesired characters
            newSubDirstr    = str(newSubDir).replace(" ", "_")
            newSubSubDirStr = str(newSubSubDir).replace(" ", "_")
            newSubSubDirStr = newSubSubDirStr.replace("__", "_")
            newSubSubDirStr = newSubSubDirStr.replace("/","-")
            newpath         = upstream + os.sep + str(newDir) + os.sep + newSubDirstr + os.sep + newSubSubDirStr
            
            # If ImageType is Localizer, then change the subsubdir name 
            imagetype    = dicominfo.ImageType 
            if 'LOCALIZER' in imagetype:
                newpath      = upstream + os.sep + str(newDir) + os.sep + str(newSubDir).replace(" ", "_") + os.sep + 'Localizers'
            
            # New file name will be: IM-SeriesNumber-InstanceNumber.dcm
            instance    = dicominfo.InstanceNumber
            series      = dicominfo.SeriesNumber
            newfilename = 'IM-' + f'{series:04}' + '-' + f'{instance:04}' + '.dcm'  
            newfile     = newpath + os.sep + newfilename

            if not os.path.exists(newpath):
                os.makedirs(newpath)
            
            shutil.copy(filename, newfile)
                
       line = file.readline()

