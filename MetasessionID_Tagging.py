import os
import re
import pandas as pd
import shutil
import argparse
from session_number import session_number_dict
from session_number import session_number_lang_dict
from title_mapping import title_mapping_dict

# Argument parsing
parser = argparse.ArgumentParser(description='Process some paths.')
parser.add_argument('--base_dir', required=True, help='Base directory path')
args = parser.parse_args()

def normalize_space(string):
    """
    Normalize spaces in a string by replacing multiple spaces with a single space.
    
    Args:
    string (str): Input string.
    
    Returns:
    str: Normalized string.
    """    
    return str(re.sub(r'\s+', ' ', string)).strip()

def normalizespace_with_lower(string):
    """
    Normalize spaces and convert the string to lowercase.
    
    Args:
    string (str): Input string.
    
    Returns:
    str: Normalized and lowercase string.
    """    
    return str(re.sub(r'\s+', ' ', string)).strip().lower()

def extract_grade_id_in_edu_res_report(value):
    """
    Extract the grade ID from a given value.
    
    Args:
    value (str): Input value.
    
    Returns:
    str: Extracted grade ID.
    """    
    if not value[-1].isdigit():
        return value[2:]
    else:
        return str(int(''.join(filter(str.isdigit, value)))) 

def split_title_for_session_numbers(title):
    """
    Split the title to extract session number and session title.
    
    Args:
    title (str): Input title.
    
    Returns:
    tuple: Session number and session title.
    """    
    pattern = r"(الحصة\s[\w\s]+|Session\s\d+|Stunde\s\d+|Sesión\s\d+|Sessione\s\d+):*(?:(.+))?"    
    match = re.search(pattern, title.strip())    
    if match:
        session_number = re.sub(r'\s+', ' ', match.group(1)).strip() if match.group(1) else ""
        session_title = re.sub(r'\s+', ' ', match.group(2)).strip() if match.group(2) else ""
    else:
        session_number = ""
        session_title = title
    return session_number, session_title

def session_number_mapping(session_number):
    """
    Map the session number to its corresponding value.
    
    Args:
    session_number (str): Input session number.
    
    Returns:
    str: Mapped session number.
    """    
    if not session_number:
        return "1"
    return str(session_number_dict.get(session_number, 1))
    
def session_number_lang_mapping(session_number):
    """
    Map the session number to its corresponding language.
    
    Args:
    session_number (str): Input session number.
    
    Returns:
    str: Mapped session number language.
    """    
    if not session_number:
        return 'fails to detect language'
    return session_number_lang_dict.get(session_number, 'fails to detect language')

def add_one_leading_zeros(num):
    """
    Add leading zeros to a number if it is a single digit.
    
    Args:
    num (str): Input number.
    
    Returns:
    str: Number with leading zeros.
    """    
    if str(num).isdigit():
        return f"{int(num):02}"
    else:
        return num

def extract_grade_from_folder_tag(tag):
    """
    Extract the grade from the folder tag.
    
    Args:
    tag (str): Folder tag.
    
    Returns:
    tuple: Grade and any error encountered.
    """    
    grade_from_tag_error=''
    matcha = re.search(r'G(\d+)', tag)
    matchb = re.search(r'G([A-Za-z0-9\s\-\+]+)', tag)
    if matcha:
        grade = str(int(matcha.group(1)))
        return grade, grade_from_tag_error
    elif matchb:
        grade = str(matchb.group(1))
        return grade, grade_from_tag_error
    else:
        grade = "(NF)"
        grade_from_tag_error = " - Grade can't be extracted from the tagging!"        
        return grade, grade_from_tag_error
    
def extract_session_from_folder_tag(tag):
    """
    Extract the session number from the folder tag.
    
    Args:
    tag (str): Folder tag.
    
    Returns:
    tuple: Session number and any error encountered.
    """    
    session_from_tag_error=''
    match = re.search(r'S(\d+)', tag)
    if match:
        session_num=str(int(match.group(1)))
    else:
        session_num="(NF)"
        session_from_tag_error=" - Session number can't be extracted from the tagging!"
    return session_num, session_from_tag_error
    
def extract_term_from_folder_tag(tag):
    """
    Extract the term number from the folder tag.
    
    Args:
    tag (str): Folder tag.
    
    Returns:
    tuple: Term number and any error encountered.
    """    
    term_from_tag_error=''
    match = re.search(r'T(\d+)', tag)
    if match:
        term=str(int(match.group(1)))
    else:
        term="(NF)"
        term_from_tag_error=" - Term number can't be extracted from the tagging!"
    return term, term_from_tag_error
        
