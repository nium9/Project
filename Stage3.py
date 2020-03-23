
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
'''
from scipy import signal,spatial
from scipy.spatial.distance import euclidean
import datetime
import eyed3
from eyed3.id3.tag import Tag
import numpy as np
import librosa
from scipy.io import wavfile as wav
from scipy.fftpack import fft,rfft,irfft,ifft
from math import *
from fastdtw import fastdtw

# Data/Data_for_stage_3/Sample_of_hello_internet.wav
#output.wav
#18 seconds is begining
def getData(sample,Ad_placement_begin,Ad_placement_end):
    for a in range (0,len(sample)):
        address='Data/Data_for_stage_3/ChangeConvo/Sample' +str(sample[a])+'.wav'
        print(address)
        sample_data,sample_rate=librosa.load(address,sr=44100)
        sample[a]=[sample_data,"DATA"]
    for j in range(0,len(Ad_placement_begin)):
        address='Data/Data_for_stage_3/Adplacement/begin_ad/Sample' +str(Ad_placement_begin[j])+".wav"
        print(address)
        Ad_placement_data,Ad_placement_rate=librosa.load(address,sr=44100)
        Ad_placement_begin[j]=[Ad_placement_data,"AD_Begin"]
    for i in range(0,len(Ad_placement_end)):
        address='Data/Data_for_stage_3/Adplacement/end_ad/Sample'+str(Ad_placement_end[i])+'.wav'
        print(address)
        data,rate=librosa.load(address,sr=44100)
        Ad_placement_end[i]=[data,"AD_End"]
    return sample+Ad_placement_begin+Ad_placement_end
def get_time_of_hi(data):
    return round(data.size/44100)


def Sliding_window(sample_array,podcast_data):
    time=[]
    threshold=[0.1,0.3]
    window_movement=441 #move 1/10 second 441 => move 1/100 of a second
    #window_size is fixed it whatever the sample size is
    #sample array [[soundfile,"Convo"],[Soudfiles,"Ad"]]
    for i in sample_array:
        counter=0
        current_sample=i[0]
        current_sample_desc=i[1]
        size_of_sample=current_sample.size
        for j in range(size_of_sample,data.size,window_movement):
            slice_audio=podcast_data[counter:j]
            if len(slice_audio)==0:
                break
            HI_FTT=slice_audio
            # HI_FTT = (HI_FTT - np.mean(HI_FTT)) / (np.std(HI_FTT) * len(HI_FTT))
            # current_sample = (current_sample - np.mean(current_sample)) /  np.std(current_sample)
            # highest_result=sqrt(sum(pow(a-b,2) for a, b in zip(current_sample, HI_FTT)))
            # highest_result=np.correlate(HI_FTT, current_sample)[0] #cross corelation
            highest_result=1- spatial.distance.cosine(HI_FTT,current_sample) #cosine simularity
            # highest_result, path = fastdtw(current_sample, HI_FTT, dist=euclidean)
            if current_sample_desc=="DATA":
                if threshold[0]<highest_result: # 0.1 is threshold
                    time.append([current_sample_desc,round(counter/44100),highest_result])
            else:
                if threshold[1]<highest_result:
                    time.append([current_sample_desc,round(counter/44100),highest_result])
            counter=counter+window_movement
    return time
        ########################################################################
        # highest_result=signal.correlate(HI_FTT,current_sample,'valid','fft')[0]
        #r=np.corrcoef(HI_FTT,current_sample)
        #max_index=np.argmax(highest_result)
        #highest_result=highest_result[max_index]
        #highest_result=np.inner(HI_FTT,current_sample)/(np.linalg.norm(HI_FTT)*(np.linalg.norm(current_sample))) # 0.076
        ########################################################################
def check_max(standerised,h,val):
    #val=["Speach",coorelate_value]
    if val[2] > standerised[h][1]:
        if check_range(standerised,h,i)==True:
            standerised[h][1]=val[2]
            standerised[h][0]=val[0]
        else:
            return standerised
    return standerised
    
    
######################################################################################
####################
#                       NOT WORKING                           # 
 
def check_range(standerised,time_stamp,val):
    if time_stamp<=5 or time_stamp>=len(standerised):
        return True
    for i in range(time_stamp-3,time_stamp+3):
        if standerised[i][1]==val[1]:
            return False
    return True
    
    
################################################################################################
def standarised_time(result,time_of_hi):
    standarised=[["Speach",0] for i in range(0,time_of_hi)]
    print(time_of_hi)
    counter=0
    for h in range(0,len(standarised)-1):
        for i in result:
            # i= ["AD", timestamp, correlaton value]
            if i[1]==h:
                standarised=check_max(standarised,h,i)
    return standarised
def main_loop(podcast_data,sample):
    # result=/[]
    # for j in range(0,len(sample_fft)):
        # current_sample=sample_fft[j][0]
    result=Sliding_window(sample,podcast_data) ## option 2 work kinda but not really
    # print(result)
    print("*"*80)
    print("done Analysis" )
    average_values=standarised_time(result,get_time_of_hi(podcast_data))
    print("*"*80)
    # print(average_values)
    # average_values=[[desc,cr],[],..... time of data]
    return average_values
def print_data(average_values):
    a={}
    for k in range(0,len(average_values)):
        #print(str(datetime.timedelta(seconds=k)) + " "+ str(average_values[k]))
        # a[str(datetime.timedelta(seconds=k))]=average_values[k]
        a[k]=average_values[k]
    for i in a:
        print("{} - {} ".format(i,a[i]))
    print(a.items())
    sorted_x = sorted(a.items(), key=lambda kv: (kv[1][0],kv[1][1]),reverse = True)
    count=0
    for i in sorted_x:
        print("time {} ,- Desc - {} , coorelate - {} ".format(str(datetime.timedelta(seconds=i[0])),i[1][0],i[1][1]))
        count=count+1
            # break
            # if count>9:
        print("*"*80)
    return sorted_x
data,rate = librosa.load('Data/Data_for_stage_3/135.mp3',sr=44100)
# -1 <-> +1 the data is between
#[2,5,6,7,8,9] sample
#[2,3,4] begin_add
#[2,3,4] end_add
sample_of_all_data=getData([2,5],[2],[3])
for i in sample_of_all_data:
    print(i[0])
    print(i[1])
def set_chapter(list_of_timestamp):
    tag=Tag()
    previous=0
    counter=int(0)
    for i in list_of_timestamp:
        tag.chapters.set("Chapter "+ str(counter), (previous*1000, i*1000))
        previous=i*1000
        counter+=1
    return tag
def printChapter(chapter):
    print(chapter)
    # The element ID is the unique key for this chapter
    print("== Chapter '%s'" % chapter.element_id)
    # TIT2 sub frame
    print("-- Title:", chapter.title)
    # TIT3 sub frame
    print("-- Start time: %d; End time: %d" % chapter.times)
    # Start and end offset - tuple. None is used to set to "no offset"
    print("-- Start offset: %s; End offset: %s" %
          tuple((str(o) for o in chapter.offsets)))
    print("-- Sub frames:", str(list(chapter.sub_frames.keys())))

## sample of all data [["convo",sounfile],["ad",soundfile]]
print("*"*80)
list_of_timestamp=print_data(main_loop(data,sample_of_all_data)) ## prodduced suppringly good result
# list_of_timestamp=sorted(list_of_timestamp, key=lambda kv: (kv[0]),reverse = True)
# temp=set_chapter(list_of_timestamp)
metadata=eyed3.load("Data/Data_for_stage_3/135.mp3")
for i in metadata.tag.chapters:
    printChapter(i)
'''
DO CLASSIFICATION- filtering
# OR MERGER SOUND FILES TOGETHER
OR TRY FFT AGAIN AND SEE IF CANCEL
'''
'''
hello internet wav edition:
11:00
30:42
39:42
43:00
AD_placment :
53:31 - 55:31
23:57 - 26:04
1:13:01- 1:14:53

'''
################################################################################
    #                 counter=counter+1
    #                 standarised[j[1]]= j[2]
    #             highest=0
    #     if counter==0:
    #         standarised[h]=0
    #     else:
    #         standarised[h]=standarised[h]/counter
    #         counter=0
    # for k in range (0,len(standarised)):
    #     standarised[k]=standarised[k]/len(sample_fft)
################################################################################
# sample_fft=[(fft(sample[i][0]),sample[i][1]) for i in range(0,len(sample))]
# ad_placement_begin_fft=[(fft(ad_placement_array_begin[i][0]),ad_placement_array_begin[i][1]) for i in range(0,len(ad_placement_array_begin))]
# ad_placement_end_fft=[(fft(ad_placement_array_end[i][0]),ad_placement_array_end[i][1]) for i in range(0,len(ad_placement_array_end))]
# ##############################################################################
