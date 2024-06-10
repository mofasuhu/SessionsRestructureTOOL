import os
import re
import pandas as pd
import json

def search_json(session_folder):
    """
    Search for session data in major_data based on session folder.
    
    Args:
    session_folder (str): The name of the session folder.
    
    Returns:
    dict: Data related to slides in the session folder.
    """    
    for session in major_data:
        if session_folder in session:
            slide_data = session[session_folder]
            return slide_data
    return dict()

def add_one_leading_zeros(num):
    """
    Add a leading zero to a single-digit number.
    
    Args:
    num (str): Input number.
    
    Returns:
    str: Number with leading zero.
    """    
    if str(num).isdigit():
        return f"{int(num):02}"
    else:
        return num

def add_two_leading_zeros(num):
    """
    Add two leading zeros to a number.
    
    Args:
    num (str): Input number.
    
    Returns:
    str: Number with two leading zeros.
    """    
    if str(num).isdigit():
        return f"{int(num):03}"
    else:
        return num    
    
def normalize_space(string):
    """
    Normalize spaces in a string by replacing multiple spaces with a single space and converting to lowercase.
    
    Args:
    string (str): Input string.
    
    Returns:
    str: Normalized string.
    """    
    return str(re.sub(r'\s+', ' ', string)).strip().lower().replace("_", " ")

def insert_special_rows_for_exam_prep(directory):
    """
    Insert special rows for exam preparation in a DataFrame created from CSV files.
    
    Args:
    directory (str): Directory containing the .tex and .csv files.
    
    Returns:
    tuple: DataFrame with inserted rows and the path to the CSV file.
    """    
    df = pd.DataFrame()
    csv_file_path = ''
    for filename in os.listdir(directory):
        if filename.endswith(".tex"):
            tex_file_path = os.path.join(directory, filename)
            csv_file_path = os.path.join(directory, filename.replace('.tex', '.csv'))

            if not os.path.exists(csv_file_path):
                print(f"No CSV found for {filename}. Skipping...")
                continue

            with open(tex_file_path, 'r', encoding='utf-8') as tex_file:
                tex_content = tex_file.read()

            input_positions = [m.start() for m in re.finditer(r'\\input\{NonQuestions/.*?\}', tex_content)]
            insert_positions = []
            for pos in input_positions:
                insert_positions.append(tex_content[:pos].count('\\slide'))
                


            df = pd.read_csv(csv_file_path, encoding="utf-8").fillna("")

            df['item_id'] = df['item_id'].astype(str).str.replace('.0', '')
            condition = (df.iloc[0]['type'] == 'image' and df.iloc[0]['content'] == 'title') and (df.iloc[1]['type'] == 'image' and df.iloc[1]['content'] == 'toc')
                    
            for insert_pos in reversed(insert_positions):
                factor = insert_positions.index(insert_pos)
                if insert_pos==0:
                    print(1,insert_pos)
                    adjusted_insert_pos = 0
                    df = pd.concat([df.iloc[:adjusted_insert_pos], pd.DataFrame([{'type': 'image', 'content': 'title'}, {'type': 'image', 'content': 'toc'}]), df.iloc[adjusted_insert_pos:]]).reset_index(drop=True)
                elif factor==0 and insert_pos!=0 and not condition:
                    print(2,insert_pos)
                    factor+=1
                    adjusted_insert_pos = insert_pos * factor
                    df = pd.concat([df.iloc[:adjusted_insert_pos], pd.DataFrame([{'type': 'image', 'content': 'instructional'}]), df.iloc[adjusted_insert_pos:]]).reset_index(drop=True)               
                elif factor==0 and insert_pos!=0 and condition:
                    print(3,insert_pos)
                    factor+=2
                    adjusted_insert_pos = insert_pos * factor
                    df = pd.concat([df.iloc[:adjusted_insert_pos], pd.DataFrame([{'type': 'image', 'content': 'instructional'}]), df.iloc[adjusted_insert_pos:]]).reset_index(drop=True)
                elif factor==1 and insert_pos!=0 and condition:
                    print(4,insert_pos)
                    adjusted_insert_pos = insert_pos * factor + 1
                    df = pd.concat([df.iloc[:adjusted_insert_pos], pd.DataFrame([{'type': 'image', 'content': 'instructional'}]), df.iloc[adjusted_insert_pos:]]).reset_index(drop=True)
                elif factor==1 and insert_pos!=0 and not condition:
                    print(5,insert_pos)
                    adjusted_insert_pos = insert_pos * factor
                    df = pd.concat([df.iloc[:adjusted_insert_pos], pd.DataFrame([{'type': 'image', 'content': 'instructional'}]), df.iloc[adjusted_insert_pos:]]).reset_index(drop=True)                    
                elif factor>1 and insert_pos!=0 and condition:
                    print(6,insert_pos)
                    adjusted_insert_pos = insert_pos + 1
                    df = pd.concat([df.iloc[:adjusted_insert_pos], pd.DataFrame([{'type': 'image', 'content': 'instructional'}]), df.iloc[adjusted_insert_pos:]]).reset_index(drop=True)
                elif factor>1 and insert_pos!=0 and not condition:
                    print(7,insert_pos)
                    adjusted_insert_pos = insert_pos
                    df = pd.concat([df.iloc[:adjusted_insert_pos], pd.DataFrame([{'type': 'image', 'content': 'instructional'}]), df.iloc[adjusted_insert_pos:]]).reset_index(drop=True)               

            df['slide_no'] = range(1, len(df) + 1)
            df.to_csv(csv_file_path, index=False)
    return df, csv_file_path
            
