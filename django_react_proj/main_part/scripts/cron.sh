cd /home/ubuntu/djangotest/django_react_proj/main_part/scripts
source ../../../logrocket_env/bin/activate
rm 4upperblocks.csv
rm results.csv
rm results_final.csv
rm script4_results.csv
rm stock_counts.csv

/usr/bin/python3 ./auto.py
/usr/bin/python3 ./count.py
/usr/bin/python3 ./final.py
/usr/bin/python3 ./script4.py
/usr/bin/python3 ./script5.py

chmod 644 *.csv
mv *.csv /home/ubuntu/djangotest/django_react_proj/main_part