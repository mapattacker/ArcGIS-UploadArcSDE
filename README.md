## Append new data to ArcSDE geodatabase with a delay
---
### Description
This script serves to automate to append mutiple datasets into existing feature classes within a server ArcSDE geodatabase. It also take into consideration of not overloading the database by having a delay in execution to run (perhaps after office hours), and shutting down the computer after script completion. Basically it is can be breakdown into:

1) Append new data into existing feature classes in an ArcSDE geodatabase

2) Allow a delay by hours when the script will execute, and PC will shutdown after that

3) Generate an output in csv showing the status of append

### Requirements
ArcGIS installation and write access to an ArcSDE geodatabase
Shutdown meant for windows PC. ArcGIS is only available in windows anyway.
