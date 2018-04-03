import sys
import os


def parse_args(argv):
    if (len(argv) != 5):
        print('There should be exactly 5 arguments')
        return
    else:
        if (argv[1] == "UNION"):
            print('Union - Case')
            union(argv[2], argv[3], argv[4])
        else:
            if (argv[1] == "SEPERATE"):
                print('Seperate - Case')


def union(input1_path, input2_path, output_path):

    if (not(os.path.exists(input1_path)) or  not (os.path.exists(input1_path))):
        print('file 1 or file 2 does not exist')
        return

    file1_extension = get_file_extension(input1_path)
    file2_extension = get_file_extension(input2_path)

    if (file1_extension != file2_extension):
        print('files extensions should be the same')
        return



def get_file_extension(file_path):
    file_name,file_extension = os.path.splitext(file_path)
    return(file_extension)

# parse_args((sys.argv))
union('doc1d.txt','doc2d.txty','')