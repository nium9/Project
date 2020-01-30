import pydub
import simpleaudio as sa
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
#from kivy.lang import Bulider
from stage1 import *
from kivy.uix.progressbar import ProgressBar
from kivy.config import Config
from kivy.clock import Clock
import threading
from functools import partial

####################################################
########### prerequesites ##########################
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')

'''
may need to use threading
it does play and stops audio AudioSegment the problem is pausing.
need volume Button/ not necessary
need progessbar
need to show the length of track
need to make a better layout
'''
class MenuPage(Widget):
    def __init__(self,**kwargs):
        super(MenuPage, self).__init__(**kwargs)
        self.s1=stage1()
        self.Stream=self.s1.get_stream().get_combined_audio_file()
        self.current_value=0
        self.index=0
        self.ids.song_name.text=self.get_details(self.index)
        self.currently_playing=self.select_stream(self.index)
        self.event_play=Clock.schedule_once(self.placeholder,0)
    def update_value(self,song_value,dt):
            self.ids.load_bar.value = ((self.ids.load_bar.value + (dt/(song_value)))*100)
            print("value of bar {} Value of song {}".format(self.ids.load_bar.value,song_value))
    def play_next_previous(self,skip_previous,type_of_skip,dt):
        #need to change button for play to go back to play when skipping a song
        if type_of_skip=='notNatual':
             self.event_play.cancel()
             self.event_progress_bar.cancel()
        if self.index <=len(self.Stream) and self.index>=0:
            # self.event_play.cancel()
            if self.ids.instance.text=='Stop':
                self.playing.stop()
            self.reset_bar()
            self.index=self.index+skip_previous
            self.ids.instance.text='Stop'
            self.ids.instance.state='normal'
            self.ids.song_name.text=self.get_details(self.index)
            self.currently_playing=self.select_stream(self.index)
            self.play()
            print("the song is {} and the length in seconds is {}".format(self.get_details(self.index),len(self.currently_playing)))
            self.event_progress_bar=Clock.schedule_interval(partial(self.update_value,len(self.currently_playing)/1000),1)
            self.event_play=Clock.schedule_once(partial(self.play_next_previous,1,'natural'),len(self.currently_playing)/1000)
            # self.event_play()
            #self.playing=pydub.playback._play_with_simpleaudio(self.currently_playing)
    def plays_or_stop(self,instance):
        if instance.text=='Play':
            instance.text="Stop"
            self.reset_bar()
            self.play()
            print("now playing " + self.get_details(self.index))
            self.event_progress_bar=Clock.schedule_interval(partial(self.update_value,len(self.currently_playing)/1000),1)
            self.event_play=Clock.schedule_once(partial(self.play_next_previous,1,'natural'),len(self.currently_playing)/1000)
        else:
            print("stop " + self.get_details(self.index))
            instance.text='Play'
            self.reset_bar()
            self.stop()
            self.event_play.cancel()
            self.event_progress_bar.cancel()
            #play_obj.stop()
#####################################################################
    def play(self):
        self.playing=pydub.playback._play_with_simpleaudio(self.currently_playing)
        # self.playing.wait_done()
    def stop(self):
        self.playing.stop()
    def placeholder(self,dt):
        pass ## does nothing it mainly to inilise event_play as a scheduler
    def reset_bar(self):
        self.ids.load_bar.value=0
#####################################################################
    def select_stream(self,i):
        return list(self.Stream.values())[i]
    def get_details(self,i):
        a=list(self.Stream.keys())
        return list(self.Stream.keys())[i]
    def get_index(self):
        return self.index
#####################################################################
class MyApp(App):
    def build(self):
        return MenuPage()
######################################################################

if __name__=="__main__":
    MyApp().run()
######################################################################
####################### code i used before may use later.
# Bulider.load_string('''
# <MenuPage>:
#     BoxLayout:
#         orientation:'vertical'
#         ToggleButton:
#             id:music_button
#             text:'song'
#             on_press:root.plays_or_stop()
# ''')
# def play_previous(self):
#     #need to change button for play to go back to play when skipping a song
#     if self.index >0:
#         # self.event_play.cancel()
#         if self.ids.instance.text=='Stop':
#             self.playing.stop()
#         self.index=self.index-1
#         self.ids.instance.text='Stop'
#         self.ids.instance.state='normal'
#         self.ids.song_name.text=self.get_details(self.index)
#         self.currently_playing=self.select_stream(self.index)
#         self.play()
#         print("the song is {} and the length in seconds is {}".format(self.get_details(self.index),len(self.currently_playing)))
#         self.event_play=Clock.schedule_once(self.play_next,(len(self.currently_playing)/1000))
#         #self.event_play()
#         #self.playing=pydub.playback._play_with_simpleaudio(self.currently_playing)
# was in plays_or_stop() below this
# th=threading.Thread(target=self.play)
# th.start()
# th.join()
#     self.playing=sa.play_buffer(self.currently_playing.raw_data,
# num_channels=self.currently_playing.channels,
# bytes_per_sample=self.currently_playing.sample_width,
# sample_rate=self.currently_playing.frame_rate)
# if(self.playing.is_playing()):
#     print("still playing")
#     try:
#         self.playing.wait_done()
# self.event_play()
#self.stop()
#play_obj=sa.play_buffer(self.M.raw_data,self.M.channels,self.M.sample_width,self.M.frame_rate)
#pydub.playback.play(self.M)
#self.play_next()
#it's alive play works and stop doesn't work
#maybe a for loop
