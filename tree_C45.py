import numpy as np
import operator

'''
-------------------------------------------------------------------------------
c4.5 决策树 到createTree_c为止 为决策树代码
最终希望达到：
1、组合基本为赢家组合  
2、组内标签大部分相同，少量是别的标签（把最终的熵提出来观察一下）
3、组合间有小部分重复股票——s的设定
4、最终组间画图，用净值或是收益曲线，让组间行情看起来是分开的

原ide3决策树代码改动部分：
1、连续变量离散化：函数名带_c的都做了改变
2、设定了s，主要是根据splitDataSet_c函数，让他分得时候错位分
3、最大层高设为了4（退出条件，可改）
4、后面增加了cut_leaf减去输家组合，和getclustercode函数提取item样本，显示每组的股票
------------------------------------------------------------------------------
'''
#选择最优属性时使用（划分数据集）
def splitDataSet_a(dataSet, axis, value, LorR='L'):
    retDataSet = []
    if LorR == 'L':
        for featVec in dataSet:
            if float(featVec[axis]) < value:
                retDataSet.append(featVec)
    else:
        for featVec in dataSet:
            if float(featVec[axis]) > value:
                retDataSet.append(featVec)
    return retDataSet

#分裂左右子数时，设定一定的错位值s
def splitDataSet_c(dataSet, axis, value, s, LorR='L'):
    retDataSet = []
    if LorR == 'L':
        for featVec in dataSet:
            if float(featVec[axis]) < value*(1-s):
                retDataSet.append(featVec)
    else:
        for featVec in dataSet:
            if float(featVec[axis]) > value*(1+s):
                retDataSet.append(featVec)
    return retDataSet

#计算给定数据的熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)   #计算数据集中实例的总数
    labelCounts = {}
    for featVec in dataSet: #the the number of unique elements and their occurance
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0 
        labelCounts[currentLabel] += 1   #观察每个类别数量
    shannonEnt = 0.0
    for key in labelCounts:   #使用类别标签发生频率计算类别出现概率
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * np.math.log(prob,2) #log base 2    (l(x_i)=-log2(p(x_i)))
    return shannonEnt   #熵

# 选择最好的数据集划分方式
def chooseBestFeatureToSplit_c(dataSet, labelProperty):
    numFeatures = len(labelProperty)  # 特征数
    baseEntropy = calcShannonEnt(dataSet)  # 计算根节点的信息熵
    infoGainRatio_dict = {}
    for i in range(numFeatures):  # 对每个特征循环
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)  # 该特征包含的所有值
        newEntropy = 0.0
        if labelProperty[i] == 0:  # 对离散的特征
            for value in uniqueVals:  # 对每个特征值，划分数据集, 计算各子集的信息熵
                subDataSet = splitDataSet_a(dataSet, i, value)
                prob = len(subDataSet) / float(len(dataSet))
                newEntropy += prob * calcShannonEnt(subDataSet)
        else:  # 对连续的特征
            sortedUniqueVals = list(uniqueVals)  # 对特征值排序
            sortedUniqueVals.sort()
            #只取中间段进行划分点选取
            sortedUniqueVals = sortedUniqueVals[int(len(sortedUniqueVals)*0.4):int(len(sortedUniqueVals)*0.6)]
            maxinfoGainRatio = -np.inf
            bestPartValue = 0

            for j in range(len(sortedUniqueVals) - 1):  # 计算划分点
                partValue = (float(sortedUniqueVals[j]) + float(sortedUniqueVals[j+1])) / 2
                # 对每个划分点，计算信息熵
                dataSetLeft = splitDataSet_a(dataSet, i, partValue,'L')
                dataSetRight = splitDataSet_a(dataSet, i, partValue,'R')
                probLeft = len(dataSetLeft) / float(len(dataSet))
                probRight = len(dataSetRight) / float(len(dataSet))
                Entropy = probLeft*calcShannonEnt(dataSetLeft) + probRight*calcShannonEnt(dataSetRight)
                feature_ent = -probLeft*np.math.log(probLeft,2)-probRight*np.math.log(probRight,2)
                infoGainRatio = (baseEntropy - Entropy)/feature_ent
                if infoGainRatio > maxinfoGainRatio:
                    maxinfoGainRatio = infoGainRatio
                    bestPartValue = partValue
                infoGainRatio_dict[i] = (bestPartValue,infoGainRatio)

    sortedbestFeature = sorted(infoGainRatio_dict.items(),key=lambda x:x[-1][-1],reverse=True)
    bestFeature = sortedbestFeature[0][0]
    bestValue = sortedbestFeature[0][1][0]
    return bestFeature, bestValue

#判断数据集的各个属性集是否完全一致
def judgeEqualLabels(dataSet): 
    feature_leng = len(dataSet[0]) - 1   
    data_leng = len(dataSet)
    is_equal = True    
    for i in range(feature_leng):
        first_feature = dataSet[0][i]   
        for _ in range(1, data_leng):
            if first_feature != dataSet[_][i]:
                return False    
    return is_equal

