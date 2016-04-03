import arcpy, time, subprocess, traceback

#input time for script to run
time.sleep(60*60*float(raw_input("number of hours:")))
start = time.time()

#################### ENTER VARIABLES #####################################

arcpy.env.workspace = r'C:\Users\XXXX\Documents\XXXX.gdb'   #path to file geodatabase containing new feature classes
ArcSDE = r'C:\Users\XXXX\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\XXXX.sde' #path to ArcSDE geodatabase
feature_dataset_name = 'feature_dataset_name' #input feature dataset name in ArcSDE geodatabase where original feature classes reside
status_csv = r'C:\Users\XXXX\Desktop\upload_status.csv'   #path to a csv output which gives status of job and error message if any

listappend = [("fc_original1","fc_new1"),("fc_original2","fc_new2"),    #update feature class names of original and new ones that are to be appended into the former
               ("fc_original3","fc_new3"),("fc_original4","fc_new4")]

##########################################################################

file = open(status_csv,'a')
feature_dataset = '{}\{}}'.format(ArcSDE, feature_dataset_name)

#Function to append new feature classes to original feature classes in ArcSDE
def append():
    i = 0
    for row in range(len(listappend)):
        try:
            arcpy.Append_management(listappend[i][1], "{}\{}".format(feature_dataset,listappend[i][0]),"NO_TEST", "", "")
            file.write("{},appended\n".format(listappend[i][1]))
        except:
            file.write("{},failed\n".format(listappend[i][1]))  #record any failed uploads in ouput csv
        i += 1

##########################################################################

edit = arcpy.da.Editor(ArcSDE)
attempt = 0
while attempt < 10: #10 attempts to upload, in case there are errors
    try:
        print 'Editor starting\n'
        edit.startEditing()
        edit.startOperation()
        arcpy.env.maintainSpatialIndex = True
        append()    #Input append function here
        edit.stopOperation()
        edit.stopEditing(True)
        file.write("\n\nFeatures saved successfully in sde")
        break
    except Exception, err:
        attempt += 1
        traceback = traceback.print_exc()   #traceback errors
        gpError = "ArcGIS Error:{}".format(arcpy.GetMessages(2))  #geoprocessing errors from ArcGIS
        file.write("{} attempts tried\n{}\n{}\n".format(attempt, traceback, gpError))   #record the errors in output csv
        file.write("----------------------------------------\n")
        time.sleep(20)  #sleep for 20 sec before next attempt to upload, in case server is busy

end = time.time()
date = time.strftime("%d%b%y %H:%M:%S")

file.write("\nscript ended {} secs\n".format(end-start))
file.write(date)
file.close()

#shutdown computer after script is completed
subprocess.call(['C:\Windows\system32\shutdown.exe', "/s"])
