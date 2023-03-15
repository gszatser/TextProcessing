#!/usr/bin/env python
# coding: utf-8

# # Pilot Data Text Analysis

# ##### I am now looking at word frequency for my sample data. I am curious if certain words are used more habitually in the participant with hearing loss than in the participant with normal hearing.
# 
# ##### I attempted to identify the three most frequently used words, how often, and compare the words used by one participant with how often the same words are used by the other.
# 
# ##### I am curious if, with treatment, if these words will be used in greater or lesser frequency and whether they could be indicative of treatment benefit
# 
# ##### As you can tell, I have a long way to go - but I think the data are interesting. I am VERY open to suggestions!

# In[15]:


from collections import Counter

with open('OTC7_Transcript.txt', 'r') as file:
    lines = file.readlines()

speaker_word_freq = {'*SP02:': Counter(), '*SP03:': Counter()}
#exclude joining words
excluded_words = ['the', 'is', 'a', 'of', 'and', 'to', 'in']

for line in lines:
    parts = line.strip().split('\t')
    if len(parts) != 2:
        continue  
        #skip lines without a tab character
    speaker, words = parts
    #exclude the action 'pause' and split the remaining words into a list
    words = [word for word in words.replace('pause', '').lower().split() if word not in excluded_words]
    #check if the word is from spk1 or 2, and add to the correct counter list
    if speaker == '*SP02:':
        speaker_word_freq[speaker] += Counter(words)
    elif speaker == '*SP03:':
        speaker_word_freq[speaker] += Counter(words)

#print the top three most frequent words for each speaker and their frequency count, along with the frequency count of those words for the other speaker
for speaker, word_freq in speaker_word_freq.items():
    other_speaker = '*SP03:' if speaker == '*SP02:' else '*SP02:'
    print(f"Top three most frequent words for {speaker}:")
    for i, freq in enumerate(sorted(word_freq.items(), key=lambda x: -x[1])[:3], start=1):
        other_freq = speaker_word_freq[other_speaker][freq[0]]
        print(f"{i}. '{freq[0]}' said {freq[1]} times by {speaker} ({other_freq} times by {other_speaker})")


# In[16]:


word_spk1 = input("Enter the word you want to look up for Speaker 1: ")
freq_spk1 = speaker_word_freq['*SP02:'][word_spk1]


print(f"The word '{word_spk1}' was said {freq_spk1} times by Speaker 1.")


word_spk2 = input("Enter the word you want to look up for Speaker 2: ")
freq_spk2 = speaker_word_freq['*SP03:'][word_spk2]


print(f"The word '{word_spk2}' was said {freq_spk2} times by Speaker 2.")


# In[17]:


import matplotlib.pyplot as plt

x_labels = list(all_words)
x_pos = range(len(x_labels))

plt.figure(figsize=(12, 6))
plt.bar(x_pos, spk02_counts, color='tab:purple', alpha=0.7, label='Speaker 1 - Hearing Loss')
plt.bar(x_pos, spk03_counts, color='tab:green', alpha=0.7, label='Speaker 2 - Normal Hearing', bottom=spk02_counts)
plt.xticks(x_pos, x_labels, rotation=90)
plt.xlabel('Word')
plt.ylabel('Frequency')
plt.legend(loc='best')
plt.title('Top Three Most Frequent Words Spoken by Each Speaker')
plt.tight_layout()
plt.show()


# In[22]:


import numpy as np #thank you geeksforgeeks.org/

word = input("Enter a word to look up: ")
word_freq_to_graph = [speaker_word_freq[speaker].get(word, 0) for speaker in speakers]

fig, ax = plt.subplots()
x_pos = np.arange(len(speakers))
ax.bar(x_pos, word_freq_to_graph, align='center')
ax.set_xticks(x_pos)
ax.set_xticklabels(speakers)
ax.set_title(f"Frequency of '{word}'")
for i, freq in enumerate(word_freq_to_graph):
    ax.text(i, freq, str(freq), ha='center', va='bottom')

plt.show()

#woohoo! took forever but put in one word for all speakers, and prints side by side!!!!!


# In[ ]:




