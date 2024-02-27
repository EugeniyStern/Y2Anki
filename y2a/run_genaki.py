import genanki
from .fuf import fuf
import random
from .config import conf
import json

class anki_deck_writer:
    def __init__ (self, fuf:fuf):
       self.dir = fuf.fuf_dir()
       self.hash = fuf.fuf_hash()
       self.title = fuf.fuf_title()
       self.model_id = str(random.randrange(1 << 30, 1 << 31))

    def write_anki_deck_file(self, audio:bool, video:bool):
        # model
        my_model = genanki.Model(
            self.model_id,
            'Y2A generated cards',
            fields=[
                {'name': 'CardNumber'},
                {'name': 'SrcLanguage'},
                {'name': 'TrgLanguage'},                
                {'name': 'MyMediaVideo'},
                {'name': 'MyMediaAudio'},

            ],
            templates=[
                {
                'name': 'Card 1',
                'qfmt': '{{MyMediaVideo}}',
                'afmt': '{{SrcLanguage}}<hr id="answer">{{TrgLanguage}}',
                },
            ])
        
        deck_id = random.randrange(1 << 30, 1 << 31)
        my_deck = genanki.Deck( 
            deck_id,
            'YGEN_{}'.format(self.title))
        
        # read JSON with filenames
        sentence_filename = self.dir + "\\sentences.json"
        text_file = open(sentence_filename, "r")
        json_string = text_file.read()

        sentences = json.loads(json_string)

        c = conf()   

        my_package = genanki.Package(my_deck)

        for i in range(len(sentences)):
            if video == True:
                fname_video = '{root}\\{fn}_video.mp4'.format(root=self.dir, fn=sentences[i]["filename"])
                my_package.media_files.append(fname_video)

            if audio == True:
                fname_audio = '{root}\\{fn}_audio.mp4'.format(root=self.dir, fn=sentences[i]["filename"])
                my_package.media_files.append(fname_audio)    

            video_file = "[sound:"+sentences[i]["filename"]+"_video.mp4]"
            audio_file = "[sound:"+sentences[i]["filename"]+"_audio.mp4]"

            my_note = genanki.Note(
                    model=my_model,
                    fields=[str(i),
                            sentences[i]["sentence"],
                            sentences[i]["trg_text"],
                            video_file,
                            audio_file
                            ])
            my_deck.add_note(my_note)

        deck_file = '{root}\\deck_file.apkg'.format(root=self.dir)
        my_package.write_to_file(deck_file)

        

        

        


