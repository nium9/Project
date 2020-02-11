'''
Also have to focus on waveaudio files.
features:
    Repeated sounds,
    ad placement.
Use hello internet as a start as train and test
then use Twp to validate the model
need same sample rate()
So i extend stage 1 in terms of manpulating the files in a way so i concantinate
them but the actual finding the gaps i need to do .
#Comparing them may be easier than I thought
use stage1 to help you ie change metadata
###
fast fourier transform
short-time fourier transform
fouriver anlaysis
'''
import datetime
import pydub
import speech_recognition as sr
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft,rfft
import numpy as np
import librosa
from librosa import stft
# Data/Data_for_stage_3/Sample_of_hello_internet.wav
#output.wav
data,rate = librosa.load('Data/Data_for_stage_3/Sample_of_hello_internet.wav',sr=44100)
sample = [2,5,6,7]
for a in range (0,len(sample)):
    address='Data/Data_for_stage_3/Sample' +str(sample[a])+'.wav'
    print(address)
    sample_data,sample_rate=librosa.load(address,sr=44100)
    sample[a]=sample_data
# fft_value_sample = np.abs(fft(sample_data))
sample_fft=[rfft(sample[i]) for i in range(0,len(sample))]
time_of_hi=round(data.size/44100)
print(data.size)
print("*"*80)
result=[]

def Sliding_window(current_sample):
    counter=0
    time={}
    for i in range(current_sample.size,data.size,current_sample.size):
        slice_audio=data[(counter):(i)]
        if len(slice_audio)==0:
            break
        HI_FTT=rfft(slice_audio)
        print(HI_FTT)
        print(current_sample)
        r=np.correlate(HI_FTT, current_sample)
        highest_result=result[np.argmax(r)]
        print(counter/44100)
        print(result.shape)
        print(highest_result)
        ## so instead of doing correlate i should do the formula of correolate
        # ifft( rfft(Hi) * rfft(sample) )
    #    result=(np.inner(slice_audio, current_sample)/(norm(slice_audio)*norm(current_sample)))
        time[counter/44100]=["Sample"+str(j+1),result]
        # result=[]
        print("*" * 80)
        counter=i
    return time
def test(current_sample):
    #Test=rfft(data)
    a={}
    result=np.correlate(data, current_sample)
    # for i in range(0,len(result)):
        # a[i]
    print(len(result))
    return np.argmax(result)/44100
    #this works but does all in one go

def standarised(result):
    standarised=[0 for i in range(0,time_of_hi)]
    for i in range(0,len(result)):
        for j in result[i]:
            standarised[round(j[0])]+= (j[1][1])
#    for k in range(standerised):
#        standarised[k]=standarised/len(sample)
    return standarised

for j in range(0,len(sample)):
    current_sample=sample_fft[j]
    # a=test(current_sample)
    # print(str(datetime.timedelta(seconds=a)))
    result.append(Sliding_window(current_sample))
    # print(result)

## 42 seconds - 44 seconds
for h in range(0,len(result)):
    result[h]=sorted(result[h].items())
print (result)
# average_values=standarised(result)
# a={}
# for k in range(0,len(average_values)):
#     print(str(datetime.timedelta(seconds=k)) + " "+ str(average_values[k]))
#     a[str(datetime.timedelta(seconds=k))]=average_values[k]
# print(a)
# sorted_x = sorted(a.items(), key=lambda kv: kv[1],reverse = True)
# count=0
# for i in sorted_x:
#     print(i)
#     count=count+1
#     if count>10:
#         break
#     print("*"*80)
#     #print(sorted_x)
#
# '''
# sound=pydub.AudioSegment.from_mp3("Data/Data_for_stage_3/Hello_internet_135.mp3")
# sound.export('Data/Data_for_stage_3/hello_internet_wav_edition.wav' , format="wav")
# sound_sample=pydub.AudioSegment.from_wav("Data/Data_for_stage_3/Stage1.wav")
# sound_sample_mp3=pydub.AudioSegment.from_mp3("Data/Data_for_stage_3/stage2.mp3")
# '''
# ###################################################################################
