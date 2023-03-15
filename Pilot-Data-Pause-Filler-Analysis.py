#!/usr/bin/env python
# coding: utf-8

# # Pilot Data Text Analysis

# #### I am currently working on a project that is looking to compare speech utterances between participants with normal hearing and those with hearing loss. It is a work in progress and I am open to feedback!
# #### To explain my thought process, I uploaded a small portion of one of my transcribed files, called 'OTC7_Transcript.txt'. I am curious if participants with hearing loss pause during speaking more often compared to their partner with normal hearing. 
# #### I am still learning how to transcribe speech, so right now I am just using plain words like 'pause' to indicate when a participant pauses while speaking
# #### I am also curious about habits used when speaking, such as the use of filler words like 'um' or 'like' when considering what to say next in response to the other speaker
# #### I want to compare this to the hearing loss treatment, but I do not have those data collected just yet, so right now I am looking at pre-treatment data
# #### This is a small step towards my larger project, but I am hoping to expand this to machine learning, but I am not there just yet

# In[44]:


from collections import Counter

spk1_counter = Counter()
spk2_counter = Counter()
spk1_word_counter = Counter()
spk2_word_counter = Counter()
#Let's go through the file, open it, find each speaker, split the words in each line per speaker, and count the words
#I want to have a word count but also a 'pause' count
#Until my transcription skills improve, I am treating pause, even though an action, as a word for simplicity
def pause_counter():
    with open('OTC7_Transcript.txt', 'r') as file:
        for line in file:
            if line.startswith('*SP02:'):
                words = line.split()
                spk1_counter.update(words)
                spk1_word_counter.update([w for w in words if w != 'pause'])
            elif line.startswith('*SP03:'):
                words = line.split()
                spk2_counter.update(words)
                spk2_word_counter.update([w for w in words if w != 'pause'])

    spk1_pause_count = spk1_counter.get('pause', 0)
    spk2_pause_count = spk2_counter.get('pause', 0)
#Print number of pauses per speaker
    print("Speaker 1 pauses", spk1_pause_count, "times.")
    print("Speaker 2 pauses", spk2_pause_count, "times.")
#Find total words spoken per speaker, including pauses
    spk1_total_words = sum(spk1_word_counter.values())
    spk2_total_words = sum(spk2_word_counter.values())
#Determine who pauses more often despite one talker speaking more often
#Speaker 1 is the participant with hearing loss and Speaker 2 is the participant with normal hearing
    spk1_pause_rate = spk1_pause_count / spk1_total_words * 100 if spk1_total_words > 0 else 0
    spk2_pause_rate = spk2_pause_count / spk2_total_words * 100 if spk2_total_words > 0 else 0

    return spk1_total_words, spk2_total_words, spk1_pause_rate, spk2_pause_rate
#Print the total number of spoken words that excludes the action of 'pause'
spk1_total_words, spk2_total_words, spk1_pause_rate, spk2_pause_rate = pause_counter()
print("Speaker 1 total words spoken (excluding 'pause'):", spk1_total_words)
print("Speaker 2 total words spoken (excluding 'pause'):", spk2_total_words)

print("Speaker 1 pause rate:", spk1_pause_rate)
print("Speaker 2 pause rate:", spk2_pause_rate)


# In[45]:


#Now I want to modify the above code and see, out of the total pauses, who paused more?
#Is this a valid measure? Does this actually tell me who is pausing more?
def pause_counter(file):
    spk1_counter = Counter()
    spk2_counter = Counter()
    total_pause_counter = Counter()

    with open(file, 'r') as file:
        for line in file:
            if line.startswith('*SP02:'):
                words = line.split()
                spk1_counter.update(words)
                total_pause_counter.update(words)
            elif line.startswith('*SP03:'):
                words = line.split()
                spk2_counter.update(words)
                total_pause_counter.update(words)

    spk1_pause_count = spk1_counter.get('pause', 0)
    spk2_pause_count = spk2_counter.get('pause', 0)
    total_pause_count = total_pause_counter.get('pause', 0)

    spk1_pause_pct = spk1_pause_count / total_pause_count * 100 if total_pause_count > 0 else 0
    spk2_pause_pct = spk2_pause_count / total_pause_count * 100 if total_pause_count > 0 else 0

    return spk1_pause_pct, spk2_pause_pct

spk1_pct, spk2_pct = pause_counter('OTC7_Transcript.txt')

print(f"Speaker 1 makes {spk1_pct:.2f}% of the pauses.")
print(f"Speaker 2 makes {spk2_pct:.2f}% of the pauses.")


# In[46]:


import matplotlib.pyplot as plt

spk1_pct, spk2_pct = pause_counter('OTC7_Transcript.txt')
#plot bar graph here
x = ['Speaker 1', 'Speaker 2']
y = [spk1_pct, spk2_pct]
#designate my axes
plt.bar(x, y)
plt.ylim(0, 100)
plt.title('Pauses per speaker over total pauses')
plt.xlabel('Participant')
plt.ylabel('Percentage (%)')

plt.show()
#From this graph, it looks like Speaker 2 (one without hearing loss) pauses more - but they also spoke more often


# In[47]:


#Plot Speaker 1 and 2 in a scatter plot to show pause rate over total words spoken (without pause)
plt.scatter(spk1_total_words, spk1_pause_rate, label='Speaker 1')
plt.scatter(spk2_total_words, spk2_pause_rate, label='Speaker 2')
plt.title('Pause Rate vs Total Words Spoken')
plt.xlabel('Total Words Spoken (excluding "pause")')
plt.ylabel('Pause Rate')
plt.legend()
plt.show()
#Interesting - I think this might be better representative of who is actually pausing more when they are actually talking!
#Prob not significant, but interesting


# In[48]:


#Ok, we got our calculations - now I would like to see python tell me exactly what this means
if spk1_total_words > spk2_total_words:
    print("Speaker 1 talks more.")
elif spk2_total_words > spk1_total_words:
    print("Speaker 2 talks more.")
else:
    print("Both speakers talk the same amount.")

if spk1_pause_rate > spk2_pause_rate:
    print("Speaker 1 pauses more.")
elif spk2_pause_rate > spk1_pause_rate:
    print("Speaker 2 pauses more.")
else:
    print("Both speakers pause at the same rate.")


# In[59]:


#Now let's see how many filler words each speaker uses!
filler_words = ['hm', 'um', 'uh', 'eh', 'ah']

spk1_counter = Counter()
spk2_counter = Counter()

with open('OTC7_Transcript.txt', 'r') as file:
    for line in file:
        if line.startswith('*SP02:'):
            words = line.split()
            for word in words:
                if word in filler_words:
                    spk1_counter[word] += 1
        elif line.startswith('*SP03:'):
            words = line.split()
            for word in words:
                if word in filler_words:
                    spk2_counter[word] += 1

print("Speaker 1:")
for word in filler_words:
    count = spk1_counter.get(word, 0)
    print(f"{word}: {count}")

print("Speaker 2:")
for word in filler_words:
    count = spk2_counter.get(word, 0)
    print(f"{word}: {count}")

