from utils import openai_authenticate, openai_completion

engine = 'gpt-4'

object_list = """
  - L-shaped block
  - block
  - bowl
  - container
  - cross
  - diamond
  - flower
  - heart
  - hexagon
  - letter A
  - letter E
  - letter G
  - letter M
  - letter R
  - letter T
  - letter V
  - pallet
  - pan
  - pentagon
  - ring
  - round
  - shorter block
  - small block
  - star
  - triangle
"""
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
  - purple paisley
"""


def generate_prompt(rule, group, candidate):
    system_prompt = f"""You are interfacing with a robotics environment that has a robotic arm learning to pick up objects based on some linguistic command (e.g. "pick up red bowl"). At each interaction, the researcher will specify the command that you need to teach the robot. In order to teach the robot, you will need to help design the training distribution by specifying what properties the target object can have based on the given command. Target objects in this environment have two properties: object type, object color.  Any object type can be paired with any color, but an object can only take on exactly one object type and exactly one color.
Object types:
{object_list}
Object colors:
{color_list}
    """
    user_prompt = f"""The command is "{rule}". In an instantiation of the environment that contains only some subset of the object types and colors, could the target object have {group} "{candidate}"? Think step-by-step and then finish with a new line that says "Final answer:" followed by "yes" or "no"."""
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]



def main():
    for group in ["object type", "object color"]:
        for candidate in object_list if group == "object type" else color_list:
            prompt = generate_prompt(rule, group, candidate)
            choices, _ = openai_completion(prompt, engine, 0.0, True)
            final_answer = choices[0]["content"].split("\nFinal answer: ")[-1]



if __name__ == '__main__':
    main()