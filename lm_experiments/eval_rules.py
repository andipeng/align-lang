import csv
from glob import glob
import json
import matplotlib.pyplot as plt

rule_to_group_to_possibles = {}

for csv_file in glob("results/*.csv"):
    with open(csv_file) as f:
        i=0
        # csv_reader = csv.reader(f, headers=True)
        csv_reader = csv.DictReader(f)
        for line in csv_reader:
            # i += 1
            # if i == 1:
            #     continue
            # line = line.split(",")
            rule = line["rule"]
            if rule not in rule_to_group_to_possibles:
                rule_to_group_to_possibles[rule] = {}
            if line["answer"] == "yes":
                if line["group"] not in rule_to_group_to_possibles[rule]:
                    rule_to_group_to_possibles[rule][line["group"]] = []
                rule_to_group_to_possibles[rule][line["group"]].append(line["candidate"])

gold_labels = json.load(open("../gt_annotations.json"))

pertask_EMs = {}
pertask_overlaps = {}
for task in gold_labels:
    rule = task["task_name"]
    try:
        assert rule in rule_to_group_to_possibles
    except:
        breakpoint()
    gt_objects = task["object type"]
    pred_objects = rule_to_group_to_possibles[rule]["object type"]
    gt_colors = task["object color"]
    pred_colors = rule_to_group_to_possibles[rule]["object color"]
    # remove parentheticals
    pred_objects = [object.split("(")[0].strip() for object in pred_objects]
    pred_colors = [color.split("(")[0].strip() for color in pred_colors]
    # evaluate
    pertask_EMs[rule] = {
        "object type": set(gt_objects) == set(pred_objects),
        "object color": set(gt_colors) == set(pred_colors),
    }
    type_overlap = len(set(gt_objects).intersection(set(pred_objects))) / len(set(gt_objects).union(set(pred_objects)))
    color_overlap = len(set(gt_colors).intersection(set(pred_colors))) / len(set(gt_colors).union(set(pred_colors)))
    try:
        assert pertask_EMs[rule]["object type"] == (abs(type_overlap - 1) < 1e-5)
        assert pertask_EMs[rule]["object color"] == (abs(color_overlap - 1) < 1e-5)
    except:
        breakpoint()
    pertask_overlaps[rule] = {
        "object type": type_overlap,
        "object color": color_overlap,
    }


print(pertask_EMs)
print(pertask_overlaps)
    

objects = list(pertask_overlaps.keys())
object_types = [pertask_overlaps[obj]['object type'] for obj in objects]
object_colors = [pertask_overlaps[obj]['object color'] for obj in objects]

fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(objects, object_types, color='blue', width=-0.4, align='edge', label='Object type')
ax.bar(objects, object_colors, color='orange', width=0.4, align='edge', label='Object color')

ax.legend()
ax.set_xticklabels(objects, rotation=20, ha='right')
ax.set_ylabel('Score')
ax.set_title('Object type and color scores')

plt.tight_layout()
plt.savefig("figures/object_type_color_scores.png")
