import random

range_min = 0
range_max = 1000000

def ptr(): # Fake pointers
    return random.randint(0, range_max)

class Node:
    def __init__(self, data, link) -> None:
        self.data = data
        self.link = link

    def move(self, otheraddr):
        return self.link ^ otheraddr


class LList:

    def __init__(self, data=()):
        self.llist = {}
        self.headprev = ptr()
        self.headptr = ptr()

        self.tailptr = ptr()
        self.tailnext = ptr()
        
        self.head = Node(data="Head", link=self.headprev ^ self.tailptr)
        self.llist[self.headptr] = self.head

        self.tail = Node(data="Tail", link=self.headptr ^ self.tailnext)
        self.llist[self.tailptr] = self.tail
        
        for d in data:
            self.insert(d)


    def insert(self, data, to="tail"):
        if to=="tail":
            startptr = self.tailptr
            endp = self.tailnext
        elif to=="head":
            startptr = self.headptr
            endp = self.headprev
        else:
            print("Can only insert to head or tail")
            return
        
        startnode = self.llist.get(startptr)

        nextptr = startnode.link ^ endp
        nextlink = self.llist.get(nextptr).link

        new = Node(data=data, link=startptr ^ nextptr)
        newptr = ptr()
        self.llist[newptr] = new

        self.llist.get(startptr).link = endp ^ newptr
        self.llist.get(nextptr).link = nextlink ^ startptr ^ newptr

    
    def remove(self, data):
        prevptr = self.headptr
        currptr = self.llist.get(prevptr).link ^ self.headprev
        currnode = self.llist.get(currptr)

        while (currnode.data != "Tail"):
            print(currnode.data)
            nextptr = currnode.link ^ prevptr
            nextnode = self.llist.get(nextptr)
            print(nextnode.data)

            if currnode.data == data:
                prevnode = self.llist.get(prevptr)

                prevnode.link = prevnode.link ^ currptr ^ nextptr
                nextnode.link = nextnode.link ^ currptr ^ prevptr

                del self.llist[currptr]
                print("Found and Deleted")
                break
            else:
                prevptr = currptr
            
            currptr = nextptr
            currnode = nextnode

            print(f"{prevptr}, {currptr}, {nextptr}")
        
        print("Nothing there")



    def __iter__(self):
        self.__currptr = self.headptr
        self.__prevptr = self.headprev
        return self

    def __next__(self):
        prevptr = self.__currptr
        prevnode = self.llist.get(prevptr)
        currptr = prevnode.link ^ self.__prevptr

        currnode = self.llist.get(currptr)

        if currnode.data == "Tail":
            raise StopIteration
        
        self.__currptr = currptr
        self.__prevptr = prevptr

        return currnode.data
    

test_data=tuple(i for i in range(0,10))

llist = LList(data=test_data)

for d in llist:
    print(d)

llist.remove(5)
llist.remove(0)
llist.remove(9)
llist.insert(12, to="head")
llist.insert(9)
llist.insert(10, to="head")
llist.remove(12)

for d in llist:
    print(d)
