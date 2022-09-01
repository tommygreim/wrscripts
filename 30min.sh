for i in `seq 1800 -1 1` ; do tput sc;tput cup 0 $(($(tput cols)-5)); echo -e "\e[32m $i \e[39m";tput rc; ; sleep 1;done &
