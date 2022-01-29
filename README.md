<h1>Real-Time Competition Tracking System version 3</h1>
Program Kerja Divisi Eksternal BEM CIT 2021/2022 <br>
Helps in getting events from several instagram accounts. Events or competition scraped from these accounts will help university students find competitions to join. <br>
<h2>Install</h2>
1. Chrome browser must be installed <br>
2. Download <a href="https://sites.google.com/a/chromium.org/chromedriver/" rel="nofollow">chromedriver</a> and put it into  the program directory <br>
3. Install requirements: <code>pip install -r requirements.txt </code> <br>

<h2>Programs</h2>
- <code>main.py</code>: Main program to run.<br>
- <code>constants.py</code>: Manages constants taken from <code>
rcts-api-key-fake.json</code> and <code>
rcts_account_credentials.json </code>.<br>
- <code>google_api.py</code>: Contains class and methods used to connect to gsheets API.<br>
- <code>rdataframe.py</code>: Contains class and methods to manage data.<br>
- <code>filter.py</code>: Contains functions to filter competitions.<br>
- <code>ig_post.py</code>: Contains class of single instagram post.<br>
- <code>rselenium.py</code>: Manages chromebrowser commands.<br>

<h2>Constants</h2>
- <code>rcts-api-key-fake.json</code>: API key to connect to Google Sheets (emptied).<br>
- <code>rcts_account_credentials.json</code>: Instagram account credentials (password emptied).<br>

<h2>Input</h2>
Taken from google sheets. <br>

<h2>Run Program</h2>
Type in command prompt/terminal:<br>

```
python main.py
```
<h2>Output</h2>
This program inserts the filtered competitions to Google Sheets. 
