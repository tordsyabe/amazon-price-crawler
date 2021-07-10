import os
from dotenv import load_dotenv

load_dotenv()

print(os.environ.get("CHROMEDRIVER_PATH"))
print(os.environ.get("GOOGLE_CHROME_BIN"))