'''
Created on Jun 19, 2019

@author: ben
'''

from pathlib import Path
from Main.Setup_CPE_XML_Template import generate_setup_cpe
from Main.FJSP_FolderReader_Document_Data_Ingest_CPE import generate_folder_reader_document_data_ingest_cpe
from Main.FJSP_FolderReader_Document_Data_Process_CPE import generate_folder_reader_document_data_process_cpe
from Main.FJSP_FolderReader_Model_Data_Ingest_CPE import generate_folder_reader_model_data_ingest_cpe
from Main.FJSP_FolderReader_Model_Data_Process_CPE import generate_folder_reader_model_data_process_cpe

from Main.Collection_Processor_Setup import generate_collection_processor_setup
from Main.FJSP_Collection_Processor_Document_Data_Ingest import generate_FJSP_Collection_Processor_Document_Data_Ingest
from Main.FJSP_Collection_Processor_Document_Data_Process import generate_FJSP_Collection_Processor_Document_Data_Process
from Main.FJSP_Collection_Processor_Model_Data_Ingest import generate_FJSP_Collection_Processor_Model_Data_Ingest
from Main.FJSP_Collection_Processor_Model_Data_Process  import generate_FJSP_Collection_Processor_Model_Data_Process

from Main.FJSP_FolderReader_Base import Generate_FJSP_Collection_Processor_Base
from Main.DocumentClassifier_CPE import Generate_Document_Classifier_CPE
from Main.FJSP_Build_Models_And_Tag import generate_FJSP_Build_Models_And_Tag
from Main.DoNothing import generate_do_nothing

import os
import argparse
import csv
import multiprocessing as mp
from Main.ConfigFile import ConfigFile


def clean_xml(file_root, new_root):
    
    #if file_root[0] != "/":
    #    raise Exception("file_root should not be a relative path.")
    if file_root[-1] != "/":
        file_root = "{}/".format(file_root)
    
    if not Path(file_root).exists():
        print("The root directory {} does not exist.".format(file_root))
    
    #if new_root[0] != "/":
    #    raise Exception("new_root should not be a relative path.")
    if new_root[-1] != "/":
        new_root = "{}/".format(new_root)
    
    p = Path(file_root)
    file_root_parts = p.parts
    
    xml_list = list(p.glob("**/*.xml"))
    for xml_file in xml_list:
        xml_file_parent_parts = xml_file.parent.parts
        new_folder = Path(new_root)
        for x in range(len(file_root_parts), len(xml_file_parent_parts)):
            new_folder = new_folder / xml_file_parent_parts[x]
        p_new_folder = Path(new_folder)
        p_new_folder.mkdir(parents=True, exist_ok=True)
        
        with xml_file.open() as in_xml_file:
            out_xml = p_new_folder / xml_file.name
            with out_xml.open(mode="w") as out_xml_file:
                for line in in_xml_file.readlines():
                    if len(line.strip()) == 0:
                        continue
                    out_xml_file.write("{}\n".format(line.rstrip()))
                    
                    
            
        
        #p_new_folder.mkdir(parents=True, exist_ok=True)

