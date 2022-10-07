\ProvidesClass{presentation}

% --- basic ---------------------------------------------------------------------------------------

\LoadClass[11pt, aspectratio=169, final]{beamer}

% --- layout --------------------------------------------------------------------------------------

% document
\RequirePackage{adjustbox}
\adjustboxset*{center}
\RequirePackage{color}
\RequirePackage{xcolor}
\RequirePackage{textpos}

% --- text ----------------------------------------------------------------------------------------
% text
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{enumerate}
\RequirePackage{soul}
\sethlcolor{yellow}
\RequirePackage{verbatim}

%\renewcommand{\familydefault}{\sfdefault}
\RequirePackage[cm]{sfmath}
\renewcommand<>{\hl}[1]{\only#2{\beameroriginal{\hl}}{#1}}

\usefonttheme{structurebold}

% --- theme ---------------------------------------------------------------------------------------

% colors (from https://github.com/chriskempson/tomorrow-theme)
\definecolor{background}{HTML}{1D1F21}
\definecolor{selection}{HTML}{373B41}
\definecolor{foreground}{HTML}{C5C8C6}
\definecolor{comment}{HTML}{969896}
\definecolor{red}{HTML}{CC6666}
\definecolor{orange}{HTML}{F5871F}
\definecolor{yellow}{HTML}{EAB700}
\definecolor{green}{HTML}{718C00}
\definecolor{aqua}{HTML}{3E999F}
\definecolor{blue}{HTML}{4271AE}
\definecolor{purple}{HTML}{8959A8}

\usetheme[width=2cm]{Hannover}
\usecolortheme{beaver}
\setbeamercolor*{palette primary}{fg=darkred!60!black, bg=selection}  % title background
\setbeamercolor*{sidebar}{fg=darkred, bg=background}
\setbeamercolor{frametitle}{bg=selection, fg=foreground}
\setbeamercolor{title}{fg=foreground}
\setbeamercolor{palette sidebar primary}{fg=foreground}  % sidebar subsection
\setbeamercolor{palette sidebar secondary}{fg=foreground}  % sidebar section
\setbeamercolor{palette sidebar tertiary}{fg=red}  % sidebar name
\setbeamercolor{palette sidebar quaternary}{fg=aqua}  % sidebar title
\setbeamercolor*{item}{fg=foreground}
\setbeamertemplate{itemize items}[default]
\setbeamercovered{transparent}
\setbeamertemplate{navigation symbols}{}

% --- quotes --------------------------------------------------------------------------------------

\RequirePackage[T1]{fontenc}
%\RequirePackage{libertine}
\RequirePackage{framed}
\newcommand*\openquote{\makebox(25,-22){\scalebox{5}{``}}}
\newcommand*\closequote{\makebox(25,-22){\scalebox{5}{''}}}
\colorlet{shadecolor}{foreground}
\makeatletter
\newif\if@right
\def\shadequote{\@righttrue\shadequote@i}
\def\shadequote@i{\begin{snugshade}}
		\def\endshadequote{%
			\if@right\hfill\fi\end{snugshade}}
\@namedef{shadequote*}{\@rightfalse\shadequote@i}
\@namedef{endshadequote*}{\endshadequote}
\makeatother

% graphics
\RequirePackage{graphicx}
\RequirePackage{animate}
\RequirePackage{xmpmulti}

% bibliography
\RequirePackage[style=verbose,backend=bibtex,bibstyle=numeric,sorting=none]{biblatex}
\bibliography{database}
\renewcommand\footnoterule{{\color{black} \hrule height 0pt}} % no line above footnotes
\renewcommand{\footnotesize}{\tiny}
\setbeamercolor{bibliography entry author}{fg=black,bg=black}
\setbeamercolor{bibliography entry title}{fg=black,bg=black}
\setbeamercolor{bibliography entry location}{fg=black,bg=black}
\setbeamercolor{bibliography entry note}{fg=black,bg=black}

% http://tex.stackexchange.com/questions/41683/why-is-it-that-coloring-in-soul-in-beamer-is-not-visible
\makeatletter
\newcommand\SoulColor{%
	\let\set@color\beamerorig@set@color
	\let\reset@color\beamerorig@reset@color}
\makeatother
\SoulColor

% logo (not built-in to hannover)
\addtobeamertemplate{headline}{}{%
\begin{textblock*}{\paperwidth}(0.5cm,\textheight-1.75cm)
	\includegraphics[width=1cm]{logo} % logo of my university
\end{textblock*}}
