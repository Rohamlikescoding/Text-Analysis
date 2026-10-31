import re


input = """Python is a versatile, high-level programming language loved by developers worldwide.
Why do so many programmers start with Python?
Because Python prioritizes readability, simplicity, and clear syntax!
Whether you want to build web applications, analyze data, or automate tedious tasks, Python has the tools you need.
As you write more Python code, you will discover that writing code in Python feels almost like writing structured English.
Programming takes practice, time, and patience.
So keep writing Python, keep building projects, and keep solving real problems.
Remember: Great programmers are not born; they are made through daily practice with real code!"""




def print_hi(text):
    print(f'{text}')

def calc_words(text):
    words = text.lower().split()
    print("total words:",len(words))
    return words

def avg_word_length(words):
    temp = [ len(word) for word in words ]
    result = 0 if len(temp)==0 else float(sum(temp)/len(temp))
    print("avg word length:",result)
    return result



def calc_character(text):
    characters = text.replace(" ","")
    print("characters with space:",len(text))
    print("characters without space:",len(characters))

def calc_lines(text):
    lines = text.split("\n")
    print("total lines:",len(lines))

def calc_sentences(text):
    sentences = len(re.findall(r"[^?!.][?!.]", text))

    print("total sentences:",sentences)

def word_frequency(text):
    words = text.lower().replace("?","").replace("!","").replace(".", "").replace(",", "").split()
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        elif word not in frequency:
            frequency[word] = 1

    sorted_frequency = dict(sorted(frequency.items(), key=lambda x: x[1] , reverse=True))
    print(frequency)
    # print(sorted_frequency)

    print(list(sorted_frequency)[0:5])
    return frequency


if __name__ == '__main__':
    print_hi(input)
    total_words = calc_words(input)
    avg_word_length(total_words)
    calc_character(input)
    calc_lines(input)
    calc_sentences(input)
    word_frequency(input)

