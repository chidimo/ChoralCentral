# run with `source virtualenvwrapper.sh && workon env_name && python script_name.py`
# `source virtualenvwrapper.sh && workon __cc && python django_data_dump.py`

import os
import time

dump_directory = '/home/parousia/backups'
datetime = time.strftime('%Y_%m_%d_%H_%M_%S')
db_save_file = "choralcentral_json_dump_{}.json".format(datetime)

if not os.path.exists(dump_directory):
    os.makedirs(dump_directory)

django_data_dump_cmd = "python manage.py dumpdata --indent 4 --natural-foreign > " + os.path.join(dump_directory, db_save_file)
os.system(django_data_dump_cmd)
