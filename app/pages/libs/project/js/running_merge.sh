#! /bin/bash
current_directory="$PWD/app/pages/libs/project/js"
parent_directory="$(dirname "$current_directory")"
proj_js="$parent_directory/proj.js"
rm -f $proj_js
cat "$current_directory/running_proj.txt" | while read line
do
    if [ $line ]; then
        cat "$current_directory/$line" >> $proj_js
        echo -e "\n" >> $proj_js
    fi
done