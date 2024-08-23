# CSE-398-final-project

# Jesse Warren

## Dataset (https://drive.google.com/drive/folders/1MSJ8VZbyOEz7Rlbi2YX_kQBxINfnt2H1?usp=drive_link)

## Directory Structure (Important Files and Folders Only)
```
collect.py ==> This script was used to webscrape test captchas from the reCAPTCHA demo website.
detection.sh ==> This shell script runs the object detection model by invoking detect.py in the yolo architecture.
evaluation.py ==> This script runs the model on the images in test_capchas in the directory below and the generated labels are saved in test_labels
web.py ==> This script invokes the web driver to run object detection on the reCAPTCHA demo site.
value.txt ==> This is a storage file to correctly access the labels once object detection is run. The number is incremented each run.
├── eval ==> Contains script for comparing test_labels_eval and test_labels to graph IOU for the model.
│   intersection_over_union.py ==> This script evaluates the model with the IoU technique and creates a graph to visualize the results.
│   metrics.py ==> Once the evaluation.py script has been ran and test_labels have been generated. This script evaluates the model on images       correct and captchas correct.
│   visualize.py ==> This script is used to create visualizations of the test captchas with ground truth and predicted labels.
│   ├── test_captchas ==> Folder to store test captchas. (Note: this directory was removed and uploaded to Google Drive)
│   ├── test_captcha_labels ==> Folder to store test captcha labels. (Note: this directory was removed and uploaded to Google Drive)
│   └── test_labels ==> Folder to store generated labels for evaluation. (Note: this directory was removed and uploaded to Google Drive)
├── graphs ==> Where all graphs and visualizations are saved to.
├── labeling ==> Folder for labeling processes
│   script.sh ==> Shell script to invoke labeling pipeline.
│   ├──outdir ==> Images to be labeled.
│   ├──outdir2 ==> Images and labels generated here.
│   └──images_processed ==> Images are removed from outdir and placed here as they are labeled.
├── models ==> Where each trained model was saved to. (Note: the model 'modelA1' was removed and uploaded to Google Drive)
└── yolov5 (Note: this directory was removed and uploaded to Google Drive)
    segment.py ==> A script for splitting data from the images folder into the test_images folder (also will move labels)
    augment.py ==> A script for taking a group of images/labels and augmenting them. Results will be placed in the next 2 folders.
    ├── augmented_images ==> Empty folder where generated augmented images were placed
    ├── augmented_labels ==> Empty folder where generated augmented labels were placed
    ├── tmp_images ==> Folder for images to be augmented are placed
    ├── tmp_labels ==> Folder for labels to be augmented are placed
    ├── data.yaml ==> Contains class mapping (0 is cross, 1 is ...)
    ├── runs
    │   ├── detect ==> Output directory for detection related tasks.
    │   │   ├── expX
    │   └── train ==> Output directory for training related tasks
    │       ├── expX
    └── utils ==> Bulk of YOLO training scripts.
        └──dataset ==> Where the dataset was stored to (Note: this directory was removed and uploaded to Google Drive)
            ├── images ==> Training images
            ├── labels ==> Training labels
            ├── test_images ==> Testing images
            ├── test_labels ==> Testing labels
            └── test_labels_eval ==> Predicted labels on testing images
```
Note: run 'conda env create -f environment.yml' to import my conda environment
## Example Commands

### Training a model

```
# Start training process
cd yolov5
python train.py --data data.yaml --epochs N --batch-size 5 --weights yolov5s.pt --img 416
# Save model weights
cp runs/exp{latest-exp-number}/best.pt ../models/new_model.pt
```

### Evaluating the model 

```
# Runs the yolo model on the test captchas, generating the labels in test_labels
python evaluation.py
cd eval
# This script compares the ground truth labels to the predicted labels, generating the evaluation metrics
python metrics.py

```

### Testing the model on the reCAPTCHA Demo Site

```
# Runs the yolo model on the reCAPTCHA Demo Site
python web.py
```

### Generating Visualizations

```
# In its current state, the labels and image path must be changed in the script
cd eval
python visualize.py
```


#### Running the Model on a Single Image

```
# First argument is the image ID, second is the model weights (no extension), third is the extension for the image (optional, defaults to png)
sh detection.sh 000033 modelA1 png
# Will output the annotated image in output.png, the bounding boxes used in bbx.txt, and the ground-truth bounding boxes in label.txt
```

### Augmenting Images

```
cd yolov5
# First argument is the image directory
# Second argument is the label directory
# Third argument is the number of images to augment (use -1 for all in directory) 
python augment.py tmp_images/ tmp_labels/ -1
# Then run the following to move the augmented images into the training directories.
mv augmented_images/*.png utils/dataset/images && mv augmented_labels/*.txt utils/dataset/labels
```

### Separating into Training/Testing Datasets

```
cd yolov5
# moves 20% of the images in dataset/images into dataset/test_images along with their corresponding labels from labels/ into test_labels
python segment.py
# RECOMMENDED NOT TO RUN TWICE! 
# Reset the test directories before rerunning by moving the images from test_images and test_labels back to the original directories
```

### Labeling Images

```
cd labeling
sh script.sh
# Moves images from outdir to images proccessed as they are labeled. Labels are saved in outdir2
# More detailed directions when the script is run
```


## Considerations and Final Comments
1. run 'conda env create -f environment.yml' to import my conda environment
2. The dataset used to train the model and the rest of the yolov5 folder along with the test captchas and their labels have been placed in a Google Drive folder.
3. The model, 'modelA1' is also in the Google Drive folder.
4. The zip file on course site had a 50MB limit. Therefore, a lot of resources ended up going into the following google drive link.
# Google Drive (https://drive.google.com/drive/folders/1MSJ8VZbyOEz7Rlbi2YX_kQBxINfnt2H1?usp=drive_link)
