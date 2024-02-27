
from y2a import fuf
from y2a import link
from y2a import transribe
from y2a import mediafiles
from y2a import run_genaki

def main(yt_link:str, n_video:int, n_audio:int,src_lang:str, trg_lang:str):    
    # set video data
    my_link = link.y2a_link(yt_link)
    #return

    #prepare directory
    a = fuf(my_link.title)

    #download full video
    my_link.vid(n_video).download(output_path = a.fuf_dir(), filename = 'full_video.mp4')

    #download full audio
    my_link.vid(n_audio).download(output_path = a.fuf_dir(), filename = 'full_audio.mp4')

    #transcribe
    trans = transribe.transcribe(dir = a.fuf_dir(),src_lang=src_lang, trg_lang = trg_lang)
    trans.go()

    # write media files
    media_writer = mediafiles.media_writer(a)
    media_writer.write_files(audio=True,video=True)

    # write anki file
    card_writer = run_genaki.anki_deck_writer(a)
    card_writer.write_anki_deck_file(audio=True, video=True)


if __name__ == '__main__':
    #https://www.youtube.com/watch?v=jc2iqTOTmI0
    #https://www.youtube.com/watch?v=d_nHAmQLe1Q

    #https://www.youtube.com/watch?v=h9dAAlBfMoE
    #https://www.youtube.com/watch?v=9qaoHdfNRtk&list=RDCMUCFf1Cux0gRv51vtLPgcyCow&index=14
    main("https://www.youtube.com/watch?v=9qaoHdfNRtk", 1, 14, "de", "en")


