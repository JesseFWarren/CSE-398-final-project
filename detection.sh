rm output.png &> /dev/null
rm output.jpg &> /dev/null
cd yolov5
if [ "$1" == "" ] || [ $# -gt 3 ]; then
        echo "Pass in the image id (000033 for example) as the first argument. Include extenstion as optional third arg (default png)"
        exit
fi
if [ -d "runs/detect/exp" ]; then
  echo "Wiping runs/detect/exp"
  rm -r runs/detect/exp*
fi
EXT="png"
if [ "$3" != "" ] && [ $# -lt 3 ]; then
        EXT=$3
fi

python detect.py --data utils/data.yaml --save-txt --source data/test_images/$1.$EXT --weights "../models/$2.pt"  # &> /dev/null
echo "Model inference results saved to output.$EXT, bbx.txt, and label.txt"
mv runs/detect/exp*/$1.$EXT ../output.$EXT
mv runs/detect/exp*/labels/$1.txt ../bbx.txt
cp data/test_labels/$1.txt ../label.txt