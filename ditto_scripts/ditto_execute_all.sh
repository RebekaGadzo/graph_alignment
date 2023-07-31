SKIP_WAIT=1

if [ "$1" != "-w" ]; then
  SKIP_WAIT=0
fi

if [ "$SKIP_WAIT" -eq "1" ]; then 
	echo "Flag -w was passed. Automatic pause will be added."
fi

echo "Starting script blocking training"
sh blocking_training.sh

if [ "$SKIP_WAIT" -eq "1" ]; then 
	read -p "Continue with the blocking execution"
fi

echo "Starting script blocking execute"
sh blocking_execute.sh

if [ "$SKIP_WAIT" -eq "1" ]; then 
	read -p "Continue with the ditto train"
fi

echo "Starting script ditto train"
sh ditto_train.sh

if [ "$SKIP_WAIT" -eq "1" ]; then 
	read -p "Continue with ditto (matching) execution"
fi

echo "Starting script ditto matching"
sh ditto_match.sh