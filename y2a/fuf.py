# files and folders
import hashlib
from .config import conf
import os
import json

import unicodedata
import re

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

class fuf:
    def __init__ (self, title):
       self.title = title
       self.hash = str(hashlib.sha256(str(title).encode('utf-8')).hexdigest())[0:8]
       c = conf()
       self.dir_name = c.root() + self.hash + "_"+ slugify(self.title, True)
       isExist = os.path.exists(self.dir_name)
       if not isExist:
        os.makedirs(self.dir_name)
        print("The new directory is created!")
    
    def fuf_dir(self):
       return self.dir_name
    
    def fuf_hash(self):
        return self.hash
    
    def fuf_title(self):
       return self.title



    
    