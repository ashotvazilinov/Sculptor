l1 = [2,4,3]
l2 = [5,6,4]
x = l2[0]

# print(len(l1))
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
# class Solution(object):
#     def addTwoNumbers(self, l1, l2):
#         # l1 = l1[::-1]
#         # l2 = l2[::-1]
#         is_more_than_ten_old = 0
#         is_more_than_ten_new = 0
#         new = []
#         if len(l1) > len(l2):
#             x = len(l1)
#             y = len(l1) - len(l2)
#             for j in range(y):
#                 l2.append(0)
#         else:
#             x = len(l2)
#             y = len(l2) - len(l1)
#             for j in range(y):
#                 l1.append(0)
#         for i in range(x):
#             if is_more_than_ten_new == is_more_than_ten_old:
#                 print('equal')
#                 is_more_than_ten_new = is_more_than_ten_old
#                 z = l1[i] + l2[i]
#                 if z >= 10:
#                     is_more_than_ten_new = is_more_than_ten_old + 1
#                     z -= 10
#                 new.insert(0, z)
#             else:
#                 print('not equal')
#                 is_more_than_ten_new = is_more_than_ten_old
#                 z = (l1[i] + l2[i]) + 1
#                 if z >= 10:
#                     is_more_than_ten_new = is_more_than_ten_old + 1
#                     z -= 10
#                 new.insert(0, z)
#                 # print(is_more_than_ten_new)
#                 # print(is_more_than_ten_old)
#                 # print(z)
        
#         return new[::-1]


# result = Solution().addTwoNumbers([9,9,9,9,9,9,9], [9,9,9,9])
# print(result)
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        # l1 = l1[::-1]
        # l2 = l2[::-1]
        # print(l1, l2)
        new = 0
        Z1 = 0
        Z2 = 0
        if len(l1) > len(l2):
            x = len(l1)
            y = len(l1) - len(l2)
            for j in range(y):
                l2.append(0)
        else:
            x = len(l2)
            y = len(l2) - len(l1)
            for j in range(y):
                l1.append(0)
        for i in range(x):
            z1 = l1[i]*10**i
            Z1 = Z1 + z1
            z2 = l2[i]*10**i
            Z2 = Z2 + z2
        not_new = (Z1 + Z2)
        conver_not_new_to_str = str(not_new)[::-1]
        i = []
        k = 0
        for j in conver_not_new_to_str:
            k = int(j)
            i.append(k)
        new = i
        return new


result = Solution().addTwoNumbers([9,9,9,9,9,9,9], [9,9,9])
print(result)