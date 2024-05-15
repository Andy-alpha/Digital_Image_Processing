import sys
sys.path.append('./utils')

# util.py

import numpy as np
import cv2

def region_growing(img, seed):
    # parameters
    height, width = img.shape
    visited = np.zeros_like(img, dtype=np.uint8)
    dx = [-1, 0, 1, 0]
    dy = [0, -1, 0, 1]

    # stack for region pixels
    stack = []
    stack.append((seed))

    while len(stack) > 0:
        s = stack.pop()
        x, y = s

        if np.all(img[x, y] > 128):  # threshold condition
            visited[x, y] = 255  # mark as visited

            # check neighbours
            for i in range(4):
                nx, ny = x + dx[i], y + dy[i]
                if nx >= 0 and nx < height and ny >= 0 and ny < width:
                    if visited[nx, ny] == 0:
                        stack.append((nx, ny))

    return visited

class Point(object):
    # 按Matrix顺序来，x是行号，y是列号
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y

def getGrayDiff(img,currentPoint,tmpPoint):

    return abs(int(img[currentPoint.x,currentPoint.y]) - int(img[tmpPoint.x,tmpPoint.y]))

def selectConnects(p: int)->list[Point]:
    if p != 0:
        connects = [Point(-1, -1), Point(0, -1), Point(1, -1), Point(1, 0), Point(1, 1), \

                    Point(0, 1), Point(-1, 1), Point(-1, 0)]
    else:
        connects = [ Point(0, -1),  Point(1, 0),Point(0, 1), Point(-1, 0)]
    return connects

def regionGrow(img: cv2.Mat, seeds: list, thresh: int, p = 1)->cv2.Mat:
    # thresh表示与领域的相似距离，小于该相似距离就合并
    height, weight = img.shape
    print(f"Image height = {height}, weight = {weight}")
    seedMark = np.zeros(img.shape)
    seedList = []
    for seed in seeds:
        seedList.append(seed)
    label = 255
    connects = selectConnects(p)

    while (len(seedList) > 0):
        currentPoint = seedList.pop(0)

        seedMark[currentPoint.x, currentPoint.y] = label
        # Eight directions
        for i in range(8):
            tmpX = int(currentPoint.x + connects[i].x)
            tmpY = int(currentPoint.y + connects[i].y)

            if tmpX < 0 or tmpY < 0 or tmpX >= height or tmpY >= weight:
                continue
            grayDiff = getGrayDiff(img, currentPoint, Point(tmpX, tmpY))

            if grayDiff < thresh and seedMark[tmpX,tmpY] == 0:
                seedMark[tmpX, tmpY] = label
                seedList.append(Point(tmpX, tmpY))
    return seedMark

def splitMerge(src: cv2.Mat, dst: cv2.Mat, h0: int, w0: int, h: int, w: int, maxMean: float, minStdVar: float, cell: int=4):
    win = src[h0: h0+h, w0: w0+w]
    mean = np.mean(win)         # 窗口的均值
    stdVar = np.std(win, ddof=1)   # 窗口的无偏标准差
    # cv2.meanStdDev(win, mean, var)
    if (mean < maxMean) and (stdVar > minStdVar) and (h < 2 * cell) and (w < 2 * cell):
        # 满足谓词逻辑P，判为目标区域，设为白色
        dst[h0: h0+h, w0: w0+h] = 255
        # print("h0={}, w0={}, h={}, w={}, mean={:.2f}, stdVar={:.2f}".format(h0, w0, h, w, mean, stdVar))

    else:
        # 不满足谓词逻辑条件P
        if (h > cell) and (w > cell):
            # split recursively
            splitMerge(src, dst, h0, w0, (h+1)//2, (w+1)//2, maxMean, minStdVar, cell)
            splitMerge(src, dst, h0, w0 + (w+1)//2, (h+1)//2, (w+1)//2, maxMean, minStdVar, cell)
            splitMerge(src, dst, h0 + (h+1)//2, w0, (h+1)//2, (w+1)//2, maxMean, minStdVar, cell)
            splitMerge(src, dst, h0 + (h+1)//2, w0 + (w+1)//2, (h+1)//2, (w+1)//2, maxMean, minStdVar, cell)
        else:
            # Can't split anymore, set to black
            dst[h0: h0+h, w0: w0+h] = 0
