% https://grad.wisc.edu/currentstudents/doctoralguide/

\ProvidesClass{dissertation}

% --- basic ---------------------------------------------------------------------------------------

% required: 10 to 12 point font

\LoadClass[11pt, twoside, openright]{report}
\RequirePackage[letterpaper, margin=1in]{geometry}  % 1 inch margins required
\RequirePackage{setspace}
\RequirePackage{afterpage}
\RequirePackage{xcolor}
\RequirePackage{array}

% --- layout --------------------------------------------------------------------------------------

\let\stdchapter\chapter
\renewcommand\chapter{\cleardoublepage\stdchapter}

\let\stdsection\section
\renewcommand\section{\clearpage\stdsection}

\RequirePackage{afterpage}

\newcommand\blankpage{%
    \null
    \thispagestyle{empty}%
    \addtocounter{page}{-1}%
    \newpage}

% --- floats --------------------------------------------------------------------------------------

% force all floats to center (see https://tex.stackexchange.com/a/53383)
\makeatletter
\g@addto@macro\@floatboxreset{\centering}
\makeatother

% --- headers -------------------------------------------------------------------------------------

% required: page number in upper right, nothing else

\RequirePackage{fancyhdr}
\fancypagestyle{plain}{
  \fancyhf{}
  \fancyhead[R]{\thepage}
  \fancyfoot{}
	\renewcommand{\headrulewidth}{0pt}
	\renewcommand{\footrulewidth}{0pt}
}
\pagestyle{plain}{\rhead{\thepage}}

\setlength{\headheight}{14pt}

% --- text ----------------------------------------------------------------------------------------

% text
\RequirePackage[utf8]{inputenc}
\setlength\parindent{0pt}
\setlength{\parskip}{1em}
\renewcommand{\familydefault}{\sfdefault}

\newcommand{\RomanNumeral}[1]{\textrm{\uppercase\expandafter{\romannumeral #1\relax}}}
\RequirePackage{etoolbox}
\AtBeginEnvironment{verse}{\singlespacing}

\newenvironment{dquote}
  {
  \singlespacing
  \it
  }
  {
  }

\newcommand{\dsignature}[1]{\hfill \normalfont{-- #1}}

% --- tables --------------------------------------------------------------------------------------

\BeforeBeginEnvironment{table}{\clearpage}
\AfterEndEnvironment{table}{\clearpage}

% --- lists ---------------------------------------------------------------------------------------

\RequirePackage[shortlabels]{enumitem}
\setlist[enumerate, 1]{nosep}
\setlist[enumerate, 2]{nosep, topsep=-5ex}
\setlist[enumerate, 3]{nosep, topsep=-5ex}
\setlist[enumerate, 4]{nosep, topsep=-5ex}
\newenvironment{denumerate}
  {
  \begin{enumerate}
  \singlespacing
  }
  {
  \end{enumerate}
  }

\setlist[itemize, 1]{nosep}
\setlist[itemize, 2]{nosep, topsep=-5ex}
\setlist[itemize, 3]{nosep, topsep=-5ex}
\setlist[itemize, 4]{nosep, topsep=-5ex}
\newenvironment{ditemize}
  {
  \begin{itemize}
  \renewcommand{\labelitemi}{$\rightarrow$}
  \singlespacing
  }
  {
  \end{itemize}
  }

% --- code environment ----------------------------------------------------------------------------

\RequirePackage{etoolbox}
\RequirePackage{pmboxdraw}  % for box drawing charachters
\RequirePackage[section]{minted}
\usemintedstyle{default}
\setminted[python]{linenos=false, frame=none}

\definecolor{bg}{rgb}{0.95, 0.95, 0.95}

\RequirePackage[many]{tcolorbox}
\tcbuselibrary{minted}

%\tcbset{step={\refstepcounter{equation}}}

\NewTCBListing[number within=chapter, auto counter]{codefragment}{mo}{%
  colback=bg,
  boxrule=1pt,
  colframe=bg,
  arc=0pt,
  shadow=false,
  new/use counter=equation,
  boxsep=1ex, top=0pt, left=0pt, right=0pt, bottom=0pt,
  comment={\hfill(\arabic{chapter}.\arabic{equation})},
  listing outside comment,
  righthand width=3em,
  sidebyside gap=0pt,
  minted language=#1,
  %before skip =-0.5\baselinestretch,
  %after skip=2\baselinestretch,
}

\BeforeBeginEnvironment{codefragment}{\begin{singlespace}\stepcounter{equation}}
\AfterEndEnvironment{codefragment}{\end{singlespace}}

\newmintinline[bash]{bash}{bgcolor=bg}
\newmintinline[python]{python}{bgcolor=bg}

\newcommand{\includepython}[1]{\inputminted[bgcolor=bg]{python}{#1}}
\newcommand{\includebash}[1]{\inputminted[bgcolor=bg]{bash}{#1}}

% --- graphics ------------------------------------------------------------------------------------

\RequirePackage{graphics}
\RequirePackage{graphicx}
\RequirePackage{epsfig}
\RequirePackage{epstopdf}
\RequirePackage{etoc}
\RequirePackage{tikz}
\RequirePackage{pdflscape}  % provides \begin{landscape}; \end{landscape}

\BeforeBeginEnvironment{figure}{\clearpage}
\AfterEndEnvironment{figure}{\clearpage}

% for some reason this doesn't work...
\newenvironment{lsfigure}
  {
  \begin{landscape}
  \begin{figure}
  }
  {
  \end{landscape}
  \end{figure}
  }

% --- math ----------------------------------------------------------------------------------------

\RequirePackage{amssymb}
\RequirePackage{amsmath}
\RequirePackage[cm]{sfmath}
\RequirePackage{bm} % bold mathtype
\DeclareMathOperator{\me}{e}

% --- misc / ? ------------------------------------------------------------------------------------

\RequirePackage[nottoc]{tocbibind}
\RequirePackage{fixltx2e}
\RequirePackage{pdfpages}
\RequirePackage[utf8]{inputenc}

% --- hyperref ------------------------------------------------------------------------------------

\RequirePackage[colorlinks=true, linkcolor=black, urlcolor=blue, citecolor=black,
anchorcolor=black]{hyperref}
\RequirePackage[all]{hypcap}  % helps hyperref work properly

\renewcommand{\chapterautorefname}{Chapter}
\renewcommand{\sectionautorefname}{Section}
\renewcommand{\subsectionautorefname}{Section}
\renewcommand{\subsubsectionautorefname}{Section}

% --- bibliography --------------------------------------------------------------------------------

\RequirePackage[backend=biber, natbib=true, sorting=none, maxbibnames=99, isbn=false]{biblatex}
\bibliography{bibliography}