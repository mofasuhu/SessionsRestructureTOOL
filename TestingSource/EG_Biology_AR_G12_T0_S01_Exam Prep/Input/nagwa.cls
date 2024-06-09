%CLSversion 1.1.2
\ProvidesClass{nagwa}[2016/08/08]

%==========================Packages==========================

\RequirePackage{kvoptions} % to allow adding key-pair options
\RequirePackage{pdfpages} % to include any PDF images
\RequirePackage{tikz} % our standard package for math environments
\RequirePackage{amsmath} % our standard package for math environments\typeout{Required packages loaded...}
%\RequirePackage{xstring} % to check if parameter is number
\typeout{Packages loaded...}

%==========================Options==========================

\DeclareStringOption{country}{} 
\DeclareStringOption{nagwalang}{}
\DeclareStringOption{math}{}
\DeclareStringOption{numerals}{}
\DeclareStringOption{directions}{}
\DeclareStringOption{qrcmode}{}
\ProcessKeyvalOptions*\relax

\let\country=\nagwa@country
\typeout{ Your country \country}
\let\nagwalang=\nagwa@nagwalang
\typeout{ Your language \nagwalang}
\let\math=\nagwa@math
\typeout{ Your symbols language is \math}
\let\directions = \nagwa@directions
\typeout{ Your directions are in \directions}
\let\numerals = \nagwa@numerals
\typeout{ Your numerals are in \numerals}
\let\qrcmode = \nagwa@qrcmode
\typeout{ Your mode are in \qrcmode}

\def\objecttype#1{\def\@objecttype{#1}}
\DeclareOption{EduScreen}{\objecttype{EduScreen}}
\DeclareOption{Singles}{\objecttype{Singles}}
\DeclareOption{TikZFigure}{\objecttype{TikZFigure}}
\DeclareOption{ExampleExtraction}{\objecttype{ExampleExtraction}}
\DeclareOption{ExamplePDF}{\objecttype{ExamplePDF}} 
\DeclareOption{instances}{\objecttype{instances}} 
\DeclareOption{instancePDF}{\objecttype{instancePDF}} 
\DeclareOption{DisplayedEquation}{\objecttype{DisplayedEquation}}
\DeclareOption{InlineEquation}{\objecttype{InlineEquation}}
\DeclareOption{englishArabicInstances}{\objecttype{englishArabicInstances}}
\DeclareOption{Worksheet}{\objecttype{Worksheet}}
\DeclareOption{Explainer}{\objecttype{Explainer}}
\DeclareOption{LessonPlan}{\objecttype{LessonPlan}}
\DeclareOption{Exam}{\objecttype{Exam}}
\DeclareOption{InlineChem}{\objecttype{InlineChem}}
\DeclareOption{DisplayedChem}{\objecttype{DisplayedChem}}
\DeclareOption{InlineEquationForFlashcard}{\objecttype{InlineEquationForFlashcard}}
\DeclareOption{DisplayedEquationForFlashcard}{\objecttype{DisplayedEquationForFlashcard}}
\DeclareOption{InlineChemForFlashcard}{\objecttype{InlineChemForFlashcard}}
\DeclareOption{DisplayedChemForFlashcard}{\objecttype{DisplayedChemForFlashcard}}
\DeclareOption{TikZFigureForFlashcard}{\objecttype{TikZFigureForFlashcard}}
\DeclareOption*{}{}
\DeclareMathOperator{\adj}{adj}						   
\ProcessOptions*\relax
\typeout{Options loaded...}

%==========================Inputs==========================

\input{.worksheet}
\input{.exam}
\input{.explainer}
\input{.nagwawebSVG}
\input{.nagwawebSVG.flashcard}
\input{.lessonplan}
\input{nagwa.commands}
%\input{\nagwalang.\country.commands}

% font style and size
\everymath{\displaystyle}

\directlua{
luatexbase.add_to_callback("show_error_hook", function ()
texio.write_nl("[" .. status.filename .. ": " .. status.linenumber .. "]")
if (status.lasterrorcontext) then texio.write_nl(status.lasterrorcontext) end
texio.write_nl("ERROR_END")
end, "show_error_hook")
}