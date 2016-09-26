#!/bin/bash
initctl --version
if [ $? -ne 0 ]
    then
        systemctl --version
        if [ $? -ne 0 ]
            then
                echo FAILED!
                echo No systemd nor init.d installed!
                exit $?
            else
                python setup.py install
                cp -v etc/systemd/system/multi-user.target.wants/dvs.service /etc/systemd/system/multi-user.target.wants/dvs.service
                systemctl daemon-reload
                systemctl start dvs
        fi
    else
        python setup.py install
        cp -v etc/init.d/dvs /etc/init.d/dvs
        cp -v etc/default/dvs /etc/default/dvs
        chmod -v a+x /etc/init.d/dvs
        service dvs start
fi