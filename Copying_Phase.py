import os
import shutil
import re
import pandas as pd

               
def normalizespace_with_lower(string):
    """
    Normalize spaces and convert the string to lowercase.
    
    Args:
    string (str): Input string.
    
    Returns:
    str: Normalized and lowercase string.
    """    
    return str(re.sub(r'\s+', ' ', string)).strip().lower()


def replace_non_alphanumeric_with_space(input_string):
    """
    Replace non-alphanumeric characters in the string with spaces and normalize spaces.
    
    Args:
    input_string (str): Input string.
    
    Returns:
    str: Modified string with non-alphanumeric characters replaced and normalized.
    """    
    input_string = input_string.replace('_',' ')
    return normalizespace_with_lower(re.sub(r'[^\w\s]', ' ', input_string))


# Read the Excel file into a Pandas DataFrame
file_path = os.path.join("TestingSource", "MetasessionID_Tagging.xlsx")

df = pd.read_excel(file_path, sheet_name='Sheet1')

# Regular expression pattern to match .tex files
filespattern = re.compile(r"^(?:([A-Za-z]+)_)?([A-Za-z0-9\s-]+)_([A-Za-z0-9\s-]+)(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?(?:_([A-Za-z0-9\s-]+))?$")

# List of files not to be copied
files_not_wanted_to_copy = [
    "Angle.tex","Combination.tex","ComplexConjugate.tex","CrossProduct.tex",
    "EgExamsStylesAR-800-600.tex","Factorial.tex","G6 Science_AR.tex",
    "Interval.tex","LineSegment-bak.tex","LineSegment.tex","MathLabel.tex",
    "Matrix.tex","MeasureAngle.tex","Moment.tex","Parallel.tex",
    "Permutation.tex","RD.tex","Ray.tex","SeqTerm.tex",
    "SetComplement-bak-bak.tex","SetComplement-bak.tex","SetComplement.tex",
    "SetMinus.tex","StLine.tex","Template_AR.tex","Triangle.tex",
    "Unicodes.tex","UnitVector.tex","Vector.tex","VectorComponents.tex",
    "VectorMagnitude.tex","arPresentation.tex","arSlides.tex",
    "arTutorPages.tex","enPresentation.tex","merge_files.tex",
    "nagwa.commands-bak.tex","nagwa.commands.tex","template.tex",
    "EgExamsStylesEN-800-600.tex","enSlides.tex","enTutorPages.tex",
    "Apache License.txt",".worksheet-bak.tex",".exam.tex",
    ".explainer.tex",".explainer-bak.tex",".lessonplan.tex",
    ".nagwawebSVG.flashcard.tex",".nagwawebSVG.tex",".pdfStyles.tex",
    ".worksheet.tex"
]

# List of file extensions not to be copied
ext_not_wanted_to_copy = [
    ".zip",".cls",".dtx",".lua",".otf",".out",".pl",".sty",".ttf",
    ".synctex.gz", ".log", ".aux"
]

def copy_items(old_path, new_path, FolderName, NewFolderName):
    """
    Copy items from the old path to the new path, excluding unwanted files and extensions.
    
    Args:
    old_path (str): Original path of the files.
    new_path (str): Destination path for the files.
    FolderName (str): Original folder name.
    NewFolderName (str): New folder name to be used.
    """    
    if '(NF)' in new_path or '(MultiIDs)' in new_path:
        return  # Exit the function if any of the conditions are met
    
    if not os.path.exists(new_path):
        os.makedirs(new_path)    

    
    FolderName_list=replace_non_alphanumeric_with_space(FolderName).split()
    main_pdf=FolderName+'.pdf'
    for root, _, files in os.walk(old_path):
        for file in files:
            if (file.endswith('.tex')) and (filespattern.match(file.rsplit('.', 1)[0].lower())) and (all(x in file.lower() for x in FolderName_list)) and ('old' not in file.lower()):
                main_tex_file_path = os.path.join(root, file)
                main_tex_destination_path = os.path.join(new_path, f"{NewFolderName}.tex")
                main_pdf=file.replace('.tex','.pdf')
                try:
                    shutil.copy(main_tex_file_path, main_tex_destination_path)
                except:
                    print(f"Main tex \"{main_tex_file_path}\" can't be copied to {main_tex_destination_path}.")
                    continue
            elif not (any(file.lower().endswith(ext) for ext in ext_not_wanted_to_copy) or (file in files_not_wanted_to_copy+[main_pdf])):
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(new_path, file)
                try:
                    shutil.copy(source_file_path, destination_file_path)
                except:
                    print(f"File \"{source_file_path}\" can't be copied to {destination_file_path}.")
                    continue

counter = 0          
for index, row in df.iterrows():
    old_path = row['OldPath']
    new_path = row['NewPath']
    FolderName = row['FolderName']
    NewFolderName = row['NewFolderName']

    
    copy_items(old_path, new_path, FolderName, NewFolderName)
    counter += 1
    print(f"\r{counter}", end="")
print("")
print("All items copied successfully.")