import sys
import os
import re

#what should we do if we get an empty file? create an empty answer file?

def parse_args(argv):
    if (len(argv) in [0,1]):
        print "No arguments accepted"
        return
    elif (argv[1] not in ["UNION","SEPERATE","DISTINCT","LIKE"]):
        print "unknown command"
        return
    elif (len(argv) != 5 and argv[1] in ["UNION","SEPERATE", "DISTINCT"]):
        print "number of parameters for command is wrong, should be 5"
        return
    elif (len(argv) not in [4,5,6] and argv[1] == "LIKE"):
        print('number of parameters for command is wrong, should be 4 or 5 or 6')
        return
    else:
        if (argv[1] == "UNION"):
            union(argv[2], argv[3], argv[4])
        elif(argv[1] == "SEPERATE"):
                seperate(argv[2], argv[3], argv[4])
        elif (argv[1] == "DISTINCT"):
            distinct(argv[2],argv[3],argv[4])
        else:
            reg = "*"
            output_path = "output.txt"
            if (len(argv) >4):
                reg = argv[4]
            if(len(argv) > 5):
                output_path = argv[5]

            like(argv[2],argv[3],reg,output_path)



def input_and_index_validation(input_path, index):
    if (not os.path.exists(input_path)):
        print 'Input file not found'
        return None

    input_file_name, input_file_extension = get_file_name_and_extension(input_path)

    if (input_file_extension not in ['.txt', '.csv']):
        print 'Error! Illegal file extension'
        return None

    input_file = read_file_by_lines(input_path)

    if (len(input_file) == 0):
        return None

    if (is_file_structure_consistent(input_file, input_path) == -1):
        print 'Error! File structure is not consistent'
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
        input_vars[0],input_vars[1]

    if parameter == "*":
        current_file = read_file_by_lines(input_path)
        write_file_replace_if_exists(output_path, current_file)
        return
    try:
        pattern = re.compile(parameter)
    except re.error:
        print 'Error! Invalid regular expression'
        return

    current_file = read_file_by_lines(input_path)
    current_file = [x.split("::") for x in current_file]
    answer = [x for x in current_file if pattern.search(x[index]) is not None]
    ans = ['::'.join(x) for x in answer]
    write_file_replace_if_exists(output_path, ans)


def distinct(input_path, column_index, output_path):
    input_vars = input_and_index_validation(input_path, column_index)

    if input_vars is None:
        return
    else:
        input_file, input_file_extension = input_vars[0], input_vars[1]
    file = read_file_by_lines(input_file+input_file_extension)
    file = [x.split("::") for x in file]
    required_column = [x[column_index] for x in file]
    is_iterable = False
    if required_column[0] in ['[]\n', '()\n', '{}\n', '[]', '()', '{}']: is_iterable = True
    else:
        try:
            x = eval(required_column[0])
            try:
                iter(x)
                is_iterable = True
            except TypeError:
                pass
        except SyntaxError:
            pass

    if not is_iterable:
        sorted_set = sorted(set(required_column))
    else:
        unsorted_set = set(required_column)
        sorted_set = sorted(unsorted_set, key=required_column.index)

    write_file_replace_if_exists(output_path, sorted_set)


