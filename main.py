import re


default_text = """Python is a versatile, high-level programming language loved by developers worldwide.
Why do so many programmers start with Python?
Because Python prioritizes readability, simplicity, and clear syntax!
Whether you want to build web applications, analyze data, or automate tedious tasks, Python has the tools you need.
As you write more Python code, you will discover that writing code in Python feels almost like writing structured English.
Programming takes practice, time, and patience.
So keep writing Python, keep building projects, and keep solving real problems.
Remember: Great programmers are not born; they are made through daily practice with real code!"""


def calc_words(text):
    return len(text.lower().split())

def avg_word_length(text):
    words = re.sub(r"[^\w\s]", "", text.lower()).split()
    words_list= [len(word) for word in words]
    words_result = 0 if len(words_list)==0 else round(sum(words_list)/len(words_list),2)
    return words_result

def calc_character(text):
    characters = len(text.replace(" ","").replace("\n",""))
    return characters

def calc_lines(text):
    lines = text.split("\n")
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

    return {"text":text, "charactersWithOutSpace" :characters_wo, "charactersWithSpace":characters, "lines": lines, "sentences": sentences, "avgWords": avg_word, "frequency": frequency['all'], "topFrequency": frequency['top'], "words": words}

if __name__ == '__main__':
    result = calculate(default_text)
    for key, value in result.items():
        print(f'{key}: {value}')