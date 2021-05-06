s = "/FpML/header/message/"

s_list = s.split('/')
k = len(s_list)
if s_list[k-1] == '':
    print("Emplty")
    del(s_list[k-1])
#for s_name in s_list:
print(s_list)
print('/xmlns:'.join(s_list))
