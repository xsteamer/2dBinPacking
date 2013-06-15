# BoxPlacer.DrawContainer() is the only function that uses the pygame module
import pygame as pg
import sys
import random as rn
import copy

class BoxClass():
    def __init__(self,w,h):
        self.x = None
        self.y = None
        self.w = w
        self.h = h
        self.area = w*h

class ContainerClass():
    def __init__(self,w,h,x,y,idN):
        self.w = w
        self.h = h
        self.area = w*h
        self.x = x
        self.y = y
        self.id = idN
        self.placedBoxes = []
        self.sliceTree = [{'w': w, 'h': h, 'x': x, 'y': y, 'A':w*h}]

class BoxPlacer():
    def __init__(self):
        self.list = []
        self.contId = 0
        self.containers = []
        self.thrownOut = []    

    def AddBox(self,w,h):
        self.list.append(BoxClass(w,h))

    def AddContainer(self,w,h):
        y = 0
        widthUsed = 0;
        for cont in self.containers:
            widthUsed += cont.w
        self.containers.append(ContainerClass(w,h,widthUsed,y,self.contId))
        self.contId += 1

    def SortDecArea(self):
        self.sortedList = sorted(self.list, key=lambda box: box.area, reverse=True)
        self.list = self.sortedList

    def StandardFit(self,box,cont):
        sliceDims = cont.sliceTree
        for index,dims in enumerate(sliceDims):
            #print "empty space:",index
            if (box.h <= dims['h'] and box.w <= dims['w']):
                boxPlaced = self.StandardGuillotine(box,cont,sliceDims,index,dims)
                if boxPlaced is True:
                    break
            elif (box.w <= dims['h'] and box.h <= dims['w']):
                box.w, box.h = box.h, box.w # rotate box
                boxPlaced = self.StandardGuillotine(box,cont,sliceDims,index,dims)
                if boxPlaced is True:
                    break
            else:
                boxPlaced = False
                #print "doesn't fit
        return boxPlaced

    def StandardGuillotine(self,box,cont,sliceDims,index,dims):
        box.x = dims['x']
        box.y = dims['y']
        cont.placedBoxes.append(box)
        #print "fits!"
        # remove old rectangle
        sliceDims.pop(index)

        if splitStrat is 7:
            strat = rn.randint(1,2)
        else:
            strat = splitStrat

        # Horizontal Split
        # make new rectangle with same width of old rectangle on top of newly placed box
        slice1 = {'w': dims['w'], 'h': dims['h'] - box.h, 'x': dims['x'], 'y': dims['y'] + box.h}
        slice1['A'] = slice1['w']*slice1['h']
        # make new rectangle with same height as newly placed box to the side of newly placed box
        slice2 = {'w': dims['w'] - box.w, 'h': box.h, 'x': dims['x'] + box.w, 'y': dims['y']}
        slice2['A'] = slice2['w']*slice2['h']
        # Vertical Split
        slice3 = {'w': box.w, 'h': dims['h'] - box.h, 'x': dims['x'], 'y': dims['y'] + box.h}
        slice3['A'] = slice1['w']*slice1['h']
        slice4 = {'w': dims['w'] - box.w, 'h': dims['h'], 'x': dims['x'] + box.w, 'y': dims['y']}
        slice4['A'] = slice2['w']*slice2['h']
        
        if strat is 1:
            # Horizontal Split
            used1 = slice1
            used2 = slice2
        elif strat is 2:
            # Vertical Split
            used1 = slice3
            used2 = slice4
        elif strat is 3:
            if dims['w'] < dims['h']:
                used1 = slice1
                used2 = slice2
            else:
                used1 = slice3
                used2 = slice4
        elif strat is 4:
            if dims['w'] > dims['h']:
                used1 = slice3
                used2 = slice4
            else:
                used1 = slice1
                used2 = slice2
        elif strat is 5:
            if dims['w']-box.w < dims['h']-box.h:
                used1 = slice1
                used2 = slice2
            else:
                used1 = slice3
                used2 = slice4
        elif strat is 6:
            if dims['w']-box.w > dims['h']-box.h:
                used1 = slice3
                used2 = slice4
            else:
                used1 = slice1
                used2 = slice2  
        
        if not (used1['w'] is 0 or used1['h'] is 0):
            sliceDims.insert(index,used1)
        if not (used2['w'] is 0 or used2['h'] is 0):
            sliceDims.insert(index,used2)
        return True

    def SmallestAreaFit(self,box,cont):
        cont.sliceTree = sorted(cont.sliceTree, key=lambda s: s['A'])
        sliceDims = cont.sliceTree
        for index,dims in enumerate(sliceDims):
            if (box.h <= dims['h'] and box.w <= dims['w']):
                boxPlaced = self.StandardGuillotine(box,cont,sliceDims,index,dims)
                if boxPlaced is True:
                    break
            elif (box.w <= dims['h'] and box.h <= dims['w']):
                box.w, box.h = box.h, box.w # rotate box
                boxPlaced = self.StandardGuillotine(box,cont,sliceDims,index,dims)
                if boxPlaced is True:
                    break
            else:
                boxPlaced = False
                #print "doesn't fit
        return boxPlaced

    def LargestAreaFit(self,box,cont):
        cont.sliceTree = sorted(cont.sliceTree, key=lambda s: s['A'], reverse=True)
        sliceDims = cont.sliceTree
        for index,dims in enumerate(sliceDims):
            if (box.h <= dims['h'] and box.w <= dims['w']):
                boxPlaced = self.StandardGuillotine(box,cont,sliceDims,index,dims)
                if boxPlaced is True:
                    break
            elif (box.w <= dims['h'] and box.h <= dims['w']):
                box.w, box.h = box.h, box.w # rotate box
                boxPlaced = self.StandardGuillotine(box,cont,sliceDims,index,dims)
                if boxPlaced is True:
                    break
            else:
                boxPlaced = False
                #print "doesn't fit
        return boxPlaced

    def Place(self,strat=0):
        boxPlaced = False
        box = self.list.pop(0)
        for cont in self.containers:
            if strat == 2:
                boxPlaced = self.SmallestAreaFit(box,cont)
            elif strat == 3:
                boxPlaced = self.LargestAreaFit(box,cont)
            else:
                boxPlaced = self.StandardFit(box,cont)
            if boxPlaced is True:
                break
            
        if boxPlaced is False:
            self.thrownOut.append(box)

    def ViewUnplaced(self):
        if len(self.list) is not 0:
            print "Unplaced"
            for box in self.list:
                print "w:",box.w,"h:",box.h

    def ViewContainers(self):
        for cont in self.containers:
            print "container:",cont.id
            if len(cont.placedBoxes) is not 0:
                print "Placed"
                for box in cont.placedBoxes:
                    print "w:",box.w,"h:",box.h,"@ (",box.x,",",box.y,")"
            if len(cont.sliceTree) is not 0:
                print "Empty Spaces"
                for rect in cont.sliceTree:
                    print "w:",rect['w'],"h:",rect['h'],"@ (",rect['x'],",",rect['y'],")"

    def ViewThrownOut(self):
        if len(self.thrownOut) is not 0:
            print "Thrown Out"
            for box in self.thrownOut:
                print "w:",box.w,"h:",box.h

    def ViewList(self):
        print ""
        self.ViewUnplaced()
        self.ViewContainers()
        self.ViewThrownOut()

    def PackingFactor(self):
        totalAreaConts = 0
        totalAreaBoxes = 0
        totalAreaEmpty = 0
        for cont in self.containers:
            totalAreaConts += cont.area
            for box in cont.placedBoxes:
                totalAreaBoxes += box.area
            for rect in cont.sliceTree:
                totalAreaEmpty += (rect['w']*rect['h'])
        for box in self.thrownOut:
            totalAreaBoxes += box.area

    def DrawContainer(self):
        widthUsed = 0
        maxHeight = 0
        for cont in self.containers:
            widthUsed += cont.w
            if cont.h > maxHeight:
                maxHeight = cont.h
        maxDim = max([widthUsed,maxHeight])
        scale = 1000.0/maxDim
        window = pg.display.set_mode((int(widthUsed*scale),int(maxHeight*scale)))
        
        for cont in self.containers:
            for box in cont.placedBoxes:
                pg.draw.rect(window, (255,255,255), (box.x*scale,box.y*scale,box.w*scale,box.h*scale), 1)
            for rect in cont.sliceTree:
                pg.draw.rect(window, (0,0,255), (rect['x']*scale,rect['y']*scale,rect['w']*scale,rect['h']*scale), 0)

            pg.draw.rect(window, (0,255,0), (cont.x*scale,cont.y*scale,cont.w*scale,cont.h*scale), 1)

        pg.display.flip()

        pg.time.wait(2000)



        

