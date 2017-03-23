import os
import socket
import re

#判断是否图片文件
def IsPic(path):
    p = path.lower()
    if p.endswith('.jpg') or p.endswith('.jpeg') or p.endswith('.png') or p.endswith('.bmp') or p.endswith('.gif'):
        return True
    else:
        return False

def IsVideo(path):
    p = path.lower()
    if p.endswith('.mp4') or p.endswith('.avi') or p.endswith('.mkv') or p.endswith('.wmv'):
        return True
    else:
        return False

#拼接url
def JoinUrl(us):
    url = ''
    for u in us:
        url = url.strip('\\') + '\\' + u.strip('\\')
    return url.strip('\\')

#获取IP
def GetLocalIp():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

#判断文件夹是否包含两张以上的图片
def IsContainPic(path):
    if os.path.isdir(path) == False:
        return False
    picCount = 0
    fileList = os.listdir(path)
    for f in fileList:
        filePath = os.path.join(path, f)
        if os.path.isfile(filePath) and IsPic(filePath):
            picCount += 1
            if picCount > 1:
                return True
    return False

#判断文件夹是否包含子文件夹
def IsContainSubDir(path):
    if os.path.isdir(path) == False:
        return False
    fileList = os.listdir(path)
    subDirCount = 0
    for f in fileList:
        filePath = os.path.join(path, f)
        if os.path.isdir(filePath):
            subDirCount += 1
            if subDirCount > 1:
                return True
    return False

def GetAllPicDir(path):
    fullpath = os.path.join(os.getcwd(), path)
    if os.path.isdir(fullpath) == False:
        return []

    pathList = []
    if IsContainPic(fullpath):
        pathList.append(path)

    subDir = os.listdir(fullpath)
    for s in subDir:
        subDirPath = os.path.join(fullpath, s)
        pathList += GetAllPicDir((path+'\\'+s).strip('\\'))
    return pathList

def GetDirHaveSubDir(path):
    fullpath = os.path.join(os.getcwd(), path)
    if os.path.isdir(fullpath) == False:
        return []

    pathList = []
    if IsContainSubDir(fullpath):
        pathList.append(path)

    subDir = os.listdir(fullpath)
    for s in subDir:
        subDirPath = os.path.join(fullpath, s)
        pathList += GetDirHaveSubDir((path+'\\'+s).strip('\\'))
    return pathList


def AnalyzeRequest(req):
    strAuth = '#whyoldareyou'
    ind = req.find(strAuth)
    if ind == -1:
        return 'nayayayayayayayayaya'
    else:
        return req[1:ind]
    # 将正则表达式编译成Pattern对象  
    #pattern = re.compile(r'/qr\?s=([^\&]+)\&qr=Show\+QR')  
    # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None  
    #match = pattern.match(self.path)  
    #return match.group(1)
