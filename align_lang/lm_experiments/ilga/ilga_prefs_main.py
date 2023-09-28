from align_lang.lm_experiments.utils import openai_authenticate, openai_completion, load_openai_cache
import pandas as pd
import os
import json
from tqdm import tqdm
import argparse


engine = 'gpt-4'
results_path = f'output'
use_azure = False
openai_cache_file = f'openai_cache_{engine}.jsonl'

rules=[
    #"Bring me a fruit",
    #"Bring me something to put food in",
    #"Bring me a cereal bowl",
    #"Bring me my favorite food",
    #"Put down the mug full of water",
    #"Put down the pan",
    #"Put away the cardboard box",
    #"Put away the food in the right place",
    #"Sweep the scraps into the sink",
    #"Sweep the food into the sink",
    #"Sweep the dust into the trash",
    #"Sweep the floor in my room",
]

def get_preferences_prompt(rule: str, scene1: set, scene2: set):
    scene1 = {tuple(obj) for obj in scene1}
    scene2 = {tuple(obj) for obj in scene2}
    intersection_scenes = scene1.intersection(scene2)
    
    intersection_scenes = sorted(list(intersection_scenes))
    scene1_minus_scene2 = sorted(list(scene1 - scene2))
    scene2_minus_scene1 = sorted(list(scene2 - scene1))
    user_prompt = f"""The user is demonstrating the task: "{rule}". 

There are two scenes. The user takes a different trajectory in the first scene vs. the second. 

The first and second scene both have the following features:
{json.dumps(intersection_scenes)}
The first and second scene differ on the following features:
First scene-
{json.dumps(scene1_minus_scene2)}
Second scene-
{json.dumps(scene2_minus_scene1)}

What are the most likely high-level preferences to have caused the difference in the user's behavior and why? The user took different trajectories in the two scenes. Please give a list of brief preferences (with only one reason) and assign a confidence score to each answer, in the format [["answer", score], ["answer", score], ...]. Please ensure all scores sum up to 1.
    """
    print(user_prompt)
    return [
        {"role": "user", "content": user_prompt},
    ]

def main(args):
    openai_authenticate(use_azure)
    os.makedirs(results_path,exist_ok=True)
    openai_cache = load_openai_cache(openai_cache_file)
    preferences = {}
    for r, rule in tqdm(enumerate(rules)):
        print(rule)

        scenes = json.load(open(f"{args.scenes_dir}/rule-11/{args.preference_file}.json"))

        # sample two (similar) scenes where trajs differ
        preferences_prompt = get_preferences_prompt(rule, scenes["scene1"], scenes["scene2"])
        choices, _ = openai_completion(preferences_prompt, engine, 0.0, use_azure, openai_cache, openai_cache_file)
        preferences_list = json.loads(choices[0]['message']['content'])
        print(preferences_list)
        # pick out most likely answer (potentially including ties)
        preferences[f"rule-{r}"] = preferences_list

    # df = pd.DataFrame(rows, columns=['rule','candidate','answer'])
    json.dump({
        "preference_id": args.preference_file,
        "preferences": preferences,
    }, open(f'preferences-gpt/{args.preference_file}.json', "w"), indent=4)
    r+=1
    print()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scenes_dir', type=str, default="scenes", help="scenes directory")
    parser.add_argument('--preference_file', type=str, default=None, help="preference file we want to save to")
    args = parser.parse_args()
    main(args)