## project description

Product specifications extractor driven by Neural Network classifiers that exploit some domain 
knowledge

## how to run

The project is already trained on the domain "Cameras".

    pip install -r requirements.txt
    python main.py <url>

for example:

    > python main.py "https://www.dpreview.com/products/canon/slrs/canon_eosm50"
    ...
    > cat result.json
    {
    "Articulated LCD": "Fully articulated",
    "Body type": "SLR-style mirrorless",
    "Dimensions": "116 x 88 x 59 mm (4.57 x 3.46 x 2.32″)",
    "Effective pixels": "24 megapixels",
    "Focal length mult.": "1.6×",
    "Format": "MPEG-4, H.264",
    "GPS": "None",
    "ISO": "Auto, 100-25600 (expands to 51200)",
    "Lens mount": "Canon EF-M",
    "Max resolution": "6000 x 4000",
    "Max shutter speed": "1/4000 sec",
    "Screen dots": "1,040,000",
    "Screen size": "3″",
    "Sensor size": "APS-C (22.3 x 14.9 mm)",
    "Sensor type": "CMOS",
    "Storage types": "SD/SDHC/SDXC slot (UHS-I compatible)",
    "USB": "USB 2.0 (480 Mbit/sec)",
    "Weight (inc. batteries)": "390 g (0.86 lb / 13.76 oz)",
    "__unstructured": []
    }

The standard output shows informations about every Table and List found 
on the specified URL.  
Every red row, is a table/list that the classifier has tagged as `unrelevant` and so skipped.  
Every green row is a table/list that the classifier think is relevant about the trained domain 
and is reported on the final `result.json`.

The `result.json` file shows every information extracted.  
The system tries to extract <key, value> pairs and whenever it can't put the informations
on a special key named `__unstructured`.

## classifiers

The project uses two simple classifiers implmented with Keras and saved on `models/`.  

The two notebooks `list_classifier` and `table_classifier` show the process of 
traning/testing/saving of the models.  

The data on which they are trained is on `data/and/` which contains:

   1. `list.csv`: features values extracted on not_relevant/relevant lists
   2. `table.csv`: features values extracted on not_relevant/relevant tables
   3. `camera_hot_words.txt`: 200 *stems* of relevant words about the "Cameras" domain 
