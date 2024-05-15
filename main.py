import argparse
import cv2
from utils.util import Point, regionGrow, splitMerge

def choose_all_points(image: cv2.Mat, step: int)->list:
    seeds = []
    height, weight = image.shape
    for i in range(1, height, step):
        for j in range(1, weight, step):
            seeds.append(Point(i, j))
    return seeds

# An alogorithm to choose the seed poit by clicking on the image
def choose_seed_point(image: cv2.Mat)->list:
    seeds = []
    def click_event(event, x, y, flags, param):
        nonlocal seeds
        if event == cv2.EVENT_LBUTTONDOWN:
            # Caution! Transpose (x, y) to (row, column) form.
            seed_point = Point(y, x)
            print(f"Seed Point: {seed_point.getX()}, {seed_point.getY()}")
            seeds.append(seed_point)
    cv2.imshow("Select Seed Point", image)
    cv2.setMouseCallback("Select Seed Point", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return seeds

if __name__ == "__main__":
    # Path to the image file
    # image_path = "/path/to/your/image.jpg"
    parser = argparse.ArgumentParser(description='Image Processing')
    parser.add_argument('-m', '--mode', type=str, metavar="'r'|'s'", choices=['r', 's'], default='r', help="'r' for 'regionGrow' and 's' for 'spiltMerge'")
    parser.add_argument('-i', '--image', type=str, metavar='/path/to/image', default='images/image.jpg', help='Path to the image file')
    parser.add_argument('-o', '--output', type=str, metavar='/path/of/output.jpg', default='output/output.jpg', help='Path to the output file')
    parser.add_argument('--thresh', type=int, metavar='INT', default=10, help='Threshold value for region growing')
    parser.add_argument('--step', type=int, metavar='STRIDE', default=200, help='Intevals when choosing points automatically')
    parser.add_argument('--select', type=str, metavar="'auto'|'manual'", choices=['auto', 'manual'], default='manual', help="select whether you would like to choose points automatically or manually in 'regionGrow' mode")
    parser.add_argument('-c', '--cell'  , type=int, default=4, help='Cell is the size of minimum split area')
    parser.add_argument('--max', type=float, metavar='maxMean', default=80.0, help='Set the upper bound of mean value')
    parser.add_argument('--min', type=float, metavar='minVar', default=10.0, help='Set the lower bound of standard variation')

    args = parser.parse_args()
    mode = args.mode
    image_path = args.image
    output_path = args.output

    # img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.imread(image_path, 0)
    if (mode == 'r'):
        select = args.select
        seeds = choose_seed_point(img) if (select == "manual") else choose_all_points(img, step=args.step)
        print('Processing……')
        # seeds.append(seed)
        # seeds = [ig.Point(10,10), ig.Point(82,150), ig.Point(20,300)]

        result = regionGrow(img, seeds, thresh=args.thresh)
        cv2.imwrite(output_path, result)
        cv2.imshow('Region Growing', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif (mode == 's'):
        import numpy as np
        height, weight = img.shape
        result = np.zeros([height, weight])
        mean = np.mean(img)
        var = np.std(img, ddof=1)
        src = img.copy()
        print("h={}, w={}, mean={:.2f}, var={:.2f}".format(height, weight, mean, var))

        maxMean = args.max    # Set the upper bound of mean value
        minVar = args.min     # Set the lower bound of standard variation

        splitMerge(src, result, 0, 0, height, weight, maxMean, minStdVar=minVar, cell=args.cell)
        
        cv2.imwrite(output_path, result)
        cv2.imshow('Spilt Merging', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
