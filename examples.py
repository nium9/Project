#coding: utf-8

from kivy.core.audio import SoundLoader
from kivy.utils import platform
from kivy.logger import Logger
import time
from stage1 import *


class MusicPlayerAndroid(object):
    def __init__(self):

        from jnius import autoclass
        MediaPlayer = autoclass('android.media.MediaPlayer')
        self.mplayer = MediaPlayer()

        self.secs = 0
        self.actualsong = ''
        self.length = 0
        self.isplaying = False

    def __del__(self):
        self.stop()
        self.mplayer.release()
        Logger.info('mplayer: deleted')

    def load(self, filename):
        try:
            self.actualsong = filename
            self.secs = 0
            self.mplayer.setDataSource(filename)
            self.mplayer.prepare()
            self.length = self.mplayer.getDuration() / 1000
            Logger.info('mplayer load: %s' %filename)
            Logger.info ('type: %s' %type(filename) )
            return True
        except:
            Logger.info('error in title: %s' % filename)
            return False

    def unload(self):
            self.mplayer.reset()

    def play(self):
        self.mplayer.start()
        self.isplaying = True
        Logger.info('mplayer: play')

    def stop(self):
        self.mplayer.stop()
        self.secs=0
        self.isplaying = False
        Logger.info('mplayer: stop')

    def seek(self,timepos_secs):
        self.mplayer.seekTo(timepos_secs * 1000)
        Logger.info ('mplayer: seek %s' %int(timepos_secs))


class MusicPlayerWindows(object):
    def __init__(self):
        self.secs = 0
        self.actualsong = ''
        self.length = 0
        self.isplaying = False
        self.sound = None

    def __del__(self):
        if self.sound:
            self.sound.unload()
            Logger.info('mplayer: deleted')

    def load(self, filename):
        self.__init__()
        self.sound = SoundLoader.load(filename)
        if self.sound:
            if self.sound.length != -1 :
                self.length = self.sound.length
                self.actualsong = filename
                Logger.info('mplayer: load %s' %filename)
                return True
            else:
                Logger.info ('mplayer: songlength = -1 ...')
        return False

    def unload(self):
        if self.sound != None:
            self.sound.unload()
            self.__init__ # reset vars

    def play(self):
        if self.sound:
            self.sound.play()
            self.isplaying = True
            Logger.info('mplayer: play')

    def stop(self):
        self.isplaying = False
        self.secs=0
        if self.sound:
            self.sound.stop()
            Logger.info('mplayer: stop')

    def seek(self, timepos_secs):
        self.sound.seek(timepos_secs)
        Logger.info('mplayer: seek %s' %int(timepos_secs))

def main():
    s1=stage1()
    Stream=s1.get_stream()
    songs = []
    a=Stream.get_combined_audio_file()
    for i in a:
        songs.append(a[i])

    Logger.info ('platform: %s' %platform)

    if platform == 'win':
        mplayer = MusicPlayerWindows()
    elif platform == 'android':
        mplayer = MusicPlayerAndroid()
    else:
        exit()

    for s in songs:
        if mplayer.load(s): # checking load, seek
            mplayer.play()
            time.sleep(2)
            mplayer.seek(90)
            time.sleep(2)
            mplayer.stop()
            mplayer.unload()

        else:
            Logger.info ('cant load song: %s' %s)


if __name__ == '__main__':
    main()
