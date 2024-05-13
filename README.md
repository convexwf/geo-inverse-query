# geo-inverse-query

This is a simple Python script that queries the region of a given latitude and longitude.

## Prerequisites

- Docker
- Docker-compose

## How to use

Very simple.

Just run the script with the following command to initialize the environment:

```bash
# git clone
$ bash build.sh
```

The script will do the following:

1. Build the docker image from `src/` directory.
   - The docker image is based on `python:3.10-slim`.
   - During the build, the script will install the required Python packages.
2. Deploy the docker container and the MongoDB container.
3. Initialize DB
   - Download the polygon data via `wget` tool.
   - Extract the polygon data from the downloaded file and save them as json files.
   - Read the extracted polygon data from json file and insert them into the MongoDB.

Then you can use the following command to enter the container:

```bash
# enter the container
$ bash dev_into.sh
```

## Examples

### [command line]

```bash
# [command line]
$ python geo_engine.py --lat 23.1667 --lon 113.2333
ID: 440111, Name: 广东省广州市白云区
```

### [interactive mode]

```bash
# [interactive mode]
$ python geo_engine.py -i
Please input the latitude of the location: 23.1667
Please input the longitude of the location: 113.2333
ID: 440111, Name: 广东省广州市白云区
Continue? (Y/n):
```

### [from file]

```bash
# [from file]
$ python geo_engine.py -f test_data/input.txt -o test_data/output.csv
```

### Exit the container

```bash
# exit the container
$ exit
```

### GCJ-02 Coordinate System Support

The query result is based on the WGS-84 coordinate system. If you want to query the region of a given latitude and longitude in GCJ-02 coordinate system, you can add the `--coords gcj02` option.

```bash
# [command line]
$ python geo_engine.py --lat 23.1667 --lon 113.2333 --coords gcj02
# [interactive mode]
$ python geo_engine.py -i --coords gcj02
# [from file]
$ python geo_engine.py -f test_data/input.txt -o test_data/output.csv --coords gcj02
```

## Further Information

### How to update the polygon data

If you want to update the polygon data by yourself, you can refer to `https://github.com/xiangyuecn/AreaCity-JsSpider-StatsGov` to get detailed information.

The above link only provides the polygon data of China.

I will offer the support for the polygon data of other countries in the future.

### Clean the environment

If you want to clean the environment, you can use the following command:

```bash
# clean the environment
$ bash clean.sh
```

The script will do the following:

- Stop and remove the docker container.
- Remove the docker image.
- If needed, remove untagged images.
