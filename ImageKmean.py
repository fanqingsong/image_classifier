import colorsys
import os
import shutil
import numpy as np
from PIL import Image
import kmeans
import sys


class ImagesCluster(object):
    def __init__(self, imagedir, k):
        self._imageDir = imagedir

        # 建立输出文件夹
        self._image2VectorDir = os.path.join(imagedir, 'image2vector')

        # 若不存在则创建
        if not os.path.isdir(self._image2VectorDir):
            os.mkdir(self._image2VectorDir)

        # 建立文档存储经过特征工程处理后的数据
        self._imageVectorFile = os.path.join(self._image2VectorDir, 'images.txt')

        self._k = k

        # for delete previous directory
        for i in range(50):
            clusterDir = os.path.join(self._imageDir, 'cluster-{}'.format(i))
            if os.path.isdir(clusterDir):
                shutil.rmtree(clusterDir)

    # 生成所有图片地址
    def _loadImages(self):
        images = os.listdir(self._imageDir)
        imagesfile = [os.path.join(self._imageDir, image) for image in images]
        return imagesfile

    def _hsv2L(self, h, s, v):
        QH = 0
        if (h <= 20) or (h >= 315):
            QH = 0
        if 20 < h <= 40:
            QH = 1
        if 40 < h <= 75:
            QH = 2
        if 75 < h <= 155:
            QH = 3
        if 155 < h <= 190:
            QH = 4
        if 190 < h <= 270:
            QH = 5
        if 270 < h <= 295:
            QH = 6
        if 295 < h <= 315:
            QH = 7

        QS = 0
        if 0 <= s <= 0.2:
            QS = 0
        if 0.2 < s <= 0.7:
            QS = 1
        if 0.7 < s <= 1:
            QS = 2

        QV = 0
        if 0 <= v <= 0.2:
            QV = 0
        if 0.2 < v <= 0.7:
            QV = 1
        if 0.7 < v <= 1:
            QV = 2

        L = 9 * QH + 3 * QS + QV
        assert 0 <= L <= 71
        return L

    def _getImageColorVector(self, image):
        # 读取图片源码
        originImage = Image.open(image)
        # 转换为矩阵
        ndarr = np.array(originImage.convert("RGB"))
        # 取矩阵行数
        rowcnt = ndarr.shape[0]
        # 取矩阵列数
        colcnt = ndarr.shape[1]
        #colors = ndarr.shapr[2]
        # 生成含12个元素0的序列
        LVector = [0] * 12

        for oneRow in range(rowcnt):
            for oneCol in range(colcnt):
                r, g, b = ndarr[oneRow][oneCol]

                h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
                h = h * 360
                ll = self._hsv2L(h, s, v)
                LVector[int(ll/6)] += 1

        lsum = sum(LVector)
        result = [v * 1.0/lsum for v in LVector]
        print(image, result)
        return result

    def _getdata(self):
        date_file = open(self._imageVectorFile, 'r')
        imagesdata = []
        for line in date_file:
            # 读取每个图片的数据
            p = line.strip('\n').split(',')
            # imagesdata存储图片数据
            imagesdata.append(list(map(eval, p[1:])))
        return imagesdata

    def _getimagedir(self):
        date_file = open(self._imageVectorFile, 'r')
        imagesdir = []
        for line in date_file:
            p = line.strip('\n').split(',')
            imagesdir.append(p[0])
        return imagesdir

    def _extractfeature(self):
        # 取所有图片地址（数组）
        images = self._loadImages()
        # 打开经过特征工程处理后的数据
        file = open(self._imageVectorFile, 'w')
        for oneimage in images:
            # 跳过文件夹
            if not os.path.isdir(oneimage):
                # 取图片颜色向量
                lvector = self._getImageColorVector(oneimage)
                file.write(oneimage+',')
                file.write(','.join(map(str, lvector)))
                file.write('\n')
        file.close()

    def cluster(self):
        self._extractfeature()

        km = kmeans

        # 从文件中读取向量数据
        points = self._getdata()
        print(points)

        # 数据注入算法，返回图片所归属类别
        imageMembers = km.k_means(points, self._k)
        print(imageMembers)

        for idx, m in enumerate(imageMembers):
            # 取所有图片所在路径
            srcdir = self._getimagedir()

            # 取出第idx个图片的路径
            src = srcdir[idx]

            # m为图片所属归类，src为该图片路径
            print('clusterid:', m)
            print('src', src)

            # 创建每类图片的文件夹cluster-{%d}
            dest = os.path.join(os.path.join(self._imageDir), 'cluster-%d' % m)
            if not os.path.exists(dest):
                os.makedirs(dest)
            print(dest)

            # 将图片拷贝至所属分类对应的文件夹中
            shutil.copy(src, dest)


if __name__ == '__main__':
    cluster_num = 2 

    print("sys.argv=%s" % sys.argv)

    if len(sys.argv) >= 2 :
        cluster_num = int(sys.argv[1])

    print("cluster_num=%d" % cluster_num)

    basedir = os.path.dirname(os.path.abspath(__file__))
    imagedir = os.path.join(basedir, 'images')

    imageluster = ImagesCluster(imagedir, cluster_num)
    imageluster.cluster()












