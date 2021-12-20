# UCI Transfer Equivalency Reverse Search
Students who wish to transfer from a California Community College (CCC) to a University of California (UC) or California State University (CSU) school predominantly use [Assist](https://www.assist.org) to find official course equivalencies. Assist is a unidirectional search: students enter their CCC, the CSU or UC to which they want to transfer, and their major, and Assist delineates the courses that fulfill the corresponding requirements. 

I offer here the ability to reverse that search, allowing students to start with a specific UC or CSU course requirement and then find all CCCs that offer an equivalent course. This is especially useful during the COVID-19 era, in which students can take classes online from schools across California. For the sake of simplicity (and personal relevance), I've limited my approach to UCI ICS (Information and Computer Sciences) equivalencies, but the scripts I've included provide a strong point of departure for processing the Assist agreements for other schools.

I've used the data acquired from the scripts in this repository to create a search tool that displays requirements on [my website](https://www.jacobtbigham.com/transfers):

![Layout for UCI transfer reverse search](https://www.jacobtbigham.com/static/img/transfers/transfer.PNG)

For a **tl;dr** (just show me the code) version of this information, see [here](#tldr).

## The Problem: Why hasn't this been done already?

Assist does not make scouring its data easy. In fact, the relevant data (the articulation agreements) are only available as PDFs—and those PDFs present data in two columns with variable formatting and language. These factors complicate assessing relationships between equivalent courses. 

Here is a snippet of a typical Assist articulation agreement:

![Typical Assist agreement](https://www.jacobtbigham.com/static/img/transfers/assist.PNG)

Packages for extracting text from PDFs will read this text horizontally, which complicates understanding *and* and *or* relationships between and within course equivalencies, especially when there are occasional agreements that don't include the *and* keyword for compound requirements.

There are also several additional notes, bullet points, comments, and keywords that populate Assist agreements in inconsistent and often unpredictable ways.

And then, of course, you have to actually access the PDFs for each school and major in order to do any meaningful processing—which requires using Assist's API, which is not necessarily intuitive.

So, to build a reverse Assist search, you have to first find all relevant PDFs, then creatively parse the information therein, then process the resulting semi-formatted text, then aggregate all CCC courses on their UC/CSU equivalencies. It's not the hardest task in the world—but for the vast majority of students, it's not worth the effort.

## A Solution: My approach and the scripts in this repository

### 1. Finding and Downloading PDFs
Each articulation agreement has a unique ID number, which you can access from the Assist API if you know the receiving school (UC/CSU) ID, sending school (CCC) ID, year code, and major. For example, https://assist.org/api/agreements?receivingInstitutionId=76&sendingInstitutionId=113&academicYearId=72&categoryCode=major will direct you to a JSON file with the agreement ID numbers (keys) for students transferring from De Anza College (school ID 113) to Cal State Los Angeles (school ID 76) for the 2021-2022 year (year ID 72). By default, I grab only the most recent—valid—agreements

School IDs are available at https://assist.org/api/institutions, and year IDs are simply years since 1950 (so, for example, year ID 49 would be the 1998-1999 cycle).

To find which schools have articulation agreements with each other, visit, for example, https://assist.org/api/institutions/113/agreements. That takes you to a JSON file with all schools that have articulation agreements with Cal State Los Angeles and the years for which they have agreements stored on Assist.

Once you have the key for a particular agreement, you can access the PDF at https://assist.org/api/artifacts/{key_val}. For instance, the key for the 2021-2022 articulation agreement for Nursing - B.S. from De Anza College to Cal State Los Angeles is 25330408, so https://assist.org/api/artifacts/25330408 takes you to that agreement.

In the included files, the PDFGrabber class finds and downloads agreements for a given destination (UC/CSU) school and major. The major name must exactly match that in the agreements JSON (e.g., https://assist.org/api/agreements?receivingInstitutionId=76&sendingInstitutionId=113&academicYearId=72&categoryCode=major). In the case that the receiving (UC/CSU) school does not have information at this URL, change the categoryCode from *major* to *dept*.

When constructing a PDFGrabber, the major_code parameter is used for naming the PDFs that are stored on your machine, and the delay (in seconds) parameter is the time between successive API requests (there are roughly 200 requests for each school/major combination).

I decided to store the PDFs locally to facilitate inspecting agreements for debugging and verification.

To find and download the articulation agreements for the Computer Science major at UCI, for example, run the following:

```
from pdfgrabber import PDFGrabber
grabber = PDFGrabber(120, 'Computer Science, B.S.', 'CS', 0.2)
grabber.get_pdfs()
```

This will store all Computer Science articulation agreements to UCI in the `/agreements` folder relative to the location for the `pdfgrabber.py` script.

### 2. Extracting Text from the PDFs and Processing
Each articulation agreement is processed to create a dictionary whose keys are the required courses from a UC or CSU and whose values are the equivalent courses at the CCC. This functionality is carried out by the PDFExtractor class.

The desired approach to processing the text in the PDFs is a hybrid between vertical and horizontal scanning, as we want to process horizontal blocks in vertical succession. I found that splitting each page into horizontally-split halves and then merging them back together allowed [pdfminer](https://pypi.org/project/pdfminer/) to process the agreement text accordingly.

Agreements for different majors have different structure and additional sections. The logic I used for processing the UCI ICS major agreements will not immediately extend to, for example, most humanities majors. If you wish to 

I split the agreement text on a regular expression for unit values for each class—like (4.00). To me, that was the most obvious way to insure I was splitting classes, since every class has a unit value on the agreements. However, that incurs some additional considerations for extra text (like "Same-As:" and any bulleted information) that does not contain a unit value. The logic for processing the agreements is found in the process_page function in the PDFExtractor class. It's not a pretty function, but it's not especially complicated. The general approach is to find all the components of a requirement (indicated by *and* and *or* keywords), then find all the components of the equivalent, and finally add that pair to a dictionary. The majority of courses do not have equivalents at CCCs, as indicated by "No Course Articulated" in the agreements. Such courses are ignored.

I initially considered creating a state machine as a more elegant way of tokenizing the text input, but I figured that a simple if-else structure—though it would be a little clunky—would ultimately be easier to debug and easier for others to extend and alter.

After having [downloaded](#1-finding-and-downloading-pdfs) the agreement PDFs, you should have an `agreements` directory with a collection of files named similar to `report_120_54_CS.pdf` (where the 120 here is the ID of the receiving school, 54 is the ID of the sending school, and CS is the code you entered to represent the major whose files you scraped). To convert that file to a dictionary of major requirements to equivalent courses, you would run the following:

```
extractor = PDFExtractor('report_120_54_CS.pdf')
reqs_to_equivs = extractor.process_page()
```

Of course, we want to process all the agreements (roughly 100) for each major and create a JSON file that relates all equivalencies, which we do next.


### 3. Aggregating the Data
Armed with the ability to scrape the equivalencies for each PDF (and to generate a dictionary mapping requirement to equivalent), we can aggregate them on the requirements to generate a JSON file that maps requirements to a list of equivalent courses from all schools. This is a relatively straightforward process (simply iterating over successive PDFExtractors), and it is performed by the DatabaseMaker class.

The full sequence of calls to fetch PDFs, extract text, and aggregate into a JSON file is as follows:

```
grabber = PDFGrabber(120, 'Computer Science, B.S.', 'CS', 0.2)
id_to_key = grabber.get_pdfs()
maker = DatabaseMaker('UCI', 'CS', id_to_key)
maker.add_classes()
```

Note that, unlike in the [previous call](#1-finding-and-downloading-pdfs) to get_pdfs(), we're explicitly storing the id_to_key dictionary.

This code takes a couple minutes to run. The result is a roughly-finished JSON file that outlines the schools with courses that meet the requirements for the school and major you supplied.

### 4. Manual Editing
Because of inconsistencies in formatting, you will likely need and want to make manual adjustments to the resulting JSON file. Having the PDFs saved locally allows you to quickly find discrepancies as they arise in the JSON file. If you explore different majors and different schools, you'll likely find you need to perform substantial post-processing (and, likely, editing to the process_page function in the PDFExtractor class).

## Front-End
For security reasons, I won't share the back-end interface for connecting the front-end to the data generated by the scripts in this repository—but the approach is straightforward: list available majors, then use ajax to send a call for the corresponding courses (when a user selects a major), and finally use ajax to send a call for the equivalencies (when a user selects a required major course).

The interface appears as follows:

![Front-end interface for reverse transfer search](https://www.jacobtbigham.com/static/img/transfers/transfer_animation.gif)

## TL;DR
If you want to generate a JSON file that contains a list of CCCs with courses that meet particular CSU or UC requirements, then use do the following:
1. Find the UC or CSU's school ID at https://assist.org/api/institutions
2. Find the specific major for which you want to find course equivalencies (if you run into errors for your destination school, then you made need to change the categoryCode to *dept* in line 30 of `pdfgrabber.py`
3. Decide on a nickname for the major (like "CS" for Computer Science) and pick a delay time for API calls (like 0.2 seconds)
4. Run the following code in a Python shell:

	```
	from pdfgrabber import PDFGrabber
	from databasemaker import DatabaseMaker
	school_id = ENTER_SCHOOL_ID_HERE
	school_name = ENTER_SCHOOL_NAME_HERE
	major = ENTER_MAJOR_HERE
	nickname = ENTER_NICKNAME_HERE
	delay = ENTER_DELAY_HERE
	grabber = PDFGrabber(school_id, major, nickname, delay)
	id_to_key = grabber.get_pdfs()
	maker = DatabaseMaker(school_name, nickname, id_to_key)
	maker.add_classes()
	```

5. Manually edit the resulting JSON file.

You very likely will find that you need to edit some of the logic in the process_page function in `pdfextractor.py` to get a clean JSON file. I left the logic I used for producing clean files for ICS majors at UCI.
