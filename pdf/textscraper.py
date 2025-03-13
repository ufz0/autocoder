from tika import parser 

def getPdfContent(filename: str) -> str:
    raw = parser.from_file(filename)
    return raw['content'] 

