from github import Github
import re
import hashlib
import requests

def get_asset_info(id: int | str, asset_name: str):
    """
    Fetches information about a specific asset from a GitHub release.
    Args:
        id (int | str): The ID or tag name of the release to fetch.
        asset_name (str): The name of the asset to search for in the release.
    Returns:
        tuple: A tuple containing the asset's download URL (str) and its SHA256 hash (str).
    """
    g = Github()

    repo = g.get_repo("iotaledger/ledger-app-iota")
    release = repo.get_release(id)
    release_assets = release.get_assets()
    release_text = release.raw_data['body']

    sha256 = re.search(rf'\|.*{re.escape(asset_name)}.*\|([a-f0-9]{{64}})\|', release_text).group(1)

    for asset in release_assets:
        if asset.name == asset_name:
            return asset.browser_download_url, sha256
        
def download_and_verify(url: str, sha256: str):
    """
    Downloads a file from a URL and verifies its SHA256 hash. Stores the file in the current directory.
    Args:
        url (str): The URL to download the file from.
        sha256 (str): The expected SHA256 hash of the file.
    Returns:
        bool: True if the file's hash matches the expected hash, False otherwise.
    """

    # Download the file
    response = requests.get(url)
    filename = url.split('/')[-1]

    with open(filename, 'wb') as f:
        f.write(response.content)

    # Calculate the SHA256 hash of the downloaded file
    sha256_hash = hashlib.sha256()
    with open(filename, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    # Compare the calculated hash with the expected hash
    print(f"Calculated SHA256: {sha256_hash.hexdigest()}")
    print(f"Expected SHA256: {sha256}")
    return sha256_hash.hexdigest() == sha256

def unpack(filename: str):
    """
    Unpacks a tar.gz file.
    Args:
        filename (str): The name of the tar.gz file to unpack.
    """
    import tarfile
    with tarfile.open(filename, 'r:gz') as tar:
        tar.extractall(filter='fully_trusted')


def main():
    file_name = 'nanos.tar.gz'
    url, hash = get_asset_info('ledger-app-iota-v0.9.2', file_name)
    val = download_and_verify(url, hash)
    if val:
        print("Hash verified successfully.")
    else:
        print("Verification failed.")
        return -1

    unpack(file_name)

if __name__ == "__main__":
    main()
