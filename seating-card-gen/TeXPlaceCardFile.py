class TeXPlaceCardFile:
    def __init__(self, filename, eventName):
        self.fd = open(filename, 'w')
        self.eventName = eventName

    def __enter__(self):
        self.start_placecard_tex()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_placecard()
        self.fd.close()

    def start_placecard_tex(self):
        self.fd.write(
            r'''\documentclass[letterpaper,oneside]{article}
        %\usepackage{luatextra}
        \usepackage{graphicx}
        \usepackage{tikz}
        \usetikzlibrary{calc}
        \usepackage{eso-pic}
        \usepackage[margin=0mm, paper=letterpaper]{geometry}
        \usepackage{rotating}
        \usepackage{calc}

        \pagestyle{empty}
        \AddToShipoutPicture{%
        \begin{tikzpicture}[remember picture,overlay]
        \coordinate (CYT) at ($(current page.center) + ( 0, 0.25in)$) ;
        \coordinate (CYB) at ($(current page.center) - ( 0, 0.25in)$) ;
        \coordinate (CXR) at ($(current page.center) + ( 0.25in, 0)$) ;
        \coordinate (CXL) at ($(current page.center) - ( 0.25in, 0)$) ;

        \coordinate (LL)    at ($(current page.south west) + (         0, 5.5in)$) ;
        \coordinate (LR)    at ($(current page.south west) + ( .35in, 5.5in)$) ;
        \coordinate (RL)    at ($(current page.south east) + (-.35in, 5.5in)$) ;
        \coordinate (RR)    at ($(current page.south east) + (         0, 5.5in)$) ;

        \coordinate (TT)    at ($(current page.north west) + (4.25in, 0        )$) ;
        \coordinate (TB)    at ($(current page.north west) + (4.25in,-.35in)$) ;
        \coordinate (BT)    at ($(current page.south west) + (4.25in, .35in)$) ;
        \coordinate (BB)    at ($(current page.south west) + (4.25in, 0        )$) ;

        \draw [dotted] (CYT) -- (CYB) ;
        \draw [dotted] (CXL) -- (CXR) ;
        \draw [dotted] (LL)    -- (LR)    ;
        \draw [dotted] (RL)    -- (RR)    ;
        \draw [dotted] (TT)    -- (TB)    ;
        \draw [dotted] (BT)    -- (BB)    ;
        \end{tikzpicture}%
        }

        \usetikzlibrary{shapes,arrows}
        \tikzset{%
            block/.style    = {draw, ultra thick, rectangle, minimum height = 3cm,
            minimum width = 3cm}
        }

        \newcommand{\placecard}[4]{
            \begin{minipage}[t][0.5\textwidth-10mm][t]{.5\textheight-10mm}
            \vskip1mm
            \sffamily\large%
            \includegraphics[width=1.5in]{/home/timtro/Documents/logos/UOIT_black_noTM}\hskip5mm\vrule\hskip5mm\hfill%
            \resizebox{3.1in}{!}{\vbox{\huge ''' + self.eventName +
            r'''\\ Seating Assignment}}\hbox to0.25in{}\\[2cm]\begin{tabular}{lcl}
            {\Large Name} &:&{\LARGE\bfseries #1},\hskip1cm {\LARGE #2}\\[2mm]
            {\Large Student ID} &:& {\bfseries\LARGE #3}\\
            \end{tabular}
            %Course Code:\ \hrulefill\hbox to2in{}\vfill
            %CRN:\ \hrulefill\hbox to2in{}\vfill
            \vfill
            Date:\ \hrulefill\hbox to1.75in{}\vfill
            Signature:\ \hrulefill\hbox to1.75in{}\vskip-3mm
            % \vbox to 1cm{}
            \begin{tikzpicture}[overlay]
                \node [block] (seatno) at (11.33cm, 1.8cm) {\Huge #4};
                \node [above of=seatno, node distance=2cm] {\small Seat Number.};
            \end{tikzpicture}
            \end{minipage}
        }

        \newcommand{\blankplacecard}[1]{
            \begin{minipage}[t][0.5\textwidth-10mm][t]{.5\textheight-10mm}
            \vskip1mm
            \sffamily\large%
            \includegraphics[width=1.5in]{/home/timtro/Documents/logos/UOIT_black_noTM}\hskip5mm\vrule\hskip5mm\hfill%
            \resizebox{3.1in}{!}{\vbox{\huge ''' + self.eventName +
            r'''\\ Seating Assignment}}\hbox to0.25in{}\\[2cm]\begin{tabular}{lcl}
            {\Large Name} &:&{\hrulefill}\\[15mm]
            {\Large Student ID} &:& {\hrulefill}\\
            \end{tabular}
            %Course Code:\ \hrulefill\hbox to2in{}\vfill
            %CRN:\ \hrulefill\hbox to2in{}\vfill
            \vfill
            Date:\ \hrulefill\hbox to1.75in{}\vfill
            Signature:\ \hrulefill\hbox to1.75in{}\vskip-3mm
            % \vbox to 1cm{}
            \begin{tikzpicture}[overlay]
                \node [block] (seatno) at (11.33cm, 1.8cm) {\Huge #1};
                \node [above of=seatno, node distance=2cm] {\small Seat Number.};
            \end{tikzpicture}
            \end{minipage}
        }

        \setlength{\parskip}{0pt}
        \setlength{\parindent}{0pt}
        \setlength{\fboxsep}{0pt}
        \begin{document}''')

    def print_placecard_sheet(self, fourIdxsAndSeries):

        assert len(fourIdxsAndSeries) == 4
        (d1, d2, d3, d4) = fourIdxsAndSeries

        self.fd.write(r'''\null\vfill%
        \hfill%
        \begin{sideways}%
        \placecard''')
        self.fd.write('{' + d1[1]['Last Name'] + '}')
        self.fd.write('{' + d1[1]['First Name'] + '}')
        self.fd.write('{' + str(d1[0]) + '}')
        self.fd.write('{' + str(d1[1]['Seat Number']) + '}')
        self.fd.write(r'''%
        \end{sideways}\hfill\null\hfill%
        \begin{sideways}%
        \placecard''')
        self.fd.write('{' + d2[1]['Last Name'] + '}')
        self.fd.write('{' + d2[1]['First Name'] + '}')
        self.fd.write('{' + str(d2[0]) + '}')
        self.fd.write('{' + str(d2[1]['Seat Number']) + '}')
        self.fd.write(r'''%
        \end{sideways}\hfill\null%
        \vfill\null\vfill%
        \hfill%
        \begin{sideways}%
        \placecard''')
        self.fd.write('{' + d3[1]['Last Name'] + '}')
        self.fd.write('{' + d3[1]['First Name'] + '}')
        self.fd.write('{' + str(d3[0]) + '}')
        self.fd.write('{' + str(d3[1]['Seat Number']) + '}')
        self.fd.write(r'''%
        \end{sideways}\hfill\null\hfill%
        \begin{sideways}%
        \placecard''')
        self.fd.write('{' + d4[1]['Last Name'] + '}')
        self.fd.write('{' + d4[1]['First Name'] + '}')
        self.fd.write('{' + str(d4[0]) + '}')
        self.fd.write('{' + str(d4[1]['Seat Number']) + '}')
        self.fd.write(r'''%
        \end{sideways}\hfill\null%
        \vfill\null
        \clearpage''')


    def print_blank_placecard_sheet(self, fourRand):

        self.fd.write(r'''\null\vfill%
        \hfill%
        \begin{sideways}%
        \blankplacecard''')
        self.fd.write('{' + str(fourRand[0]) + '}')
        self.fd.write(r'''%
        \end{sideways}\hfill\null\hfill%
        \begin{sideways}%
        \blankplacecard''')
        self.fd.write('{' + str(fourRand[1]) + '}')
        self.fd.write(r'''%
        \end{sideways}\hfill\null%
        \vfill\null\vfill%
        \hfill%
        \begin{sideways}%
        \blankplacecard''')
        self.fd.write('{' + str(fourRand[2]) + '}')
        self.fd.write(r'''%
        \end{sideways}\hfill\null\hfill%
        \begin{sideways}%
        \blankplacecard''')
        self.fd.write('{' + str(fourRand[3]) + '}')
        self.fd.write(r'''%
        \end{sideways}\hfill\null%
        \vfill\null
        \clearpage''')

    def end_placecard(self):
        self.fd.write(r'\end{document}')
