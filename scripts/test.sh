#!/bin/sh
cd /cygdrive/dmomo/django-TDD
python manage.py schemamigration polls --auto
if [ "$?" == "0" ];then
    python manage.py migrate polls
    if [ "$?" == "0" ];then
        git push origin master
        echo "done!!"
    else
        echo "NO!!!"
    fi
else
    git push origin master
    echo "done!"
fi
