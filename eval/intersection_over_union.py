# import the necessary packages
import cv2
import sys
import matplotlib.pyplot as plt
import os

os.makedirs("graphs", exist_ok=True)

description = "Crosswalks-and-stairs"

def process_file(file):
    if not os.path.isfile(file):
        return []
    # Get the labels from a file
    labels = []
    f = open(file, "r")
    for line in f:
        tokens = line.split()
        if (len(tokens) == 0):
            continue
        if (tokens[0] in ["7", "8"]): # ignore useless classes
            continue
        x, y, w, h = [float(tokens[i]) for i in range(1,5)]
        w,h = w/2, h/2
        box = [x-w, y-h, x+w, y+h]
        labels.append(box)
    f.close()
    return labels

def bb_intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
    
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)

	# return the intersection over union value
	return iou, boxAArea, boxBArea

if len(sys.argv) < 3:
    print("Must provide two arguments to represent the folders containing the labels (1st) and the predictions (2nd) to process")
    exit(1)
labels_dir = sys.argv[1].strip()
predictions_dir = sys.argv[2].strip()
if labels_dir == "":
    print("labels directory wasn't provided")
if predictions_dir == "":
    print("predictions directory wasn't provided")
    
# loop over the detections
buckets = [0] * 10
count = 0
avg = 0
label_count = 0
total_box_size = 0
missed_box_size = 0
for file in os.listdir(labels_dir):
    labels = process_file(os.path.join(labels_dir, file))
    label_count += len(labels)
    predictions = process_file(os.path.join(predictions_dir, file))
    for box in labels:
        maxxer = 0
        mindex = None
        max_area_box = 0
        for pred in predictions:
            iou, area_box, area_pred = bb_intersection_over_union(box, pred)
            if maxxer < iou:
                maxxer = iou
                mindex = pred
                max_area_box = area_box
        if maxxer < 0.5:
            missed_box_size += max_area_box
        total_box_size += max_area_box
        if mindex is None:
            break
        count += 1
        avg += maxxer
        i = int(maxxer * 10)
        if i >= 10:
            i = 9
        buckets[i] += 1
        predictions.remove(mindex)

print(buckets)
print("Missed boxes have size:", missed_box_size, "\tBoxes have an average size:", total_box_size)
print("Average IOU:", avg / count)
print("Missed", label_count - count, "out of", label_count)
buckets[0] += label_count - count # add the missing to the last bucket

# creating the bar plot
plt.bar([f"{10*i}-{10*(i+1)}" for i in range(10)], buckets)

model = input("What is the model used in your analysis\n")
for i in range(len(buckets)):
    plt.text(i, buckets[i], buckets[i], ha = 'center')
plt.xlabel("IOU Buckets")
plt.ylabel("Number of examples in the bucket")
plt.title(f"IOU of predictions ({model}) on {description} test set")
plt.savefig(os.path.join("graphs", f"{model}_{description}_iou.png"))