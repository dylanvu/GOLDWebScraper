# GOLDWebScraper

This is a Web Scraper to track the available course spaces of classes in any department in UCSB GOLD. The Web Scraper utilizes Selenium to log the user into GOLD and navigate to web pages and BeautifulSoup to parse though the HTML.

## Prerequisites Before Using

Microsoft Excel is required to edit .xlsx files and to view them.

Python

An IDE (I used PyCharm) to run the main.py script

Some other stuff. Not too sure yet, maybe setting up a virutal environment? Installing the necessary Python libraries/frameworks? The .venv from PyCharm is included so this may not be necessary. Not too sure.

## Using the Program

Open up the Excel file called "Input Sheet" and input the courses and departments that you are interested in.

It's important that the first row is only the shortened department name as seen on the GOLD dropdown menu. So, Chemical Engineering is CH E, Computer Science is CMPSC. etc.

Under the department (second row onwards), enter in the course number. For example, Computer Science 16 would be "16" under the the header CMPSC. Please ensure that there are no gaps between courses. If you want to scrape the entire department, type in "All" in the box under the department.

Please refer to the "Example Input Sheet" for an example of a properly formatted input sheet.

Next, modify the .env file with your GOLD username and password. Ensure that they are in quotations.

Finally, run main.py! The print statements will tell you how far the program is along/what it is doing. When the script is done, there should be a new Excel sheet named "Output Sheet." See "Example Output Sheet."

Please note that if you run the program again, the old sheet will be overwritten. So it will be best to copy the values onto a separate Excel sheet. Future development of this program will improve functionality.
