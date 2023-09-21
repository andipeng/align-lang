from utils import openai_authenticate, openai_completion
import pandas as pd
import os
from tqdm import tqdm


engine = 'gpt-4'
results_path = f'results'

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
    "Bring me a letter. If there are multiple, bring the one that comes earliest in the alphabet",
    "Bring me something I can drink water out of"
]
candidates_list=[
    ['letter T', 'letter A', 'letter V', 'letter E', 'letter G', 'letter M', 'letter R'],
    ['pan', 'bowl', 'container']
]

def generate_prompt(rule, candidates):
    system_prompt = f"""You are interfacing with a robotics environment that has a robotic arm learning to pick up objects based on some linguistic command (e.g. "pick up red bowl"). At each interaction, the researcher will specify the command that you need to teach the robot. In order to teach the robot, you will need to help design the training distribution by specifying what properties the target object can have based on the given command. Target objects in this environment have two properties: object type, object color.  Any object type can be paired with any color, but an object can only take on exactly one object type and exactly one color.
Object types:
{object_list}
Object colors:
{object_colors}
    """
    user_prompt = f"""The command is "{rule}". This command could be referring to the following object types: {", ".join(candidates)}. Rank these object types by how well they fit the intent of the command from best to worst. Think step-by-step and then finish with a new line that says "Final answer:" followed by a comma-separated ranked list ordered from best match to worst match."""
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]



# rules = [rules[6]]
def main():
    openai_authenticate(True)
    types=object_list.split('\n  - ')[1:]
    colors=object_colors.split('\n  - ')[1:]
    group_dict={
        "object type":types,
        "object color":colors
    }
    os.makedirs(results_path,exist_ok=True)
    r=0
    for rule, candidates in tqdm(list(zip(rules,candidates_list))):
        rows=[]
        answer=False
        attempt=0
        while not answer:
            attempt+=1
            messages = generate_prompt(rule, candidates)
            choices,_=openai_completion(messages, engine, 0.0, True)
            try:
                answer = choices[0]['message']['content'].split("\nFinal answer: ")[-1].replace('\n', '').strip()
                # assert(answer.lower() in ['yes','no'])
                print(candidates, answer)

            except Exception as e:
                answer=False
                if attempt>=10:
                    answer='error'
                    print(f'''Error: {rule} \n {e}''')
        row=[rule, True, candidates, answer]
        rows.append(row)
        df = pd.DataFrame(rows, columns=['rule','ranking','candidates','answer'])
        df.to_csv(f'{results_path}/{engine}_rank-{r}.csv')
        r+=1



if __name__ == '__main__':
    main()