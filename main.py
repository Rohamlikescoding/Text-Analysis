from user_input_utils import handle_user_input

if __name__ == '__main__':

    result =handle_user_input()

    for key, value in result.items():
        print(f'{key}:\n {value}')