# KODI Media File Cleaner


Cleans file and folder names of unwanted characters and media formats specified in the filename; ready for use on your Kodi setup.

### What it can do:
Reads all files and folders in root directory.
Removing all unwanted characters/names from files, folders and sub-folders in the root directory i.e.: `2000 bob's movie HDCAM 1280P Hevc Psa -Hive Pdtv Megusta` -> `Bob's Movie (2000)`.
It will also format TV shows files when specified _(e.g.: Folder: `Bob's TV Show (2000) S01`, File: `Bob's TV Show (2000) S01E01.mov`)_.
It can offer to remove any undesired files, either if they are not of a certain extension type or have known undesired content.

### What it can't do:
Clean any additional names such as directors, actors, or film types such as interview, short, comedy etc. That will have to be done manually.


### Set Up:
`make init`
OR
`pipenv sync -d`


### Run:
Change *\</Volumes/Media/Staging/* in MakeFile and use: `make run`

OR

`pipenv run main.py --filepath [/Path/To/Media/Staging/] --tv_shows 0`

For TV Shows run with `yes, true, t, y, 1` can be supplied with the second argument `--tv_shows`.

------------
# N.B. (Please Note)
The current setup expects your media directory to have two sub-folders: *films* and *shows*.
```
<Root>
└── films
|   └── <Bob's Movie (2000)>
|       └── <Bob's Movie (2000).mov>
|       └── <Bob's Movie (2000).srt>
└── shows
    └── <Bob's Show (1980)>
        └── <Bob's Show (1980) S01>
            └── <Bob's Show (1980) S01E01>
                └── <Bob's Show (1980) S01E01.mov>
                └── <Bob's Show (1980) S01E01.srt>
```