def process_slide(title, slide_path, slide_no, data, filename):
    """
    Process a slide based on its type and add relevant information to the data list.
    
    Args:
    title (str): Title of the slide.
    slide_path (str): Path to the slide.
    slide_no (int): Slide number.
    data (list): List to store slide data.
    filename (str): Name of the .tex file.
    """    
    if 'NonQuestions' in slide_path:
        item_id = re.findall(r'NonQuestions/(Slide_\d+|Image_\d+)', slide_path)
        if item_id:
            append_non_question_slide(data, slide_no, title, item_id[0])
    elif 'Questions' in slide_path:
        question_id = re.findall(r'Questions/(\d+\.*\d*)', slide_path)
        if question_id:
            question_source = 'past_papers' if 'Past Years' in title or 'أسئلة التجميعات' in title else ''
            append_question_slide(data, slide_no, title, question_id[0], question_source)
            
def process_slides(slides, filename):
    """
    Process all slides in a .tex file and generate data for a CSV file.
    
    Args:
    slides (list): List of slides to process.
    filename (str): Name of the .tex file.
    
    Returns:
    list: Data generated from the slides.
    """    
    data = []
    slide_no = 1
    for a, title, b, slide_path in slides:
        title = a + title + b
        process_slide(title, slide_path, slide_no, data, filename)
        slide_no += 1
    data.append([slide_no + 1, 'image', 'thank_you', '', 'Thank You', '', '', '', ''])
    return data

def process_tex_file(folderpath, filename):
    """
    Process a .tex file to extract slide information and generate a CSV file.
    
    Args:
    folderpath (str): Path to the folder containing the .tex file.
    filename (str): Name of the .tex file.
    """    
    tex_file_path = os.path.join(folderpath, filename)
    try:
        with open(tex_file_path, 'r', encoding='utf-8') as file:
            content = ''.join([line for line in file if not line.lstrip().startswith('%')])

        document_content_re = re.compile(r'\\begin{document}(.*?)\\end{document}', re.DOTALL)
        document_content = document_content_re.search(content)

        if not document_content:
            raise ValueError("Check document content!")

        slides_re = re.compile(r'\\slide+\{.*?\}\{(\\begin\{minipage\}\{\d*pt\})?(.*?)(\\end\{minipage\})?\}\{(.*?)\}', re.DOTALL)
        slides = slides_re.findall(document_content.group(1))

        data = process_slides(slides, filename)

        if data:
            output_csv_path = os.path.join(folderpath, filename.replace('.tex', '.csv'))
            df = pd.DataFrame(data, columns=['slide_no', 'type', 'content', 'item_id', 'title', 'language', 'prompt', 'code', 'question_source'])
            df.to_csv(output_csv_path, encoding='utf-8', index=False)
    except Exception as e:
        print(f"Error in processing file {filename}: {e}.")
    
def append_non_question_slide(data, slide_no, title, item_id):
    """
    Append a non-question slide to the data list.
    
    Args:
    data (list): List to store slide data.
    slide_no (int): Slide number.
    title (str): Title of the slide.
    item_id (str): ID of the slide item.
    """    
    if slide_no == 1 and 'Activity' not in title:
        data.append([1, 'image', 'title', item_id, title, '', '', '', ''])
        data.append([2, 'image', 'toc', item_id, title, '', '', '', ''])
    elif 'Python Activity' in title:
        data.append([slide_no + 1, 'coding', '', item_id, title, 'python', '', '', ''])
    elif title == 'Activity':
        data.append([slide_no + 1, 'activity', '', item_id, title, '', '', '', ''])
    else:
        data.append([slide_no + 1, 'image', 'instructional', item_id, title, '', '', '', ''])


        
