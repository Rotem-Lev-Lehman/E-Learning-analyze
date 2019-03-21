import csv


def myReader(fileName):
    with open(fileName, 'rb') as csvfile:
        creader = csv.reader(csvfile, delimiter='|')

        count = 15
        for row in creader:
            if(count == 0):
                break
            str = ""
            for i in row:
                str += i + ","
            str += ";\n"
            print str

            count -= 1


myReader("D:\\data for kobi\\eLearning\\new episode level\\episode_run_0000_part_00")