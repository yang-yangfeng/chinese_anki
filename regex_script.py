import re

CARD_REGEX = """(<div class=hanzi>.*</div>)\n(<span style=""font-family:SimSun; font-size: 22px; color: #B80000; "">.*</span>)\n.*\n.*\n.*\n<hr>\n.*\n"\t".*\n(<span style=""font-family:SimSun; font-size: 22px; color: #B80000; "">.*</span>)\n(<div class=pinyin>.*</div>)\n(<div class=english>.*</div>)\n.*\n<hr>\n.*\n.*\n.*\n(\[sound:.*?\.mp3\]).*\n.*\n.*\n"""

with open("Mandarin_ Vocabulary.txt", "r") as anki_txt:
    file_string = anki_txt.read()

matches = re.findall(CARD_REGEX, file_string)

NEW_CARD_TEMPLATE = '{}\t"{}\n{}\n{}\n{}"\t"{}{}"\t{}\n'

# Load tags
id_to_tags = {}
with open("Mandarin_Vocabulary_Notes_Clean.txt") as notes:
    for line in notes:
        # Ignore headers
        if not line.startswith("#"):
            id_ = int(line.split("\t", 1)[0])
            tags = line.rsplit("\t", 1)[-1]
            id_to_tags[id_] = tags

with open("Mandarin_Vocabulary_fixed.txt", "w") as new_anki:
    # Write headers
    new_anki.write("#separator:tab\n#html:true\n#guid column:1\n#tags column:4\n")

    for i, match in enumerate(matches):
        hanzi, front_font, back_font, pinyin, english, mp3 = match
        id_ = i+1
        new_card = NEW_CARD_TEMPLATE.format(id_, hanzi, front_font, pinyin, mp3, back_font, english, id_to_tags[id_])
        new_anki.write(new_card)
