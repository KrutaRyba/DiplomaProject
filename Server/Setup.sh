#!/bin/sh

# Fail if anything fails
set -e

# Bold-formatted echo
becho() {
  local normal=$(tput sgr0)
  local bold=$(tput bold)
  local msg="${bold}$1${normal}"
  echo "${msg}"
}

becho "Installing osmium-tool"
case "$OSTYPE" in
  darwin*)
  brew update
  brew install osmium-tool
  ;; 
  linux*)
  sudo apt-get update
  sudo apt-get install osmium-tool
  ;;
  *)
  becho "${OSTYPE}: unsupported"
  exit 1
  ;;
esac

osm_folder="${HOME}/Downloads"
osm_file='ukraine-latest.osm.pbf'
files=(`find ${osm_folder} -maxdepth 1 -name ${osm_file}`)
if [ ${#files[@]} -eq 0 ]; then 
  becho "Dowloading ${osm_file} file to the ${osm_folder}"
  curl -L "https://download.geofabrik.de/europe/${osm_file}" --output "${osm_folder}/${osm_file}"
else
  becho "Using existing ${osm_file} file in the ${osm_folder}"
fi

server_config_file="ServerConfig.json"
becho "Modifying ${server_config_file}"
sed -i '' -r -e "s#\"osm_file\"[^,]*#\"osm_file\":\"${osm_folder}/${osm_file}\"#g" "${server_config_file}"

python3 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

pip install -r requirements.txt

deactivate
