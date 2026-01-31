import re

def clean_text(text:str)-> str:
    text = text.lower()
    
    # this will replace all the line breaks and tabs with spaces
    text= text.replace("\n"," ").replace("\t"," ")
    
    # removing punctuation while keeping letter,numbers and spaces
    text = re.sub(r"[^a-z0-9\s\+\.\#]"," ",text)
    
    # removinf extra spaces(multiple -> single)
    text = re.sub(r"\s+"," ",text)
    return text.strip()