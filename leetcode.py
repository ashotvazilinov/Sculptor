# l1 = [2,4,3]
# l2 = [5,6,4]
# x = l2[0]


class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
a = ListNode(2)
b = ListNode(4)
c = ListNode(3)
a.next = b
b.next = c
d = ListNode(5)
e = ListNode(6)
f = ListNode(4)
d.next = e
e.next = f
l1 = a
l2 = d
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        # l1 = l1[::-1]
        # l2 = l2[::-1]
        # print(l1, l2)
        result_one = []
        result_two = []
        while l1:
            print(l1.val)
            to_append = l1.val
            l1 = l1.next
            result_one.append(to_append)
        l1 = result_one
        while l2: 
            print(l2.val)
            to_append = l2.val
            l2 = l2.next
            result_two.append(to_append)
        l2 = result_two
    

        target = 0
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
        i
        def make_list(arr):
            head = ListNode(arr[0])
            node = head
            for v in arr[1:]:
                node.next = ListNode(v)
                node = node.next
            return head
        target = make_list(i)
        return target
        

        

result = Solution().addTwoNumbers(a, d)
print(result)