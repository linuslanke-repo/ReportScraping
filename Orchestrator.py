

from imports import *
print("Starting URLs Extractor")
script_1='Href_Links_Extractor_Saver.py'
script_2='Href_Downloader.py'
subprocess.run([sys.executable, script_1],check=True)

print("*************************** URL Extraction Completed **************************.")
subprocess.run([sys.executable, script_2],check=True,encoding='utf-8')
print("*************************** Reports Downloaded **************************.")
print("Pipeline Execution Finish")