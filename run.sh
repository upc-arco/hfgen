if [ $# -lt 1 ]; then
  echo 1>&2 "$0: not enough arguments. Please provide the target year."
  exit 2
fi

year=$1

chmod +x get_dblp_with_api.py
chmod +x list_generator.py
chmod +x conflict_checker.py 
chmod +x hfgen.py 

echo "*********************************************"
echo "Fetching xml files from dblp data base..."
./get_dblp_with_api.py


echo "*********************************************"
echo "Building hpca ranking..."
./list_generator.py --endYear=$year > missed_criteria.txt
echo "Ranking done. Publications that did not matched criteria can be found at 'missed_criteria.txt'"

echo "*********************************************"
echo "Checking for conlifcts"
./conflict_checker.py
mv out.txt  data/$year.in

echo "*********************************************"
echo "Building the ranking table..."
./hfgen.py $year

echo "*********************************************"
echo "HPCA hall of fame table saved as 'hpca_hof_$year.html'"


