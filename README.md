# ledger-nano-s-iota-installer

This tool can be used to install the IOTA app on the deprecated Ledger Nano S device.

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)

## Running the script

1. Download (Click on the `Code` button and `Download ZIP`) or clone this repository.
2. Open a terminal inside the unpacked ZIP or the repository if you cloned it.
3. Run the download script to download verify the checksum of the IOTA app:
```bash
uv run download.py
```
4. Now you can install the IOTA app with:
```bash
cd nanos
uv run ledgerctl install -f app_nanos.json
```
5. Follow the instructions on your Ledger Nano S device to complete the installation.

**Note:** If the installation fails and you see an error 5103 somewhere it is probably related to not having enough space on your Ledger Nano S device. You can try to remove some apps from your Ledger Nano S device to free up space. Afterwards, you can try to run the last command again.
