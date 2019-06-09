from django.shortcuts import render
from konlpy.tag import Twitter

import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
nltk.download('book')


nlpy = Twitter()

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def result(request):
    global noun_list
    try:
        text = request.GET['korean_sentence']

        word_list = text.split()
        word_list = nlpy.nouns(text)
        
        word_dict = {}

        for word in word_list:
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1

        noun_list = list(word_dict.items())
        noun_list.sort(key=lambda x:x[1], reverse=True)
        
        top_five = []
        for noun, num in noun_list:
            
            top_five.append((noun, num))
            if 4==top_five.index((noun, num)):
                break

        return render(request, 'result.html', {'text': text, 'words': word_dict.items(),
        'top_five': top_five, 'total_word': len(word_list), 'noun_list': noun_list})

    except:

        text = request.GET['english_sentence']
        
        word_dict = {}

        tagged_list = pos_tag(word_tokenize(text))

        word_list = [word for word,pos in tagged_list if pos in ['NN','NNP']]

        print(word_list)
        for word in word_list:
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
        
        noun_list = list(word_dict.items())
        noun_list.sort(key=lambda x:x[1], reverse=True)
        
        top_five = []
        for noun, num in noun_list:
            
            top_five.append((noun, num))
            if 4==top_five.index((noun, num)):
                break

        
        return render(request, 'result.html', {'text': text, 'words': word_dict.items(),
        'top_five': top_five, 'total_word': len(word_list), 'noun_list': noun_list})
