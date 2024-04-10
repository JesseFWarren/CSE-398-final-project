cd yolov5
if [ "$1" == "" ] || [ $# == 0 ]; then
        echo "Pass in the weights to use for evaluation (with models/), and with extension"
        exit
fi
if [ -d "runs/detect/exp" ]; then
  echo "Wiping runs/detect/exp"
  rm -r runs/detect/exp*
fi

python detect.py --data data.yaml --save-txt --source utils/dataset/test_images --weights "../$1"
echo "Model inference results saved to utils/dataset/test_labels_eval"
rm utils/dataset/test_labels_eval/*.txt
mkdir -p utils/dataset/test_labels_eval
mv runs/detect/exp/labels/*.txt utils/dataset/test_labels_eval
echo "Proceed to run eval/intersection_over_union.py like:"
echo "python eval/intersection_over_union.py yolov5/utils/dataset/test_labels yolov5/utils/dataset/test_labels_eval"