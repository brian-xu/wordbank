import json
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader


def process(raw_wordbank):
    lines = raw_wordbank.split()
    with open("wordBank.json") as f:
        prev = json.load(f)
    words = {}
    for key in prev:
        words[key] = set(prev[key])
    bank_name = ""
    for line in lines:
        if line:
            if not line[0].isalpha():
                bank_name = line[1:-2].capitalize()
                if bank_name not in words:
                    words[bank_name] = []
            elif bank_name:
                words[bank_name].add(line.lower())
                words["Normal"].add(line.lower())
    for key in words:
        words[key] = sorted(list(words[key]))
    with open("wordBank.json", "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=4)
    return words


raw_wordbank = """
GENERAL WORD BANK:




“JUMP”:
Leap
Spring
Bound
Hop
Vault
Skip
Pounce
Bounce
Surge
Propel
Soar
Launch
Ascend
Hurdle
Jolt
Rebound
Catapult
Flop
Ricochet
Flip
Up



“FAST”:

"""

words = process(raw_wordbank)

environment = Environment(loader=FileSystemLoader("./"))
results_filename = "wordbank.html"
results_template = environment.get_template("template.html")
context = {"words": words}
with open(results_filename, mode="w", encoding="utf-8") as results:
    results.write(results_template.render(context))
    print(f"... wrote {results_filename}")
