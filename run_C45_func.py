import pandas as pd
from tree_C45 import createTree_c  #在同一文件夹且注意工作路径
from tree_C45 import cut_leaf
from tree_C45 import getclustercode

def get_cluster(date):
    factor=pd.read_excel("F:/JetBrains/PyCharm 2018.2.4/files/一、数据和因子提取/factor_hs300/new2/factor_hs300_{}.xlsx".format(date),index_col='index')
    factor.dropna(axis=0, inplace=True)
    for j in list(factor.columns)[:-1]:
        factor.loc[:, j] = (factor.loc[:, j]-factor.loc[:, j].mean())/factor.loc[:, j].std()
    mydata = [factor.loc[k, :].round(2).tolist() for k in factor.index]

    labels = list(factor.columns[0:-1])  # 也可根据columns设，为简化
    labelProperty = [1] * len(labels)
    item = []
    mytree = createTree_c(item, mydata, labels, labelProperty, s=0.08, z=1.1, min_samples_leaf=18, max_depth=8)

    item=cut_leaf(item, value=10.0)
    item=cut_leaf(item, value=9.0) #item为每组样本详情
    item=cut_leaf(item, value=8.0) #item为每组样本详情

    codedata = factor.index.tolist()
    cluster = getclustercode(codedata, mydata, item)   #获得分类，每一类显示股票代码
    return cluster
