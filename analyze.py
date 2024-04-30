import cv2
import numpy as np

# 读取图片， 在图片上面标点
# img = cv2.imread('/Users/micdz/Downloads/IMG_9087.JPG')
# # 将img resize为A4纸大小，固定宽度为1000
img_shape = [1500//2, 2121//2]
#
# dst_img = img.copy()
# points = []
#
a4_size = [297,210]
#
big_armor_size = [230, 127]
small_armor_size = [135, 125]
dart_armor_size = [140, 140]


#
# # 计算到图像上的尺寸
big_armor_size = [int(big_armor_size[0] / a4_size[0] * img_shape[1]), int(big_armor_size[1] / a4_size[1] * img_shape[0])]
small_armor_size = [int(small_armor_size[0] / a4_size[0] * img_shape[1]), int(small_armor_size[1] / a4_size[1] * img_shape[0])]
dart_armor_size = [int(dart_armor_size[0] / a4_size[0] * img_shape[1]), int(dart_armor_size[1] / a4_size[1] * img_shape[0])]
#
# # 鼠标在图片上面点击的回调函数
# def on_mouse(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         print('x = %d, y = %d'%(x, y))
#         points.append((x, y))
#         cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=10)
#         cv2.imshow('image', img)
#
# # 创建窗口并绑定窗口事件
# cv2.namedWindow('image')
# cv2.setMouseCallback('image', on_mouse)
#
# # 显示图片
# cv2.imshow('image', img)
# cv2.waitKey(0)


def analyze_ballistic(points, dst_img):
    # 在这里执行分析，将分析结果显示在result_label上
    # 然后将结果显示在result_label上
    # 显示所有点的平均值
    x_sum = 0
    y_sum = 0
    for point in points:
        x_sum += point[0]
        y_sum += point[1]
    x_mean = x_sum // len(points)
    y_mean = y_sum // len(points)
    print('x_mean = %d, y_mean = %d' % (x_mean, y_mean))

    # 在imagewindow中绘制出所有的点和所有点的平均值
    cv2.circle(dst_img, (x_mean, y_mean), 1, (0, 255, 0), thickness=3)
    # 以平均点为中心，画圆，圆的半径以50、100、150、200、250增大
    for i in range(1, 10):
        cv2.circle(dst_img, (x_mean, y_mean), i * 50, (0, 255, 0), thickness=2)

    score = 0.0
    distance = 0.0
    hit_small = 0
    hit_large = 0
    hit_dart = 0

    for point in points:
        # 计算点到平均点的距离
        distance += np.sqrt((point[0] - x_mean) ** 2 + (point[1] - y_mean) ** 2)
        # 判断点在哪个圆内
        for i in range(1, 10):
            if (point[0] - x_mean) ** 2 + (point[1] - y_mean) ** 2 <= (i * 50) ** 2:
                cv2.circle(dst_img, (point[0] + 5, point[1] + 5), 1, (0, 0, 255), thickness=3)
                # 在点旁边标记环数
                score += (10 - i + 1)
                cv2.putText(dst_img, str(10 - i + 1), point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                break

    for point in points:
        # 判断在小装甲板内的点
        if point[0] >= x_mean - small_armor_size[0] // 2 and point[0] <= x_mean + small_armor_size[0] // 2 and point[
            1] >= y_mean - small_armor_size[1] // 2 and point[1] <= y_mean + small_armor_size[1] // 2:
            hit_small += 1
        # 判断在大装甲板内的点
        if point[0] >= x_mean - big_armor_size[0] // 2 and point[0] <= x_mean + big_armor_size[0] // 2 and point[
            1] >= y_mean - big_armor_size[1] // 2 and point[1] <= y_mean + big_armor_size[1] // 2:
            hit_large += 1
        # 判断在飞镖内的点
        if point[0] >= x_mean - dart_armor_size[0] // 2 and point[0] <= x_mean + dart_armor_size[0] // 2 and point[
            1] >= y_mean - dart_armor_size[1] // 2 and point[1] <= y_mean + dart_armor_size[1] // 2:
            hit_dart += 1
    # 计算最小包围圆形，并绘制出来
    min_circle = cv2.minEnclosingCircle(np.array(points))
    cv2.circle(dst_img, (int(min_circle[0][0]), int(min_circle[0][1])), int(min_circle[1]), (255, 0, 0), thickness=2)

    # 计算平均环数和距离
    score = score / len(points)
    distance = distance / len(points)
    hit_small = hit_small / len(points)
    hit_large = hit_large / len(points)
    hit_dart = hit_dart / len(points)
    min_radius = min_circle[1]
    min_radius = min_radius / img_shape[0] * a4_size[1]
    # 中心点旁边puttext，提示“center”
    cv2.putText(dst_img, 'center', (x_mean, y_mean), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    fontSize = 0.5
    # 在左上角显示平均环数和平均距离
    cv2.putText(dst_img, 'score = %f' % (score), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, fontSize, (0, 255, 0), 2)
    cv2.putText(dst_img, 'distance = %f' % (distance), (0, 100), cv2.FONT_HERSHEY_SIMPLEX, fontSize, (255, 0, 0), 2)
    cv2.putText(dst_img, 'hit_small = {}%'.format(hit_small * 100), (0, 150), cv2.FONT_HERSHEY_SIMPLEX, fontSize,
                (255, 255, 0), 2)
    cv2.putText(dst_img, 'hit_large = {}%'.format(hit_large * 100), (0, 200), cv2.FONT_HERSHEY_SIMPLEX, fontSize,
                (0, 100, 255), 2)
    cv2.putText(dst_img, 'hit_dart = {}%'.format(hit_dart * 100), (0, 250), cv2.FONT_HERSHEY_SIMPLEX, fontSize, (255, 0, 255),
                2)
    cv2.putText(dst_img, 'min_radius = %f' % (min_radius), (0, 300), cv2.FONT_HERSHEY_SIMPLEX, fontSize, (255, 0, 255), 2)
    # 以平均点为中心，绘制smll armor的框
    cv2.rectangle(dst_img, (x_mean - small_armor_size[0] // 2, y_mean - small_armor_size[1] // 2),
                  (x_mean + small_armor_size[0] // 2, y_mean + small_armor_size[1] // 2), (255, 255, 0), 3)

    # 以平均点为中心，绘制big armor的框
    cv2.rectangle(dst_img, (x_mean - big_armor_size[0] // 2, y_mean - big_armor_size[1] // 2),
                  (x_mean + big_armor_size[0] // 2, y_mean + big_armor_size[1] // 2), (0, 100, 255), 3)

    # 以平均点为中心，绘制dart armor的框
    cv2.rectangle(dst_img, (x_mean - dart_armor_size[0] // 2, y_mean - dart_armor_size[1] // 2),
                  (x_mean + dart_armor_size[0] // 2, y_mean + dart_armor_size[1] // 2), (255, 0, 255), 3)

    # cv2.imshow('image', dst_img)
    # cv2.waitKey(0)

    return score, distance, hit_small, hit_large, hit_dart, min_radius,  dst_img
