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

    return {"text":text, "characters_without_space" :characters_wo, "characters_with_space":characters, "lines": lines, "sentences": sentences, "avg_word_length": avg_word, "frequency": frequency['all'], "top_word_frequency": frequency['top'], "words": words}

def read_file(file_url):
    with open(file_url, "r", encoding="utf-8") as file:
        return calculate(file.read())

def file_choice():
        continued = input("file not found :(\nDo you want to continue? \n (y)try another file\n (m)main menu\ntype anything else to exit: ").lower().strip()
        return continued

def handle_file(file_url):
    while True:
        try:
            return read_file(file_url)
        except FileNotFoundError :
            continued= file_choice()
            if continued == "y":
                file_url = input("Enter your file's CORRECT path:")
            elif continued == "m":
                return  "menu"
            else:
                return {"End of the program": "Bye!"}


def handle_user_input():
    while True:
        option = user_input_function("")
        if option == "1":
            return calculate(input("Enter your text:\n"))
        elif option == "2":
            continued =handle_file(input("Enter your file's path:\n"))
            if continued== "menu":
                continue
            else:
                return continued
        elif option == "3":
            return calculate(default_text)
        else:
            print("Invalid option! please choose correctly!")


def user_input_function(text):
    if text == "":
        input_result = input("Choose what do you want to do:\n 1)Provide desired text manually\n 2)Provide a file path (.txt)\n 3)Use default text\nEnter your choice Number:")
    else:
        input_result = input(text)
    return input_result

if __name__ == '__main__':
    result =handle_user_input()

    # result = calculate(default_text)
    for key, value in result.items():
        print(f'{key}: {value}')