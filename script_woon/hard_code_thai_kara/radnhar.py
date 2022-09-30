UNIT_DICT = {
	"1": "nueng",
	"2": "sorng",
	"3": "sarm",
	"4": "see",
	"5": "har",
	"6": "hok",
	"7": "jed",
	"8": "paed",
	"9": "gao",
	"0": "soon",
}

POSITION =  ["saen", "muen", "pun", "roi", "sib", ""]


def number_to_string_list(number):
	number_str = str(number)
	number_str_ls = list(number_str)
	return number_str_ls

'''
takes input of an integer between 0-999999 and output thai-karaoke text 
'''
def mega_int_to_thai(num: int):
    if num == 0:
        return "soon"

    number_str_ls = number_to_string_list(num)  # list max lenght == 6
    output = []
    position_counter = 6
    for i in range(len(number_str_ls) - 1, -1, -1): # looping the string list in reversed
        number = number_str_ls[i]
        number_length = len(number_str_ls)
        position_counter -= 1
        if number == "0":
            continue

        output.append(POSITION[position_counter])
        if i == number_length - 2 and number == "2": # deal with 20s
           output.append("yee")
        elif i == number_length - 2 and number == "1": # deal with 10s
           output.append("")
        elif i == number_length - 1 and number == "1" and number_length >= 2:
            if number_str_ls[i-1] == "0":
                output.append(UNIT_DICT[number])
            else:
                output.append("ed")
        else:
            output.append(UNIT_DICT[number])

    output.reverse()
    return ''.join(output)


'''
takes a number and outputs a 2d array
where each element is length == 6 except for first elem
'''
def number_to_mega_list(num: int):
    number_str_ls = number_to_string_list(num)
    num_init = len(number_str_ls) % 6
    init_ls = number_str_ls[:num_init]
    slice_ls = number_str_ls[num_init:]
    end_ls = [slice_ls[i:i+6] for i in range(0, len(slice_ls), 6)]
    joined_ls = [init_ls] + end_ls
    output_ls = list()
    for ls in joined_ls:
        if len(ls) != 0:
            output_ls.append(int(''.join(ls)))
    return output_ls

def any_int_to_thai(num: int):
    mega_ls = number_to_mega_list(num)
    output = ''
    for i in range(len(mega_ls)):
        input = mega_ls[i]
        output += mega_int_to_thai(input)
        if i != len(mega_ls) - 1:
            output += 'larn'
    return output

def literal_translation(num: str):
	number_str_ls = list(num)
	output = list()
	for num in number_str_ls:
		output.append(UNIT_DICT[num])
	return ''.join(output)

def float_to_thai(number):
	if type(number) is int:
		return any_int_to_thai(number)
	else:
		number_str_ls = number_to_string_list(number)
		position = number_str_ls.index(".")
		int_part, float_part = int(''.join(number_str_ls[:position])), ''.join(number_str_ls[position+1:])
		float_output = any_int_to_thai(int_part) + "jood" + literal_translation(float_part)
		return float_output

if __name__ == '__main__':
    inputs = 534456205.1598415
    print(inputs)
    print(float_to_thai(inputs))