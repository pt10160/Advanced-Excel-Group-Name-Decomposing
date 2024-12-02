# By Zeqi Lai #v1.2.1
#紧急修复V1.2的输出语法错误
#基于SOMEIP_CMX_ADC_MCU_.xlsx表格的DataTypeDefinition页
#自动化寻址脚本，用于解开成员的嵌套关系，输出完整成员名
#并输出检查用.txt文件，print用.txt文件，if的条件用.txt文件    
#1.2新增功能：可以识别ARRAY类型的成员，输出头尾的成员名
#1.2新增功能：可以识别FLOAT类型的成员，输出赋值文件
#请不要删除原有被调用函数，以免影响脚本的其他部分
import xlrd
import tkinter 
from tkinter import filedialog
import fileinput

##########################################################################
#使用方法： 
#直接点击运行
#弹窗选择表格
#输入起始值
#输出三个文件
#输出文件位置默认为脚本所在文件夹
#在VSCODE中选择文件夹的话，可以将脚本输出到选择的文件夹中
##########################################################################
#被调用函数
##########################################################################

# A function gives "" to every string in a list
def add_quotation(strings):
    processed_strings = []
    for string in strings:
        processed_string = string
        processed_string = processed_string.replace(string, '"' + string + '"')
        processed_strings.append(processed_string)
    return processed_strings
# A function gives "" to every string in a list
def remove_after_equal(strings):
    processed_strings = []
    for string in strings:
        processed_string = string
        processed_string = processed_string.replace(string, string.split('=')[0])
        processed_strings.append(processed_string)
    return processed_strings
# A function merge two list of string by adding each corresponding string, with comma seperate
def merge_two_list(list1, list2):
    merged_list = []
    for i in range(len(list1)):
        merged_list.append(list1[i] + ',' + list2[i])
    return merged_list
#Alternative function for merge_two_list
def m_t2(list1, list2):
    merged_list = []
    for i in range(len(list1)):
        merged_list.append(list1[i] + ' ' + list2[i])
    return merged_list
# A function gives PRINT() to every string in a list
def add_print(strings):
    processed_strings = []
    for string in strings:
        processed_string = string
        processed_string = processed_string.replace(string, 'PRINT(' + string + '); ')
        processed_strings.append(processed_string)
    return processed_strings
# A function add ==1,/n to the end of every string in a list
def add_equal(strings):
    processed_strings = []
    for string in strings:
        processed_string = string
        processed_string = processed_string.replace(string, string + '==1,')
        processed_strings.append(processed_string)
    return processed_strings
# identifier V0.9alpha 等待更新为列表式而非枚举法
def process_strings(strings):
    processed_strings = []
    dtype = r'= %d \n'
    ftype = r'= %f \n'
    replacements = {
        '.se:uint8': dtype,
        '.se:uint16': dtype,
        '.se:uint32': dtype,
        '.se:uint64': dtype,
        '.se:boolean': dtype,
        '.se:float': ftype,
        '.se:double': ftype,
    }
    for string in strings:
        processed_string = string
        for key, value in replacements.items():
            processed_string = processed_string.replace(key, value)
        processed_strings.append(processed_string)
    return processed_strings
# identifier V0.9beta 更改为if条件内嵌输出语句
def p_s2(strings):
    processed_strings = []
    dtype = r' == 1'
    ftype = r' < 1.01 '
    replacements = {
        '.se:uint8': dtype,
        '.se:uint16': dtype,
        '.se:uint32': dtype,
        '.se:uint64': dtype,
        '.se:boolean': dtype,
        '.se:float': ftype,
        '.se:double': ftype,
    }
    for string in strings:
        processed_string = string
        for key, value in replacements.items():
            processed_string = processed_string.replace(key, value)
        processed_strings.append(processed_string)
    return processed_strings
#赋值专用PS3
def p_s3(strings):
    processed_strings = []
    dtype = r' = 1;'
    ftype = r' = 1.0;'
    replacements = {
        '.se:uint8': dtype,
        '.se:uint16': dtype,
        '.se:uint32': dtype,
        '.se:uint64': dtype,
        '.se:boolean': dtype,
        '.se:float': ftype,
        '.se:double': ftype,
    }
    for string in strings:
        processed_string = string
        for key, value in replacements.items():
            processed_string = processed_string.replace(key, value)
        processed_strings.append(processed_string)
    return processed_strings


# A function gives () && to every string in a list
def a_p2(strings):
    processed_strings = []
    for string in strings:
        processed_string = string
        processed_string = processed_string.replace(string, '(' + string + ') &&')
        processed_strings.append(processed_string)
    return processed_strings

#a function add 1.1>  to the start while detected float, others don't change
def add_float(strings):
    processed_strings = []
    for string in strings:
        if '.se:float' in string:
            newstring = string.replace('.se:float',') && (')
            processed_string = '0.99 < ' + newstring + string
        elif '.se:double' in string:
            newstring = string.replace('.se:double',') && (')
            processed_string = '0.99 < ' + newstring + string
        else:
            processed_string = string
        processed_strings.append(processed_string)
    return processed_strings
#base on the start_value, edit the output file name
def edit_output_file_name(start_value):
    output_name = '检查用' + start_value + '.txt'
    output_preif_name = start_value + '_preif.txt'
    output_print_name = start_value + '_print.txt'
    output_number_name = start_value + '_赋值.txt'
    return output_name, output_preif_name, output_print_name, output_number_name


##########################################################################
#主函数区域
##########################################################################

# 弹窗选择文件，默认为读取‘DataTypeDefinition’页表
def make_it_work():
    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    print(file_path)
    filename = file_path
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_name('DataTypeDefinition')
    return sheet

