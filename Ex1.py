import sys
import os
import re

#what should we do if we get an empty file? create an empty answer file?

def parse_args(argv):
    if (len(argv) == 0):
        print "No arguments accepted"
        return
    elif (argv[0] not in ["UNION","SEPERATE","DISTINCT","LIKE"]):
        print "unknown command"
        return
    elif (len(argv) != 5 and argv[0] in ["UNION","SEPERATE", "DISTINCT"]):
        print "number of parameters for command is wrong, should be 4"
        return
    elif (len(argv) not in [5,6] and argv[0] == "LIKE"):
        print('number of parameters for command is wrong, should be 5 or 6')
        return
    else:
        if (argv[1] == "UNION"):
            union(argv[2], argv[3], argv[4])
        elif(argv[1] == "SEPERATE"):
                seperate(argv[2], argv[3], argv[4])
        elif (argv[1] == "DISTINCT"):
            distinct(argv[2],argv[3],argv[4])
        else:
            output_path = "/"
            if(len(argv) == 6): output_path = argv[5]
            like(argv[2],argv[3],argv[4],output_path)



def input_and_index_validation(input_path, index):
    if (not os.path.exists(input_path)):
        print 'Input file not found'
        return None

    input_file_name, input_file_extension = get_file_name_and_extension(input_path)

    if (input_file_extension not in ['.txt', '.csv']):
        print 'Error! Illegal file extension'
        return None
    if (is_file_structure_consistent(input_path) == -1):
        print 'Error! File structure is not consistent'
        return None

    input_file = read_file_by_lines(input_path)

    if (len(input_file) == 0):
        return None

    num_of_attributes = len(input_file[0].split("::"))

    if (index < 0 or index >= num_of_attributes):
        print 'Error! Column does not exist in table'
        return None

    return [input_file_name, input_file_extension]


def like(input_path, index, parameter, output_path):
    input_vars = input_and_index_validation(input_path,index)

    if input_vars is None:
        return
    else:
        input_file, input_file_extension = input_vars[0],input_vars[1]

    try:
        pattern = re.compile(parameter)
    except re.error:
        print 'Error! Invalid regular expression'
        return

    answer = [x for x in input_file if pattern.search(x[index]) is not None]
    write_file_replace_if_exists(output_path + input_file_extension, answer)


def distinct(input_path, column_index, output_path):
    input_vars = input_and_index_validation(input_path, column_index)

    if input_vars is None:
        return
    else:
        input_file, input_file_extension = input_vars[0], input_vars[1]

    required_column = [x[column_index] for x in input_file]

    if (is_int(required_column[0]) or is_str(required_column[0])):
        sorted_set = sorted(set(required_column))
    else:
        unsorted_set = set(required_column)
        sorted_set = sorted(unsorted_set, key=required_column.index)

    write_file_replace_if_exists(output_path + input_file_extension, sorted_set)


