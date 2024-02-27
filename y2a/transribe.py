import whisper_timestamped as whisper
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import json
import os
from .config import conf
import subprocess

class transcribe:
    def __init__ (self, dir, src_lang, trg_lang):
        self.dir = dir
        self.src_lang = src_lang
        self.trg_lang = trg_lang

    def go(self):

        c = conf()
        path_audio_mp4 = self.dir + "\\full_audio.mp4"
        path_audio_wav = self.dir + "\\full_audio.wav"
        
        subprocess.run([c.ffmpeg(), 
                        "-i",
                        path_audio_mp4,
                        "-ac","2","-f","wav",
                        path_audio_wav])


        audio = whisper.load_audio(path_audio_wav)

        model = whisper.load_model("openai/whisper-small", device="cpu")
        print('load_model - Ok')

        # magic #1 is here
        result = whisper.transcribe(model, audio, language=self.src_lang)
        print('transcribe - Ok')


        
        sentences = []
        new_sentence = ''
        NN = 0

        # prepare json dictionary
        for i in range(len(result["segments"])):
            if new_sentence == '':
                sentence_start = result["segments"][i]["start"]

            new_sentence = new_sentence + result["segments"][i]["text"]
            if result["segments"][i]["text"][-1] == '.':
                NN = NN + 1
                sentences.append( {"N":NN, "sentence":new_sentence, "start":sentence_start, 
                                "end":result["segments"][i]["end"], "trg_text":""} )
                new_sentence = ''

        if new_sentence != '':
            NN = NN + 1
            sentences.append( {"N":NN, "sentence":new_sentence, "start":sentence_start, 
                                "end":result["segments"][i]["end"], "trg_text":""} )  

        # nightmare / translation models
        model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
        tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

        tokenizer.src_lang = self.src_lang

        for i in range(len(sentences)):
            encoded_hi = tokenizer(sentences[i]["sentence"], return_tensors="pt")
            generated_tokens = model.generate(**encoded_hi, forced_bos_token_id=tokenizer.get_lang_id(self.trg_lang))
            trg_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
            sentences[i]["trg_text"] = trg_text[0]
            print(trg_text[0])

        # write sentences.json
        json_string = json.dumps(sentences)
        json_file_name = self.dir + "\\sentences.json"
        text_file = open(json_file_name, "w")
        text_file.write(json_string)
        text_file.close()

        self.sentences = sentences


