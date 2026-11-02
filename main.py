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

def handle_file(file_url):
    try:
        with open(file_url , "r", encoding="utf-8") as file:
            return calculate(file.read())
    except FileNotFoundError :
        continued = str(input("file not found :(\nDo you want to continue (y/n/w for wrong option)?"))
        if continued == "y":
            return handle_file(str(input("Enter your file's CORRECT path:")))
        elif continued == "w":
            return handle_user_input(user_input_function(""))
        else:
            return {"End of the program":"Bye!"}


def handle_user_input(option):
    if option == "1":
        return calculate(str(input("Enter your text:\n")))
    elif option == "2":
        return handle_file(str(input("Enter your file's path:\n")))
    elif option == "3":
        return calculate(default_text)
    else:
        return handle_user_input(user_input_function("Invalid option! please choose correctly!:\n"))


def user_input_function(text):
    if text == "":
        input_result = str(input("Choose what do you want to do:\n 1)Provide desired text manually\n 2)Provide a file path (.txt)\n 3)Use default text\nEnter your choice Number:"))
    else:
        input_result = str(input(text))
    return input_result

if __name__ == '__main__':
    result =handle_user_input(user_input_function(""))

    # result = calculate(default_text)
    for key, value in result.items():
        print(f'{key}: {value}')