from string import Template

XML_SETUP_CPE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<collectionReaderDescription xmlns="http://uima.apache.org/resourceSpecifier">
  <frameworkImplementation>org.apache.uima.java</frameworkImplementation>
  <implementationName>descriptors.Setup_CPE</implementationName>
  <processingResourceMetaData>
    <name>DocumentClassifier_CPE</name>
    <description/>
    <version>1.0</version>
    <vendor/>
    <configurationParameters>
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
        <description>Sets if this process should use the job queue. It accepts 3 values.
0: Do not use job queue
1: insert data
2: process data</description>
        <type>Integer</type>
        <multiValued>false</multiValued>
        <mandatory>true</mandatory>
      </configurationParameter>
      
      <configurationParameter>
        <name>ProjectName</name>
        <type>String</type>
        <multiValued>false</multiValued>
        <mandatory>true</mandatory>
      </configurationParameter>
      <configurationParameter>
        <name>ProjectType</name>
        <type>String</type>
        <multiValued>false</multiValued>
        <mandatory>true</mandatory>
      </configurationParameter>
      <configurationParameter>
        <name>CheckoutTimeout</name>
        <type>Integer</type>
        <multiValued>false</multiValued>
        <mandatory>true</mandatory>
      </configurationParameter>
      <configurationParameter>
        <name>ProjectOwnerUserName</name>
        <description>This is the username for the project owner</description>
        <type>String</type>
        <multiValued>false</multiValued>
        <mandatory>true</mandatory>
      </configurationParameter>
      <configurationParameter>
        <name>ProjectOwnerEmail</name>
        <type>String</type>
        <multiValued>false</multiValued>
        <mandatory>true</mandatory>
      </configurationParameter>
      <configurationParameter>
        <name>ProjectOwnerFirstName</name>
        <type>String</type>
        <multiValued>false</multiValued>
        <mandatory>true</mandatory>
      </configurationParameter>
      <configurationParameter>
        <name>ProjectOwnerLastName</name>
        <type>String</type>
        <multiValued>false</multiValued>
        <mandatory>true</mandatory>
      </configurationParameter>
      
    </configurationParameters>
    <configurationParameterSettings>
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
        <name>DatabasePort</name>
        <value>
          <string>$DATABASE_PORT</string>
        </value>
      </nameValuePair>
      <nameValuePair>
        <name>UseJobQueue</name>
        <value>
          <integer>$JOB_QUEUE_VALUE</integer>
        </value>
      </nameValuePair>
      
      <nameValuePair>
        <name>ProjectName</name>
        <value>
          <string>$PROJECT_NAME</string>
        </value>
      </nameValuePair>
      <nameValuePair>
        <name>ProjectType</name>
        <value>
          <string>$PROJECT_TYPE</string>
        </value>
      </nameValuePair>
      <nameValuePair>
        <name>CheckoutTimeout</name>
        <value>
          <integer>$CHECKOUT_TIMEOUT</integer>
        </value>
      </nameValuePair>
      <nameValuePair>
        <name>ProjectOwnerUserName</name>
        <value>
          <string>$PROJECT_OWNER_USER_NAME</string>
        </value>
      </nameValuePair>
      <nameValuePair>
        <name>ProjectOwnerEmail</name>
        <value>
          <string>$PROJECT_OWNER_EMAIL</string>
        </value>
      </nameValuePair>
      <nameValuePair>
        <name>ProjectOwnerFirstName</name>
        <value>
          <string>$PROJECT_OWNER_FIRST_NAME</string>
        </value>
      </nameValuePair>
      <nameValuePair>
        <name>ProjectOwnerLastName</name>
        <value>
          <string>$PROJECT_OWNER_LAST_NAME</string>
        </value>
      </nameValuePair>
      <nameValuePair>
    </configurationParameterSettings>
    <typeSystemDescription>
      <imports>
        <import location="../../objects/DatabaseConnection.xml"/>
      </imports>
    </typeSystemDescription>
    <typePriorities/>
    <fsIndexCollection/>
    <capabilities>
      <capability>
        <inputs/>
        <outputs>
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

def generate_setup_cpe(output_file, database_server, database, database_user, database_password, database_port, use_job_queue,
                       project_name, project_type, checkout_timeout, proejct_owner_user_name, project_owner_email, project_owner_first_name,
                       project_owner_last_name):
    """output_file: a pathlib object"""
    job_queue_value = None
    if (use_job_queue == True):
        job_queue_value = "1"
    else:
        job_queue_value = "0"
    s = Template(XML_SETUP_CPE_XML)
    #proejct type should be dual_validation
    if project_type == "1":
        project_type = "dual_validation" #This needs to match the java code project types. 
    ret = s.substitute(DATABASE_SERVER=database_server, DATABASE_USER=database_user, DATABASE=database,
                       DATABASE_PASSWORD=database_password, DATABASE_PORT=database_port, JOB_QUEUE_VALUE=job_queue_value,
                       PROJECT_NAME=project_name, PROJECT_TYPE=project_type, CHECKOUT_TIMEOUT=checkout_timeout, 
                       PROJECT_OWNER_USER_NAME=proejct_owner_user_name,
                       PROJECT_OWNER_EMAIL=project_owner_email, PROJECT_OWNER_FIRST_NAME=project_owner_first_name, 
                       PROJECT_OWNER_LAST_NAME=project_owner_last_name)
    with output_file.open(mode="w") as out_file:
        out_file.write(ret)
    
      