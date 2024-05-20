#!/usr/bin/bash

declare -a models=(
  "DETECTRON2"
  "YOLO"
)

helpFunction()
{
   echo ""
   echo "Usage: $0 -u username -p password -m modelName"
   echo -e "\t-u GIT Username for log in"
   echo -e "\t-p password"
   echo -e "\t-m modelname which you wants to install, currently supports ${models[*]}"
   exit 1 # Exit script after printing help
}

while getopts "u:p:m:" opt
do
   case "$opt" in
      u ) user="$OPTARG" ;;
      p ) pass="$OPTARG" ;;
      m ) model="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$pass" ] || [ -z "$user" ] || [ -z "$model" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

if [ "$model" = "${models[0]}" ]; then
  pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu118                                                                                                                                
  pip3 install --force-reinstall pillow==9.5.0 
  pip3 install git+https://$user:$pass@git.pancir.it/egor.bakharev/SharedLib-Det2Rec
elif [ "$model" = "${models[1]}" ]; then
  pip install git+https://$user:$pass@git.pancir.it/egor.bakharev/SharedLib-YoloRec
else 
  echo "UNKNOWN RECOGNIZER SPECIFIED!!!"
fi