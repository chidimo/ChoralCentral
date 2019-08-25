# mysqldump -u parousia -h parousia.mysql.pythonanywhere-services.com 'parousia$funn'  > db-backup-funn.sql
# https://www.pythonanywhere.com/forums/topic/119/

#!/usr/bin/python
import os
import time

db_User_Name = 'parousia'
DB_User_Password = 'chinekeIGWEna474'
app_name = 'choralcentral'
DB_Name = 'parousia$choral'
backupDir = '/home/parousia/backups/choralcentral/mysql'
datetime = time.strftime('%Y-%m-%d-%H-%M-%S')
db_save_file = "{}_{}_{}.sql".format(db_User_Name, app_name, datetime)

print("creating backup folder")
if not os.path.exists(backupDir):
    os.makedirs(backupDir)

print("Now creating backup for ", app_name)
mysqldump_cmd = "mysqldump -u " + db_User_Name + " --password='" +\
    DB_User_Password + "' -h parousia.mysql.pythonanywhere-services.com --databases '" +\
    DB_Name + "' > " + os.path.join(backupDir, db_save_file)
print("Dump cmd:\n", mysqldump_cmd)

os.system(mysqldump_cmd)
