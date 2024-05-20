#!/usr/bin/bash

helpFunction()
{
   echo ""
   echo "Usage: $0 -u username -p password"
   echo -e "\t-u FTP Username for log in"
   echo -e "\t-p password"
   exit 1 # Exit script after printing help
}

while getopts "u:p:" opt
do
   case "$opt" in
      u ) user="$OPTARG" ;;
      p ) pass="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$pass" ] || [ -z "$user" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

wget -P ../ ftp://$user:$pass@172.24.18.81:21/yolov8x.pt