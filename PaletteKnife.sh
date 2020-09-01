#!/bin/bash

# Binary file URL
BINARY_URL='https://github.com/Steveice10/GameYob/releases/download/1.0.8/GameYob.zip'
ZIP_FILE_NAME="GameYob.zip"
UNZIPPED_DIR="3ds-arm"
ELF_FILE_NAME="GameYob.elf"

# Make sure that we're in the same directory as the script.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd ${DIR}

header="IOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiCAgICAgICAgICAgIOKWiOKWiOKWiOKWiCAgICAgICAgICAgIOKWiOKWiOKWiOKWiOKWiCAgICAg4paI4paI4paI4paI4paIICAgICAgICAgICAgDQrilpHilpHilojilojilojilpHilpHilpHilpHilpHilojilojiloggICAgICAgICAg4paR4paR4paI4paI4paIICAgICAgICAgICDilpHilpHilojilojiloggICAgIOKWkeKWkeKWiOKWiOKWiCAgICAgICAgICAgICANCiDilpHilojilojiloggICAg4paR4paI4paI4paIICDilojilojilojilojilojiloggICDilpHilojilojiloggICDilojilojilojilojilojiloggIOKWiOKWiOKWiOKWiOKWiOKWiOKWiCAgIOKWiOKWiOKWiOKWiOKWiOKWiOKWiCAgICDilojilojilojilojilojiloggDQog4paR4paI4paI4paI4paI4paI4paI4paI4paI4paI4paIICDilpHilpHilpHilpHilpHilojilojiloggIOKWkeKWiOKWiOKWiCAg4paI4paI4paI4paR4paR4paI4paI4paI4paR4paR4paR4paI4paI4paI4paRICAg4paR4paR4paR4paI4paI4paI4paRICAgIOKWiOKWiOKWiOKWkeKWkeKWiOKWiOKWiA0KIOKWkeKWiOKWiOKWiOKWkeKWkeKWkeKWkeKWkeKWkSAgICDilojilojilojilojilojilojiloggIOKWkeKWiOKWiOKWiCDilpHilojilojilojilojilojilojiloggICDilpHilojilojiloggICAgICDilpHilojilojiloggICAg4paR4paI4paI4paI4paI4paI4paI4paIIA0KIOKWkeKWiOKWiOKWiCAgICAgICAgIOKWiOKWiOKWiOKWkeKWkeKWiOKWiOKWiCAg4paR4paI4paI4paIIOKWkeKWiOKWiOKWiOKWkeKWkeKWkSAgICDilpHilojilojilogg4paI4paI4paIICDilpHilojilojilogg4paI4paI4paI4paR4paI4paI4paI4paR4paR4paRICANCiDilojilojilojilojiloggICAgICAg4paR4paR4paI4paI4paI4paI4paI4paI4paI4paIIOKWiOKWiOKWiOKWiOKWiOKWkeKWkeKWiOKWiOKWiOKWiOKWiOKWiCAgIOKWkeKWkeKWiOKWiOKWiOKWiOKWiCAgIOKWkeKWkeKWiOKWiOKWiOKWiOKWiCDilpHilpHilojilojilojilojilojiloggDQrilpHilpHilpHilpHilpEgICAgICAgICDilpHilpHilpHilpHilpHilpHilpHilpEg4paR4paR4paR4paR4paRICDilpHilpHilpHilpHilpHilpEgICAgIOKWkeKWkeKWkeKWkeKWkSAgICAg4paR4paR4paR4paR4paRICAg4paR4paR4paR4paR4paR4paRICANCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICANCiDilojilojilojilojiloggICDilojilojilojiloggICAgICAgICAgICAg4paI4paI4paIICAgICDilojilojilojilojilojiloggICAgICAgICAgICAgICAgICAgICAgICAgICANCuKWkeKWkeKWiOKWiOKWiCAgIOKWiOKWiOKWiOKWkSAgICAgICAgICAgICDilpHilpHilpEgICAgIOKWiOKWiOKWiOKWkeKWkeKWiOKWiOKWiCAgICAgICAgICAgICAgICAgICAgICAgICAgDQog4paR4paI4paI4paIICDilojilojiloggICAg4paI4paI4paI4paI4paI4paI4paI4paIICAg4paI4paI4paI4paIICAg4paR4paI4paI4paIIOKWkeKWkeKWkSAgIOKWiOKWiOKWiOKWiOKWiOKWiCAgICAgICAgICAgICAgICAgIA0KIOKWkeKWiOKWiOKWiOKWiOKWiOKWiOKWiCAgICDilpHilpHilojilojilojilpHilpHilojilojilogg4paR4paR4paI4paI4paIICDilojilojilojilojilojilojiloggICAg4paI4paI4paI4paR4paR4paI4paI4paIICAgICAgICAgICAgICAgICANCiDilpHilojilojilojilpHilpHilojilojiloggICAg4paR4paI4paI4paIIOKWkeKWiOKWiOKWiCAg4paR4paI4paI4paIIOKWkeKWkeKWkeKWiOKWiOKWiOKWkSAgICDilpHilojilojilojilojilojilojiloggICAgICAgICAgICAgICAgICANCiDilpHilojilojilogg4paR4paR4paI4paI4paIICAg4paR4paI4paI4paIIOKWkeKWiOKWiOKWiCAg4paR4paI4paI4paIICAg4paR4paI4paI4paIICAgICDilpHilojilojilojilpHilpHilpEgICAgICAgICAgICAgICAgICAgDQog4paI4paI4paI4paI4paIIOKWkeKWkeKWiOKWiOKWiOKWiCDilojilojilojilogg4paI4paI4paI4paI4paIIOKWiOKWiOKWiOKWiOKWiCAg4paI4paI4paI4paI4paIICAgIOKWkeKWkeKWiOKWiOKWiOKWiOKWiOKWiCAgICAgICAgICAgICAgICAgIA0K4paR4paR4paR4paR4paRICAg4paR4paR4paR4paRIOKWkeKWkeKWkeKWkSDilpHilpHilpHilpHilpEg4paR4paR4paR4paR4paRICDilpHilpHilpHilpHilpEgICAgICDilpHilpHilpHilpHilpHilpEgICAgICAgICAgICAgICAgICAgDQp2MS4xIC0gMzAvMDgvMjAyMA=="

