from pydub import AudioSegment, effects  

rawsound = AudioSegment.from_file("Data/Data_for_stage_3/Sample_of_hello_internet.wav", "m4a")  
normalizedsound = effects.normalize(rawsound)  
normalizedsound.export("./output.wav", format="wav")
