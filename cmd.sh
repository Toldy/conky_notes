#!/usr/bin/bash

###############################################################################################
# Met affiche le contenu du fichier conky passé en paramètre en lui enlevant les commentaires #
###############################################################################################

while read line
do
    if [ ${line::1} != "#" ]
    then
	echo $line
    fi
done < $1 2>/dev/null
