from collections import Counter

# my_list = [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 6]
# print(Counter(my_list))
# print(Counter(my_list).items())
# print(Counter(my_list).keys())
# print(Counter(my_list).values())

#
num_of_shoes = int(input())
ss = list(map(int, input().split()))
shoeSizes = Counter(ss)
num_of_cus = int(input())
det = []
for i in range(0, num_of_cus):
    details_of_purchase = list(map(int, input().split()))
    det.append(details_of_purchase)

# print(num_of_shoes, ss, num_of_cus, shoeSizes, det)

total_purchase = 0
det = [[2, 33], [2, 22]]
for i in det:
    if i[0] in shoeSizes and shoeSizes[i[0]] > 0:
        total_purchase += i[1]
        shoeSizes[i[0]] -= 1

print(total_purchase)
