#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# datetime:2021/6/11 4:52 下午
import json
import os

startKey = "@start_h5_test"
endKey = "@end_h5_test"
originToNewDict = {'author': '管理者', 'priority': '用例等级', 'casetype': '用例类型'}
newList = ['author', 'priority', 'casetype']
newListValue = ['', '', 'unit']


def transfer(fileNameSet):
    for fileName in fileNameSet:
        print("start transfer file: " + fileName)
        myList = getOriginJsonObj(fileName)
        print("after getJsonObj: " + myList.__str__())
        if len(myList):
            # 列表不为空，则需要进行转换
            toNewText(myList, fileName)
        else:
            # 说明不存在有用的注释，继续转换下一个文件
            continue
        print("transfer file : " + fileName + "done...")
    print("transfer all files done!!!")


def getOriginJsonObj(fileName):
    file = open(fileName, "r", encoding="utf-8")
    originString = ""
    myList = []
    flag = 0
    index = 0
    # print("===originString before: " + originString)
    for line in file.readlines():
        if line.strip() == startKey:
            print("find startKey, index: " + index.__str__())
            flag = 1
            continue
        elif line.strip() == endKey:
            # 将之前保存的字符串转换为json对象，并保存在dict中
            print("find endKey, index: " + index.__str__())
            print("index: " + index.__str__() + ", originString: " + originString)
            obj = json.loads(originString)
            myList.append(obj)
            index = index + 1
            flag = 0
            originString = ""
        else:
            if flag:
                print("need transfer line: [ " + line.strip() + " ]")
                originString = originString + line.strip()
                # print("flag = " + flag.__str__() + " originString= " + originString)
            else:
                print("normal line...")
                continue
    file.close()
    return myList


def toNewText(jsonObjList, fileName):
    print("start overwrite...")
    file = open(fileName, "r", encoding="utf-8")
    listIndex = 0
    overwriteIndex = 0
    flag = 0
    allLine = []

    print("start append")
    for line in file.readlines():
        # if flag == 0:
        # starIndex = -1
        if startKey in line:
            print("find startKey, index: " + listIndex.__str__() + ", start one of overwrite...")
            flag = 1
            # 在上一行末尾增加一个*号
            starIndex = allLine[len(allLine) - 1].find("*")
            print("starIndex: " + starIndex.__str__())
            if starIndex != -1:
                strList = list(allLine[len(allLine) - 1])
                strList.insert(starIndex, "*")
                newStr = "".join(strList)
                allLine[len(allLine) - 1] = newStr
            else:
                print("[before note] not found *")

            # 复写第一行
            if newListValue[overwriteIndex] != '':
                newLine = "* @" + newList[overwriteIndex] + " " + newListValue[overwriteIndex] + "\n"
            else:
                newLine = "* @" + newList[overwriteIndex] + " " + str(jsonObjList[listIndex][originToNewDict[newList[overwriteIndex]]]) + "\n"
            # 对齐第一行注释的*号
            newLine = f'{" " * starIndex}{newLine}'
            print("listIndex: " + listIndex.__str__() + ", overwrite line: " + overwriteIndex.__str__() + ", newLine is: " + newLine + "starIndex: " + starIndex.__str__())
            allLine.append(newLine)
            overwriteIndex = overwriteIndex + 1
        elif endKey in line:
            print("find endKey, index: " + listIndex.__str__() + ", end one of overwrite...")
            listIndex = listIndex + 1
            flag = 0
            overwriteIndex = 0
        elif flag:
            if overwriteIndex < len(originToNewDict):
                # 继续复写
                if newListValue[overwriteIndex] != '':
                    newLine = "* @" + newList[overwriteIndex] + " " + newListValue[overwriteIndex] + "\n"
                else:
                    newLine = "* @" + newList[overwriteIndex] + " " + str(jsonObjList[listIndex][originToNewDict[newList[overwriteIndex]]]) + "\n"
                newLine = f'{" " * starIndex}{newLine}'
                print("listIndex: " + listIndex.__str__() + ", overwrite line: " + overwriteIndex.__str__() + ", newLine is: " + newLine + "starIndex: " + starIndex.__str__())
                allLine.append(newLine)
                overwriteIndex = overwriteIndex + 1
            else:
                print("useless line, no need keep, skip this line")
                continue
        else:
            if "*/" in line:
                # 对齐最后一行注释的*号
                allLine.append(f'{" " * starIndex}{line.strip()}' + "\n")
            else:
                print("normal line, keep this line")
                allLine.append(line)
    file.close()
    print("end append, line size:", len(allLine))

    fw = open(fileName, "w+", encoding="utf-8")
    for line in allLine:
        fw.write(line)
    print("overwrite done!!!")


def backupFile(fileNames):
    print("back up done!!!")
    return 0


def findValidFile(path, suffix=None):
    f_list = []

    def files_list(father_path):
        sub_path = os.listdir(father_path)
        # 读取父路径下全部文件或文件夹名称
        for sp in sub_path:
            full_sub_path = os.path.join(father_path, sp)
            # 生成完整子路径
            if os.path.isfile(full_sub_path):
                # 判断是否为文件
                file_name, post_name = os.path.splitext(full_sub_path)
                # 获取文件后缀名
                if len(file_name.split(".")) > 1:
                    realPostName = file_name.split(".")[1] + post_name
                else:
                    realPostName = file_name
                if realPostName == suffix:
                    f_list.append(file_name + post_name)
            else:
                # 如果是文件夹，递归调用
                files_list(full_sub_path)

    files_list(path)
    return f_list


if __name__ == '__main__':
    fileSet = findValidFile("/Users/coderlin/MIProject/experiment-api/experiment-api-python", "test.js")  # 这里的后缀名不要带.号
    print("input fileSet: " + str(fileSet))
    # 1. 将文件列表进行备份
    backupFile(fileSet)
    # 2. 逐个文件转换
    transfer(fileSet)
