
m = input('Please enter the file path: ')
n = input('Please enter the old word: ')
o = input("Please enter the new word: ")


def replace(file_path, oword, nword):
    with open(file_path, "r") as file:
        text = file.read()
        ntext = text.replace(oword, nword)
    with open(file_path, "w") as file:
        file.write(ntext)
replace(m,n,o)


print('done')