boxes = BoxPlacer()
for i in range(200):
    r1 = rn.randint(5,25)
    r2 = rn.randint(5,25)
    boxes.AddBox(r1,r2)
    
boxes.SortDecArea()
boxes.AddContainer(100,160)
boxes.AddContainer(100,160)
boxes.AddContainer(100,160)
boxes.AddContainer(100,160)
boxes.AddContainer(100,160)


boxesArray = [boxes]
for i in range(1,21):
    boxesArray.insert(i,copy.deepcopy(boxes))

splitStrat = 1
while len(boxes.list) is not 0:
    boxes.Place()
while len(boxes2.list) is not 0:
    boxes2.Place(2)
while len(boxes3.list) is not 0:
    boxes3.Place(3)

splitStrat = 2
while len(boxes4.list) is not 0:
    boxes4.Place()
while len(boxes5.list) is not 0:
    boxes5.Place(2)
while len(boxes6.list) is not 0:
    boxes6.Place(3)

splitStrat = 3
while len(boxes7.list) is not 0:
    boxes7.Place()
while len(boxes8.list) is not 0:
    boxes8.Place(2)
while len(boxes9.list) is not 0:
    boxes9.Place(3)

splitStrat = 4
while len(boxes10.list) is not 0:
    boxes10.Place()
while len(boxes11.list) is not 0:
    boxes11.Place(2)
while len(boxes12.list) is not 0:
    boxes12.Place(3)

splitStrat = 5
while len(boxes13.list) is not 0:
    boxes13.Place()
while len(boxes14.list) is not 0:
    boxes14.Place(2)
while len(boxes15.list) is not 0:
    boxes15.Place(3)

#strat 2, splitStrat 3 seems optimal

##boxes.ViewList()
##boxes2.ViewList()
##boxes3.ViewList()
boxes.DrawContainer()
boxes2.DrawContainer()
boxes3.DrawContainer()
boxes4.DrawContainer()
boxes5.DrawContainer()
boxes6.DrawContainer()
boxes7.DrawContainer()
boxes8.DrawContainer()
boxes9.DrawContainer()
boxes10.DrawContainer()
boxes11.DrawContainer()
boxes12.DrawContainer()
boxes13.DrawContainer()
boxes14.DrawContainer()
boxes15.DrawContainer()

while True:
    for event in pg.event.get(): 
        if event.type == pg.QUIT: 
            sys.exit(0)
        else:
            pass
            #print event

