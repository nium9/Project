import eyed3
import pydub
import random
import os
from pydub.utils import which

eyed3.log.setLevel("ERROR")
pydub.AudioSegment.ffmpeg = r"/absolute/path/to/ffmpeg"
pydub.AudioSegment.converter = which("ffmpeg")
class songs:
    def __init__(self):
        self.set_new_song()
        self.album_art=self.get_album_art()
###############################################################
    def get_album_art(self):
        IMAGES = self.Music_metadata.tag.images
        for IMAGE in IMAGES:
            if IMAGE.picture_type!= None:
                print (IMAGE.makeFileName())
                #Image.image_data
                return IMAGE.mime_type 
    def get_songs(self):
        return self.Music
    def get_song_name(self):
        try:
            if self.Music_metadata.tag.title!=None:
                return self.Music_metadata.tag.title
            else:
                return self.name
        except:
            print("ERROR " + self.name)
            return self.name
    def set_new_song(self):
        self.name= str(random.choice(os.listdir("Data/Music/")))
        self.address= "Data/Music/"+self.name
        try:
            self.Music=pydub.AudioSegment.from_mp3(self.address)
            self.Music_metadata=eyed3.load(self.address)
        except:
            print(self.address)

    def length(self):
        try:
            audiofile = eyed3.load(self.address)
            return audiofile.info.time_secs/60 # give time in minuets
        except:
            print("Fail to use metadata")
            try:
                return len(self.get_songs())/(1000*60)
            except:
                print("ERROR fail to use song"+ self.address)
                self.set_new_song()