if [[ "$OSTYPE" == "darwin"* ]]; then
    base64 -D <<< ${header}
else
    base64 -d <<< ${header}
fi
echo
echo
if [ ! -f "${ELF_FILE_NAME}" ]; then
    echo "${ELF_FILE_NAME} not found."
    echo "Downloading replacement."
    # curl -L "${BINARY_URL}" -o "${ZIP_FILE_NAME}"
    echo
    echo "Download complete. Extracting contents..."
    unzip -qq "${ZIP_FILE_NAME}" 
    cp "${UNZIPPED_DIR}/${ELF_FILE_NAME}" "./"
    rm -r "${UNZIPPED_DIR}"
    echo "Extraction complete."
    echo "Proceeding to binary manipulation."
fi

echo
echo
echo
python3 elf_edit.py  # Edit the binary file.
echo
echo "Compiling new .cia file from modified binary."
chmod +x ./makerom  # Ensure that we can actually execute the compiler application.
./makerom -f cia -o GameYob.cia -elf GameYob.elf -DAPP_ENCRYPTED=false -rsf ref/template.rsf -target t -exefslogo -icon ref/icon.icn -banner ref/banner.bnr -major 1 -minor 0 -micro 8 -DAPP_TITLE="GameZob" -DAPP_PRODUCT_CODE="CTR-P-GYOB" -DAPP_UNIQUE_ID="0xF8003" -DAPP_SYSTEM_MODE="64MB" -DAPP_SYSTEM_MODE_EXT="Legacy" -DAPP_CATEGORY="Application" -DAPP_USE_ON_SD="true" -DAPP_MEMORY_TYPE="Application" -DAPP_CPU_SPEED="268MHz" -DAPP_ENABLE_L2_CACHE="false" -DAPP_VERSION_MAJOR="1" -logo "ref/logo.bcma.lz"
echo "Compilation complete."
echo "Gameyob.cia now ready for installation."