def union(input1_path, input2_path, output_path):
    if (not (os.path.exists(input1_path)) or not (os.path.exists(input2_path))):
        print('file 1 or file 2 does not exist')
        return

    file1_name, file1_extension = get_file_name_and_extension(input1_path)
    file2_name, file2_extension = get_file_name_and_extension(input2_path)

    if (file1_extension not in ['.txt','.csv']):
        print('input files in the wrong formats')
        return
    if (file2_extension not in ['.txt','.csv']):
        print('input files in the wrong formats')
        return
    if (file1_extension != file2_extension):
        print('files extensions should be the same')
        return

    file1 = read_file_by_lines(input1_path)
    file2 = read_file_by_lines(input2_path)

    if (is_file_structure_consistent(file1, input1_path) == -1):
        print(input1_path + 'structure is not consistent, different number of attributes')
        return
    if (is_file_structure_consistent(file2, input2_path) == -1):
        print(input2_path + 'structure is not consistent, different number of attributes')
        return


    file2_first_line = None
    file1_first_line = None

    if (len(file1) != 0):
        file1_first_line = file1[0].split("::")

    if (len(file2) != 0):
        file2_first_line = file2[0].split("::")

    if (file1_first_line == None and file2_first_line==None):
        print ('both tables are empty')
        return

    if (file1_first_line == None):
        write_file_replace_if_exists(output_path, file2)
        return

    if (file2_first_line == None):
        write_file_replace_if_exists(output_path, file1)
        return
    else:
        attrbs = get_first_line_attrbs(file1_first_line)
        if check_both_lines_have_same_attr(file2_first_line,attrbs) == -1:
            print('Error! The table\'s format does not match')
            return
    file1_after_append = [line + '::' + file1_name for line in file1]
    file2_after_append = [line + '::' + file2_name for line in file2]
    whole_file_after_append = file1_after_append + file2_after_append
    write_file_replace_if_exists(output_path,whole_file_after_append)

def get_first_line_attrbs(line):
    ans = []
    for attr1_raw in line:
        attr1 = attr1_raw
        if attr1 in ['[]\n','()\n','{}\n','[]','()','{}']:
            attr1 = attr1[0] + '1, ' + attr1[1]
        try:
            att1_as_code = eval(attr1)
            ans.append(type(att1_as_code))
        except (SyntaxError,NameError):
            ans.append(type(attr1))

    return ans


def check_both_lines_have_same_attr(line1, attrbs):
    if len(line1) != len(attrbs): return -1
    index = 0
    for att1_raw in line1:
        att1 = att1_raw
        if att1 in ['[]\n','()\n','{}\n','[]','()','{}']:
            att1 = att1[0] + '1, ' + att1[1]
        try:
            att1_as_code = eval(att1)
            current_type = type(att1_as_code)
        except (SyntaxError,NameError):
            current_type = type(att1)
        if current_type != attrbs[index]:
            return -1
        else:
            index+=1
    return 0


def seperate(input_path, output_path1, output_path2):
    if (not (os.path.exists(input_path))):
        print('Input file not found')
        return
    input_file_name, input_file_extension = get_file_name_and_extension(input_path)

    if (input_file_extension != '.txt' and input_file_extension != '.csv'):
        print('input file is in the wrong formats')
        return

    file_by_lines = read_file_by_lines(input_path)

    if (is_file_structure_consistent(file_by_lines, input_path) == -1):
        return

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

    write_file_replace_if_exists(output_path1, file_1_lines)
    write_file_replace_if_exists(output_path2, file_2_lines)


def get_file_name_and_extension(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    return (file_name, file_extension)


def read_file_by_lines(file_path):
    with open(file_path) as f:
        lines = f.read().splitlines()

    lines = [line.strip() for line in lines if line is not None and line != ""]
    return lines


def is_file_structure_consistent(file, file_path):
    if len(file) == 0: return 0
    first_line_attrbs = get_first_line_attrbs(file[0].split("::"))
    for x in file:
        if check_both_lines_have_same_attr(x.split("::"), first_line_attrbs) == -1:
            print(file_path + ' structure is not consistent, different number of attributes')
            return -1
    return 0




def write_file_replace_if_exists(file_path, file_content): #ata king
    if file_path is None or file_path=="":
        print 'invalid output path'
        return
    if os.path.isfile(file_path):
        os.remove(file_path)
    output_file = open(file_path, "a")
    for line in file_content:
        output_file.write(line + '\n')
    output_file.close()

# seperate('out.txt', 'file1_1', 'file2_1')
# is_file_structure_consistent('out.txt')
parse_args((sys.argv))