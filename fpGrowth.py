#!/usr/bin/env python
# -*- coding: utf-8 -*-

#FP樹中節點的類定義
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None #nodeLink 變量用於鏈接相似的元素項
        self.parent = parentNode #指向當前節點的父節點
        self.children = {} #空字典，存放節點的子節點

    def inc(self, numOccur):#計數加1
        self.count += numOccur

#將樹以文本形式顯示
    def disp(self, ind=1):
        print ('  ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)

#構建FP-tree
def createTree(dataSet, minSup=1):  #parm dataset 是 {frozenset(items) : 數量}
    headerTable = {}  # headerTable is {item : [cnt, ptr]}
    for trans in dataSet:  #第一次遍歷：統計各個數據的頻繁度  #做出headerTable  #trans是frozenset( item )
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]  #一開始是存數字 #dataSet[trans]代表item的數量
            #用頭指針表統計各個類別的出現的次數，計算頻繁量：頭指針表[類別]=出現次數
    for k in list(headerTable):  #刪除未達到最小頻繁度的數據
        if headerTable[k] < minSup:
            del (headerTable[k])
    freqItemSet = set(headerTable.keys())#保存達到要求的數據  # freqItemSet是所有符合支持度的item集合
    # print ('freqItemSet: ',freqItemSet)
    if len(freqItemSet) == 0:
        return None, None  #若達到要求的數目為0
    for k in headerTable: #遍歷頭指針表
        headerTable[k] = [headerTable[k], None]  #保存計數值及指向每種類型第一個元素項的指針 # value=[數量, ptr]
    # print ('headerTable: ',headerTable)

    retTree = treeNode('Null Set', 1, None)  #初始化tree
    for tranSet, count in dataSet.items():  # 第二次遍歷： #構成FP-tree
        localD = {}
        for item in tranSet:  # put transaction items in order
            if item in freqItemSet:#只對頻繁項集進行排序
                localD[item] = headerTable[item][0]  #localD is {item : 數量}  headerTable is {item : [數量, ptr]}

        #使用排序後的頻率項集對樹進行填充
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]  #  WATCHOUT!!!
            updateTree(orderedItems, retTree, headerTable, count)  # populate tree with ordered freq itemset
            #         (items,        inTree,  headerTable, count)
    return retTree, headerTable  #返回樹和頭指針表


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:  # 首先檢查是否存在該節點
        inTree.children[items[0]].inc(count)  # 存在則計數增加
    else:  # 不存在則將新建該節點
        inTree.children[items[0]] = treeNode(items[0], count, inTree)#創建一個新節點
        if headerTable[items[0]][1] == None:  # 若原來不存在該類別，更新頭指針列表
            headerTable[items[0]][1] = inTree.children[items[0]]#更新指向
        else:#更新指向
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:  #仍有未分配完的樹，迭代
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)

#節點鏈接指向樹中該元素項的每一個實例。
# 從頭指針表的 nodeLink 開始,一直沿著nodeLink直到到達鏈表末尾
def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def loadSimpDat():
    simpDat =  [['A', 'B', 'C', 'D'],
                ['B', 'C', 'E'],
                ['A', 'B', 'C', 'E'],
                ['B']]
    return simpDat

#createInitSet() 用於實現上述從列表到字典的類型轉換過程
def createInitSet(dataSet):  #parm dataset is list[list[]]
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict  # retDict is {frozenset() : 1}

#從FP樹中發現頻繁項集
def ascendTree(leafNode, prefixPath):  #遞歸上溯整棵樹  #prefixPath:out
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(treeNode):  #參數:節點  #return a [{frozenset() : 數量}](dataSet)
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)#尋找當前非空節點的前綴
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count  #建構排除自己的dataSet
        treeNode = treeNode.nodeLink  #相同item的旁系節點
    return condPats  #return a [{frozenset() : 數量}]

#遞歸查找頻繁項集
def mineTree(inTree, headerTable, minSup, preFix, freqItemList):  #preFix 是 set()  #freqItemList:out
    # 頭指針表中的元素項按照頻繁度排序,從小到大
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: (p[1][0]))]  #bigL是所有headerTable的item依出現次數小到大
    for basePat in bigL:  #從底層開始
        #加入頻繁項列表
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        #print ('finalFrequent Item: ',newFreqSet)
        freqItemList.append(newFreqSet)
        #遞歸調用函數來創建基
        condPattBases = findPrefixPath(headerTable[basePat][1])  #condPattBases is a dataSet 
        #print ('condPattBases :',basePat, condPattBases)

        #2. 構建條件模式Tree
        myCondTree, myHead = createTree(condPattBases, minSup)  #make a sub tree and a headerTab for basePat
        #將創建的條件基作為新的數據集添加到fp-tree
        #print ('head from conditional tree: ', myHead)
        if myHead != None and len(preFix)<4: #3. 遞歸  #terminate when the subHeaderTab(myHead) is empty
            #  len(preFix)<4 limit the recursive mineTree
            #print ('conditional tree for: ',newFreqSet)
            #myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def mineTreeP(inTree, headerTable, minSup, preFix, freqItemList):  #preFix 是 set()  #freqItemList:out [item(set), ]
    # 頭指針表中的元素項按照頻繁度排序,從小到大
    bigL = {v[0]:v[1][0] for v in sorted(headerTable.items(), key=lambda p: (p[1][0]))}  #bigL是所有headerTable的item依出現次數小到大  bigL is [(item,[cnt,ptr])]
    for basePat, baseCnt in bigL.items():  #從底層開始
        #加入頻繁項列表
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        print ('finalFrequent Item: ',newFreqSet)
        freqItemList.update({frozenset(newFreqSet):baseCnt})  #freqItemList.append(newFreqSet)
        #遞歸調用函數來創建基
        condPattBases = findPrefixPath(headerTable[basePat][1])  #condPattBases is a dataSet 
        print ('condPattBases :',basePat, condPattBases)

        #2. 構建條件模式Tree
        myCondTree, myHead = createTree(condPattBases, minSup)  #make a sub tree and a headerTab for basePat
        #將創建的條件基作為新的數據集添加到fp-tree
        print ('head from conditional tree: ', myHead)
        if myHead != None and len(preFix)<4: #3. 遞歸  #terminate when the subHeaderTab(myHead) is empty
            #  len(preFix)<4 limits the recursive mineTree
            print ('conditional tree for: ',newFreqSet)
            myCondTree.disp(1)
            mineTreeP(myCondTree, myHead, minSup, newFreqSet, freqItemList)