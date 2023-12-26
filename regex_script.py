import re

CARD_REGEX = """(<div class=hanzi>.*</div>)\n(<span style=""font-family:SimSun; font-size: 22px; color: #B80000; "">.*</span>)\n.*\n.*\n.*\n<hr>\n.*\n"\t".*\n(<span style=""font-family:SimSun; font-size: 22px; color: #B80000; "">.*</span>)\n.*\n(<div class=english>.*</div>)\n.*\n<hr>\n.*\n.*\n.*\n(\[sound:.*?\.mp3\]).*\n.*\n.*\n"""

with open("Mandarin_ Vocabulary.txt", "r") as anki_txt:
    file_string = anki_txt.read()

matches = re.findall(CARD_REGEX, file_string)

NEW_CARD_TEMPLATE = '"{}\n{}\n{}"\t"{}{}"\n'

with open("Mandarin_Vocabulary_fixed.txt", "w") as new_anki:
    # Write headers
    new_anki.write("#separator:tab\n#html:true\n")

    for match in matches:
        hanzi, front_font, back_font, english, mp3 = match
        new_card = NEW_CARD_TEMPLATE.format(hanzi, front_font, mp3, back_font, english)
        new_anki.write(new_card)
