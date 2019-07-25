"""
Created on Jul 25, 2019

@author: ben
"""
import yaml

class ConfigFile:
    
    def create_clean_file(self):
        arg_dict = {}
        arg_dict["clean_xml"] = True;
        arg_dict["copy_root"] = "./";
        arg_dict["new_root"] = "./new_root/"
        with open("./clean_xml.yaml", "w") as yml_file:
            yaml.dump(arg_dict, yml_file)
    
    def create_default_file(self):
        """
        Generate the default config file using the arg_dict dictionary. Use this to create the yaml object. 
        """
        arg_dict = {}
        arg_dict["General"] = {}
        arg_dict["General"]["generate_xml"] = True
        arg_dict["General"]["root"] = "./"
        
        arg_dict["Database Connection"] = {}
        arg_dict["Database Connection"]["database_server"] = "localhost"
        arg_dict["Database Connection"]["database"] = "database"
        arg_dict["Database Connection"]["database_type"] = "pgsql"
        arg_dict["Database Connection"]["database_port"] = "5432"
        arg_dict["Database Connection"]["database_user"] = "user"
        arg_dict["Database Connection"]["database_password"] = "password"
        
        arg_dict["Project"] = {}
        arg_dict["Project"]["project_name"] = "Project Name"
        arg_dict["Project"]["project_type"] = "1"
        
        arg_dict["Project"]["checkout_timeout"] = "600"
        arg_dict["Project"]["project_owner_user_name"] = "project user"
        arg_dict["Project"]["project_owner_email"] = "project_user@email.com"
        arg_dict["Project"]["project_owner_first_name"] = "Project"
        arg_dict["Project"]["project_owner_last_name"] = "User"
        arg_dict["Project"]["category_text_folder"] = "category_text"
        arg_dict["Project"]["document_text_folder"] = "document_text"
        
        arg_dict["Threading and Queues"] = {}
        arg_dict["Threading and Queues"]["job_queue"] = False
        arg_dict["Threading and Queues"]["threads"] = 1
        
        arg_dict["Files to Read"] = {}
        arg_dict["Files to Read"]["no_text"] = False 
        arg_dict["Files to Read"]["no_csv"] = False 
        arg_dict["Files to Read"]["no_pdf"] = False 
        arg_dict["Files to Read"]["no_docx"] = False
        
        arg_dict["Files to Read"]["csv_id"] = ["id", "Id", "ID", "IDENTIFIER"]
        arg_dict["Files to Read"]["csv_text"] = ["text", "TEXT", "SEARCH FIELD", "charge"]
        arg_dict["Files to Read"]["csv_category"] = ["ncic_code"]
        with open("./config.yaml", "w") as yml_file:
            yaml.dump(arg_dict, yml_file)
    
    def create_default_with_comments(self):
        """
        Use the default config file to create a large string here and add comments.  
        """
        
        s = """# Generated with comments, please tailor this to your needs and continue. 
General:
  # This will generate the xml. The other option is to clean it. There is an associated configuration file to clean. 
  # To use that configuration file, copy this file and rename the clean_xml.yaml file to config.yaml in this directory
  generate_xml: true
  
  # The root path 
  root: ./
  
Database Connection:
  # The database server to connect to
  database_server: localhost
  
  #The database to use
  database: database
  
  #The database user to use
  database_user: user
  
  #The database user's password
  database_password: password
  
  #The database type. Only pgsql is supported right now
  database_type: 'pgsql'
  #The database port, the default is the default pgsql port. 
  database_port: '5432'
  
Project:
  # The project name
  project_name: Project Name
  
  # The project type. This should only be 1 for now to denote a dual validation project. 
  #If additional projects are added, update this configuration, the xml files, the project files, and the database. 
  project_type: '1'
  
  #The timeout for how long users can reserve a document.  
  checkout_timeout: '600'
  
  # User information
  # If this user is not in the database, it will create this user. 
  project_owner_user_name: project user
  project_owner_email: project_user@email.com
  project_owner_first_name: Project
  project_owner_last_name: User
  
  # The folder containing the category and document text data. 
  # The category folder only gets used when reading in category data.
  # The document folder only gets used when reading in document data (data to categorize). 
  category_text_folder: category_text
  document_text_folder: document_text
  
Files to Read:
  # Files to read. Set to true to NOT read files of this type.
  # Setting this to false will read that file type. 
  no_csv: false
  no_docx: false
  no_pdf: false
  no_text: false

  # The id columns in the csv files.
  # Please note that this list is not exhaustive. If your csv files contain id columns with names that are not in this list, add them here.
  csv_id:
  - id
  - Id
  - ID
  - IDENTIFIER
  
  #The text columns in the csv files. 
  csv_text:
  - text
  - TEXT
  - SEARCH FIELD
  - charges
  
  # The category columns. This is almost certainly going to be project-specific. 
  csv_category:
  - ncic_code
  
Threading and Queues:
  # If job_queue is set to true, this will create xml files that will use a queue system rather than threads
  job_queue: false
  
  # The number of threads to use. This will be 1 when job_queue is true. 
  threads: 1"""
        with open("./config.yaml", "w") as yml_file:
            yml_file.write(s)
    
    def load_config(self):
        arg_dict = None
        with open("./config.yaml", "r") as yml_file:
            arg_dict = yaml.load(yml_file)
        return arg_dict
