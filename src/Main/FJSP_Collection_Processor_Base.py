from string import Template
from pathlib import Path
from builtins import None

FJSP_Collection_Processor_Document_Data_Ingest = """<?xml version="1.0" encoding="UTF-8"?>
<collectionReaderDescription xmlns="http://uima.apache.org/resourceSpecifier">
    
  <frameworkImplementation>org.apache.uima.java</frameworkImplementation>
    
  <implementationName>collection_readers.FolderReader</implementationName>
    
  <processingResourceMetaData>
        
    <name>FolderReader</name>
        
    <description>This object reads through files and folders and selects all files that match the search criteria. It then loads the appropriate file reader object and populates the CAS.
Please note that all header  parameters are case senseative. ID is not the same as id or Id. I might fix this in future revisions but for now, we expect that the CSV headers will match whichever information is in the array.
Also, this application will match headers in order.  If the user specifies the CsvIdHeaders field as
 CsvIdHeaders = ["id", "Id", "ID", "IDENTIFIER"]
and the spreadsheet contains an "IDENTIFIER" and an "id" column, the application marks the "id" column as the id column.</description>
        
    <version>1.0</version>
        
    <vendor/>
        
    <configurationParameters>
            
      <configurationParameter>
                
        <name>BaseFolder</name>
                
        <description>The base folder to walk.</description>
                
        <type>String</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>true</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>IsRecursive</name>
                
        <description>Should the application perform a recursive walk over the base directory or only look in the base folder? Set to "true" to use a recursive walk.</description>
                
        <type>Boolean</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>true</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>ReadText</name>
                
        <description>Read txt files where an entry is 1 text string per row.</description>
                
        <type>Boolean</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>false</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>ReadPdf</name>
                
        <description>Should the search include pdf documents?</description>
                
        <type>Boolean</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>true</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>ReadCsv</name>
                
        <description>Should the search include csv documents?</description>
                
        <type>Boolean</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>false</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>ReadHtml</name>
                
        <description>Should the search include html documents?</description>
                
        <type>Boolean</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>false</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>ReadWord</name>
                
        <description>Should the search include word documents?</description>
                
        <type>Boolean</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>false</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>CsvIdHeaders</name>
                
        <description>This is the set of labels that will represent the id column in csv files. If the user does not provide a list of labels to use for lookup, it will  default to "id".</description>
                
        <type>String</type>
                
        <multiValued>true</multiValued>
                
        <mandatory>true</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>CsvTextHeaders</name>
                
        <description>The list of values that will define text columns in the csv file.</description>
                
        <type>String</type>
                
        <multiValued>true</multiValued>
                
        <mandatory>true</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>CsvCategoryHeaders</name>
                
        <description>The list of values that will define category columns in the csv file.</description>
                
        <type>String</type>
                
        <multiValued>true</multiValued>
                
        <mandatory>true</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>DataType</name>
                
        <description>This specifies how the applciation should insert the data.
DataType = 0: Document data/data to categorize
DataType = 1: Category data/model data
DataType = 2: Both for a full many to many mapping.
The default is 0.</description>
                
        <type>Integer</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>false</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>DatabaseServer</name>
                
        <description>The database server to connect to.</description>
                
        <type>String</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>true</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>Database</name>
                
        <description>Database to connect to on the server.</description>
                
        <type>String</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>true</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>DatabaseUserName</name>
                
        <description>The username for the connecting user</description>
                
        <type>String</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>true</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>DatabasePassword</name>
                
        <description>Password for the associated database user. Please note that this is clearcase in plain text. There might be additional options to connect to a database, but for now, localhost is the database to connect to.</description>
                
        <type>String</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>true</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>DatabasePort</name>
                
        <description>This is the port to atempt to connect to. If this is not provided, it will atempt to connect to the default port based on the type provided.</description>
                
        <type>String</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>false</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>DatabaseType</name>
                
        <description>This is the database type we are trying to connect to. This is required if the DatabasePort value is not assigned. The port will be assigned the default value for the database type.</description>
                
        <type>String</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>false</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>LoggingUserId</name>
                
        <description>This is the logging user that will run this application.</description>
                
        <type>Integer</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>false</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>UseJobQueue</name>
                
        <description>Sets if this process should use the job queue
0: disable the job queue
1: insert document
2: process documents</description>
                
        <type>Integer</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>true</mandatory>
              
      </configurationParameter>
            
      <configurationParameter>
                
        <name>CleanData</name>
                
        <type>Boolean</type>
                
        <multiValued>false</multiValued>
                
        <mandatory>true</mandatory>
              
      </configurationParameter>
          
    </configurationParameters>
        
    <configurationParameterSettings>
            
      <nameValuePair>
                
        <name>BaseFolder</name>
                
        <value>
                    
          <string>$BASE_DOCUMENT_FOLDER</string>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>IsRecursive</name>
                
        <value>
                    
          <boolean>true</boolean>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>ReadCsv</name>
                
        <value>
                    
          <boolean>true</boolean>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>ReadPdf</name>
                
        <value>
                    
          <boolean>true</boolean>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>ReadHtml</name>
                
        <value>
                    
          <boolean>true</boolean>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>ReadWord</name>
                
        <value>
                    
          <boolean>true</boolean>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>CsvIdHeaders</name>
                
        <value>
                    
          <array>
                        
            <string>IDENTIFIER</string>
                        
            <string>id</string>
                        
            <string>Id</string>
                        
            <string>ID</string>
                      
          </array>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>CsvTextHeaders</name>
                
        <value>
                    
          <array>
                        
            <string>text</string>
                        
            <string>Text</string>
                        
            <string>TEXT</string>
                        
            <string>SEARCH FIELD</string>
                        
            <string>charge</string>
                      
          </array>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>DataType</name>
                
        <value>
                    
          <integer>$DATA_TYPE</integer>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>DatabaseServer</name>
                
        <value>
                    
          <string>$DATABASE_SERVER</string>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>DatabaseUserName</name>
                
        <value>
                    
          <string>$DATABASE_USER</string>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>Database</name>
                
        <value>
                    
          <string>$DATABASE</string>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>DatabasePassword</name>
                
        <value>
                    
          <string>$DATABASE_PASSWORD</string>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>DatabaseType</name>
                
        <value>
                    
          <string>5432</string>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>ReadText</name>
                
        <value>
                    
          <boolean>true</boolean>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>UseJobQueue</name>
                
        <value>
                    
          <integer>$JOB_QUEUE_VALUE</integer>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>CleanData</name>
                
        <value>
                    
          <boolean>true</boolean>
                  
        </value>
              
      </nameValuePair>
            
      <nameValuePair>
                
        <name>CsvCategoryHeaders</name>
                
        <value>
                    
          <array>
                        
            <string>ncic_code</string>
                      
          </array>
                  
        </value>
              
      </nameValuePair>
          
    </configurationParameterSettings>
        
    <typeSystemDescription>
            
      <imports>
                
        <import location="../../objects/DatabaseConnection.xml"/>
                
        <import location="../../objects/UnprocessedText.xml"/>
              
      </imports>
          
    </typeSystemDescription>
        
    <typePriorities/>
        
    <fsIndexCollection/>
        
    <capabilities>
            
      <capability>
                
        <inputs/>
                
        <outputs>
                    
          <type allAnnotatorFeatures="true">objects.UnprocessedText</type>
                    
          <type allAnnotatorFeatures="true">objects.DatabaseConnection</type>
                  
        </outputs>
                
        <languagesSupported/>
              
      </capability>
          
    </capabilities>
        
    <operationalProperties>
            
      <modifiesCas>true</modifiesCas>
            
      <multipleDeploymentAllowed>false</multipleDeploymentAllowed>
            
      <outputsNewCASes>true</outputsNewCASes>
          
    </operationalProperties>
      
  </processingResourceMetaData>
    
  <resourceManagerConfiguration/>
  
</collectionReaderDescription>
"""

