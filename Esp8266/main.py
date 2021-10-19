import json
from composeActs import ComposeActs

with open("presentation.json") as file:
    presentation = json.load(file)
    composer = ComposeActs(presentation)
    num_acts = presentation["length"]
    
    for i in range(1, num_acts+1):
        key = "act" + str(i)
        composer.read_moviments(key)