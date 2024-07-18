import numpy as np
import pandas as pd

# 读取数据
data = pd.read_excel(r"Y:\DeskTop\数模解压\第2讲 TOPSIS\代码和例题数据\20条河流的水质情况数据.xlsx")
# 将数据转换为numpy数组，确保数据类型正确
newdata = np.array(data)  # 尝试将数据转换为浮点数类型

# 极小化的正向化函数
def mintomax(maxx, index, x):
    for i in range(len(x)):
        x[i, index] = maxx - x[i, index]# 注意这里是 x[i, index]
    return x

# 中间型指标转换为极大型
def midtomax(midx,index,x):
    num = [ abs(midx-i)  for i in x[:,index]]
    M = max(num)
    print(f"中间型指标的M is {M}")
    for i in range(len(x)):
        x[i,index] = 1 - abs(x[i,index]-midx)/M

    return x
# 区间型转化为极大型
def intervaltomax(left,right,index,x):
    minx,maxx = min(x[:,index]),max(x[:,index])
    M = max(left-minx,maxx-right)
    print(f"区间型的M is {M}")
    for i in range(len(x)):
        if x[i,index]<left:
            x[i,index] = 1 - (left - x[i,index])/M
        else :
            if x[i,index]>right:
                x[i,index] = 1 - (x[i,index]-right)/M
            else:
                x[i,index] = 1

    return x


def standard(left, right, x):
    for i in range(right - left + 1):
        sum = np.power(np.sum(x[:, left + i]**2, axis=0),1/2)
        print(f'sum is {sum}' )
        for j in range(len(x)):
            x[j, left + i] = x[j, left + i] / sum

    return x
def score(left,right,x):
    Zmax = [max(x[:,i+left]) for i in range(right-left+1) ]
    Zmin = [min(x[:,i+left]) for i in range(right-left+1) ]
    print(f"Zmax is {Zmax}")
    print(f"Zmin is {Zmin}")
    S = [0]*20
    for i in range(len(x)):
        sum1 ,sum2 =0,0
        for j in range(right-left+1):
            sum1 += np.power(Zmax[j] - x[i,j+left],2)
            sum2 += np.power(Zmin[j] - x[i,j+left],2)
        sum1 = np.power(sum1,1/2)
        sum2 = np.power(sum2,1/2)
        S[i] =sum2/(sum1+sum2)
    return S
def normalization(x):
    sum1 = sum(x)
    for i in range(len(x)):
        x[i] = x[i]/sum1
    return x

# 应用函数
newdata = mintomax(np.max(newdata[:, 3]), 3, newdata)
print("第三列细菌数极小指标正向化结果")
print(newdata)
newdata = midtomax(7,2,newdata)
print("第二列ph值中间指标正向化")
print(newdata)
newdata = intervaltomax(10,20,4,newdata)
print("第四列植物营养物质区间指标正向化")
print(newdata)
# # 标准化
# print('标准化')
newdata = standard(1,4,newdata)
print("标准化的矩阵")
print(newdata)
# 计算得分并归一化
result = score(1,4,newdata)
result = normalization(result)
rank = [[k,v] for k, v in zip(newdata[:,0], result)]
rank = sorted(rank, key=lambda x: x[1], reverse=True)
print(rank)


