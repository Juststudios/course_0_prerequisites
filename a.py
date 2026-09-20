import datetime
lop = [[],[],[],[]]
inpt = ""
play =True

# class Task:
#      def __init__(self, task, id, dueDate):
#          self.id = id
#          self.task = task
#          self.dueDate = dueDate
#          self.isDue = False
#
#
# def apend(self, lop):
#     lop.append[0](self.id)
#     lop.append[1](self.task)
#     lop.append[2](self.dueDate)
#     lop.append[3](self.isDue)





def Startup():
    print("Hello User")
    print("What would you like to do today")
    print("1.Add something to my list")
    print("2. Mark Something As completed")
    print("3. View List")
    print("4. quit")


def list(lop):
    a = 0
    for x in lop:
        a+=1
        num = str(x)
        print(lop[0][a]+"."+lop[1][a])

def addToList(lop ):
    task = input("What would you like to add to the list\n")
    dueDate = input("What would you like to add to the list\n")
    isDue = False
    id = len(lop)+1
    lop[0].append(id)
    lop[1].append(task)
    lop[2].append(dueDate)
    lop[3].append(isDue)

    return lop

def removeList(lop):
    list(lop)
    rtask = int(input("What would you like to remove from the list\n")) +1
    lop[0].pop(rtask)
    lop[1].pop(rtask)
    lop[2].pop(rtask)
    lop[3].pop(rtask)

    return lop

def markd(lop):
    list(lop)

while play:
    Startup()
    try:
        inpt=int(input())
        if inpt ==1:
            lop = addToList(lop)
        elif inpt == 2:
           lop = removeList(lop)
        elif inpt==3:
           list(lop)
        elif inpt ==4:
            play =False
        else:
            print("Invalid Input")
    except ValueError:
            print("Invalid Input")


