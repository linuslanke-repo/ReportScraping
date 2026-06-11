from imports import *

MAX_CONCURRENT_DOWNLOADS = 5
def highest_year_catcher(urls):
    year_pattern=re.compile(r'(19\d{2}|20\d{2})')
    max_year=0
    for url in urls:
        matches=year_pattern.findall(url)
        if matches:
            url_max=max(int(m) for m in matches)
            if url_max>max_year:
                max_year=url_max
    if max_year == 0:
        return urls
    return [url for url in urls if str(max_year) in url]
async def download_file(semaphore, session, url, LINKS_DIR):
    async with semaphore:
        try:
            parsed_url=urlparse(url)
            base_name= parsed_url.path.split('/')[-1].split('.')[0]
            if base_name.lower() in ['','download','index','php']:
                query_params=parse_qs(parsed_url.query)
                if 'id' in query_params:
                    base_name=f'report_{query_params["id"][0]}'
                else:
                    base_name=f'report_{abs(hash(url))}'
            file_name = f"{base_name}.pdf"
            file_path = os.path.join(LINKS_DIR, file_name)

            # impersonate="chrome110" flawlessly mimics a real Chrome browser's TLS signature
            response = await session.get(url, impersonate="chrome110",verify=False, timeout=60)

            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                # print(f"Success: {file_name}")
            else:
                print(f"Failed HTTP {response.status_code}: {url}")

        except Exception as e:
            print(f"Error on {url}: {str(e)}")


async def execute_bulk_download(urls, LINKS_DIR):
    """Orchestrates the asynchronous download queue."""
    os.makedirs(LINKS_DIR, exist_ok=True)

    # Semaphore controls how many files download at the exact same millisecond
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

    # AsyncSession maintains persistent connections where possible, boosting speed
    async with AsyncSession(verify=False) as session:
        tasks = [download_file(semaphore, session, url, LINKS_DIR) for url in urls]

        # Execute all tasks concurrently
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("Downloading Reports using extracted URLs")
    print("Filtering shtml links if any")

    if os.path.exists(LINKS_DIR):
        if not REPORTS_DIRECTORY:
            REPORTS_DIRECTORY = 'Report_Downloads'
            os.makedirs(REPORTS_DIRECTORY, exist_ok=True)
        TARGET_DIR = os.path.join(REPORTS_DIRECTORY, date_part)
        SOURCE_DIR=  os.path.join(LINKS_DIR, date_part)
        os.makedirs(TARGET_DIR, exist_ok=True)
        for filename in tqdm.tqdm(os.listdir(SOURCE_DIR),desc="Downloading Reports", unit="company"):
            if filename.lower().endswith('.txt'):
                file_path = os.path.join(SOURCE_DIR, filename)

                folder_name=os.path.splitext(filename)[0]
                COMPANY_NAME_DIR=os.path.join(TARGET_DIR,folder_name)
                os.makedirs(COMPANY_NAME_DIR, exist_ok=True)
                with open(file_path, 'r',encoding='utf-8') as file:
                    ALL_URLS = [line.strip() for line in file if line.strip()]

                #Filtering shtml links from ALL_URLS
                ALL_URLS=[url for url in ALL_URLS if ".shtml" not in url]

                if ALL_URLS and len(ALL_URLS)>10 :
                        URLS_TO_DOWNLOAD=highest_year_catcher(ALL_URLS)
                else:
                    URLS_TO_DOWNLOAD=ALL_URLS
                asyncio.run(execute_bulk_download(URLS_TO_DOWNLOAD, COMPANY_NAME_DIR))