def extract_class_title_from_tag(tag):
    """
    Extract the class title from the folder tag.
    
    Args:
    tag (str): Folder tag.
    
    Returns:
    tuple: List of class titles and any error encountered.
    """    
    temp_list=[]
    class_title_error=''
    for key,_ in title_mapping_dict.items():
        if all(part in tag.lower() for part in key.split()):
            temp_list.append(key)
    if temp_list:
        targetphrase=max(temp_list,key=len)
        targettitles_list=title_mapping_dict.get(targetphrase, targetphrase)
        return targettitles_list, class_title_error
    else:
        class_title_error = " - The tagging has no matching class title in the educational resources report!"
        return [tag], class_title_error
    
def extract_subject_and_type_from_tag(tag):
    """
    Extract the subject and session type from the folder tag.
    
    Args:
    tag (str): Folder tag.
    
    Returns:
    tuple: Subject, session type, and any error encountered.
    """    
    temp_list=[]
    subject_and_type_error=''
    for key,_ in title_mapping_dict.items():
        if all(part in tag.lower() for part in key.split()):
            temp_list.append(key)
    if temp_list:
        targetphrase=max(temp_list,key=len)
        if 'regular' in targetphrase:
            session_type = 'regular'
        elif 'intensive' in targetphrase:
            session_type = 'intensive' 
        elif 'exam prep' in targetphrase:
            session_type = 'exam prep'    
        elif 'marathon' in targetphrase:
            session_type = 'marathon'
        else:
            session_type = 'regular'
        subject = targetphrase.replace(f" {session_type}",'').replace(' _en_ ','♕en♕').replace(' _ar_ ','♕ar♕').replace(' _en_','♕en♕').replace(' _ar_','♕ar♕').replace(' _en','♕en').replace(' _ar','♕ar').replace('_','').replace('♕ar♕','_AR').replace('♕en♕','_EN').replace('♕ar','_AR').replace('♕en','_EN')        
    else:
        session_type = 'UnknownSessionType'
        subject = 'UnknownSubject'
        subject_and_type_error = " - Subject & Session Type can't be extracted from the tagging!"
    return subject, session_type, subject_and_type_error 

# Date and time format
datetime_format = '%Y-%m-%d'

current_folder = os.getcwd()

# Regular expressions for folder validation
tagging_folder_pattern = r"^(?:([A-Za-z]+)_)?([A-Za-z0-9\s-]+)_([A-Za-z0-9\s-]+)(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?$"

# Paths to output files
csv_file_path = os.path.join("TestingSource", "MetasessionID_Tagging.xlsx")

# Load reference data
ref_df = pd.read_csv(os.path.join("TestingSource", "processed_sessions_educational_resources_report.csv"), encoding="utf-8")
ref_df["Grade ID"]=ref_df["Grade ID"].astype(str)
ref_df["Session Number"]=ref_df["Session Number"].astype(str)
ref_df["Term"]=ref_df["Term"].astype(str)

# Paths to class files
ar_CLS_folder_path=os.path.join("TestingSource", 'AR_CLS')
en_CLS_folder_path=os.path.join("TestingSource", 'EN_CLS')


