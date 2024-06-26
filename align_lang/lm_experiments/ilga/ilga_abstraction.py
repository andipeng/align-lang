import argparse
from align_lang.lm_experiments.utils import openai_authenticate, openai_completion, load_openai_cache
import pandas as pd
import os
import json
from tqdm import tqdm

engine = 'gpt-4'
results_path = f'output'
use_azure = False
openai_cache_file = f'openai_cache_{engine}.jsonl'

object_list = """
  - tomato
  - peach
  - apple
  - banana
  - pepper"""
object_colors = """
  - brick
  - tiles
  - wooden
  - granite
  - plastic
  - styrofoam
  - carpet
  - tiger
  - rainbow
  - blue
  - green
  - olive
  - orange
  - pink
  - purple
  - red
  - yellow"""

types=object_list.split('\n  - ')[1:]
colors=object_colors.split('\n  - ')[1:]
composed_objects = [f"{obj_color} {obj_type}" for obj_color in colors for obj_type in types]
group_dict={
    "object type":types,
    "object color":colors,
    "objects": composed_objects,
}
print(group_dict)


rules=[
    # ILGA tasks
    #"Bring me a fruit"
    #"Bring me something to put food in"
    #"Bring me a cereal bowl"
    "Bring me my favorite food"
    #"Put down the mug"
    #"Put down the pan"
    #"Put away the cardboard box"
    #"Put away the food"
    #"Sweep the scraps into the sink"
    #"Sweep the food into the sink"
    #"Sweep the dust into the trash"
    #"Sweep the floor in my room"
    ""
]

def generate_prompt_state_abstractions(preference_rule, rule, candidate):
    # preferences = "\n- ".join(preferences_list)
    system_prompt = f"""You are interfacing with a robotics environment that has a robotic arm learning to act on objects based on some linguistic command (e.g. "pick up red bowl"). At each interaction, the researcher will specify the command that you need to teach the robot. In order to teach the robot, you will need to help design the training distribution by specifying what properties the target object can have based on the given command. Target objects in this environment have two properties: object type, object color.  Any object type can be paired with any color, but an object can only take on exactly one object type and exactly one color.

Object list:
{composed_objects}
    """
    #print(system_prompt)
    user_prompt = f"""The command is "{rule}". A user has the following preference rules for the command: "{preference_rule}". In an instantiation of the environment that contains only some subset of the objects, is the presence of a {candidate} important for the robot to know about? Recall that the object types and colors are mutually exclusive. Think step-by-step and then finish with a new line that says "Final answer:" followed by "yes" or "no" and nothing else. If unsure, make your best guess."""
    #print(user_prompt)
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

# rules = [rules[6]]
def main(args):
    openai_authenticate(use_azure)
    os.makedirs(results_path,exist_ok=True)
    openai_cache = load_openai_cache(openai_cache_file)
    for r, rule in tqdm(enumerate(rules)):
        print(rule)

        preferences_list = json.load(open(f"preferences-human/{args.preference_file}.json"))["preferences"][f"rule-{r}"]
        if len(preferences_list) > 1:
            top_preference = max(preferences_list, key=lambda x: x[1])
            top_preference = top_preference[0]
        else:
            top_preference = preferences_list[0]
        rows = []

        # generate_prompt_state_abstractions(preferences_list, rule, candidate)
        for c, candidate in enumerate(composed_objects):
            answer=False
            attempt=0
            while not answer:
                attempt+=1
                messages = generate_prompt_state_abstractions(top_preference, rule, candidate)
                choices, _ = openai_completion(messages, engine, 0.0, use_azure, openai_cache, openai_cache_file)
                try:
                    answer = choices[0]['message']['content'].split("\nFinal answer: ")[-1].replace('\n', '').strip(".").strip()
                    assert(answer.lower() in ['yes','no'])
                    print(f"{c}/{len(composed_objects)}", candidate, answer)
                    
                except Exception as e:
                    answer=False
                    breakpoint()
                    if attempt>=10:
                        answer='error'
                        print(f'''Error: {rule} \n {e}''')
            row=[rule, candidate, answer]
            rows.append(row)
        df = pd.DataFrame(rows, columns=['rule','candidate','answer'])
        df.to_csv(f'{results_path}/{engine}_rule-{r}_{args.preference_file}.csv')
        r+=1
        print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--preference_file', type=str, default=None, help="preference file we want to load")
    args = parser.parse_args()
    main(args)