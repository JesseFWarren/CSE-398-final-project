import subprocess
import argparse
import os

def run_yolo_detection(image_id, model_name, ext="png"):
    # Construct the command
    os.chdir("yolov5")
    command = [
        "python", "detect.py", 
        "--data", "utils/data.yaml",
        "--save-txt",
        "--source", f"data/test_images/tests/{image_id}",
        "--weights", f"../models/{model_name}.pt"
    ]

    # Execute the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Optionally, print the output for debugging
    print(result.stdout)
    print(result.stderr)

def main():
    parser = argparse.ArgumentParser(description="Run YOLO model on an image")
    parser.add_argument("image_id", type=str, help="The ID of the image to process")
    parser.add_argument("model_name", type=str, help="The name of the YOLO model to use")

    args = parser.parse_args()

    run_yolo_detection(args.image_id, args.model_name)

if __name__ == "__main__":
    main()
