# Instagram geo-tagged posts Scraper:

[![Contact](https://img.shields.io/badge/Email-%20Contact-yellow.svg)](mailto:manuelhuala@outlook.com)



## Requirements:
These Python packages are required for the proper functioning

beautifulSoup4
PyQt5
requests

```sh
pip3 install -r requirements.txt
```


## Before using
This program will scrape near of 95% of public geo-tagged posts of any location only having the Unique ID that identify it on Instagram. It will be finded of three different ways:
 * On a geo-tagged posts clicking in the tag and seen it at the end of the URL before the name of the location. Like this example where the unique ID of Valdivia (Chilean city) is 212912788. 
```sh
        https://www.instagram.com/explore/locations/212912788/valdivia-chile/
```
 * [Instagram-scraper](https://github.com/arc298/instagram-scraper/) -  With this package installed, only put this into the terminal:
```sh
        instagram-scrapper --search-location {name_of_location}
```
 * Searching on [Instagram locations explorer](https://www.instagram.com/explore/locations/) then select one location and extract the unique ID like the first point.

We need to add our target locations on the *locations.JSON* file with this format : 
```sh
        { "location": "LOCATION_NAME", "id": LOCATION_ID, "lat": "LOCATION_LAT", "lng": "LOCATION_LNG" }
```

The fields of *lat* and *lng* can be avoided, but these are easy to get using the second way of obtain the unique ID location (with [Instagram-scraper](https://github.com/arc298/instagram-scraper/)) and would allow somebody do a geo-spatial analysis.

## Usage
It depends if we start from the beginning a new scrape or continue a scrape process from a specific end cursor ("pagination variable").

### *New Scrape*
We need to specify three things:
* **Posts per scrape** : Numeric value that represents how many posts are requested in each iteration of the script to Instagram's servers.
* **Posts per file** : Numeric value that represents aproximately how many posts will contain any file created with this program.
* We **need to click the name** of the target location on the table.

After that we click **Start Scrape** and wait to the script create the JSON files with the scraped info, these files have the next name format:
```sh
        E_C_{last_end_cursor_scraped}_Loc_id_{location_unique_id}_TP_{total_posts_of_the_scrape_process}.json
```
Obviusly the total_posts_of_the_scrape_process part of the name will start from 0 even if you are continuing a scrape from some point.

![new_scrape](https://user-images.githubusercontent.com/45650277/95585479-ae4ffa00-0a15-11eb-8a1c-1d8a85e304d8.gif)

### *Continue Scrape*
We need to specify four things:
* **Posts per scrape** : Numeric value that represents how many posts are requested in each iteration of the script to Instagram's servers.
* **Posts per file** : Numeric value that represents aproximately how many posts will contain any file created with this program.
* **End Cursor** : Numeric value that represents the last end_cursor scraped, it will be obtained from the last file created in the previous scrape process, in the filename after "**E_C_**" .
* We **need to click the name** of our location on the table.

After that we click **Continue Scrape** and wait to the script create the JSON files with the scraped info, you will see that the E_C_{value} part in the filenames will be decressing it means that the script follows well the "pagination" of the geo-tagged posts.

![continue_scrape](https://user-images.githubusercontent.com/45650277/95585321-75178a00-0a15-11eb-87a2-616f1055d84a.gif)