def Setup():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean_xml", action="store_true", help="If true, clean the xml documents from the copy root directory and put them in the new_root directory. ")
    parser.add_argument("--copy_root", action="store", default=None, nargs=1, help="The directory to copy xml files from.")
    parser.add_argument("--new_root", action="store", default=None, nargs=1, help="The directory to copy xml files to.")
    
    parser.add_argument("--generate_xml", action="store_true", help="If true, clean the xml documents from the copy root directory and put them in the new_root directory. ")
    parser.add_argument("--root", action="store", default=["./"], nargs=1, help="The root directory.")
    parser.add_argument("--database_server", action="store", default=["database_server"], nargs=1, help="The database server. Defaults to 'database_server'.")
    parser.add_argument("--database", action="store", default=["database"], nargs=1, help="The database to connect to. Defaults to 'database'.")
    parser.add_argument("--database_port", action="store", default=["5432"], nargs=1, help="The database port. Defaults to 5432.")
    parser.add_argument("--database_user", action="store", default=["user"], nargs=1, help="The database user. Defaults to 'user'.")
    parser.add_argument("--database_password", action="store", default=["password"], nargs=1, help="The database user password. Defaults to 'password'.")
    
    parser.add_argument("--category_text_folder", action="store", default=["category_text"], nargs=1, help="The folder containing all texts to use as a category training data.")
    parser.add_argument("--document_text_folder", action="store", default=["document_text"], nargs=1, help="The folder containing all texts to catagorze based on the training data.")
    
    parser.add_argument("--project_name", action="store", nargs=1, help="The project name.")
    parser.add_argument("--project_type", action="store", nargs=1, default=["1"], help="""The project type.
1: dual validation. This will specify a dual validation project. 
    """)
    """
    These should probably be required but we can also clean the xml, so they are not."""
    parser.add_argument("--checkout_timeout", action="store", nargs=1, default=["600"], help="The timeout for checked out documents in seconds (e.g., 600 is 600 seconds). The default is 600 seconds.")
    parser.add_argument("--project_owner_user_name", action="store", nargs=1, help="The email for the user who owns the project.")
    parser.add_argument("--project_owner_email", action="store", nargs=1, help="The email for the user who owns the project." )
    parser.add_argument("--project_owner_first_name", action="store", nargs=1, help="The project owner's first name.")
    parser.add_argument("--project_owner_last_name", action="store", nargs=1, help="The project owner's last name.")
    
    parser.add_argument("--job_queue", action="store_true", help="Use the job queue rather than CPU threads (the default). This will always set the number of threads to 1.")
    parser.add_argument("-j", "--threads", action="store", default=["1"], help="Use CPU threads.")
    
    parser.add_argument("--no_text", action="store_false", help="Do not read text files. The default is to read text files.")
    parser.add_argument("--no_csv", action="store_false", help="Do not read csv files. The default is to read csv files.")
    parser.add_argument("--no_pdf", action="store_false", help="Do not read pdf files. The default is to read pdf files.")
    parser.add_argument("--no_docx", action="store_false", help="Do not read docx files. The default is to read docx files.")
    
    parser.add_argument("--csv_id", action="append", help="This is the set of id column names to use for the csv files. Mutliple flags are allowed.")
    parser.add_argument("--csv_text", action="append", help="This is the set of text column names to use for the csv file.")
    parser.add_argument("--csv_category", action="append", help="This is the set of category column names to use for the csv file.")
    
    
    parsed_args = parser.parse_args()
    
    ret = {}
    ret["generate_xml"] = parsed_args.generate_xml
    ret["root"] = parsed_args.root[0]
    ret["clean_xml"] = parsed_args.clean_xml
    if ret["clean_xml"] == True and parsed_args.copy_root != None and parsed_args.new_root != None:
        ret["copy_root"] = parsed_args.copy_root[0]
        ret["new_root"] = parsed_args.new_root[0]
    elif ret["clean_xml"] == True:
        raise Exception("The clean flag was passed but copy_root and new_root were not.")
    
    ret["database_server"] = parsed_args.database_server[0]
    ret["database"] = parsed_args.database[0]
    ret["database_port"] = parsed_args.database_port[0]
    ret["database_user"] = parsed_args.database_user[0]
    ret["database_password"] = parsed_args.database_password[0]
    ret["category_text_folder"] = parsed_args.category_text_folder[0]
    ret["document_text_folder"] = parsed_args.document_text_folder[0]
    
    if ret["generate_xml"] == True:
        ret["project_name"] = parsed_args.project_name[0]
        ret["project_type"] = parsed_args.project_type[0]
        ret["checkout_timeout"] = parsed_args.checkout_timeout[0]
        ret["project_owner_user_name"] = parsed_args.project_owner_user_name[0]
        ret["project_owner_email"] = parsed_args.project_owner_email[0]
        ret["project_owner_first_name"] = parsed_args.project_owner_first_name[0]
        ret["project_owner_last_name"] = parsed_args.project_owner_last_name[0]
    
    ret["job_queue"] = parsed_args.job_queue
    ret["threads"] = parsed_args.threads[0]
    
    if ret["job_queue"] == True:
        ret["threads"] = "1"

    return ret
           
