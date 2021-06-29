import re
import bs4

def clean_text(inp):
    return re.sub("\n\n+", "\n", bs4.BeautifulSoup(inp, "lxml").text).strip()
