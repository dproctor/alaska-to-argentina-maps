DS_FACTOR=$2; FILENAME=$1; echo -e "$(head -n 100 $FILENAME | grep \<)" '\n' "$(awk -v dsf="$DS_FACTOR" 'int(NR/1)%dsf==0' $FILENAME)" '\n' "$(tail -n 100 $FILENAME | grep \<)"
