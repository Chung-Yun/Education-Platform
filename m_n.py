area = {}
M = int(input("input m:"))
bb =0
area_list=[]

while(bb < M ):
    area_m,area_people_num  = input("input area_m:").split(' ')
    area[area_m]=int(area_people_num)
    area_list.append(area)
    bb = bb+1

want = input("input want:")
want_list = want.split(' ')
small = 100
for i in range(len(want_list)):
    print(want_list[i],"=",area[want_list[i]])
    if area[want_list[i]] <small:
        small = area[want_list[i]]
        small_name = want_list[i]
print("all= ", area_list)

print("small_name",small_name)