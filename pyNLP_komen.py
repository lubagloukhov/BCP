__author__ = 'lubagloukhov'


import nltk
import json
import pickle
import random
import os
print os.getcwd()


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

# Pre-Process JSON file
file_name = '/Users/lubagloukhov/GitHub/scrapy_play/scrapy_play/items_komen_rss_feedpider2.json'

data = []
with open(file_name) as f:
    for line in f:
        data.append(json.loads(line, object_hook=_decode_dict))


# Combine all messages into one
#
# messages = []
# for i in range(len(data)):
#     messages.append(data[i]['message'])
# # Tokenize
# result = ''.join(messages)
# del messages
# del data
# tokens = nltk.wordpunct_tokenize(result)
# text=nltk.Text(tokens)
#
#
# # Normalize
# words = [w.lower() for w in text]
# vocab = sorted(set(words))

#
# pickle.dump(data,open("items_komen_rss_feedpider2",'wb') )
# open("items_komen_rss_feedpider2",'wb').close()
# open("items_komen_rss_feedpider",'wb').close()
# pickle.dump(messages,open("items_komen_rss_feedpider_messages",'wb') )

# Randomly sample 100(no, 200) messages

# len(data) # 5458
# gsample = random.sample(range(1,len(data)),100)
# gsample200 = random.sample(range(1,5458),200)
# pickle.dump(gsample200,open("gsample200.p",'wb') )
# open("gsample",'wb').close()

#

filename=open( "gsample200.p", "rb" )
gsample200 = pickle.load( filename )
filename.close()

gsample200_data = [data[g] for g in gsample200]

filename=open("gsample200_data",'wb')
pickle.dump(gsample200_data, filename)
filename.close()

del data
del gsample200

# Files are /Users/lubagloukhov/PycharmProjects/scry

# Tagging

# For each s in sample, tag it (binary) to identify whether it applies:
#  (i) Personal experience i.e.,
#           whether the post has an expression of someone having
#           personally experienced something of interest (such as
#           having experienced a particular condition, treatment
#           procedure, drug etc.,).
# (ii) Advice i.e.,
#           whether there is any advice in the post on something
#           of interest.
# (iii) Information i.e.,
#           whether there is any informational reference (Websites,
#           books or other resources) mentioned in the post.
# (iv) Support i.e.,
#           whether the message contains an expression of encouragement
#           and/or support (such as 'good luck, my thoughts and
#           prayers are with you!').
# (v) Outcome i.e.,
#           whether the post is telling about some positive or negative
#           outcome after taking some medicine or following some medical
#           procedure.

i=99
gsample200_data[i]

gsample200_data[i]["Personal experience"] = 1
gsample200_data[i]["Advice"] = 1
gsample200_data[i]["Information"] = 0
gsample200_data[i]["Support"] = 1
gsample200_data[i]["Outcome"] = 0

# Can we automatically classify game/scrabble as none?
# number of words?
# ["Personal experience"]  vlong?
# ["Advice"]
# ["Information"] V long or very short, bimodal distribution
# ["Support"]
# ["Outcome"]
# number of replies?
#
#
#
# # Support:
# Content: "I hope you['ll]", "I'm so happy that" , many "you's" coupled with "I" in the same sentence. Exclamation points, "happy for you", "We can... together" "Good Luck" "feel well ", "here to help", "I am so sorry for your loss", "I know it is", exclamation points, I know, sorry, my heart goes out to you, wish  you the best, will keep you in my thoughts, I think , Hang in there, pray, Congrats, glad, hugs, expect, I __ (really, truly) hope,  I am terribly sorry , "good luck", wish, hope, keep us posted, good luck
# Subject: "Re:", "Re:" + "prayers"
#
# # Personal experience:
# Content: many "I's", "that\'s my story" "experience" "My life"
#              "doctor", "tests", "surgery", "radiation", "I felt ", "treatment", I & past tense verb (had, experienced, was), recently, my, "Keeping my fingers crossed", I+verb (took), update, I am/I'm/I have/I've/I found, For me, recommend
# Subject:
#
# # Information:
# Content: "Bloomberg BusinessWeek", "news", "studies",  "study", "report", "Dr.", "Archives", "herceptin", "podcast", "http://www.uwmedicinepulse.com/", "study" & verb(Study Demonstrates ), Reference, Dr. , Published, trials, clinical trials, TAKEN FROM, podcast, soundcloud, links, lots of html tags
# Subject:
#
# # Advice:
# Content: "try" "you will" "share my story", "listen to your gut", "you should", "you might", "you want", "you do not want", "good luck", "keep us posted", encourage, be sure to, good idea , Be patient (& variants), advice, expect, If I were you, "I hope this helps.", be ___ (prepared), you+present-tense-verb(decide), do(verb),
# Subject:
#
# # Outcome:
# Content: Side effects, symptoms, surgery, drugs, "I felt", "Initial Results", "compared to", Outperforms, share my story, "went well", I took, issures, try, I think, surgery, treatment, side effects, helped, I found, vs., dates, time frames, on ___(drug name), take/taking
# Subject:

gsample_data100=gsample200_data
filename=open("gsample_data_0to99",'wb')
pickle.dump(gsample_data100,filename )
filename.close()