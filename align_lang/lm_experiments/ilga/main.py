from utils import openai_authenticate, openai_completion, load_openai_cache
import pandas as pd
import os
import json
from tqdm import tqdm


engine = 'gpt-4'
results_path = f'results'
use_azure = False
openai_cache_file = f'openai_cache_{engine}.jsonl'

object_list = """
  - L-shaped block
  - block
  - bowl
  - container
  - cross (block of this shape)
  - diamond (block of this shape)
  - flower (block of this shape)
  - heart (block of this shape)
  - hexagon (block of this shape)
  - letter A
  - letter E
  - letter G
  - letter M
  - letter R
  - letter T
  - letter V
  - pallet
  - pan
  - pentagon (block of this shape)
  - ring (block of this shape)
  - round (block of this shape)
  - shorter block
  - small block
  - star (block of this shape)
  - triangle (block of this shape)"""
object_colors = """
  - brick
  - tiles
  - wooden
  - granite
  - plastic
  - polka dot
  - checkerboard
  - tiger
  - magma
  - rainbow
  - blue
  - cyan
  - green
  - olive
  - orange
  - pink
  - purple
  - red
  - yellow
  - dark blue
  - dark cyan
  - dark green
  - dark orange
  - dark pink
  - dark purple
  - dark red
  - dark yellow
  - red and yellow stripe
  - red and green stripe
  - red and blue stripe
  - red and purple stripe
  - yellow and green stripe
  - yellow and blue stripe
  - yellow and purple stripe
  - green and blue stripe
  - green and purple stripe
  - blue and purple stripe
  - dark red and yellow stripe
  - dark red and green stripe
  - dark red and blue stripe
  - dark red and purple stripe
  - dark yellow and green stripe
  - dark yellow and blue stripe
  - dark yellow and purple stripe
  - dark green and blue stripe
  - dark green and purple stripe
  - dark blue and purple stripe
  - red and yellow polka dot
  - red and green polka dot
  - red and blue polka dot
  - red and purple polka dot
  - yellow and green polka dot
  - yellow and blue polka dot
  - yellow and purple polka dot
  - green and blue polka dot
  - green and purple polka dot
  - blue and purple polka dot
  - dark red and yellow polka dot
  - dark red and green polka dot
  - dark red and blue polka dot
  - dark red and purple polka dot
  - dark yellow and green polka dot
  - dark yellow and blue polka dot
  - dark yellow and purple polka dot
  - dark green and blue polka dot
  - dark green and purple polka dot
  - dark blue and purple polka dot
  - red swirl
  - yellow swirl
  - green swirl
  - blue swirl
  - purple swirl
  - dark red swirl
  - dark yellow swirl
  - dark green swirl
  - dark blue swirl
  - dark purple swirl
  - red paisley
  - yellow paisley
  - green paisley
  - blue paisley
  - purple paisley"""

rules=[
    #"Bring me the red heart",
    #"Bring me the heart",
    #"Bring me the tiger-colored object",
    #"Bring me a letter from the word 'letter'",
    #"Bring me a consonant with a warm color on it",
    #"Bring me a vowel with multiple colors on it",
    #"Bring me something to drink water out of",
    #"Bring me something I can put food in",
    #"Rotate the red heart",
    #"Rotate a letter from the word 'letter'",
    #"Rotate something I can put food in",
    #"Sweep the hexagon into the square without touching the red pan",
    #"Sweep the letter into the square without touching the pan",
    #"Sweep the letter into the square without touching anything red",
    "Bring me a fruit."
]


# def generate_prompt_verbs(rule):
#     system_prompt = f"""You are interfacing with a robotics environment that has a robotic arm learning to act based on some linguistic command (e.g. "examine and pick up red bowl without touching the pallet"). At each interaction, the researcher will specify the command that you need to teach the robot. To fulfill each command, the robot may need to act on objects in different ways. Your job is to identify the different categories of ways the robot must interact with each relevant object (e.g. object to pick up, object to avoid, etc.). In other words, you are identifying verb abstractions present in the command. There may be one or more categories, and one or more objects may fall into the category. If there are a sequence of actions enacted upon the same set of objects (e.g. object to examine, object to pick up), then please merge these categories into one ("object to examine and pick up")"""
#     user_prompt = f"""The command is "{rule}". How many categories of relevant objects are here? Merge categories that describe the same set of objects so that we have the shortest list of categories. Give the final answer in the form:
# <n> categories: <comma-separated list of category names>