def Generate_FJSP_Collection_Processor_Base(output_file, 
                                            is_document_data,
                                            is_insert,
                                            base_document_folder, 
                                            database_server, 
                                            database, 
                                            database_user, 
                                            database_password, 
                                            database_port, 
                                            use_job_queue):
    """output_file: a pathlib object"""
    job_queue_value = None
    data_type = None
    
    #is_document_data == true: it is document data
    #is_document_data == false: it is category data
    if is_document_data == True:
        data_type = "0"
    else:
        data_type = "1"
    
    #is_insert == true: insert
    #is_insert == false: process
    if use_job_queue == False:
        job_queue_value = "0"
    elif use_job_queue == True && is_insert == True:
        job_queue_value = "1"
    elif use_job_queue == True && is_insert == False:
        job_queue_value = "2"
    
        
        
    s = Template(FJSP_Collection_Processor_Document_Data_Ingest)
    ret = s.substitute(DATA_TYPE=data_type, DATABASE_SERVER=database_server, DATABASE_USER=database_user, DATABASE=database,
                       DATABASE_PASSWORD=database_password, DATABASE_PORT=database_port, 
                       BASE_DOCUMENT_FOLDER=base_document_folder, JOB_QUEUE_VALUE=job_queue_value)
    with output_file.open(mode="w") as out_file:
        out_file.write(ret)
    with output_file.open(mode="w") as out_file:
        out_file.write(ret)

      