def format_doc(Filename):
    with open(Filename, 'r') as f: lines = f.readlines()
    for line in lines:
        if len(line) > 90: words = line.split()
    for word in words:
        print(word)
    else:
        print(line)

def rewrite_doc(path):
    with open(path, 'r') as f: lines = f.readlines()
new_lines = []


for line in new_lines:
    if len(line) <= 90: new_lines.append(line)
    else:
        words = line.split(' ')
    new_line = ''
    for word in words:
        if len(new_line + word) <= 90: new_line += word + ' '
    else: new_lines.append(new_line)
    new_line = word + ' '
    new_lines.append(new_line)
    with open(__path__, 'w') as f:
        for line in new_lines:
            f.write(line)
print(format_doc("tc1.txt"))