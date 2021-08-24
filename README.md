# UCI Transfer Equivalency Reverse Search
Students who wish to transfer from a California Community College (CCC) to a University of California (UC) or California State University (CSU) school predominantly use [Assist](www.assist.org) to find official course equivalencies. Assist is a unidirectional search: students enter their CCC, the CSU or UC to which they want to transfer, and their major, and Assist delineates the courses that fulfill the corresponding requirements. 

I offer here the ability to reverse that search, allowing students to start with a specific UC or CSU course requirement and then find all CCCs that offer an equivalent course. This is especially useful during the COVID-19 era, in which students can take classes online from schools across California. For the sake of simplicity (and personal relevance), I've limited my approach to UCI equivalencies, but the scripts I've included provide a strong point of departure for processing the Assist agreements for other schools.

I've used the data acquired from the scripts in this repository to create a search tool that displays requirements on [my website](https://www.jacobtbigham.com/transfers):

![Layout for UCI transfer reverse search](https://www.jacobtbigham.com/static/img/transfers/transfer.PNG)

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
Each articulation agreement has a unique ID number.

### 2. Extracting Text from the PDFs


### 3. Processing the Text


### 4. Aggregating the Data

