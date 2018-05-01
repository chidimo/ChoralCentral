# `source virtualenvwrapper.sh && workon __cc && python utils.py`

import os
import shutil

from django.conf import settings

tmp = os.path.join(settings.BASE_DIR, 'media', 'tmp')

shutil.rmtree(tmp) # remove tmp directory
os.system('python manage.py algolia_reindex') # reindex algolia database
