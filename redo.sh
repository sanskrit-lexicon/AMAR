echo "BEGIN convert amar1.txt to version temp_amar.txt"
echo "temp_amar0.txt intermediate slp1 version"
python convert.py deva,slp1 amar1.txt temp_amar0.txt
echo "check invertability"
python convert.py slp1,deva temp_amar0.txt temp_amar0_deva.txt
echo "count of lines in diff should be 0"
diff amar1.txt temp_amar0_deva.txt | wc -l
echo ""
# Additional changes
echo ""
python addinfo.py temp_amar0.txt temp_amar.txt
echo "END convert amar1.txt to version temp_amar.txt"
echo "Do you want to copy temp_amar.txt to ../amar.txt  ?"

