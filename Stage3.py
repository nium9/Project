
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
import datetime
import pydub
import numpy as np
import librosa
from scipy.io import wavfile as wav
from scipy.fftpack import fft,rfft,irfft
from scipy import signal,spatial
from sklearn import preprocessing
from math import sqrt

# Data/Data_for_stage_3/Sample_of_hello_internet.wav
#output.wav
#18 seconds is begining
def getData(podcast_array,sample):
    for a in range (0,len(sample)):
        address='Data/Data_for_stage_3/ChangeConvo/Sample' +str(sample[a])+'.wav'
        print(address)
        sample_data,sample_rate=librosa.load(address,sr=44100)
        sample[a]=sample_data
    for i in range(0,len(podcast_array)):
        address='Data/Data_for_stage_3/'+str(podcast_array[i])+'.wav'
        print(address)
        data,rate=librosa.load(address,sr=44100)
        podcast_array[i]=data
    return sample,podcast_array
def get_time_of_hi(data):
    return round(data.size/44100)


def Sliding_window(current_sample,j,podcast_data):
    counter=0
    time=[]
    window_movement=44100 #move 1/10 second 441 => move 1/100 of a second
    #window_size is fixed it whatever the sample size is
    for i in range(current_sample.size,data.size,window_movement):
        slice_audio=podcast_data[counter:i]
        if len(slice_audio)==0:
            break
        HI_FTT=fft(slice_audio)
        #need to do my on cross/auto correlation
        #a=slice_audio*current_sample ##have to be non fft version
        #highest_result=sum(rfft(a))
        # print(HI_FTT.shape)
        # print(current_sample.shape)
        ###############
        ## Normailize
        #print((HI_FTT,current_sample))
        #print("-"*80)
        HI_FTT = (HI_FTT - np.mean(HI_FTT)) / (np.std(HI_FTT) * len(HI_FTT))
        current_sample = (current_sample - np.mean(current_sample)) /  np.std(current_sample)
        #print((HI_FTT,current_sample))
        ###################
        highest_result=np.correlate(HI_FTT, current_sample)[0]
        #if highest_result>90:
            #print(highest_result)
        time.append(["Sample"+str(j+1),round(counter/44100),highest_result])


        #### correolate
        #highest_result=np.corrcoef(HI_FTT,current_sample,'valid')[0]
        #print(highest_result)
        ###################
        #print(highest_result)
        #r=np.corrcoef(HI_FTT,current_sample)
        #print(len(highest_result))
        #max_index=np.argmax(highest_result)
        #highest_result=highest_result[max_index]
        #print(highest_result)
        #highest_result=sqrt(mean_squared_error(current_sample, (HI_FTT*current_sample)))
        #highest_result=np.average(r)
        #f,highest_result=signal.coherence(HI_FTT,current_sample)
        #highest_result=sum(highest_result)
        #highest_result , _=pearsonr(HI_FTT,current_sample)
        #highest_result , _=spearmanr(HI_FTT,current_sample)
        #highest_result=np.inner(HI_FTT,current_sample)/(np.linalg.norm(HI_FTT)*(np.linalg.norm(current_sample))) # 0.076
        #highest_result=1- spatial.distance.cosine(HI_FTT,current_sample) # 0.
        #highest_result=sum(HI_FTT*current_sample)
        #print(counter/44100)
        #print(max_index)
        #print(highest_result)
        # ## so instead of doing correlate i should do the formula of correolate
        # ifft( rfft(Hi) * rfft(sample) )
        #result=(np.inner(slice_audio, current_sample)/(norm(slice_audio)*norm(current_sample)))
        #time.append(["Sample"+str(j+1),round(counter/44100),highest_result])
                    #sample             #timestamp      #result of correlate_for that second
        #r=[]
        counter=counter+window_movement
    #print(time)
    return time

def standarised_time(result,time_of_hi):
    standarised=[0 for i in range(0,time_of_hi)]
    print(time_of_hi)
    counter=0
    for h in range(0,len(standarised)-1):
        for i in result:
            for j in i:
                if j[1]==h:
                    counter=counter+1
                    standarised[j[1]]+= (j[2])
        if counter==0:
            standarised[h]=0
        else:
            standarised[h]=standarised[h]/counter
            counter=0
    # for k in range (0,len(standarised)):
    #     standarised[k]=standarised[k]/len(sample_fft)
    return standarised
def main_loop(podcast_data,sample_fft):
    result=[]
    for j in range(0,len(sample_fft)):
        current_sample=sample_fft[j]
        result.append(Sliding_window(current_sample,j,podcast_data)) ## option 2 work kinda but not really
        print("*"*80)
        print("done sample " +str(j+1)+ " analysis" )
    average_values=standarised_time(result,get_time_of_hi(podcast_data))
    print("*"*80)
    return average_values
def print_data(average_values):
    a={}
    for k in range(0,len(average_values)):
        #print(str(datetime.timedelta(seconds=k)) + " "+ str(average_values[k]))
        a[str(datetime.timedelta(seconds=k))]=average_values[k]
    #print(a)
    sorted_x = sorted(a.items(), key=lambda kv: kv[1],reverse = True)
    count=0
    for i in sorted_x:
        print(i)
        count=count+1
        if count>5:
            break
        print("*"*80)

'''
ok what this need to do is train the samples?????
or we can try and train and create a model use
the podcast data and samples as features.
'''
# podcast_array= 129 130 131 132 134
# sample =  #2 5 6 7 8 9 10 11
data,rate = librosa.load('Data/Data_for_stage_3/Sample_of_hello_internet.wav',sr=44100)
#sample, podcast_array=getData([129,130,131,132,134],[2,5,6,7,8,9])
sample, podcast_array=getData([],[2,5,6,7,8,9])
#sample=[preprocessing.normalize(i.reshape(-1,1)) for i in sample]
sample_fft=[fft(sample[i]) for i in range(0,len(sample))]
print(data)
#data=preprocessing.normalize(data.reshape(-1,1))





print(data.size)
print("*"*80)
print_data(main_loop(data,sample_fft))

# ###################################################################################
