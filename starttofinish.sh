python createmanualinput.py
#./downloadAllData.sh
./saveAllResults.sh
python get_result_total.py mergeresults
python get_result_total.py diffresults
python get_result_total.py getrenamedresults
python get_result_stats.py