def create_setup_cpe(arg_dict):
    Path("{}/ContentProcessingEngine/FJSP/".format(arg_dict["root"])).mkdir(parents=True, exist_ok=True)
    setup_cpe_xml = Path("{}/ContentProcessingEngine/FJSP/Setup_CPE.xml".format(arg_dict["root"]))
    generate_setup_cpe(setup_cpe_xml,
                       arg_dict["database_server"], 
                       arg_dict["database"], 
                       arg_dict["database_user"], 
                       arg_dict["database_password"], 
                       arg_dict["database_port"], 
                       arg_dict["job_queue"],
                       
                       project_name = arg_dict["project_name"], 
                       project_type = arg_dict["project_type"], 
                       checkout_timeout = arg_dict["checkout_timeout"], 
                       proejct_owner_user_name = arg_dict["project_owner_user_name"], 
                       project_owner_email = arg_dict["project_owner_email"], 
                       project_owner_first_name = arg_dict["project_owner_first_name"],
                       project_owner_last_name = arg_dict["project_owner_last_name"]
                       
                       )

def create_document_set(arg_dict):
    document_ingest_xml = Path("{}/ContentProcessingEngine/FJSP/FJSP_FolderReader_Document_Data_Ingest_CPE.xml".format(arg_dict["root"]))
    generate_folder_reader_document_data_ingest_cpe(document_ingest_xml,
                                                         arg_dict["document_text_folder"], 
                                                         arg_dict["database_server"], 
                                                         arg_dict["database"], 
                                                         arg_dict["database_user"], 
                                                         arg_dict["database_password"], 
                                                         arg_dict["database_port"], 
                                                         arg_dict["job_queue"])
    document_process_xml = Path("{}/ContentProcessingEngine/FJSP/FJSP_FolderReader_Document_Data_Process_CPE.xml".format(arg_dict["root"]))
    generate_folder_reader_document_data_process_cpe(document_process_xml,
                                                         arg_dict["document_text_folder"], 
                                                         arg_dict["database_server"], 
                                                         arg_dict["database"], 
                                                         arg_dict["database_user"], 
                                                         arg_dict["database_password"], 
                                                         arg_dict["database_port"], 
                                                         arg_dict["job_queue"])

def create_model_set(arg_dict):
    model_ingest_xml = Path("{}/ContentProcessingEngine/FJSP/FJSP_FolderReader_Model_Data_Ingest_CPE.xml".format(arg_dict["root"]))
    generate_folder_reader_model_data_ingest_cpe(model_ingest_xml,
                                                      arg_dict["category_text_folder"], 
                                                      arg_dict["database_server"], 
                                                      arg_dict["database"], 
                                                      arg_dict["database_user"], 
                                                      arg_dict["database_password"], 
                                                      arg_dict["database_port"], 
                                                      arg_dict["job_queue"])
    model_process_xml = Path("{}/ContentProcessingEngine/FJSP/FJSP_FolderReader_Model_Data_Process_CPE.xml".format(arg_dict["root"]))
    generate_folder_reader_model_data_process_cpe(model_process_xml,
                                                       arg_dict["category_text_folder"], 
                                                       arg_dict["database_server"], 
                                                       arg_dict["database"], 
                                                       arg_dict["database_user"], 
                                                       arg_dict["database_password"], 
                                                       arg_dict["database_port"], 
                                                       arg_dict["job_queue"])