# Specify category names in the form "object to <verb>". Do not include extra punctuation. Do not specify any concrete objects or features of objects that fall into those categories. Ignore all irrelevant object categories."""
#     return [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": user_prompt},
#     ]

def get_preferences_prompt(rule: str, scene1: set, scene2: set):
    # diff_scenes = scene1 - scene2
    intersection_scenes = scene1.intersection(scene2)
    user_prompt = f"""The user is demonstrating the task: "{rule}". 

There are two scenes. The user takes a different trajectory in the first scene vs. the second. 

The first and second scene both have the following features:
{json.dumps(intersection_scenes)}
The first and second scene differ on the following features:
First scene-
{json.dumps(scene1 - scene2)}
Second scene-
{json.dumps(scene2 - scene1)}

What is most likely to have caused the difference in the user's trajectory and why? Please assign a confidence score.
    """
    return [
        {"role": "user", "content": user_prompt},
    ]



def generate_prompt_object_abstractions(preferences, rule, object_category, group, candidate):
    system_prompt = f"""You are interfacing with a robotics environment that has a robotic arm learning to act on objects based on some linguistic command (e.g. "pick up red bowl"). At each interaction, the researcher will specify the command that you need to teach the robot. In order to teach the robot, you will need to help design the training distribution by specifying what properties the target object can have based on the given command. Target objects in this environment have two properties: object type, object color.  Any object type can be paired with any color, but an object can only take on exactly one object type and exactly one color.

A user has the following preference rules: 
{preferences}

Object types:
{object_list}
Object colors:
{object_colors}
    """
    user_prompt = f"""The command is "{rule}". In an instantiation of the environment that contains only some subset of the object types and colors, could the {object_category} have {group} "{candidate}"? Recall that the object types and colors are mutually exclusive. Think step-by-step and then finish with a new line that says "Final answer:" followed by "yes" or "no" and nothing else. If unsure, make your best guess."""
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


"""
Given the user preferences above, what are the salient features in the following scene?
{
{
    "object": "banana",
     "object_color": "yellow",
},
{
    "object": "pan",
    "object_color": "red",
},
{
    "object": "pan",
    "object_color": "green",
}
}
"""

# rules = [rules[6]]
def main():
    openai_authenticate(use_azure)
    types=object_list.split('\n  - ')[1:]
    colors=object_colors.split('\n  - ')[1:]
    group_dict={
        "object type":types,
        "object color":colors
    }
    os.makedirs(results_path,exist_ok=True)
    openai_cache = load_openai_cache(openai_cache_file)
    for r, rule in tqdm(enumerate(rules)):
        print(rule)

        # sample two (similar) scenes where trajs differ
        preferences_prompt = get_preferences_prompt(rule, scene1, scene2)
        choices, _ = openai_completion(preferences_prompt, engine, 0.0, use_azure, openai_cache, openai_cache_file)
        preferences_list = json.loads(choices[0]['message']['content'])
        # pick out most likely answer (potentially including ties)



        # if r > 10:
        #     continue
        rows=[]
        try:
            object_categories = choices[0]['message']['content'].split("\n")[-1].split(": ")[-1].strip().strip(".").split(", ")
            object_categories = [object_cat.lower() for object_cat in object_categories]
            print(object_categories)
            
        except Exception as e:
            answer=False
            if attempt>=10:
                answer='error'
                print(f'''Error: {rule} \n {e}''')
        for object_category in object_categories:  # channels
            for group in ["object type", "object color"]:
                for c, candidate in enumerate(group_dict[group]):
                    answer=False
                    attempt=0
                    while not answer:
                        attempt+=1
                        messages = generate_prompt_object_abstractions(rule, object_category, group, candidate)
                        choices, _ = openai_completion(messages, engine, 0.0, use_azure, openai_cache, openai_cache_file)
                        try:
                            answer = choices[0]['message']['content'].split("\nFinal answer: ")[-1].replace('\n', '').strip(".").strip()
                            assert(answer.lower() in ['yes','no'])
                            print(f"{c}/{len(group_dict[group])}", candidate, answer)
                            
                        except Exception as e:
                            answer=False
                            breakpoint()
                            if attempt>=10:
                                answer='error'
                                print(f'''Error: {rule} \n {e}''')
                    row=[rule, object_category, group, candidate, answer]
                    rows.append(row)
        df = pd.DataFrame(rows, columns=['rule','object_category','group','candidate','answer'])
        df.to_csv(f'{results_path}/{engine}_rule-{r}.csv')
        r+=1
        print()



if __name__ == '__main__':
    main()