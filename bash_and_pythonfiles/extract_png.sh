ls */*/Results*/results/*png | while read line; do ID=${line%%/*}; 
postfix=$(echo $line | sed 's/^.*view[0-9]\{2\}_//' );
echo $postfix
uniquetimepoint=$(echo $line | grep -oP '(BL|FU)/Results[1-9]?' | sed 's/\//_/'); 
outputname=${ID}_${uniquetimepoint}_${postfix}; cp $line /carpathia_rapidprocessing/second41cases_new/TEST/$outputname;  done
nautilus TEST
