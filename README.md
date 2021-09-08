# hpca_hfgen
HPCA Hall of Fame Page Generator

## Generating the hall of fame table

Get the up-to-date list of HPCA publications from dblp using the available script:

```$ python3 get_dblp_with_api.py```

This will download the hpca database into `xml/dblp.xml`.


Then run the scripts to automatically generate the result table:

```./run.sh <up_to_year>```

Be aware that conflicts might exist, and you have to fix them manually.

## Fixing conflicts

Open the file `script_conflicts.txt`.
There will be a list of potential conflicts, i.e., people with similar (even equal) names that might have to be corrected in the xml file.
To assign papers to the same person (solve the conflict) we should change the authors pid in the xml so it consistent throughout the document.


If the names listed in the issues look conflictuous and it could be the case that it is the same person, do the following:

 1) Open the `xml/dblp.xml` local file
 2) Search for entries using the author conflicting names
 3) On those entries, look for the url of the paper (or it's title) and search it online for more information
 4) Verify if the extra information you found about the author of that paper can solve the conflict (e.g., if the affiliation is the same across conflicting papers)
 5) If it matches, merge the pid of the author (in file `xml/dblp.xml`) so that the pid is the same accross all papers for that author
 6) Repeat with all issues listed in `script_conflicts.txt`
 8) After all conflicts have been solved, you can run the script again (do not fetch the data from dblp again or you will have to re-do the manual changes):

    ```./run.sh <up_to_year>```

You can ignore conflicts that are reported this time IF you merged all pids properly.


### Acknoledgements.
Based on original scripts:
https://github.com/teshull/hpca_hof & https://github.com/jray319/hfgen
