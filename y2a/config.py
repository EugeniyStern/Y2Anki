class conf:
    def __init__ (self):
       self._root = "C:\\Projects\\Y2A_root\\db\\"
       self._ffmpeg = "C:\\Projects\\Y2A_root\\ffmpeg.exe"

    def root(self):
        return self._root
    
    def ffmpeg(self):
        return self._ffmpeg