#!/bin/bash

# The script is used to download the latest city info from gitee.com/xiangyuecn/AreaCity-JsSpider-StatsGov

set -e

# Check https://github.com/xiangyuecn/AreaCity-JsSpider-StatsGov to update the latest version
echo "Downloading city info from gitee.com/xiangyuecn/AreaCity-JsSpider-StatsGov"
mkdir -p ${OUTPUT_JSON_DIR}
wget https://gitee.com/xiangyuecn/AreaCity-JsSpider-StatsGov/releases/download/2023.231212.240303/ok_geo.csv.7z -O ${OUTPUT_JSON_DIR}/ok_geo.csv.7z
echo "*****Successfully downloaded city info as ${OUTPUT_JSON_DIR}/ok_geo.csv.7z*****"

# Check whether 7z is installed
if ! [ -x "$(command -v 7z)" ]; then
  echo 'Error: 7z is not installed.' >&2
  echo 'Please install 7z by running `sudo apt-get install p7zip-full`' >&2
  exit 1
fi

rm -rf ${OUTPUT_JSON_DIR}/ok_geo.csv
7z x ${OUTPUT_JSON_DIR}/ok_geo.csv.7z -o${OUTPUT_JSON_DIR}
echo "*****Successfully extracted city info as ${OUTPUT_JSON_DIR}/ok_geo.csv*****"
