

from imports import *
print("Starting URLs Extractor")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

script_1 = os.path.join(BASE_DIR, "Href_Links_Extractor_Saver.py")
script_2 = os.path.join(BASE_DIR, "Href_Downloader.py")

subprocess.run([sys.executable, script_1],check=True)

print("*************************** URL Extraction Completed **************************.")
subprocess.run([sys.executable, script_2],check=True,encoding='utf-8')
print("*************************** Reports Downloaded **************************.")
print("Pipeline Execution Finish")




