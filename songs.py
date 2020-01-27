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
    def get_songs(self):
        return self.Music
    def get_song_name(self):
        try:
            return self.Music_metadata.tag.title
        except:
            return self.address
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
                return len(self.Music)/(1000*60)
            except:
                print("ERROR fail to use song"+ self.address)
                self.set_new_song()
