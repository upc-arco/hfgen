if [ $# -lt 1 ]; then
  echo 1>&2 "$0: not enough arguments. Please provide the target year."
  exit 2
fi

# capturnig the argument
year=$1

# cleanining the folder
rm ./*.txt

chmod +x get_dblp_with_api.py
chmod +x list_generator.py
chmod +x conflict_checker.py 
chmod +x hfgen.py 


if [ ! -f ./xml/dblp.xml ]; then
    echo "Database file not found! Please run the script get_dblp_with_api.py"
    echo "Exiting..."
    exit
fi


echo "*********************************************"
echo "Building hpca ranking..."
./list_generator.py --endYear=$year
echo "Ranking done. Publications that did not match criteria can be found at 'missed_criteria.txt'"

#echo "*********************************************"
#echo "Checking for conlifcts"              # old way
#./conflict_checker.py

cp out.txt  data/$year.in

echo "*********************************************"
echo "Building the ranking table..."
./hfgen.py $year

echo "*********************************************"
echo "HPCA hall of fame table saved as 'hpca_hof_$year.html'"

if [ -f conflicts.txt ]; then
    echo "*********************************************"
    echo " * IMPORTANT: There are unsolved conflicts. Please see conflicts.txt file. You can either:"
    echo " * 1) manually update the ./xml/dblp.xml database file - to specify the author - and re-run this script "
    echo " * 2) manually fix output file and re-run the hfgen.py script again"
fi

echo "*********************************************"


