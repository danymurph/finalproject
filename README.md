**About The Project**

The Pathway Exploration and Analysis tool is a web-based application designed to help bioinformatics researchers and students explore metabolic and regulatory pathways in Escherichia coli K-12 MG1655. 
This tool provides an intuitive interface for searching, filtering and examining pathway metadata, focusing on enhancing the understanding of cellular processes 

**Features:**
  - Pathway Search:
    - Search pathwyas by names, IDs, or functional roles
    - Autocomplete suggestions as you type
    - Results are displayed dynamically without reloading the page
  - Detailed Pathway Information:
    - View pathway names, classes, and descriptions
    - Expandable sections to display additional details
  - Interactive User interface:
    - Clean, responsive design with collapsible sections
    - Asynchronous data loading for seamless experience
  - Backend and Database:
    - Pathway data stored in MySQL database
    - Scripts for populating and querying pathway data
    - Results and suggestions returned as JSON for dynamic frontend rendering.

**Technical Stack**
  - Frontend:
    - HTML5, CSS, JavaScript, JQery
    - Responsive design with a focus on usability
  - Backend:
    - Python CGI scripts for database interaction
    - MySQL for storing and managing pathway metadata
  - Deployment:
    - Runs on a class-provided server.
    - Fully self-contained with database and static assets
   
**Project Structure**
  - index.html:
    - The main entry point for the application. Contains the search interface and sections
    - for displaying results
  - style.css:
    - Style sheet for the application. Provides a clean and professional look with
      responsive design
  - script.js
    - Javascript file handling user interactions, AJAX requests, and dynamic content
      rendering.
  - search_pathways.cgi
    - Backend script for handling search and suggestion queries. Interacts with the mySQL
      database and returns JSON responses
  - populate_pathways.py
    - Script for populating the database with pathway metadata from text files. Processes
      both basic pathway metadata and detailed descriptions.
      
  **Database Schema**
  
   - Single pathway table with fields for pathway ID, name, description, and class.
   - Optimized for fast keyword searches with indexed fields

****Getting Started****

**Prerequisites**
- Python 3.x with mysql-connector library
- MySQL database
- A web server capable of running Python CGI scripts

**Setup Instructions**
1. Clone the repository:

   ```bash
   git clone https://github.com/danymurph/finalproject.git
   cd finalproject
  
3. Set Up the Database:
   
   ```Import the Pathway table schema:
     
     CREATE TABLE Pathway (
     pathway_id INT AUTO_INCREMENT PRIMARY KEY,
     pathway_name VARCHAR(255) NOT NULL,
     description TEXT,
     class TEXT);

 4. Run populate_pathways.py to load data:
    
        python3 populate_pathways.py
   
 5. Configure the Web Server:
    - Place the files (index.html, style.css, script.js, search_pathways.cgi) in your
    web server's document root
    - Ensure the server is configured to execute .cgi scripts
 6. Access the Application:
    - Open index.html in a browser or navigate to the deployed server's URL

**Usage**
- Enter a search term in the search bar (e.g., 'glycolysis')
- Browse suggestions or view detailed results for pathways
- Click on pathway names for additional descriptions

**Future Work**
- Intergration of gene-to-pathway mappings for enhanced insights
- Visualization of pathways using interactive charts or maps
- Cross-referencing pathways with external databases



