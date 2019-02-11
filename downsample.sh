DS_FACTOR=$2; FILENAME=$1; echo -e "$(head -n 100 $FILENAME | grep \<)" '\n' "$(grep -v \< $FILENAME | awk -v dsf="$DS_FACTOR" 'int(NR/1)%dsf==0')" '\n' "$(tail -n 100 $FILENAME | grep \<)"