def union(input1_path, input2_path, output_path):
    if (not (os.path.exists(input1_path)) or not (os.path.exists(input1_path))):
        print('file 1 or file 2 does not exist')
        return

    file1_name, file1_extension = get_file_name_and_extension(input1_path)
    file2_name, file2_extension = get_file_name_and_extension(input2_path)

    if (file1_extension != '.txt' and file1_extension != '.csv'):
        print('input files in the wrong formats')
        return
    if (file2_extension != '.txt' and file2_extension != '.csv'):
        print('input files in the wrong formats')
        return
    if (file1_extension != file2_extension):
        print('files extensions should be the same')
        return

    if (is_file_structure_consistent(input1_path) == -1 or is_file_structure_consistent(input2_path) == -1):
        return

    file1 = read_file_by_lines(input1_path)
    file2 = read_file_by_lines(input2_path)
    file1_num_of_att = 0
    file2_num_of_att = 0
    file2_first_line = None
    file1_first_line = None

    if (len(file1) != 0):
        file1_first_line = file1[0].split("::")
        file1_num_of_att = len(file1_first_line)

    if (len(file2) != 0):
        file2_first_line = file2[0].split("::")
        file2_num_of_att = len(file2_first_line)

    if (file1_num_of_att != file2_num_of_att and (file1_first_line != None and file2_first_line != None)):
        print('Files structure is not consistent, number of attributes is different')
        return
    else:
        if (file1_first_line != None and file2_first_line != None):
            for att1, att2 in zip(file1_first_line, file2_first_line):
                if ((is_int(att1) and not (is_int(att2))) or (is_int(att2) and not (is_int(att1)))): # can we except the types to be only int or string?
                    print('Files structure is not consistent, different types')
                    return
                if ((is_str(att1) and not (is_str(att2))) or (is_str(att2) and not (is_str(att1)))):
                    print('Files structure is not consistent, different types')
                    return

    file1_after_append = [line + '::' + file1_name for line in file1]
    file2_after_append = [line + '::' + file2_name for line in file2]
    whole_file_after_append = file1_after_append + file2_after_append
    if os.path.isfile(output_path + file1_extension):
        os.remove(output_path + file1_extension)
    output_file_name, output_extension = get_file_name_and_extension(output_path)
    output_file = open(output_file_name + file1_extension, "a")
    for line in whole_file_after_append:
        output_file.write(line + '\n')
    output_file.close()


def seperate(input_path, output_path1, output_path2):
    if (not (os.path.exists(input_path))):
        print('input file does not exist')
        return
    input_file_name, input_file_extension = get_file_name_and_extension(input_path)

    if (input_file_extension != '.txt' and input_file_extension != '.csv'):
        print('input file is in the wrong formats')
        return

    if (is_file_structure_consistent(input_path) == -1):
        return

    file_by_lines = read_file_by_lines(input_path)
    prev_line = None
    file_1_lines = []
    file_2_lines = []
    switched_to_second_file = 0
    for line in file_by_lines:
        line_splitted = line.split("::")
        current_suffix = line_splitted[len(line_splitted) - 1]
        if (prev_line != None):
            prev_suffix = prev_line_splitted[len(prev_line_splitted) - 1]
            if (prev_suffix != current_suffix):
                if (switched_to_second_file == 1):
                    print('more than two values to split for in the merged file')
                    return
                switched_to_second_file = 1

        if (switched_to_second_file == 0):
            file_1_lines.append(line.replace("::" + current_suffix, ""))
        else:
            if (switched_to_second_file == 1):
                file_2_lines.append(line.replace("::" + current_suffix, ""))
        prev_line = line
        prev_line_splitted = prev_line.split("::")

    write_file_replace_if_exists(output_path1 + input_file_extension, file_1_lines)
    write_file_replace_if_exists(output_path2 + input_file_extension, file_2_lines)


def get_file_name_and_extension(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    return (file_name, file_extension)


def read_file_by_lines(file_path):
    with open(file_path) as f:
        lines = f.read().splitlines()

    lines = [line.strip() for line in lines if line is not None and line != ""]
    return lines


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False



def is_str(s):
    try:
        str(s)
        return True
    except ValueError:
        return False


def is_file_structure_consistent(file_path):
    with open(file_path) as fp:
        line = fp.readline()
        while line:
            prev_line = line
            line = fp.readline()
            if (line != None and line != ""):
                line_splitted = line.split("::")
                prev_line_splitted = prev_line.split("::")
                if (len(line_splitted) != len(prev_line_splitted)):
                    print(file_path + ' structure is not consistent, different number of attributes')
                    return -1
                for att1, att2 in zip(line_splitted, prev_line_splitted):
                    if ((is_int(att1) and not (is_int(att2))) or (is_int(att2) and not (is_int(att1)))):
                        print(file_path + ' structure is not consistent, different types')
                        return -1


def write_file_replace_if_exists(file_path, file_content): #ata king
    if os.path.isfile(file_path):
        os.remove(file_path)
    output_file = open(file_path, "a")
    for line in file_content:
        output_file.write(line + '\n')
    output_file.close()

# seperate('out.txt', 'file1_1', 'file2_1')
# is_file_structure_consistent('out.txt')
parse_args((sys.argv))