ls */*/Results*/results/*png | grep aifNotSelected | while read line; do ID=${line%%/*};
echo $ID
postfix=$(echo $line | sed 's/^.*aifNotSelected[0-9]/AIFnotselected/' );
echo $postfix
uniquetimepoint=$(echo $line | grep -oP '(BL|FU)/Results[1-9]?' | sed 's/\//_/');
echo $ununiquetimepoint
outputname=${ID}_${uniquetimepoint}_${postfix}; cp $line /carpathia_rapidprocessing/second41cases_new/TEST/$outputname;  done
nautilus TEST