def find_matching_folders():
    """
    Find and process matching folders based on certain criteria.
    
    Returns:
    list: List of matching folders with their details.
    """
    filespattern = re.compile(r"^(?:([A-Za-z]+)_)?([A-Za-z0-9\s-]+)_([A-Za-z0-9\s-]+)(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?$")
    base_dir = args.base_dir
 
    matching_folders = []
    roots = set()
    counter = 0
    repeated_folders = []
    has_MSID = True

    when_to_stop = input("\nPlease Enter a Number of Outputs to Stop at, if you are testing, else, just press Enter: ")
    stop = -1
    if when_to_stop != "":
        stop = int(when_to_stop)

    for root, dirs, files in os.walk(base_dir):
        if 'Sessions_Restructure' in root:
            continue
        repeated = ''
        Errors = ''
        if (any(r in root for r in roots)):
            continue

        # Check for necessary files and directories
        contains_tex = any(filespattern.match(f.rsplit('.', 1)[0].lower()) for f in files if f.endswith('.tex'))
        contains_nonquestions = any(d.lower() in ["nonquestions", "input/nonquestions"] for d in dirs)
        contains_questions = any(d.lower() in ["questions", "input/questions"] for d in dirs)
        contains_nagwa_cls = any(f.lower() in ["nagwa.cls", "Input/nagwa.cls", "input/nagwa.cls"] for f in files)
        
        if contains_tex and contains_nonquestions and contains_questions and contains_nagwa_cls:
            folder_name = os.path.basename(root)
            parent_folder = os.path.basename(os.path.dirname(root))
            if folder_name.lower() == 'input':
                folder_name = parent_folder
            roots.add(root)
            counter += 1
            print(f"\r{counter}", end="")
            
            if folder_name[:2].lower() in ['eg', 'in', 'sa', 'uk', 'us']:
                country = folder_name[:2]
            else:
                country = '(NF)'
                Errors += " - Country can't be extracted from the tagging!"

            class_titles, class_title_error = extract_class_title_from_tag(folder_name)
            Errors += class_title_error

            grade_id, grade_from_tag_error = extract_grade_from_folder_tag(folder_name) # str grade id
            Errors += grade_from_tag_error

            session_num, session_from_tag_error = extract_session_from_folder_tag(folder_name) # str session num
            Errors += session_from_tag_error

            term_id, term_from_tag_error = extract_term_from_folder_tag(folder_name) # str term num
            if country.lower() == 'eg':
                Errors += term_from_tag_error
            else:
                if term_id == "(NF)":
                    term_id = term_id.replace("(NF)", "0")

            subject, session_type, subject_and_type_error = extract_subject_and_type_from_tag(folder_name)
            Errors += subject_and_type_error

            # Conditions for matching reference data
            con1 = ref_df["Country"] == normalizespace_with_lower(country) # str country abbreviaiton
            con2 = ref_df["Class Title"].isin(class_titles) # list of strings
            con3 = ref_df["Grade ID"] == grade_id # str
            con4 = ref_df["Session Number"] == session_num # str
            con5 = ref_df["Term"] == term_id # str
            
            if country.lower() == 'eg':
                metasession_ids = ref_df["Meta Session Id"][(con1) & (con2) & (con3) & (con4) & (con5)].unique() # list of integers
                languages = ref_df["Session Language"][(con1) & (con2) & (con3) & (con4) & (con5)].unique()
            else:
                metasession_ids = ref_df["Meta Session Id"][(con1) & (con2) & (con3) & (con4)].unique() # list of integers
                languages = ref_df["Session Language"][(con1) & (con2) & (con3) & (con4)].unique()

            if len(metasession_ids) == 1:
                metasession_id = str(metasession_ids[0])
                has_MSID = True
            elif len(metasession_ids) > 1:
                metasession_id = '(MultiIDs)'
                has_MSID = False
                Errors += " - Multiple matching Metasession_IDs for the tagging!"
            else:
                metasession_id = '(NF)'
                has_MSID = False
                Errors += " - No matching Metasession_ID for the tagging!"

            if len(languages) == 1:
                language = str(languages[0])                
            elif len(languages) > 1:
                language = '(MultiLanguages)'
                Errors += " - Multiple matching languages for the tagging!"
            else:
                language = '(Lang_NF)'
                Errors += " - No matching language for the tagging!"

            new_folder_name = f"{metasession_id}_{country}_{subject}_G{add_one_leading_zeros(grade_id)}_T{term_id}_S{add_one_leading_zeros(session_num)}_{session_type}"
            repeated_folders.append(new_folder_name)

            repetition = repeated_folders.count(new_folder_name)
            if repetition > 1:
                repeated = str(repetition)

            new_folder_name = f"{metasession_id}_{country}_{subject}_G{add_one_leading_zeros(grade_id)}_T{term_id}_S{add_one_leading_zeros(session_num)}_{session_type}{repeated}"
            new_path = os.path.join("TestingOutput", new_folder_name)
            if not ('(NF)' in new_folder_name or '(MultiIDs)' in new_folder_name or language in ['(MultiLanguages)', '(Lang_NF)'] or os.path.exists(new_path)):
                os.makedirs(new_path)
                if language == 'ar':
                    shutil.copytree(ar_CLS_folder_path, new_path, dirs_exist_ok=True)
                else:
                    shutil.copytree(en_CLS_folder_path, new_path, dirs_exist_ok=True)

            matching_folders.append((folder_name, new_folder_name, root, new_path, language ,metasession_ids, has_MSID, repeated, Errors))
        
        if counter == stop and when_to_stop != "":
            break
    return matching_folders

matching_folders = find_matching_folders()
tags_df = pd.DataFrame(matching_folders, columns=["FolderName", "NewFolderName", "OldPath", "NewPath", "Language", "Metasession_Ids", "has_MSID", "FolderRepetition", "Errors Found"])
tags_df.to_excel(csv_file_path, index=False, engine='openpyxl')

# Remove the used educational resources report
if os.path.exists("sessions_educational_resources_report.csv"):
    os.remove("sessions_educational_resources_report.csv")
