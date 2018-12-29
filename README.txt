Files are downsampled with following command:

DS_FACTOR=50; FILENAME=originals/A2A_Section_10__Peru.kml; \
  echo -e "$(head -n 100 $FILENAME | grep \<)" '\n' "$(awk -v dsf="$DS_FACTOR" 'int(NR/1)%dsf==0' $FILENAME)" '\n' "$(tail -n 100 $FILENAME | grep \<)" \
  > reduced/A2A_Section_10__Peru_ds50.kml
