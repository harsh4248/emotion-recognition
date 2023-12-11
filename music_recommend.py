import pandas as pd

def music_recommend(detected_emotion):


    mood_music=pd.read_csv(r"data_moods.csv")

    mood_music=mood_music[['name', 'artist', 'mood']]
    mood_music.head()


    #selecting music according to moods

    if (detected_emotion=='Angry' or detected_emotion=='Disgust' or detected_emotion=='Fear'):
        filter1=mood_music['mood']=='Calm' #Filtering according to 'mood' column in dataset
        f1=mood_music.where(filter1)
        f1=f1.dropna() #dropping rows that are empty
        f2=f1.sample(n=5) #Displaying 5 songs
        f2.reset_index(inplace=True)
        # display(f2)
    if (detected_emotion=='Happy' or detected_emotion=='Neutral'):
        filter1=mood_music['mood']=='Happy' #Filtering according to 'mood' column in dataset
        f1=mood_music.where(filter1)
        f1=f1.dropna() #dropping rows that are empty
        f2=f1.sample(n=5) #Displaying 5 songs
        f2.reset_index(inplace=True)
        # display(f2)
    
    if (detected_emotion=='Sad'):
        filter1=mood_music['mood']=='Sad' #Filtering according to 'mood' column in dataset
        f1=mood_music.where(filter1)
        f1=f1.dropna() #dropping rows that are empty
        f2=f1.sample(n=5) #Displaying 5 songs
        f2.reset_index(inplace=True)
        # display(f2)
    
    if (detected_emotion=='Surprised'):
        filter1=mood_music['mood']=='Energetic' #Filtering according to 'mood' column in dataset
        f1=mood_music.where(filter1)
        f1=f1.dropna() #dropping rows that are empty
        f2=f1.sample(n=5) #Displaying 5 songs
        f2.reset_index(inplace=True)
        # display(f2)

    if (detected_emotion == None):
        return None

    return f2
    
