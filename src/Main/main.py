'''
Created on Jun 19, 2019

@author: ben
'''

from pathlib import Path
from Main.Setup_CPE_XML_Template import *
from Main.FJSP_FolderReader_Document_Data_Ingest_CPE import *
from Main.FJSP_FolderReader_Document_Data_Process_CPE import *
from Main.FJSP_FolderReader_Model_Data_Ingest_CPE import *
from Main.FJSP_FolderReader_Model_Data_Process_CPE import *

from Main.Collection_Processor_Setup import generate_collection_processor_setup
from Main.FJSP_Collection_Processor_Document_Data_Ingest import generate_FJSP_Collection_Processor_Document_Data_Ingest
from Main.FJSP_Collection_Processor_Document_Data_Process import generate_FJSP_Collection_Processor_Document_Data_Process
from Main.FJSP_Collection_Processor_Model_Data_Ingest import generate_FJSP_Collection_Processor_Model_Data_Ingest
from Main.FJSP_Collection_Processor_Model_Data_Process import generate_FJSP_Collection_Processor_Model_Data_Process


import os
import argparse



def clean_xml(file_root, new_root):
    
    #if file_root[0] != "/":
    #    raise Exception("file_root should not be a relative path.")
    if file_root[-1] != "/":
        file_root = "{}/".format(file_root)
    
    #if new_root[0] != "/":
    #    raise Exception("new_root should not be a relative path.")
    if new_root[-1] != "/":
        new_root = "{}/".format(new_root)
    
    p = Path(file_root)
    file_root_parts = p.parts
    
    xml_list = list(p.glob("**/*.xml"))
    print (xml_list)
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
    
    parser.add_argument("--job_queue", action="store_true", help="Use the job queue rather than CPU threads (the default). This will always set the number of threads to 1.")
    parser.add_argument("-j", "--threads", action="store", default=["1"], help="Use CPU threads.")
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
    
    ret["job_queue"] = parsed_args.job_queue
    ret["threads"] = parsed_args.threads[0]
    
    if ret["job_queue"] == True:
        ret["threads"] = "1"

    return ret
           
def create_setup_cpe(arg_dict):
    setup_cpe_xml = Path("{}/ContentProcessingEngine/FJSP/Setup_CPE.xml".format(arg_dict["root"]))
    generate_setup_cpe(setup_cpe_xml,
                       arg_dict["database_server"], 
                       arg_dict["database"], 
                       arg_dict["database_user"], 
                       arg_dict["database_password"], 
                       arg_dict["database_port"], 
                       arg_dict["job_queue"])

def create_document_set(arg_dict):
    document_ingest_xml = Path("{}/ContentProcessingEngine/FJSP/FJSP_Collection_Processor_Document_Data_Ingest_CPE.xml".format(arg_dict["root"]))
    generate_folder_reader_document_data_ingest_cpe(document_ingest_xml,
                                                         arg_dict["document_text_folder"], 
                                                         arg_dict["database_server"], 
                                                         arg_dict["database"], 
                                                         arg_dict["database_user"], 
                                                         arg_dict["database_password"], 
                                                         arg_dict["database_port"], 
                                                         arg_dict["job_queue"])
    document_process_xml = Path("{}/ContentProcessingEngine/FJSP/FJSP_Collection_Processor_Document_Data_Process_CPE.xml".format(arg_dict["root"]))
    generate_folder_reader_document_data_process_cpe(document_process_xml,
                                                         arg_dict["document_text_folder"], 
                                                         arg_dict["database_server"], 
                                                         arg_dict["database"], 
                                                         arg_dict["database_user"], 
                                                         arg_dict["database_password"], 
                                                         arg_dict["database_port"], 
                                                         arg_dict["job_queue"])
def create_model_set(arg_dict):
    model_ingest_xml = Path("{}/ContentProcessingEngine/FJSP/FJSP_Collection_Processor_Model_Data_Ingest_CPE.xml".format(arg_dict["root"]))
    generate_folder_reader_model_data_ingest_cpe(model_ingest_xml,
                                                      arg_dict["document_text_folder"], 
                                                      arg_dict["database_server"], 
                                                      arg_dict["database"], 
                                                      arg_dict["database_user"], 
                                                      arg_dict["database_password"], 
                                                      arg_dict["database_port"], 
                                                      arg_dict["job_queue"])
    model_process_xml = Path("{}/ContentProcessingEngine/FJSP/FJSP_Collection_Processor_Model_Data_Process_CPE.xml".format(arg_dict["root"]))
    generate_folder_reader_model_data_process_cpe(model_process_xml,
                                                       arg_dict["document_text_folder"], 
                                                       arg_dict["database_server"], 
                                                       arg_dict["database"], 
                                                       arg_dict["database_user"], 
                                                       arg_dict["database_password"], 
                                                       arg_dict["database_port"], 
                                                       arg_dict["job_queue"])
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
    
def clean(copy_root, new_root):
    clean_xml(copy_root, new_root)

def main():
    arg_dict = Setup()
    #walk_route = "/home/ben/workspace/NLP_Stack/desc/"
    #new_root = "/home/ben/workspace/NLP_Stack_Installer/desc/"
    if arg_dict["clean_xml"] == True:
        clean_xml(arg_dict["copy_root"], arg_dict["new_root"])
    
    if arg_dict["generate_xml"] == True:
        create_setup_cpe(arg_dict)
        create_document_set(arg_dict)
        create_model_set(arg_dict)
        create_cpe_set(arg_dict)
        


if __name__ == '__main__':
    main()