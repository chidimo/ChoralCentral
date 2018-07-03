# /home/parousia/.virtualenvs/choralcentral-8n7QT1vQ/bin/python /home/parousia/choralcentral/scheduled_tasks/utils.py
import os

cmd1 = 'python manage.py algolia_reindex'
cmd2 = 'python manage.py cc_backup_score'
cmd3 = 'python manage.py cc_backup_midi'

os.system(cmd1) # reindex algolia database
os.system(cmd2) # reindex algolia database
os.system(cmd3) # reindex algolia database

with open('cmds_.txt', 'w+') as f:
    f.write('Executed commands\n\n')
    f.write(cmd1)
    f.write('\n')
    f.write(cmd2)
    f.write('\n')
    f.write(cmd3)
    f.write('\n')