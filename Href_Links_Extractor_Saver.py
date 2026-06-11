

from imports import *
failed_url = []
extraction_summary_log=[]
def get_latest_pdf_href(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        href_list = []
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        try:
            accept_button = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree')]"
            )))
            driver.execute_script("arguments[0].click();", accept_button)
        except TimeoutException:
            pass

        elements = []
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))
            elements = driver.find_elements(By.TAG_NAME, "a")
        except TimeoutException:
            try:
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "tr")))
                elements = driver.find_elements(By.XPATH, "//tr//a")
            except TimeoutException:
                pass

        for element in elements:
            try:
                href = element.get_attribute("href")
                if href:
                    url_lower = href.lower()
                    if any(ext in url_lower for ext in [".pdf", "download", ".php", ".shtml"]):
                        if href not in href_list:
                            href_list.append(href)
            except Exception:
                continue

        if href_list:
            return href_list
        failed_url.append(url)
        # return "No PDF links found on the page."

    except WebDriverException:
        failed_url.append(url)
        return "Failed to load or process the page."
    finally:
        if driver:
            driver.quit()

target_urls = []
if os.path.exists(input_file):
    with open(input_file,encoding='utf-8') as file:
        target_urls =[line.strip() for line in file if line.strip()]
os.makedirs(OUTPUT_DIR,exist_ok=True)
for url in tqdm.tqdm(target_urls,desc="Extracting report URLs", unit="company_url"):
    link_name = urlparse(url).netloc.replace('www.', '').replace('.com', '')
    delay = random.uniform(1.5, 5.5)
    time.sleep(delay)
    result = get_latest_pdf_href(url)
    # print(result)
    if result:
        target_dir = os.path.join(OUTPUT_DIR, date_part)
        os.makedirs(target_dir, exist_ok=True)
        filepath = os.path.join(target_dir, f'{link_name}.txt')
        with open(filepath, 'w',encoding='utf-8') as f:
            for link in result:
                f.write(link + '\n')
        # print(f'Saved {len(result)} link(s) to {link_name}.txt')
        extraction_summary_log.append(f'Saved {len(result)} link(s) to {link_name}.txt')
    else:
        pass


print("\n --- EXTRACTION REPORT ----")
print(f'\n Failed URL(s) :')
for url in failed_url:
    print(url)
print(f'\n')
print("\n URLs count per each company website search:")
print("..........................................................")
print("\n".join(extraction_summary_log))
