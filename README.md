# skilling-2
Solution of Exercise 2

I have chosen Python instead of Java because it is much more effective for selenium based UI testing. 

Installation steps:
1. Clone the repo
2. Create Python virtual environment python3 ```python-m venv my_env```
3. Activate virtual environment ```source ./my_env/bin/activate```
4. Install dependencies ```pip install -r requirements.txt```
5. Install required browser drivers (I was testing with chrome and chromedriver) and add them to PATH
6. Launch the tests: ```behave -f allure_behave.formatter:AllureFormatter -o results -D PRODUCT=CDB -D ENV=TEST -D REMOTE=false -D CONFIG_FILE=config/chrome.json ./features/cdb_smoke_test.feature```
7. In order to view the results: ```allure serve ./results```

Features:
- Support of main browsers
- BrowserStack support - more info on https://www.browserstack.com/ (add credentials and set REMOTE to true)
- support of headless execution (launch with HEADLESS as true)
- support of multiple target environments and products

Example results:

![Alt text](/cdb.png?raw=true "Allure report")