def append_question_slide(data, slide_no, title, question_id, question_source):
    """
    Append a question slide to the data list.
    
    Args:
    data (list): List to store slide data.
    slide_no (int): Slide number.
    title (str): Title of the slide.
    question_id (str): ID of the question.
    question_source (str): Source of the question.
    """    
    data.append([slide_no + 1, 'question', '', question_id, title, '', '', '', question_source])

# Load Major.json
MAJOR_JSON_PATH = "TestingSource\\Sessions_Restructure.json"

if os.path.exists(MAJOR_JSON_PATH):
    with open(MAJOR_JSON_PATH, 'r', encoding='utf-8') as major_file:
        major_data = json.load(major_file)
else:
    major_data = []



processed_df=pd.read_csv(r"TestingSource\processed_sessions_educational_resources_report.csv", encoding="utf-8")



for session_folder in os.listdir("TestingOutput"):
    resume = True
    print(session_folder)
    session_path = os.path.join("TestingOutput", session_folder)
    if os.path.isdir(session_path):
        for file_name in os.listdir(session_path):
            if file_name == session_folder+'.tex':
                file_path = os.path.join(session_path, file_name)

                with open(file_path, 'r', encoding='utf-8') as file:
                    tex_content = file.readlines()
                new_content = "% !TeX program = lualatex --interaction=nonstopmode -include-directory=./CLS %.tex | txs:///view\n"
                if new_content in tex_content:
                    resume =False 
                
                if resume:
                    country = file_name.split('_')[1].lower()    
                    if country not in ['eg', 'in', 'sa', 'uk', 'us']:
                        country = '(NF)'
        
                    metasession_id=file_name.split('_')[0]
                    if re.match(r'^\d{12}$', metasession_id):
                        subject=processed_df['Class Subject'][processed_df['Meta Session Id']==int(metasession_id)].iloc[0]
                        language=processed_df['Session Language'][processed_df['Meta Session Id']==int(metasession_id)].iloc[0]
                        grade=add_one_leading_zeros(processed_df['Grade ID'][processed_df['Meta Session Id']==int(metasession_id)].iloc[0])
                        term=processed_df['Term'][processed_df['Meta Session Id']==int(metasession_id)].iloc[0]
                        session_title=processed_df['Session Title'][processed_df['Meta Session Id']==int(metasession_id)].iloc[0]
                    else:
                        metasession_id='(NF)'
                        subject='(NF)'
                        language='(NF)'
                        grade='(NF)'
                        term='(NF)'
                        session_title='(NF)'

                    for line in tex_content:
                        if r'\documentclass' in line:
                            new_content+=line+'\n'
                            continue

                        if r'\usepackage' in line:
                            new_content+=line+'\n'
                            continue

                        if r'\begin{document}' in line:
                            new_content+=line
                            break
                            
                    defining_lines = f"""
                    \\metasessionID{{{metasession_id}}}
                    \\sessioncountry{{{country}}}
                    \\subject{{{subject}}}
                    \\languageofinstruction{{{language}}}
                    \\grade{{{grade}}}
                    \\term{{{term}}}
                    \\sessiontitle{{{session_title}}}

                    """        
                    new_content+=defining_lines
                    
                    process_tex_file(session_path, file_name)
                    df, csv_path = insert_special_rows_for_exam_prep(session_path)
      
                    slide_data = search_json(session_folder)

                    df['item_id'] = df.apply(
                        lambda row: pd.Series(slide_data.get(row['item_id'], row['item_id'])), axis=1)

                    df=df[df['content']!='thank_you']
                    
                    titleline=''
                    tocline='\\begin{toc}\n'
                    other_lines=''
                    for index, row in df.iterrows():
                        if row["content"]=="title":
                            titleline=f"\\slide{{000}}{{{row['item_id']}}}{{{row['title']}}}{{title}}\n"
                            continue
                        if row["content"]=="toc":
                            tocline+=f"\\slide{{001}}{{{row['item_id']}}}{{{row['title']}}}{{toc}}\n\\end{{toc}}\n"
                            continue
                        other_lines+=f"\\slide{{{add_two_leading_zeros(index)}}}{{{row['item_id']}}}{{{row['title']}}}{{{row['type']}}}\n"

                    other_lines+='\\end{document}'    

                    new_content+=titleline
                    new_content+=tocline
                    new_content+=other_lines

                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(new_content)               
                    os.remove(csv_path)
                    