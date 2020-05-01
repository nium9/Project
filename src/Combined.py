import eyed3
import pydub
import random
import os
from pydub.utils import which

'''
Need to use getter and setters.

'''
pydub.AudioSegment.ffmpeg = r"/absolute/path/to/ffmpeg"
pydub.AudioSegment.converter = which("ffmpeg")
class Combined:
    def __init__(self):
        self.combined_audio_file= pydub.AudioSegment.empty()
        self.combined_dictionary={}
        # self.combined_array=[]
        #may need to change in array and a dictionary inside each element
        ##self.chapter_array=[]
###########################################################
#           Getters
    def len(self):
        return len(self.combined_dictionary)
################################################################
#           Setters
    def set_combined_audio_file(self,podcast_sample,song,podcast_file,i):
        podcast_chapter=podcast_file.get_podcast_in_chapters_list()
        self.combined_dictionary[podcast_chapter[i].title]=podcast_sample
        #self.combined_array.append({podcast_chapter[i].title:podcast_sample})
        for j in range(len(song)):
            self.combined_dictionary[song[j].get_song_name()]=song[j].get_songs()
            #self.combined_array.append({song[j].get_song_name():song[j].get_songs()})
# get album art or other metadata for user friendly
        # length_before=len(self.combined_audio_file)
        # self.combined_audio_file=self.combined_audio_file+podcast_sample+self.total_music_list(song)
        # length_after=len(self.combined_audio_file)
############################################################################################
#   Getters
    def get_combined_audio_file(self):
        return self.combined_dictionary
    def get_combined_array(self):
        return self.combined_array

######################################################################
# '''manpulating Methods '''
    def save(self):
        for i in self.combined_dictionary:
            self.combined_audio_file=self.combined_audio_file + self.combined_dictionary[i]
        self.combined_audio_file.export("test1.mp3",format="mp3")
    def total_music_list(self,arr):
        length=0
        total=pydub.AudioSegment.empty()
        for i in range(0,len(arr)):
            total=total+arr[i].get_songs()
            length=length + arr[i].length()
            print (arr[i].get_song_name())
        print(length)
        print ("*" * 100)

        return total
