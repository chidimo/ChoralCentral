# remove tmp directory. Run once daily

import os
import shutil

from django.conf import settings

tmp = os.path.join(settings.BASE_DIR, 'media', 'tmp')
shutil.rmtree(tmp)
