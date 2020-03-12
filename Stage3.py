
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
import datetime
from eyed3.id3.tag import Tag
import numpy as np
import librosa
from scipy.io import wavfile as wav
from scipy.fftpack import fft,rfft,irfft,ifft
from math import sqrt

# Data/Data_for_stage_3/Sample_of_hello_internet.wav
#output.wav
#18 seconds is begining
def getData(sample,Ad_placement_begin,Ad_placement_end):
    for a in range (0,len(sample)):
        address='Data/Data_for_stage_3/ChangeConvo/Sample' +str(sample[a])+'.wav'
        print(address)
        sample_data,sample_rate=librosa.load(address,sr=44100)
        sample[a]=(sample_data,"DATA")
    for j in range(0,len(Ad_placement_begin)):
        address='Data/Data_for_stage_3/Adplacement/begin_ad/Sample' +str(Ad_placement_begin[j])+".wav"
        print(address)
        Ad_placement_data,Ad_placement_rate=librosa.load(address,sr=44100)
        Ad_placement_begin[j]=(Ad_placement_data,"AD_Begin")
    for i in range(0,len(Ad_placement_end)):
        address='Data/Data_for_stage_3/Adplacement/end_ad/Sample'+str(Ad_placement_end[i])+'.wav'
        print(address)
        data,rate=librosa.load(address,sr=44100)
        Ad_placement_end[i]=(data,"AD_End")
    return sample,Ad_placement_begin,Ad_placement_end
def get_time_of_hi(data):
    return round(data.size/44100)


def Sliding_window(current_sample,j,podcast_data):
    counter=0
    time=[]
    window_movement=441 #move 1/10 second 441 => move 1/100 of a second
    #window_size is fixed it whatever the sample size is
    for i in range(current_sample.size,data.size,window_movement):
        slice_audio=podcast_data[counter:i]
        if len(slice_audio)==0:
            break
        HI_FTT=slice_audio
        # current_sample=fft(np.conjugate(current_sample))
        # HI_FTT=fft(slice_audio)
        # #need to do my on cross/auto correlation
        # #a=slice_audio*current_sample ##have to be non fft version
        # #highest_result=sum(rfft(a))
        # # print(HI_FTT.shape)
        # # print(current_sample.shape)
        # ###############
        # ## Normailize
        # # print((HI_FTT,current_sample))
        # # print("-"*80)
        HI_FTT = (HI_FTT - np.mean(HI_FTT)) / (np.std(HI_FTT) * len(HI_FTT))
        current_sample = (current_sample - np.mean(current_sample)) /  np.std(current_sample)
        # # print((HI_FTT,current_sample))
        # ###################
        # highest_result=signal.correlate(HI_FTT,current_sample,'valid','fft')[0]
        # print(highest_result)
        highest_result=np.correlate(HI_FTT, current_sample)[0] #either both have to be fft or normal
        #if highest_result>90:
            #print(highest_result)
        # highest_result=np.correlate(ifft( HI_FTT*current_sample),current_sample)[0]
        # highest_result=1- spatial.distance.cosine(HI_FTT,current_sample) # 0.
        time.append(["Sample"+str(j+1),round(counter/44100),highest_result])
        #r=np.corrcoef(HI_FTT,current_sample)
        #print(len(highest_result))
        #max_index=np.argmax(highest_result)
        #highest_result=highest_result[max_index]
        #print(highest_result)
        #highest_result=sqrt(mean_squared_error(current_sample, (HI_FTT*current_sample)))
        #highest_result=np.average(r)
        #f,highest_result=signal.coherence(HI_FTT,current_sample)
        #highest_result=sum(highest_result)
        #highest_result=np.inner(HI_FTT,current_sample)/(np.linalg.norm(HI_FTT)*(np.linalg.norm(current_sample))) # 0.076
        #highest_result=sum(HI_FTT*current_sample)
        #print(counter/44100)
        #print(max_index)
        #print(highest_result)
        # ## so instead of doing correlate i should do the formula of correolate
        #result=(np.inner(slice_audio, current_sample)/(norm(slice_audio)*norm(current_sample)))
        #time.append(["Sample"+str(j+1),round(counter/44100),highest_result])
                    #sample             #timestamp      #result of correlate_for that second
        #r=[]
        counter=counter+window_movement
    #print(time)
    return time
def check_max(standerised,h,val):
    # print(standerised[h])
    if val > standerised[h]:
        standerised[h]=val
    return standerised
def standarised_time(result,time_of_hi):
    standarised=[0 for i in range(0,time_of_hi)]
    print(time_of_hi)
    counter=0
    # highest=0
    for h in range(0,len(standarised)-1):
        for i in result:
            # result= [sample 1, sample 2, sample n ]
            # i= an array of j
            for j in i:
                # j= ["sample 1", timestamp, correlaton value]
                # print(j)
                if j[1]==h:
                    standarised=check_max(standarised,h,j[2])
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
    return standarised
def main_loop(podcast_data,sample_fft):
    result=[]
    for j in range(0,len(sample_fft)):
        current_sample=sample_fft[j][0]
        result.append(Sliding_window(current_sample,j,podcast_data)) ## option 2 work kinda but not really
        print("*"*80)
        print("done sample " +str(j+1)+ " analysis" )
    average_values=standarised_time(result,get_time_of_hi(podcast_data))
    print("*"*80)
    # print(average_values)
    # average_values=[[desc,cr],[],..... time of data]
    return average_values
