import re

def calc_words(text):
    return len(text.lower().split())

def avg_word_length(text):
    words = re.sub(r"[^\w\s]", "", text.lower()).split()
    words_list= [len(word) for word in words]
    words_result = 0 if len(words_list)==0 else round(sum(words_list)/len(words_list),2)
    return words_result

def calc_character(text):
    characters = len(re.sub(r"\s", "", text))
    return characters

def calc_lines(text):
    lines = text.splitlines()
    return len(lines)

def calc_sentences(text):
    sentences = re.findall(r"[.!?]+", text)
    return len(sentences)

def word_frequency(text, top_words=5):
    words= re.sub(r"[^\w\s]","" ,text.lower()).split()
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    sorted_frequency = sorted(frequency.items(), key=lambda x: x[1] , reverse=True)
    return {"all": frequency, "top": dict(sorted_frequency[:top_words])}

def calculate(text):
    words=calc_words(text)
    characters_wo=calc_character(text)
    characters=len(text)
    lines=calc_lines(text)
    sentences=calc_sentences(text)
    avg_word=avg_word_length(text)
    frequency=word_frequency(text)

    return {"text":text, "characters_without_space" :characters_wo, "characters_with_space":characters, "lines": lines, "sentences": sentences, "avg_word_length": avg_word, "frequency": frequency['all'], "top_word_frequency": frequency['top'], "words": words}
