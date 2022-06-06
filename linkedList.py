class Node:
    def __init__(self,Data) :
        self.Data=Data
        self.Next=None
class LinkedList:
    def __init__(self):
        self.head=None
        self.tail=None
        self.size = 0
    def addfirst(self,Data):
        newNode = Node(Data)
        if self.size == 0:
            self.head=newNode
        else:
            temp =self.head
            self.head=newNode
            self.head.Next=temp
    def display(self):
        elems= []
        curr = self.head
        while curr.Next != None:
            curr=curr.Next
            elems.append(curr)
        print(elems)


def main():
    myList = LinkedList()
    myList.addfirst(5)
    myList.addfirst(7)
    myList.addfirst(3)
    myList.display()
    print

if "__name__==__main__":
    main() 
    
            
       

    