def print_data(average_values):
    a={}
    for k in range(0,len(average_values)):
        #print(str(datetime.timedelta(seconds=k)) + " "+ str(average_values[k]))
        a[str(datetime.timedelta(seconds=k))]=average_values[k]
        # a[k]=average_values[k]
    #print(a)
    sorted_x = sorted(a.items(), key=lambda kv: kv[1],reverse = True)
    count=0
    for i in sorted_x:
        print(i)
        count=count+1
        if count>9:
            break
        print("*"*80)
    sorted_x=sorted_x[0:4]
    sorted_x=sorted(sorted_x,key=lambda kv:kv[0])
    return sorted_x
data,rate = librosa.load('Data/Data_for_stage_3/135.mp3',sr=44100)
# -1 <-> +1 the data is between
#[2,5,6,7,8,9] sample
#[2,3,4] begin_add
#[2,3,4] end_add
sample, ad_placement_array_begin, ad_placement_array_end=getData([2],[1,2,3,4],[2,3,4])
#sample=[preprocessing.normalize(i.reshape(-1,1)) for i in sample]
# sample_fft=[(fft(sample[i][0]),sample[i][1]) for i in range(0,len(sample))]
# ad_placement_begin_fft=[(fft(ad_placement_array_begin[i][0]),ad_placement_array_begin[i][1]) for i in range(0,len(ad_placement_array_begin))]
# ad_placement_end_fft=[(fft(ad_placement_array_end[i][0]),ad_placement_array_end[i][1]) for i in range(0,len(ad_placement_array_end))]
print("*"*80)
list_of_timestamp=print_data(main_loop(data,sample)) ## prodduced suppringly good result
'''
DO CLASSIFICATION

OR MERGER SOUND FILES TOGETHER
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
# print_data_new(main_loop_new(data,[sample_fft,ad_placement_begin_fft,ad_placement_end_fft]))
# def Sliding_window_classification(current_sample,desc,podcast_data):
#     counter=0
#     time=[]
#     threshold=0.1
#     window_movement=44100 #move 1/10 second 441 => move 1/100 of a second
#     #window_size is fixed it whatever the sample size is
#     for i in range(current_sample.size,data.size,window_movement):
#         slice_audio=podcast_data[counter:i]
#         if len(slice_audio)==0:
#             break
#         HI_FTT=fft(slice_audio)
#         HI_FTT = (HI_FTT - np.mean(HI_FTT)) / (np.std(HI_FTT) * len(HI_FTT))
#         current_sample = (current_sample - np.mean(current_sample)) /  np.std(current_sample)
#         result=np.correlate(HI_FTT, current_sample)[0]
#         if result>=threshold:
#             time.append([desc,round(counter/44100),result])
#         else:
#             time.append(["N/A",round(counter/44100),result])
#         counter=counter+window_movement
#     return time
# def standarised_time_new(result,length_of_data):
#     standarised=[["N/A",0] for i in range(0,length_of_data)]
#     #result[
#     # [["DATA",timestamp,corelation_value],["DATA",timestamp,corelation_value]],
#     # [["AD_Begin",timestamp,corelation_value],["AD_End",timestamp,corelation_value]],
#     # ]
#     for h in range(0,len(standarised)-1):
#         for i in result:
#             # result= [sample 1, sample 2, sample n ]
#             # i= an array of j
#             for j in i:
#                 # j= ["DATA", timestamp, correlaton value]
#                 if j[1]==h:
#                     if j[2]>standarised[h][1]:
#                         standarised[h]=[j[0],j[2]]
#     print(standarised)
#     return standarised
# def main_loop_new(data,arr):
#     #arr=[(value,"DATA"),(ad_break,"AD_Begin"),(ab_break,"AD_End")]
#     result=[]
#     counter=0
#     for i in arr:
#         for j in i:
#             current_sample=j[0]
#             desc=j[1]
#             result.append(Sliding_window_classification(current_sample,desc,data))
#             #result[["DATA",timestamp,corelation_value],["DATA",timestamp,corelation_value],["DATA",timestamp,corelation_value]]
#     final_result=standarised_time_new(result,get_time_of_hi(data))
#     print(final_result)
#     return final_result
# def print_data_new(average_values):
#     a={}
#     for k in range(0,len(average_values)):
#         #print(str(datetime.timedelta(seconds=k)) + " "+ str(average_values[k]))
#         a[str(datetime.timedelta(seconds=k))]=average_values[k]
#         # a[k]=average_values[k]
#     for i in a:
#         print("{} - {} " .format(i,a[i]))
# def printChapter(chapter):
#     print(chapter)
#     # The element ID is the unique key for this chapter
#     print("== Chapter '%s'" % chapter.element_id)
#     # TIT2 sub frame
#     print("-- Title:", chapter.title)
#     # TIT3 sub frame
#     print("-- subtitle:", chapter.subtitle)
#     # WXXX sub frame
#     print("-- url:", chapter.user_url)
#     # Start and end time - tuple
#     print("-- Start time: %d; End time: %d" % chapter.times)
#     # Start and end offset - tuple. None is used to set to "no offset"
#     print("-- Start offset: %s; End offset: %s" %
#           tuple((str(o) for o in chapter.offsets)))
#     print("-- Sub frames:", str(list(chapter.sub_frames.keys())))
# def make_Chapters(list_of_timestamp):
#     tag=Tag()
#     previous=0
#     for i in range(0,len(list_of_timestamp)):
#         tag.chapters.set("Chapter " + str(i+1), (previous, list_of_timestamp[i]*1000))
#
#         previous=list_of_timestamp[i]*1000
#     return tag
# temp = make_Chapters(list_of_timestamp)
# for i in temp.chapters:
#     printChapter(i)

# ###################################################################################
