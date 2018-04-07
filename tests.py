import unittest
import sys
from StringIO import StringIO

from Ex1 import parse_args

class MyTestCase(unittest.TestCase):
    ### arguments testing ###
    def test_zero_arguments(self):
        testargs = ['Ex1']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'No arguments accepted'

    def test_bad_command(self):
        testargs = ['Ex1', 'blabla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'unknown command'

    def test_union_bad_num_of_args(self):
        testargs = ['Ex1', 'UNION', 'bla','bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'number of parameters for command is wrong, should be 5'


    def test_union_bad_num_of_args_to_many(self):
        testargs = ['Ex1','UNION', 'bla', 'bla','bla','bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'number of parameters for command is wrong, should be 5'


    def test_like_bad_num_of_args(self):
        testargs = ['Ex1','LIKE', 'bla', 'bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'number of parameters for command is wrong, should be 5 or 6'


    def test_like_bad_num_of_args_to_much(self):
        testargs = ['Ex1','LIKE', 'bla', 'bla','bla','bla','bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'number of parameters for command is wrong, should be 5 or 6'

    ### END ###


    ### invalid input path###
    def test_invalid_path_UNION(self):
        testargs = ['Ex1','UNION', 'bla', 'bla','bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'file 1 or file 2 does not exist'


    def test_invalid_path_DISTINCT(self):
        testargs = ['Ex1','DISTINCT', 'bla', 'bla','bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'Input file not found'

    def test_invalid_path_LIKE(self):
        testargs = ['Ex1','LIKE', 'bla', 'bla','bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'Input file not found'

    def test_invalid_path_SEPERATE(self):
        testargs = ['Ex1','SEPERATE', 'bla', 'bla','bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'Input file not found'


     ### END ###


    ##UNION Tests###

    def test_union_1_empty_2_null(self):
        testargs = ['Ex1', 'UNION', r'blabla', r'files\extrafiles\emptyfile.txt', 'bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'file 1 or file 2 does not exist'

    def test_union_1_empty_2_null(self):
        testargs = ['Ex1', 'UNION', r'files\extrafiles\emptyfile.txt', r'blabla', 'bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'file 1 or file 2 does not exist'


    def test_union_1_null_2_empty(self):
        testargs = ['Ex1', 'UNION', r'blabla', r'files\extrafiles\emptyfile.txt', 'bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'file 1 or file 2 does not exist'


    def test_union_1_empty_2_csv(self):
        testargs = ['Ex1', 'UNION', r'files\extrafiles\noending', r'files\extrafiles\emptyfile.csv', 'bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'input files in the wrong formats'

    def test_union_1_txt_2_no(self):
        testargs = ['Ex1', 'UNION', r'files\extrafiles\emptyfile.csv', r'files\extrafiles\noending', 'bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'input files in the wrong formats'


    def test_union_1_txt_2_csv(self):
        testargs = ['Ex1', 'UNION', r'files\extrafiles\emptyfile.txt', r'files\extrafiles\emptyfile.csv', 'bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'files extensions should be the same'

    def test_union_1_csv_2_txt(self):
        testargs = ['Ex1', 'UNION', r'files\extrafiles\emptyfile.csv', r'files\extrafiles\emptyfile.txt', 'bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'files extensions should be the same'


    def test_union_1_empty_2_full(self):
        testargs = ['Ex1', 'UNION', r'files\extrafiles\emptyfile.txt', r'files\items.txt', 'bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'Error! The table\'s format does not match'


    def test_union_1_full_2_empty(self):
        testargs = ['Ex1', 'UNION', r'files\items.txt', r'files\extrafiles\emptyfile.txt', 'bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'Error! The table\'s format does not match'


    def test_union_users_ratings(self):
        testargs = ['Ex1', 'UNION', r'files\users.txt', r'files\ratings.txt', 'bla']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'Error! The table\'s format does not match'

    def test_union_bad_structure_1(self):
        testargs = ['Ex1', 'UNION', r'files\users.txt', r'files\extrafiles\bad_structure.txt', 'bla.txt']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'files\\extrafiles\\bad_structure.txt structure is not consistent, different number of attributes'

    def test_union_bad_structure_2(self):
        testargs = ['Ex1', 'UNION', r'files\users.txt', r'files\extrafiles\bad_structure_2.txt', 'bla.txt']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'files\\extrafiles\\bad_structure_2.txt structure is not consistent, different number of attributes'

    def test_union_bad_structure_3(self):
        testargs = ['Ex1', 'UNION', r'files\users.txt', r'files\extrafiles\bad_structure_3.txt', 'bla.txt']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'files\\extrafiles\\bad_structure_3.txt structure is not consistent, different number of attributes'

    def test_union_diffrent_types_str_int(self):
        testargs = ['Ex1', 'UNION', r'files\extrafiles\intfile1.txt', r'files\extrafiles\strfile1.txt', 'bla.txt']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'Error! The table\'s format does not match'

    def test_union_diffrent_types_str_iter(self):
        testargs = ['Ex1', 'UNION', r'files\extrafiles\iterativefile1.txt', r'files\extrafiles\strfile1.txt', 'bla.txt']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'Error! The table\'s format does not match'


    def test_union_diffrent_types_int_iter(self):
        testargs = ['Ex1', 'UNION', r'files\extrafiles\intfile1.txt', r'files\extrafiles\strfile1.txt', 'bla.txt']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)
        assert capturedOutput.buflist[0] == 'Error! The table\'s format does not match'



    def test_union(self):
        testargs = ['Ex1', 'UNION', r'files\users.txt', r'files\users (2).txt', 'union1.txt']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)

    def test_union_2(self):
        testargs = ['Ex1', 'UNION', r'files\items.txt', r'files\items (2).txt', 'union2.txt']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)

    def test_union_3(self):
        testargs = ['Ex1', 'UNION', r'files\ratings.txt', r'files\ratings (2).txt', 'union3.txt']
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        parse_args(testargs)



    ### END ###

###SEPERATE TESTS###




  ### END ###

if __name__ == '__main__':
    unittest.main()
