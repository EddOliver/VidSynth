import os

myDir = sorted(os.listdir("frames"),key=lambda f: int(''.join(filter(str.isdigit, f))))
for index,file in enumerate(myDir):
    print(file)