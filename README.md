# SessionsRestructureTOOL

SessionsRestructureTOOL is a Python-based tool designed to restructure session files for educational resources. This project is a simplified version of a more complex tool used internally for processing a large number of session files and their associated metadata.

## Project Structure

```
D:\\DOCS\\CV\\GITHUB\\SessionsRestructureTOOL\\
│   .gitignore
│   1-MetasessionID_Tagging_RUN.bat
│   2-Copying_Phase_RUN.bat
│   3-Distribute_Slides_RUN.bat
│   4-Editing_Main_Tex_RUN.bat
│   Copying_Phase.py
│   Distribute_Slides.py
│   Editing_Main_Tex.py
│   LICENSE
│   MetasessionID_Tagging.py
│   README.md
│   repair.bat
│   requirements.txt
│   session_number.py
│   setup.bat
│   title_mapping.py
│
├───TestingOutput/   (this will have the generated folders)
└───TestingSource/
    │   processed_sessions_educational_resources_report.csv
    │
    ├───AR_CLS/
    │   └───CLS/ (having sample files that can be replaced by the AR class files, fonts, and other required static files)
    │           a number of files
    │
    ├───EN_CLS/
    │  └───CLS/ (having sample files that can be replaced by the EN class files, fonts, and other required static files)
    │          a number of files
    │          
    ├───EG_Biology_AR_G12_T0_S01_Exam Prep/
    │   └───Input/
    │       │   a number of input files
    │       ├───NonQuestions/
    │       │       a number of questions' files
    │       └───Questions/
    │               a number of questions' files
    │
    └───EG_Spanish_G12_T0_S08/
        └───Input/
            │   a number of input files
            ├───NonQuestions/
            │       a number of non questions' files
            └───Questions/
                    a number of questions' files
```

## Features

- **Session Tagging:** Automatically tag session folders based on metadata.
- **File Copying:** Copy required files to destination folders based on tags.
- **Slide Distribution:** Distribute slides into respective session folders.
- **Main .tex Editing:** Edit main .tex files to include metadata and generate final outputs.
- **Handling Large Data Sets:** Process large numbers of session files efficiently.
- **Simplified Version:** Simplified for privacy, omitting proprietary data and including sample files for demonstration.

## Prerequisites

- Python 3.x
- Required Python packages listed in `requirements.txt`

## Requirements

The required Python packages are listed in `requirements.txt`:

```
pandas==2.1.1
glob2==0.7
requests==2.31.0
urllib3==2.2.1
openpyxl==3.1.2
```

## Files

- **MetasessionID_Tagging.py:** Script to process the base directory and generate the necessary tagging for sessions.
- **Copying_Phase.py:** Script to copy the required files from the source to the destination directories based on the tagging.
- **Distribute_Slides.py:** Script to distribute slides into their respective session folders.
- **Editing_Main_Tex.py:** Script to edit the main .tex files to include the necessary metadata and generate the final output.
- **requirements.txt:** Lists all Python dependencies needed for the project.
- **setup.bat:** Sets up the virtual environment and installs dependencies.
- **1-MetasessionID_Tagging_RUN.bat:** Runs the `MetasessionID_Tagging.py` script.
- **2-Copying_Phase_RUN.bat:** Runs the `Copying_Phase.py` script.
- **3-Distribute_Slides_RUN.bat:** Runs the `Distribute_Slides.py` script.
- **4-Editing_Main_Tex_RUN.bat:** Runs the `Editing_Main_Tex.py` script.
- **repair.bat:** Re-installs dependencies in case of updates to `requirements.txt`.
- **LICENSE:** The license under which this project is distributed.
- **README.md:** This file, providing an overview and instructions for the project.

## Installation

1. Clone the repository:

```
git clone https://github.com/mofasuhu/SessionsRestructureTOOL.git
```

2. Navigate to the project directory:

```
cd SessionsRestructureTOOL
```

3. Create and activate a virtual environment:

```
python -m venv venv
```

On Windows use:

```
venv\\Scripts\\activate
```

On macOS/Linux use:

```
source venv/bin/activate
```

4. Install the required packages:

```
pip install -r requirements.txt
```

Alternatively, you can use the provided setup script:

```
setup.bat
```

This script will create a virtual environment, install the required packages, and pause the command prompt.

## Usage

1. Run the MetasessionID_Tagging script:

```
1-MetasessionID_Tagging_RUN.bat
```

This will process the base directory and generate the necessary tagging for sessions.

2. Run the Copying Phase script:

```
2-Copying_Phase_RUN.bat
```

This will copy the required files from the source to the destination directories based on the tagging.

3. Run the Distribute Slides script:

```
3-Distribute_Slides_RUN.bat
```

This will distribute the slides into their respective session folders.

4. Run the Editing Main Tex script:

```
4-Editing_Main_Tex_RUN.bat
```

This will edit the main .tex files to include the necessary metadata and generate the final output.

## Simplifications

- The original version of the `MetasessionID_Tagging.py` script included code to download the `sessions_educational_resources_report.csv` file and process it to generate `processed_sessions_educational_resources_report.csv`. This part is omitted for privacy reasons.
- The source directory originally contained over 30,000 folders, but only a few sample folders are included in this simplified version.
- The CLS folders originally had many files, but only a few sample files are included in this simplified version.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## Contact

If you have any questions or suggestions, feel free to contact us at [mofasuhu@gmail.com](mailto:mofasuhu@gmail.com).
