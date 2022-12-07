def rewrittenDocument(file_path):
    f = open(file_path, mode = "r")
    content = f.readlines()
    body = content[6:]
    for i in range(len(body)):
        if body[i] != "\n":
            new_line = ""
            count = 0
            for j in range(len(body[i])):
                if j != 0 and j % 90 == 0:
                    lastInteger = body[i][count:j].rfind(" ")
                    new_line += (body[i][count:lastInteger + 1] + "\n")
                    count = lastInteger + 1
            new_line += body[i][count: len(body[i])]
            body[i] = new_line
    content = content[:6] + body
    f = open(file_path, mode = "w")
    f.writelines(content)
    f.close()


file_path = input("Please input the file path:")
rewrittenDocument(file_path)