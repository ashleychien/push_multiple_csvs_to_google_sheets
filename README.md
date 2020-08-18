# Push multiple CSVs to one Google Sheet!

Motivation: For one of my research projects, I was generating 12 csvs at a time and had to put all of them into a Google Sheet. For some reason, Google only lets you upload one csv at a time. The first time, I did this manually. The second time, I didn't feel like doing so much clicking, so I spent some time looking into the Google Sheets API to figure out how to do this automatically. I hope that this can be a help to others!

# Usage
This script takes in the ID of a Google Sheet and the name of a local folder which contains CSV files. It will upload each of these CSV files into the Google Sheet. The names of the tabs within the Google Sheet will be the names of the csv files, without the `.csv` postfix ("cat.csv" would become a tab in the Google Sheet named "cat"). If the sheet already contains a tab with this name, it will over-write what data is already currently there. The script will not affect other tabs in the Google Sheet.

# Steps

1. Go to https://developers.google.com/sheets/api/quickstart/python and follow Steps 1 and 2.

If Step 1 doesn't work for you, it may be because your email's organization does not allow the Google Sheets API to be enabled. (Step 1 didn't work for my @berkeley email, so I ended up using my personal email instead.)

2. Clone my repo/download `push_csvs.py`.
3. Create a Google Sheet (or use an existing one). Figure out its ID by looking at the URL in the browser. The URL looks something like this: `docs.google.com/spreadsheets/d/[ID HERE]/edit#gid=0`
4. Call `push_csvs.py` with command line arguments!

Example call:

`python push_csvs.py 1NpFD-sxSNzCfOWoyMiEC_a1xnw24TdjnUkIqLFcVSqs my_csvs`

`"1NpFD-sxSNzCfOWoyMiEC_a1xnw24TdjnUkIqLFcVSqs"` is the ID of the Google Sheet you want to place all of your csvs into. 

`my_csvs` is the directory on your local computer that contains all of the csv files you want to upload.

Note: When you first call `push_csvs.py`, an authentication page will pop up on your browser. Allow the script to access your Google Sheets.

# References
- https://developers.google.com/sheets/api/quickstart/python
- https://developers.google.com/sheets/api/guides/authorizing
- https://stackoverflow.com/questions/42362702/how-to-import-a-csv-file-using-google-sheets-api-v4
- https://stackoverflow.com/questions/41445723/how-can-i-add-a-new-tab-to-an-existing-sheet-via-the-google-sheets-api\