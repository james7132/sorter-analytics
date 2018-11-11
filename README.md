# sorter-analytics

A Google Cloud Function project for ingesting character sorter results into a
BigQuery database.

## Format

## POST Payload format

The input format payload is a JSON object with two values: of a source to match
the paylod to, and and ordered JSON array of results. The results should be
ordered in descending order, with rank 1 in the sorter coming first in the array.

```json
{
  "source": "touhou",
  "results": [
    "Hakurei Reimu",
    "Remilia Scarlet",
    "Yakumo Yukari",
  ]
}
```

## Storage Format

On Google BigQuery's end, sorters are stored in a singular table with the
following columns:

|Column|Type|Mode|Description
|:--|:--|:--|:--|
|`source`|STRING|Required|Which dataset the sorter derived from.|
|`created`|DATETIME|Required|The date the sorter was created|
|`results`|INTEGER|Repeated|The hashed IDs of every entry that was input.|

**ID Format**: To save space in storing the results, the string inputs are hashed
using [xxHash-64](https://github.com/Cyan4973/xxHash) to produce a 64-bit integer
ID. These IDs are not expected to be transferable or matchable across multiple
datasets. For all intents and purposes of this project, no source should contain
enough elements for the resultant 64-bit hash to see serious issues with hash
collisions.

## Adding additional sources

This ingest function performs input vallidation based on known datasets. To add
additional, add a new file under `sources/` with a list of all of the expected
names, one per line.

**Supported Sources**

 * `touhou`: https://github.com/execfera/charasort

## Development

This project requires the Google Cloud SDK to be installed and uses Python 3.7.1.

To set up a development enviroment, it is suggested to use virtualenv to help
manage packages.

```bash
# Install Google Cloud SDK
sudo apt-get install google-cloud-sdk

# Clone the project
git clone https://github.com/james7132/sorter-analytics
cd sorter-analytics

# Create a virtualenv for the project
virtualenv -p python3 venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
