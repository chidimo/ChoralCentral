# run with `source virtualenvwrapper.sh && workon env_name && python script_name.py`
# `source virtualenvwrapper.sh && workon __cc && python reset_api_keys.py`

import os
reset_cmd = "python manage.py reset_api_keys -quota 180"
os.system(reset_cmd)
