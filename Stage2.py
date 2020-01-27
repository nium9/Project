import pydub
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.button import Button
import simpleaudio as sa
#from kivy.lang import Bulider
from stage1 import *
from kivy.uix.progressbar import ProgressBar

'''
it does play audio AudioSegment it the latter that is the problem
ie pausing.
need to call keyboard interrrupt it somehows creates a skip
use try and except and i = i+1
'''
class MenuPage(Widget):
    def __init__(self,**kwargs):
        super(MenuPage, self).__init__(**kwargs)
        self.s1=stage1()
        self.Stream=self.s1.get_stream()
        self.M=self.select_stream(0)
        print(self.M)
        b1=Button(text="Play")
        b1.bind(on_press=self.plays_or_stop)
        self.add_widget(b1)
        #i=0
        # print("this is the length of stream")
        # print(self.Stream.get_combined_audio_file())
        # print(self.Stream.len())
        # if i<self.Stream.len():
        #     self.M = self.select_stream(i)
        #     print(self.M)
        #     i=i+1

    def plays_or_stop(self,instance):
        self.playing=pydub
        if instance.text=='Play':
            instance.text="Stop"
            #pydub.playback.play(self.M)
            #play_obj=sa.play_buffer(self.M.raw_data,self.M.channels,self.M.sample_width,self.M.frame_rate)
            self.playing.playback._play_with_simpleaudio(self.M)
            #it's alive play works and stop doesn't work
        else:
            instance.text='Play'
            self.playing.playback._play_with_simpleaudio(self.M).stop()
            #play_obj.stop()

    def select_stream(self,i):
        temp=self.Stream.get_combined_audio_file()
        ##for i in temp:
        ##    song = temp[i]
        ##    play(song)
        return list(temp.values())[i]
#####################################################################
class TestApp(App):
    def build(self):
        return MenuPage()
######################################################################

if __name__=="__main__":
    TestApp().run()
# Bulider.load_string('''
# <MenuPage>:
#     BoxLayout:
#         orientation:'vertical'
#         ToggleButton:
#             id:music_button
#             text:'song'
#             on_press:root.plays_or_stop()
# ''')