# 矩阵化页表     
def sheet_2D(sheet):
    sheet2D = []
    for row in range(sheet.nrows):
        cell_value = sheet.cell_value(row, 0)    # 获取第一列的值
        if cell_value != '':                     # 判断第一列是否为空
            row_data = []                        # 跳过第一列是否为空的行（有数列长度bug故增加此功能）
            for col in range(10):                # 仅迭代前10列
                cell_value = sheet.cell_value(row, col)
                row_data.append(cell_value)
            sheet2D.append(row_data)
    return sheet2D

#写入至文件，默认格式txt
def write_to_file(output_file, paths):
    with open(output_file, "w") as file:
        for path in paths:
            file.write(path)
            file.write("\n")

# 寻址并根据特定需求输出（成员名）(带有输出起始array功能)（V1.0A）
def find_paths_initial(matrix, start_value):
    stack = []
    addresses = []

    # Find rows with first item equal to start_value
    for row in matrix:
        if row[0] == start_value:
            stack.append((row, []))

    # Traverse the matrix using stack
    while stack:
        current_row, path = stack.pop()
        if current_row[8].startswith('Array_'):
            current_row[6] = current_row[6]+'[0]'
        path.append(str(current_row[6]))

        if current_row[8]:
            target_value = current_row[8]
            
            for row in matrix:
                if row[0] == target_value:
                    stack.append((row, path.copy()))
                    
        # attach the recognition sylabol to the end of path, using data type here
        else:
            last_target_value = '.se:' + current_row[9]
            path.append(str(last_target_value))
            address = '.'.join([str(start_value)] + path)
            cleaned_address = clean_address(address)
            cleaned_address = cleaned_address.replace('.[', '[')
            addresses.append(cleaned_address)

    return addresses

# 寻址并根据特定需求输出（成员名）(带有输出末尾array功能)（V1.0B）
def find_paths_ending(matrix, start_value):
    stackee = []
    addressee = []

    # Find rows with first item equal to start_value
    for row in matrix:
        if row[0] == start_value:
            stackee.append((row, []))

    # Traverse the matrix using stack
    while stackee:
        current_row, path = stackee.pop()
        path.append(str(current_row[6]))

        if current_row[8]:
            target_value = current_row[8]
            
            for row in matrix:

                if row[0] == target_value and row[0].startswith('Array_'):
                    value = str(int(row[5])-1)
                    path.append('['+value+']') 

                if row[0] == target_value:
                    stackee.append((row, path.copy()))
                    
        # attach the recognition sylabol to the end of path, using data type here
        else:
            last_target_value = '.se:' + current_row[9]
            path.append(str(last_target_value))
            address = '.'.join([str(start_value)] + path)
            cleaned_address = clean_address(address)
            cleaned_address = cleaned_address.replace('.[', '[')
            addressee.append(cleaned_address)
 
    return addressee

def find_paths(matrix, start_value):
    list2 = find_paths_ending(matrix, start_value)
    list1 = find_paths_initial(matrix, start_value)
    
    list3 = list1 + list2
    return list3

# 交换双点（find_paths函数中使用）
def clean_address(address):
    parts = address.split('.')
    cleaned_parts = []

    for i, part in enumerate(parts):
        if i == 0 or part != '':
            cleaned_parts.append(part)

    cleaned_address = '.'.join(cleaned_parts)
    return cleaned_address

def remove_duplicate_lines(file_path):
    lines_seen = set()  # 用于存储已经出现过的行
    output_lines = []  # 用于存储不重复的行

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # 去除行首行尾的空白字符
            if line not in lines_seen:
                lines_seen.add(line)
                output_lines.append(line)

    with open(file_path, 'w') as file:
        file.write('\n'.join(output_lines))

   
# Print条件输出语句
def out_with_print(input):
    out_with_ident = process_strings(input)
    out_with_nothing = remove_after_equal(out_with_ident)
    out_with_quotation = add_quotation(out_with_ident)
    out_with_merged = merge_two_list(out_with_quotation, out_with_nothing)
    out_with_print = add_print(out_with_merged)
    return out_with_print

# If条件内嵌输出语句
def out_with_preif(input):
    out_with_099 = add_float(input) #0.99 < float
    out_with_101 = p_s2(out_with_099) # == 1  or < 1.01
    # out_withat = merge_two_list(out_with_099, out_with_101)

    out_with_brace = a_p2(out_with_101) #() &&
    #return out_with_brace
    return out_with_brace

def out_with_number(input):
    out_with_number = p_s3(input)
    return out_with_number

# 编辑.c头文件 (功能未加入)
def edit_c_file(file_path, function_name, code_to_add):
    with fileinput.FileInput(file_path, inplace=True, backup='.bak') as file:
        for line in file:
            if function_name in line:
                print(line, end='')
                print(code_to_add)
            else:
                print(line, end='')
        # Usage: based on the file path, find the function name and input the whole function
        # expected debug process: add function of output to .txt file for a check

##########################################################################                                                              
                                                                      
#运行区域     
excel_choice = sheet_2D(make_it_work())                                                             
start_value = input('please inseart type name \n')  # 指定的起始值     
output, output_preif, output_print, output_number = edit_output_file_name(start_value)        
filtered = find_paths(excel_choice, start_value)             
outputprint = out_with_print(filtered)       
outputpreif = out_with_preif(filtered)
outputnumber = out_with_number(filtered)                             
write_to_file(output_print, outputprint)                                       
write_to_file(output_preif, outputpreif) 
write_to_file(output, filtered)
write_to_file(output_number, outputnumber)                                      
remove_duplicate_lines(output)
remove_duplicate_lines(output_preif)
remove_duplicate_lines(output_print)
remove_duplicate_lines(output_number)