def create_folder_readers(arg_dict):
    document_ingest_xml = Path("{}/ContentProcessingEngine/FJSP/FJSP_FolderReader_Document_Data_Ingest_CPE.xml".format(arg_dict["root"]))
    Generate_FJSP_Collection_Processor_Base(output_file = document_ingest_xml,
                                            is_document_data = True,
                                            is_insert = True,
                                            base_document_folder = arg_dict["document_text_folder"],
                                            database_server = arg_dict["database_server"],
                                            database = arg_dict["database"], 
                                            database_user = arg_dict["database_user"], 
                                            database_password = arg_dict["database_password"],
                                            database_type = arg_dict["database_type"],
                                            database_port = arg_dict["database_port"],
                                            use_job_queue = arg_dict["job_queue"],
                                            no_text = arg_dict["no_text"],
                                            no_csv = arg_dict["no_csv"],
                                            no_docx = arg_dict["no_docx"],
                                            no_pdf = arg_dict["no_pdf"],
                                            no_html = arg_dict["no_html"],
                                            csv_ids = arg_dict["csv_id"],
                                            csv_texts = arg_dict["csv_text"],
                                            csv_cats = arg_dict["csv_category"])
    
    document_process_xml = Path("{}/ContentProcessingEngine/FJSP/FJSP_FolderReader_Document_Data_Process_CPE.xml".format(arg_dict["root"]))
    Generate_FJSP_Collection_Processor_Base(output_file = document_process_xml,
                                            is_document_data = True,
                                            is_insert = False,
                                            base_document_folder = arg_dict["document_text_folder"],
                                            database_server = arg_dict["database_server"],
                                            database = arg_dict["database"], 
                                            database_user = arg_dict["database_user"], 
                                            database_password = arg_dict["database_password"],
                                            database_type = arg_dict["database_type"],
                                            database_port = arg_dict["database_port"],
                                            use_job_queue = arg_dict["job_queue"],
                                            no_text = arg_dict["no_text"],
                                            no_csv = arg_dict["no_csv"],
                                            no_docx = arg_dict["no_docx"],
                                            no_pdf = arg_dict["no_pdf"],
                                            no_html = arg_dict["no_html"],
                                            csv_ids = arg_dict["csv_id"],
                                            csv_texts = arg_dict["csv_text"],
                                            csv_cats = arg_dict["csv_category"])
    
    model_ingest_xml = Path("{}/ContentProcessingEngine/FJSP/FJSP_FolderReader_Model_Data_Ingest_CPE.xml".format(arg_dict["root"]))
    Generate_FJSP_Collection_Processor_Base(output_file = model_ingest_xml,
                                            is_document_data = False,
                                            is_insert = True,
                                            base_document_folder = arg_dict["category_text_folder"],
                                            database_server = arg_dict["database_server"],
                                            database = arg_dict["database"], 
                                            database_user = arg_dict["database_user"], 
                                            database_password = arg_dict["database_password"],
                                            database_type = arg_dict["database_type"],
                                            database_port = arg_dict["database_port"],
                                            use_job_queue = arg_dict["job_queue"],
                                            no_text = arg_dict["no_text"],
                                            no_csv = arg_dict["no_csv"],
                                            no_docx = arg_dict["no_docx"],
                                            no_pdf = arg_dict["no_pdf"],
                                            no_html = arg_dict["no_html"],
                                            csv_ids = arg_dict["csv_id"],
                                            csv_texts = arg_dict["csv_text"],
                                            csv_cats = arg_dict["csv_category"])
    
    model_process_xml = Path("{}/ContentProcessingEngine/FJSP/FJSP_FolderReader_Model_Data_Process_CPE.xml".format(arg_dict["root"]))
    Generate_FJSP_Collection_Processor_Base(output_file = model_process_xml,
                                            is_document_data = False,
                                            is_insert = False,
                                            base_document_folder = arg_dict["category_text_folder"],
                                            database_server = arg_dict["database_server"],
                                            database = arg_dict["database"], 
                                            database_user = arg_dict["database_user"], 
                                            database_password = arg_dict["database_password"],
                                            database_type = arg_dict["database_type"],
                                            database_port = arg_dict["database_port"],
                                            use_job_queue = arg_dict["job_queue"],
                                            no_text = arg_dict["no_text"],
                                            no_csv = arg_dict["no_csv"],
                                            no_docx = arg_dict["no_docx"],
                                            no_pdf = arg_dict["no_pdf"],
                                            no_html = arg_dict["no_html"],
                                            csv_ids = arg_dict["csv_id"],
                                            csv_texts = arg_dict["csv_text"],
                                            csv_cats = arg_dict["csv_category"])
    
    model_process_xml = Path("{}/ContentProcessingEngine/FJSP/DocumentClassifier_CPE.xml".format(arg_dict["root"]))
    Generate_Document_Classifier_CPE(output_file = model_process_xml,
                                            database_server = arg_dict["database_server"],
                                            database = arg_dict["database"], 
                                            database_user = arg_dict["database_user"], 
                                            database_password = arg_dict["database_password"],
                                            database_type = arg_dict["database_type"],
                                            database_port = arg_dict["database_port"], 
                                            use_job_queue = arg_dict["job_queue"])
    
