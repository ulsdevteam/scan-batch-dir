# Description:

This script is used to reconcile a Google Sheet's contents against a
batch directory. The script scans the directory finding all objects and
then updates the Google Sheet with information it finds. It looks for a
few types of file directory layouts relating to these types of objects:

- Books

- Manuscripts

- Newspaper Issues

- Audio (Oral Histories or General Audio files)

- Video (Oral Histories or General Videos)

- Images

Currently no other object types are addressed, but the script will
identify and add them as it finds them.

The script will ignore the following files and directories (including
contents):

- Directory named 'ignore'

- File named 'manuscript.csv'

- File named 'manuscript.xls'

- File named 'manuscript.xlsx'

## Google Sheet requirements:

Sheet Columns:

  -----------------------------------------------------------------------
  Required Columns         Description
  ------------------------ ----------------------------------------------
  'id'                     The PID of the object. This column must exist.

  'file'                   Leave this empty but the column must exist.
                           This field will be updated by the script with
                           the full path to the file.

  Optional Columns         

  'thumbnail'              Used for A/V media. If a .jpg or .png file is
                           found the full path to the file will be added
                           to this column.

  'transcript'             Used for A/V media. If a .srt or .vtt file is
                           found the full path to the file will be added
                           to this column.

                           
  -----------------------------------------------------------------------

Script Parameters:

  -------------------------------------------------------------------------
  Required Parameters       Description
  ------------------------- -----------------------------------------------
  \--config-file            Full or relative path to the configuration file
                            used for the script.

  \--log-file               Full or relative path to the log file that will
                            be generated.

  \--directory              Full path of the directory we wish to scan.

                            

  Optional Parameters       

  \--in-google-sheet-id     The ID number of the Google Sheet.

  \--in-google-sheet-name   The Name of the Tab in the Google Sheet (E.g.:
                            Sheet1)

  \--in-google-creds-file   The full or relative path to the Google
                            Credentials File.
  -------------------------------------------------------------------------

## Google Credentials File:

This is a .json file provided by ULS IT that contains the information
needed to connect to a Google Drive and Google Sheets via a service
account using an API. This .json file is tied to a service account in
Google Drive that has permissions to edit Google Sheets via the Google
APIs.

## 

## Google Sheet ID:

This is a long string of characters found in the URL bar when
editing/viewing the Google Sheet in a browser. E.g.:
'2cip4rM-c9Xnc2oisIM_Win5qODMyCl97A7pBJLElUYv'. It is located between
the "https://docs.google.com/spreadsheets/d/" and "/edit..." in the URL
bar. Make sure you choose the correct Google Sheet ID as this ID is used
to identify the Google Sheet the script will update with the PeerTube
URL. In general, each batch of media objects will have its own unique
Google Sheet ID.

The Google Sheet can be a copy of a template file provided by MAD
uploaded to Google Sheets as long as it contains the required columns
listed above.

## Usage:

Script Usage Examples:

scan-batch-dir ---help

scan-batch-dir -h

scan-batch-dir ---config-file config.conf ---log-file batch_name.log
---directory {full path to the directory to be scanned}
---in-google-sheet-id {Google Sheet ID} ---in-google-sheet-name {Google
Sheet Tab Name} ---in-google-creds-file {full path to the Google
Credentials .json file}

## Function:

For each file or directory found in the directory provided update the
Google Sheet to ensure that the object is identified in the sheet at
least by adding the full path to the 'file' column.

If a .tif file is found, create a .jp2 file from the .tif file and
record the full path to the .jp2 file in the 'file' column of the Google
Sheet.

If a .jpg or .png file is found, add the full path to the file to the
'thumbnail' column of the Google Sheet.

If a .srt or .vtt file is found, add the full path to the file to the
'transcript' column of the Google Sheet.

## File/Directory Layout:

### Manuscripts/Books/Newspaper Issues

This file layout is based upon DRL scanning practices where there is a
folder for each object id and tif files for each scanned page. When
scan-batch-dir is run a .jp2 file is created for each tif file in the
Object ID Folder and this is the file that is referenced in the 'file'
column of the spreadsheet. The Object ID folder (parent) represents the
whole digital object eg. Book, vs. page of a book and will have its own
entry in the spreadsheet with no reference in the 'file' column. The
Object ID row in the spreadsheet is normally where metadata about the
Object can be found.

- Top Level Batch Folder/Object ID Folder/0001.tif

- Top Level Batch Folder/Object ID Folder/0002.tif

- Top Level Batch Folder/Object ID Folder/0003.tif

Eg. The following shows two batches each with a single object id and
each page scan is numbered using a four-character digit. This allows the
scanning station software to automatically increment the filename when
scanning a book/manuscript/newspaper issue.

- Batch A/31735...1/0001.tif

- Batch A/31735...1/0002.tif

- Batch B/31735...2/0001.tif

- Batch B/31735...2/0002.tif

### Oral Histories/Videos/Audio

This file layout puts all A/V content regardless of batch ID into the
top level batch folder. Each batch ID can have multiple files with
extensions. Video objects will have at the minimum an object id.mkv file
but may also have an optional object id.srt or object id.vtt as well as
an optional object id.png or object id.jpg. For these files we strictly
need only the Object ID referenced in the filename so as to match the
the object ID in the SpreadSheet. Adding additional information such as
comments, editors,etc. in the filename will result in issues in
processing.

Depending upon what files are found, the .mkv or .mp3 file will be added
to the 'file' column in the spreadsheet. The other objects with .srt or
.vtt will be added to the 'transcript' column in the spreadsheet and
objects with .jpg or .png will be added to the 'thumbnail' column in the
spreadsheet. This effectively identifies these three files correctly in
preparation for being uploaded to PeerTube.

- Top Level Batch Folder/Object ID.mkv (.mov, etc.)

- Top Level Batch Folder/Object ID.mp3

- Top Level Batch Folder/Object ID.srt

- Top Level Batch Folder/Object ID.vtt

- Top Level Batch Folder/Object ID.jpg

- Top Level Batch Folder/Object ID.png

Eg. A video or a video Oral History with no custom thumbnail.

- Batch 1/31735...1.mkv

- Batch 1/31735...1.srt

Eg. An audio or an audio Oral History with a custom thumbnail:

- Batch 2/31735...1.mp3

- Batch 2/31735...1.vtt

- Batch 2/31735...1.jpg

Eg. A video file with no transcript or thumbnail (no audio):

- Batch 1/31735...1.mkv

Describe how a video works when PeerTube or Islandora selects the
thumbnail image?

If no thumbnail is present for an audio object, our default thumbnail
(microphone) will be used. If no thumbnail is present for a video
object, upon upload to PeerTube, PeerTube will randomly select a
thumbnail from one of the video frames.

If no transcript/caption file is included, PeerTube will not include or
generate any closed captioning for the object.

Eg. An audio file with no transcript or thumbnail:

- Batch 1/31735...1.mp3

### Images

The file layout below also follows DRL scanning practices where files
are scanned and placed at the top-level batch folder. Each file has its
own Object ID that matches the 'id' column in the spreadsheet.

- Top Level Batch Folder/Object ID.tif

- Top Level Batch Folder/Object ID.tif

Eg. Scanning several Images:

- Batch 1/31735...1.tif

- Batch 1/31735...2.tif

- Batch 1/31735...3.tif
