import pytube

class y2a_link:
    def __init__ (self, link):
       self.link = link

       try:
        yt = pytube.YouTube(link,use_oauth=True,allow_oauth_cache=True)
       except:
          print("Кривая ссылка")
          return
       
       self.title = yt.title
       self.vids= yt.streams.all()

       for i in range(len(self.vids)):
          print(i,'. ', self.vids[i])


    def vid(self, n:int):
       return self.vids[n]
