from text_analysis_utils import calculate

def read_file(file_url):
    with open(file_url, "r", encoding="utf-8") as file:
        return file.read()

def file_choice():
        continued = input("Error related to the file, make sure path or unicode is correct :(\nDo you want to continue? \n (y)try another file\n (m)main menu\ntype anything else to exit: ").lower().strip()
        return continued

def handle_file(file_url):
    while True:
        try:
            return calculate(read_file(file_url))
        except (OSError, UnicodeDecodeError):
            continued= file_choice()
            if continued == "y":
                file_url = input("Enter your CORRECT file:")
            elif continued == "m":
                return  None
            else:
                return {"End of the program": "Bye!"}