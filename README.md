# NOAA Data Visualizer

![Screenshot from app][logo]

[logo]: screenshot.png "Screenshot from app"

This is project crawls the NOAA Satelite Files and produces a JSON file of data about those files like the number of files, folders and what types. This project builds network graph using plotly and displays it.

This dataset collected data from thousands of folders containing ~1 million images.

## How to Run

To run the code first run:
```bash
git clone https://github.com/SBCC-Web-Dev/NOAA-data-visualizer.git
cd NOAA-data-visualizer
pip install -r requirements.txt
```
Optionally you can run the web scraper:

```bash
python -m web-scraper
```
> [!NOTE]  
> It is not recommended to run the web scraper because it will take a long time (about 1.5 hours).
> And if you do you should modify the `DELAY`

Then run the visualizer:
```bash
python main.py
```

## Additional Notes
 
Big thanks to the National Oceanic and Atmospheric Administration (NOAA) for letting me scrape this data.

Feel free to use the data I have gathered or the code written here for your own use. Happy programming!

A challenge to those that are reading this: Write a program to count how many files and folders present in the dataset using a language you are less familiar with.