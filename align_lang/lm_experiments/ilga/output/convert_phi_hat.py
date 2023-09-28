import csv

dic = {}
with open('gpt-4_rule-0_fave_food_tropical.csv') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # Skip the headers
    for row in reader:
        if row[2] == "yes":
            value = row[1].split()[0]
            key = row[1].split()[1]
            if key not in dic:
                dic[key] = [value]
            else:
                dic[key].append(value)

print(dic)