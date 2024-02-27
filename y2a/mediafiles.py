import json
import os
from .config import conf
import subprocess
from .fuf import fuf

class media_writer:
    def __init__ (self, fuf:fuf):
       self.dir = fuf.fuf_dir()
       self.hash = fuf.fuf_hash()

    def write_files(self, audio:bool, video:bool):

        sentence_filename = self.dir + "\\sentences.json"
        text_file = open(sentence_filename, "r")
        json_string = text_file.read()

        sentences = json.loads(json_string)

        c = conf()
        path_video_mp4 = self.dir + "\\full_video.mp4"
        path_audio_mp4 = self.dir + "\\full_audio.mp4"       
        path_video_mov = self.dir + "\\full_video.mov"

        #ffmpeg -i input_file.mp4 -f mov output_file.mov
        # subprocess.run([c.ffmpeg(), 
        #                 "-i",
        #                 path_video_mp4,
        #                 '-f','mov',
        #                 path_video_mov])

        for i in range(len(sentences)):
            print(sentences[i]["start"])
            sentences[i]["filename"] = '{dir}_{i:04d}'.format(dir = self.hash, i= i)

            start_ms = '{x}ms'.format(x=str(sentences[i]["start"]*1000))
            end_ms = '{x}ms'.format(x=str((sentences[i]["end"]+0.3)*1000))

            if audio == True:
                # создать укниальный номер файла
                fname_audio = '{root}\\{fn}_audio.mp4'.format(root=self.dir, fn=sentences[i]["filename"])

                subprocess.run([c.ffmpeg(), 
                                "-y", "-i",
                                path_audio_mp4,
                                "-ss",start_ms,"-to",end_ms,'-c','copy',
                                fname_audio])
            if video == True:
                # создать укниальный номер файла
                fname_video = '{root}\\{fn}_video.mp4'.format(root=self.dir, fn=sentences[i]["filename"])

                subprocess.run([c.ffmpeg(), 
                                "-y", "-i",
                                path_video_mp4,
                                "-ss",start_ms,"-to",end_ms,'-c:v','libx264','-c:a','copy',
                                fname_video])     
        
        # write sentences.json
        json_string = json.dumps(sentences)
        json_file_name = self.dir + "\\sentences.json"
        text_file = open(json_file_name, "w")
        text_file.write(json_string)
        text_file.close()           