#投票表决
def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0   #未出现过，生成一个键值对
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True) #classCount.iteritems()python3中已经没有这个属性，直接改为items
    #将字典拆为多个元祖[(‘url’, ‘value1’), (‘title’, ‘value2’)]组成的列表
    return sortedClassCount[0][0]   #返回出现次数最多的分类名称

#创建决策树
def createTree_c(item,dataSet,labels,labelProperty,s,z,min_samples_leaf,current_depth=0,max_depth=4):
    classList = [example[-1] for example in dataSet]  # 类别向量
    if classList.count(classList[0]) == len(classList):  # 如果只有一个类别，返回
        item.append(dataSet)
        # print(len(dataSet))
        return classList[0]
    if len(dataSet[0]) == 1:  # 如果所有特征都被遍历完了，返回出现次数最多的类别及类别频率
        item.append(dataSet)
        # print(len(dataSet))
        return majorityCnt(classList)   #返回出现概率最大的标签
    #规定最大深度
    if current_depth > max_depth-1:
        item.append(dataSet)
        # print(current_depth)
        return majorityCnt(classList)
    # 最小叶子节点数
    if  len(dataSet) < min_samples_leaf:
        item.append(dataSet)
        # print(len(dataSet))
        return majorityCnt(classList)
    # 组内熵下到一个阈值
    if  calcShannonEnt(dataSet) <= z:
        item.append(dataSet)
        # print(len(dataSet))
        return majorityCnt(classList)
    
    bestFeat, bestPartValue = chooseBestFeatureToSplit_c(dataSet,labelProperty)  # 最优分类特征的索引
    if bestFeat == -1:  # 如果无法选出最优分类特征，返回出现次数最多的类别
        item.append(dataSet)
        # print(len(dataSet))
        return majorityCnt(classList)

    if labelProperty[bestFeat] == 0:  # 对离散的特征
        bestFeatLabel = labels[bestFeat]
        myTree = {bestFeatLabel: {}}
        labelsNew = labels.copy()  
        labelPropertyNew = labelProperty.copy()
        del (labelsNew[bestFeat])  # 已经选择的特征不再参与分类
        del (labelPropertyNew[bestFeat])
        featValues = [example[bestFeat] for example in dataSet]
        uniqueValue = set(featValues)  # 该特征包含的所有值
        for value in uniqueValue:  # 对每个特征值，递归构建树
            subLabels = labelsNew[:]
            subLabelProperty = labelPropertyNew[:]
            myTree[bestFeatLabel][value] = createTree_c(item,
                splitDataSet_a(dataSet, bestFeat, value), subLabels,
                subLabelProperty,s,z,min_samples_leaf,current_depth+1,max_depth)
    else:  # 对连续的特征，不删除该特征，分别构建左子树和右子树
        bestFeatLabel = labels[bestFeat] + '<' + str(round(bestPartValue,2))
        myTree = {bestFeatLabel: {}}
        subLabels = labels[:]
        subLabelProperty = labelProperty[:]
        # 构建左子树
        valueLeft = 'Yes'
        myTree[bestFeatLabel][valueLeft] = createTree_c(item,
            splitDataSet_c(dataSet,bestFeat,bestPartValue,s,'L'), subLabels,
            subLabelProperty,s,z,min_samples_leaf,current_depth+1,max_depth)
        # 构建右子树
        valueRight = 'No'
        myTree[bestFeatLabel][valueRight] = createTree_c(item,
            splitDataSet_c(dataSet,bestFeat,bestPartValue,s,'R'), subLabels,
            subLabelProperty,s,z,min_samples_leaf,current_depth+1,max_depth)
    return myTree

#为确保为赢家组合，将所分类别(portfolio)中标签(例如class=6/7/8/9/10)出现最多(即垃圾组合)的组合剔除
def cut_leaf(item,value):
    item_label=[]
    for dataSet in item[:]:
        classList=[example[-1] for example in dataSet]  # 类别向量
        classCount={}
        for vote in classList:
            if vote not in classCount.keys(): classCount[vote] = 0   #未出现过，生成一个键值对
            classCount[vote] += 1
        sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True) #classCount.iteritems()python3中已经没有这个属性，直接改为items
        item_label.append(sortedClassCount[0][0])
    m = find_all_index(item_label,value)  #查找出现value最多的组合在item中的位置
    for j in m[::-1]:
        del item[j]
    return item

def find_all_index(arr,value):  #找到满足list中某个固定值的所有位置
    return [i for i,a in enumerate(arr) if a==value]

#获取完成分类后的每类股票代码
def getclustercode(codedata,mydat,item):    
    cluster=[]
    for i in item:
        evecluster=[]
        for j in i:
            evecluster.append(codedata[mydat.index(j)])
        cluster.append(evecluster)
    return cluster