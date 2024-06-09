import random
import os
import re
import json
import shutil
import logging
import stat

def remove_read_only_file(file_path):
    """
    Remove a read-only file.
    
    Args:
    file_path (str): Path to the file to be removed.
    """
    os.chmod(file_path, stat.S_IWRITE)
    os.remove(file_path)

def setup_logging(log_file, encoding='utf-8', errors='replace'):
    """
    Setup the logging system to log errors to a specified file.
    
    Args:
    log_file (str): Path to the log file.
    encoding (str): Encoding to use for the log file.
    errors (str): Error handling scheme.
    """    
    logging.basicConfig(filename=log_file, level=logging.ERROR,
                        format='%(message)s', filemode='w', encoding=encoding)

def filter_log_file(input_file_path):
    """
    Filter the log file to keep only unique lines.
    
    Args:
    input_file_path (str): Path to the log file.
    """    
    unique_lines = set()
    with open(input_file_path, 'r', encoding='utf-8', errors='replace') as file:
        for line in file:
            unique_lines.add(line)
    with open(input_file_path, 'w', encoding='utf-8', errors='replace') as file:
        for line in unique_lines:
            file.write(line)

def close_logging():
    """
    Close the logging system and remove all handlers.
    """    
    for handler in logging.root.handlers[:]:
        handler.close()
        logging.root.removeHandler(handler)

def remove_empty_log_file(log_file):
    """
    Remove the log file if it is empty.
    
    Args:
    log_file (str): Path to the log file.
    """    
    if os.path.exists(log_file) and os.path.getsize(log_file) == 0:
        os.remove(log_file)

# Load Major.json
MAJOR_JSON_PATH = "TestingSource\\Sessions_Restructure.json"

if os.path.exists(MAJOR_JSON_PATH):
    with open(MAJOR_JSON_PATH, 'r', encoding='utf-8') as major_file:
        major_data = json.load(major_file)
else:
    major_data = []

def generate_unique_12_digit_id(existing_ids):
    """
    Generate a unique 12-digit ID that does not exist in the existing IDs.
    
    Args:
    existing_ids (set): Set of existing IDs.
    
    Returns:
    str: New unique 12-digit ID.
    """    
    while True:
        new_id = ''.join([str(random.randint(1, 9)) for _ in range(1)]+[str(random.randint(0, 9)) for _ in range(11)])
        if new_id not in existing_ids:
            return new_id
    
def request_12_digit_id(session_folder, file_name):
    """
    Request a 12-digit ID for a given file or retrieve an existing one.
    
    Args:
    session_folder (str): Name of the session folder.
    file_name (str): Name of the file.
    
    Returns:
    str: 12-digit ID.
    """  
    global major_data
    if not re.match(r'^\d{12}\.(?:\d+\.)?tex$', file_name):
        for session in major_data:
            if session_folder in session:
                if file_name.rsplit('.', 1)[0] in session[session_folder]:
                    return session[session_folder][file_name.rsplit('.', 1)[0]]
        
        # Generate a new unique 12-digit ID
        existing_ids = {id for session in major_data for session_ids in session.values() for id in session_ids.values()}
        new_id = generate_unique_12_digit_id(existing_ids)
        return new_id
        
    else:
        return file_name.replace('.tex', '')


def process_sessions(sessions_path, logger):
    """
    Process session folders and distribute slides.
    
    Args:
    sessions_path (str): Path to the sessions.
    logger (Logger): Logger object for logging errors.
    """ 
    global major_data
    for session_folder in os.listdir(sessions_path):
        print(session_folder)
        session_path = os.path.join(sessions_path, session_folder)
        if os.path.isdir(session_path):
            session_entry = next((entry for entry in major_data if session_folder in entry), None)
            if session_entry is None:
                session_entry = {session_folder: {}}
                major_data.append(session_entry)

            for file_name in os.listdir(session_path):
                type_1 = re.match(r'^\d{12}\.(?:\d+\.)?tex$', file_name)
                type_2 = re.match(r'^(Slide|Image|slide|image)_\d+\.tex$', file_name)

                old_file_path = os.path.join(session_path, file_name)
                if type_1 or type_2:
                    
                    file_id = request_12_digit_id(session_folder, file_name)
                    new_file_name = file_id + '.tex'
                    new_file_path = os.path.join(session_path, file_id, new_file_name)
                    os.makedirs(os.path.join(session_path, file_id), exist_ok=True)
                    shutil.copy(old_file_path, new_file_path)
                    with open(new_file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    lines = content.split('\n')

                    # Initialize a list to store references
                    all_references = []
                    
                    # Process each line
                    for line in lines:
                        if not line.strip().startswith('%'):
                            references = re.findall(r'\{([^{}]*?\.(tikz\.pdf|tikz|pdf|jpg|png))\}', line)
                            all_references.extend(references)                    
                    all_references = list(set(all_references))    
                    for reference in all_references:
                        old_ref = reference[0]
                        ref_file_name = reference[0].split("/")[-1]
                        content = content.replace(old_ref, f"{file_id}/{ref_file_name}")
                        
                        if ref_file_name.endswith('.tikz'):
                            ref_file_name += '.pdf'
                            
                        new_ref = f"{file_id}/{ref_file_name}"
                        ref_old_path = os.path.join(session_path, ref_file_name)
                        ref_new_path = os.path.join(session_path, new_ref)
                        
                        if os.path.exists(ref_old_path):
                            shutil.copyfile(ref_old_path, ref_new_path)
                        else:
                            logger.error(f"Error: {ref_file_name} of {file_name}->{new_file_name} in {session_folder} not found!")
                        
                    with open(new_file_path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    
                    session_entry[session_folder][file_name.rsplit('.', 1)[0]] = file_id

            for file_name in os.listdir(session_path):
                old_file_path = os.path.join(session_path, file_name)
                if os.path.exists(old_file_path) and os.path.isfile(old_file_path) and file_name not in [session_folder+'.json', session_folder+'.tex', session_folder+'.csv']:
                    try:
                        remove_read_only_file(old_file_path)
                    except:
                        pass
    
        with open(MAJOR_JSON_PATH, 'w', encoding='utf-8') as json_file:
            json.dump(major_data, json_file, ensure_ascii=False, indent=4)

# Initialize logger
current_folder = os.getcwd()
logfile = os.path.join(current_folder, "TestingSource", 'Distribute_Slides_ERROR.log')

if os.path.exists(logfile):
    os.remove(logfile)

setup_logging(logfile, encoding='utf-8', errors='replace')
logger = logging.getLogger(__name__)   
                    
try:
    sessions_path = "TestingOutput"
    process_sessions(sessions_path, logger)

    close_logging()
    filter_log_file(logfile)
    remove_empty_log_file(logfile)
    
except Exception as e:
    logging.error(f"Global Error: {str(e)}.")
    close_logging()
    filter_log_file(logfile)
    remove_empty_log_file(logfile)