def create_cpe_set(arg_dict):
    cas_pool_size = arg_dict["threads"]
    threads = arg_dict["threads"]
    
    xml_document = Path("{}/ContentProcessingEngine/FJSP/Collection_Processor_Setup.xml".format(arg_dict["root"]))
    generate_collection_processor_setup(xml_document, cas_pool_size, threads)
    
    xml_document = Path("{}/ContentProcessingEngine/FJSP/FJSP_Collection_Processor_Document_Data_Ingest.xml".format(arg_dict["root"]))
    generate_FJSP_Collection_Processor_Document_Data_Ingest(xml_document, cas_pool_size, threads)
    
    xml_document = Path("{}/ContentProcessingEngine/FJSP/FJSP_Collection_Processor_Document_Data_Process.xml".format(arg_dict["root"]))
    generate_FJSP_Collection_Processor_Document_Data_Process(xml_document, cas_pool_size, threads)
    
    xml_document = Path("{}/ContentProcessingEngine/FJSP/FJSP_Collection_Processor_Model_Data_Ingest.xml".format(arg_dict["root"]))
    generate_FJSP_Collection_Processor_Model_Data_Ingest(xml_document, cas_pool_size, threads)
    
    xml_document = Path("{}/ContentProcessingEngine/FJSP/FJSP_Collection_Processor_Model_Data_Process.xml".format(arg_dict["root"]))
    generate_FJSP_Collection_Processor_Model_Data_Process(xml_document, cas_pool_size, threads)
    
    xml_document = Path("{}/ContentProcessingEngine/FJSP/FJSP_Build_Models_And_Tag.xml".format(arg_dict["root"]))
    generate_FJSP_Build_Models_And_Tag(xml_document, cas_pool_size, threads)
    
    xml_document = Path("{}/ContentProcessingEngine/FJSP/DoNothing.xml".format(arg_dict["root"]))
    generate_do_nothing(xml_document)
    
def clean(copy_root, new_root):
    clean_xml(copy_root, new_root)
    
def put_99_ncic():
    with open("/home/ben/workspace/NLP_Stack/fjsp/stat_ncic_list_cleaned.csv") as csvfile:
        with open("/home/ben/workspace/NLP_Stack/fjsp/stat_ncic_list_cleaned_alts.csv", "w") as csvfile_out:
            dict_reader = csv.DictReader(csvfile)
            h = dict_reader.fieldnames
            #charge    state    statute    ncic_code
            dict_writer = csv.DictWriter(csvfile_out, h)
            dict_writer.writeheader()
            for row in dict_reader:
                ncic_code = row["ncic_code"]
                if len(ncic_code) != 4:
                    ncic_code = "0{}".format(ncic_code)
                if ncic_code[2] == "9" and ncic_code[3] == "9":
                    dict_writer.writerow(row)
                else:
                    dict_writer.writerow(row)
                    row["ncic_code"] = "{}99".format(ncic_code[0:2])
                    dict_writer.writerow(row)
                 
            
            
def main_prod():
    #arg_dict = Setup()
    #walk_route = "/home/ben/workspace/NLP_Stack/desc/"
    #new_root = "/home/ben/workspace/NLP_Stack_Installer/desc/"
    
    """
    arg_dict = Setup()
    
    if arg_dict["clean_xml"] == True:
        clean_xml(arg_dict["copy_root"], arg_dict["new_root"])
    
    if arg_dict["generate_xml"] == True:
        create_setup_cpe(arg_dict)
        create_document_set(arg_dict)
        create_model_set(arg_dict)
        create_cpe_set(arg_dict)
    """
    
    config = ConfigFile()
    
    if not config.config_files_exist():
        print("No configuration files found, creating them.")
        config.create_clean_file_with_comments()
        config.create_default_with_comments()
        print("Configuration files created. Please edit config.yaml and clean_xml.yaml as appropriate and run this command again.")
        return
    else:
        #Clean everything
        arg_dict = config.load_clean_config()
        if arg_dict["clean_xml"] == True:
            clean_xml(arg_dict["copy_root"], arg_dict["new_root"])
        
        #Load the config file and create all of teh xml
        arg_dict = config.load_config()
        create_setup_cpe(arg_dict)
        create_folder_readers(arg_dict)
        create_cpe_set(arg_dict)
    
    #put_99_ncic()
if __name__ == '__main__':
    main_prod()        


