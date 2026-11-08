from fastapi import FastAPI

from file_handling_utils import read_file
from text_analysis_utils import calculate

app = FastAPI()
@app.get("/stats/{file_address:path}")
def home(file_address: str, top_words: int = 5):
    print("*****url:::::" ,file_address)
    text= read_file(file_address)
    return calculate(text, top_words)