import eyed3
import pydub
import os
import random
import simpleaudio
from pydub.playback import play
from pydub.utils import which
from songs import *
from Podcast import *
from Combined import *

###############################################################
# prerequesites
eyed3.log.setLevel("ERROR")
pydub.AudioSegment.ffmpeg = r"/absolute/path/to/ffmpeg"
pydub.AudioSegment.converter = which("ffmpeg")
################################################################################
'''
Need to do:
    Kivy vs andriod studio vs beeware vs Jython
    Kivy and andriod studio.
    check condition for gaps.
    need to check length of combined.
'''
class stage1:
###################################################################################
    def __init__(self):
        print("Running")
        self.podcast_file = podcast()
        self.podcast_file.find_chapters()
        #print_loop(podcast_file.get_podcast_in_chapters())
        self.podcast_file.slice_audio()
        print("podcast loaded and chapters ready")
        print(self.podcast_file.get_podcast_file())
        print(self.podcast_file.get_podcast_name())
        print(self.podcast_file.get_podcast_in_chapters_list())
        print("-"*80)
        self.Stream=self.add_song(self.podcast_file)
        print(self.Stream.get_combined_audio_file())
        print("Stream Ready")
        print(self.Stream.get_combined_array())
        print("the new array above does it work?")
################################################################################
    def create_list_song(self):
        arr=[]
        total=0
        while total <15:
            try:
                music=songs()
                arr.append(music)
                total=total+music.length()
            except:
                music.set_new_song()
                print(music.get_song_name())
                arr[len(arr)-1]=music
                total=total+music.length()

        print("music list Ready")
        print("-"*80)
        return arr

    def add_song(self,podcast):
        combined = Combined()
        arr=podcast.get_slice_audio()
        #print (end)
        for i in range(0,len(arr)):
            ##here should be the condition
            combined.set_combined_audio_file(arr[i],self.create_list_song(),podcast,i)
            # combined.set_chapter(arr[i],0,len(combined))
            # combined.set_chapter(create_list_song,0,len(combined)
        #print (combined.len())
        return combined
    def save_file(self):
        self.Stream.save()
    def get_stream(self):
        return self.Stream
    def get_length(self):
        return len(self.Stream)
if __name__ == "__main__":
    s1=stage1()
    s1.save_file()

##############################################################
'''
Debugging puporses
'''

# def length_millseconds(audiofile):
#     return print(audiofile.info.time_secs/1000)#gives length in seconds use 60 to get mins
#
# def print_loop(arr):
#     for i in arr:
#         printChapter(i)
#         print("-"*100)
#################################################################
