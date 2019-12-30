import os

try:
    os.mkdir(os.getcwd() + os.path.sep + "tmp2")
except:
    pass

FILENAME = "JMdict_e"
output = "file_"
cnt = 1

with open(FILENAME) as f:
    openedFile = False
    count = 0
    for Line in f:
        line = Line.rstrip()
        #print(line)
        if line == "<entry>" or line == "</entry>":
            count += 1

        if count % 2 == 1:
            if openedFile == False:
                openedFile = True
                shortFile = open("tmp" + os.path.sep + output + str(cnt), "w")

            shortFile.write(line + "\n")
        else:
            if openedFile == True:
                openedFile = False
                shortFile.close()
                print("[+] Written {}...".format(cnt))
                cnt += 1
