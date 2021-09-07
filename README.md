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
If conflicts are found you will be notified by the scripts. Also, there will be a file `conflicts.txt` in the project folder.

### Why are there conflicts?

In the database, authors with the same name have extra digits on their IDs.
E.g., John Snow (id: 123/456 **-1**) and John Snow (id: 123/456 **-2**) would be two different people. 
Sometimes the database does not label an author with the extra digits. So there could be a John Snow (id: 123/456) as the author, and we don't know if it is the person '**-1** 'or '**-2**'.


### How to fix the conflicts?

Open the `conflicts.txt` file. There, will be listed all authors that might have to be on the hall of fame, but have incomplete identification in the dblp database.
You will see something like this:
```
*** Unsolved conflict ***
123/456-2 John Snow 0002 papers: 7
123/456 John Snow papers: 2
total papers: 9
```

Here, author 123/456-2 might be part of the hall of fame if one of the other two papers belongs to him. So we have to check these other two papers:
 1) Open the `xml/dblp.xml` local file
 2) Search for entries of the unknown author (in this example `pid="123/456"`)
 3) In those entries, look for the URL of the paper (or its title) and search for it online for more information
 4) Verify if the extra information you found about the author of that paper (e.g., affiliation, orcid, etc.) match with those of author 123/456-2 (can be obtained by: https://dblp.org/pid/<place_the_pid_here>.html, e.g.:  https://dblp.org/pid/123/456-2.html)
 5) If it matches, modify the entry (in file `xml/dblp.xml`) so that `pid="123/456"` now becomes `pid="123/456-2"`
 6) It if does not match (or matches with someone else), try to find the specific id to assign the paper (e.g. `pid="123/456-1"`), or leave it as is (in this case, there might be reported conflicts later, but you can ignore them because you just checked manually).
 7) Repeat with all authors listed in `conflicts.txt` (there should not be many)
 8) After all conflicts have been solved, you can run the script again (do not fetch the data from dblp again or you will have to re-do the manual changes):

    ```./run.sh <up_to_year>```

You can ignore conflicts that are reported this time IF you understood step 6.


### Acknoledgements.
Based on original scripts:
https://github.com/teshull/hpca_hof & https://github.com/jray319/hfgen
