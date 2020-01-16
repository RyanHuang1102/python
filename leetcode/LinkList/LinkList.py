#!/usr/bin/python
class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        return

class SingleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_list_item(self, item):
        if not isinstance(item, ListNode):
            item = ListNode(item)
        if self.head is None: #initial
            self.head = item
        else:
            self.tail.next = item #next

        self.tail = item #replace old item
        return self.head

    def list_length(self, head):
        length = 0
        current_node = head
        while current_node is not None:
            length += 1
            current_node = current_node.next
        return length

    def print_list(self, head):
        linklist = []
        current_node = head
        while current_node is not None:
            linklist.append(current_node.data)
            current_node = current_node.next
        print linklist
        return

    #206. Reverse Linked List(easy):
    def reverseList(self, head):
        prev = None
        while head is not None:
            curr = head
            head = head.next
            curr.next = prev
            prev = curr

        return prev # prev finally brcomes head

    #328. Odd Even Linked List(medium):
    def oddEvenList(self, head):
        if head:
            odd = head
            even = evenHead = odd.next
            while even and even.next:
                odd.next = odd = even.next
                even.next = even = odd.next
            odd.next = evenHead

            return head
    #876. Middle of the Linked List(easy):
    def middleNode(sef, head):
        slow = fast = head
        while fast and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
        return slow


        
List = SingleLinkedList()
List.add_list_item(2)
List.add_list_item(1)
List.add_list_item(3)
List.add_list_item(5)
List.add_list_item(6)
List.add_list_item(4)
head=List.add_list_item(7)

List.print_list(head)

"""
    206. Reverse Linked List(easy):
head = List.reverseList(head)
List.print_list(head)
"""

"""
    328. Odd Even Linked List(medium):
List.oddEvenList(head)
List.print_list(head)
"""

"""
    876. Middle of the Linked List(easy):
slow = List.middleNode(head)
List.print_list(slow)
"""
