from pathlib import Path

from text_analysis_utils import calculate
from file_handling_utils import handle_file
from file_handling_utils import read_file
import sys

def handle_user_text_input():
    print("Enter your text (Press Ctrl+D on Linux/macOS or Ctrl+Z on Windows to stop):")
    lines = sys.stdin.readlines()
    text = ''.join(lines)
    return text


def user_input_function(text):
    if text == "":
        input_result = input("Choose what do you want to do:\n 1)Provide desired text manually\n 2)Provide a file path (.txt)\n 3)Use default text\nEnter your choice Number:")
    else:
        input_result = input(text)
    return input_result

def handle_user_input():
    while True:
        option = user_input_function("")
        if option == "1":
            text= handle_user_text_input()
            return calculate(text)
        elif option == "2":
            continued =handle_file(input("Enter your file's path:\n"))
            if continued==None:
                continue
            else:
                return continued
        elif option == "3":
            return calculate(read_file(Path(__file__).parent / "default.txt"))
        else:
            print("Invalid option! please choose correctly!")