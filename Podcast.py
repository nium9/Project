import eyed3
import pydub
import random
import os
from pydub.utils import which
'''
Prerequistes
eyed3.log.setLevel("ERROR")
pydub.AudioSegment.ffmpeg = r"/absolute/path/to/ffmpeg"
pydub.AudioSegment.converter = which("ffmpeg")
'''
class podcast:
    def __init__(self,address,name):
        self.name= name #"clockwise320.mp3"
        self.address= address+self.name#"data/Chapter_Works/"+self.name
        self.podcast_file=pydub.AudioSegment.from_mp3(self.address)
        self.podcast_meta_data=eyed3.load(self.address)
        self.podcast_chapter=self.podcast_meta_data.tag.chapters
        self.chapter_array=[]
        self.podcast_slice=[]
###############################################################



###########################################################
#           Getters
    def getKey(self,item):
        return self.chapter_time_start(item)
    def chapter_time_end(self,chapter):
        return chapter.times.end
    def chapter_time_start(self,chapter):
        return chapter.times.start
    def get_podcast_in_chapters(self):
        return self.podcast_chapter
    def get_podcast_in_chapters_list(self):
        return self.chapter_array
    def get_podcast_file(self):
        return self.podcast_file
    def get_podcast_name(self):
        return self.podcast_meta_data.tag.title
    def get_slice_audio(self):
        return self.podcast_slice
    def length(self):
        audiofile = eyed3.load(self.address)
        return audiofile.info.time_secs/60 # give time in minuets
    def length_in_seconds(self):
        return len(self.podcast_file)/1000
#############################################################################
                        # Setters
    def set_slice_audio(self,sample):
        self.podcast_slice.append(sample)

######################################################################
# '''manpulating Methods '''
    def gap_condition(self,arr):
        ## need to check is neccsary????????
        ## the condition for the gaps
        new_arr=[]
        new_arr.append(arr[0])
        for i in range (1 , len(arr)):
            if self.chapter_time_end(arr[i-1]) -  self.chapter_time_start(arr[i])<15*60*1000:
                new_arr.append(arr[i])
        return new_arr

    def find_chapters(self):
        arr=[]
        for chapter in self.podcast_chapter:
            print("*"*80)
            print("== Chapter '%s'" % chapter.element_id)
            print("-- Title:", chapter.title)
            print("-- subtitle:", chapter.subtitle)
            print("-- Start time: %d; End time: %d" % chapter.times)
            print("-- Start offset: %s; End offset: %s" %
            tuple((str(o) for o in chapter.offsets)))
            print("-- Sub frames:", str(list(chapter.sub_frames.keys())))
            arr.append(chapter)
        arr=sorted(arr,key=self.getKey)
        self.chapter_array=self.gap_condition(arr)

    def slice_audio(self):
        podcast_file=self.get_podcast_file()
        for i in self.chapter_array:
            self.set_slice_audio(podcast_file[self.chapter_time_start(i):self.chapter_time_end(i)])
