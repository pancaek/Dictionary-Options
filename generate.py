import yaml
import sys

data = ''
with open(sys.argv[1], encoding='utf-8') as f:
  data = yaml.safe_load(f)

output=''

for section in data['dictionary']['sections']:
  sectioncontent = '\\section{'+ section['name'] + '}\n\\begin{multicols*}{2}'
  for word in section['words']:
    wordcontent = '\n  \\textlangle ' + word['ortho'] + '\\textrangle\\'
    if 'ipa' in word:
      wordcontent += ' [' + word['ipa'] + ']'

    if 'etym' in word:
      wordcontent += ' \\etymsep\\ ' + word['etym']

    if 'definitions' in word:
      definitioncontent = '\n  \\begin{enumerate}'
      for definition in word['definitions']:
        if 'meaning' in definition:
          definitioncontent += '\n    \\item '
          if 'pos' in definition:
            definitioncontent += '(' + definition['pos'] + ') '
          definitioncontent += definition['meaning']

        if 'examples' in definition:
            for example in definition['examples']:
              definitioncontent += ' \\examplesep\\ '
              definitioncontent += '\\langtext{' + example['sentence'] + '} ' + '\\langtrans{' + example['trans'] + '}'

      definitioncontent += '\n  \\end{enumerate}'
      wordcontent += definitioncontent
    sectioncontent += wordcontent
  output += sectioncontent + '\n\\end{multicols*}\n\n'


#! This is a dumb way to do this but will make all sections go under a single multicol environment

if 'no-section-pagebreak' in data['dictionary']:
  if data['dictionary']['no-section-pagebreak']:
    lines = []
    for line in output.split('\n'):
      if not ('\\begin{multicols*}{2}' in line or '\\end{multicols*}' in line):
        lines.append(line)
    lines.insert(0, '\\begin{multicols*}{2}\n')
    lines.append('\\end{multicols*}')
    output = '\n'.join(lines)

with open('./main.tex', 'w+', encoding='utf-8') as out:
  out.write('''\\documentclass[openany, 12pt, b5paper]{memoir}

\\usepackage{fontspec}
\\let\\ordinal\\relax %! Fixes \ordinal conflict with memoir
\\usepackage[us]{datetime}
\\newdate{startdate}{30}{8}{2020}
\\usepackage{enumitem}
\\setlist{topsep=0pt}
\\setlist[enumerate]{%
  wide =1em,
  leftmargin=1em,
  labelwidth=1em%
}%

\\usepackage{multicol}

\\usepackage[hidelinks]{hyperref}
\\hypersetup{linktoc=all}

\\titlingpageend{\\clearforchapter}{\\clearforchapter} %! Titlingpage/openany fix for blank page
\\pagestyle{ruled}
\\makeoddfoot{plain}{}{}{\\thepage}
\\makeevenfoot{plain}{\\thepage}{}{}
\\copypagestyle{title}{empty}

\\setmainfont{Libertinus Serif}

\\setlength{\\parindent}{0pt}
\\nonzeroparskip
\\setsecnumdepth{none}

\\newcommand{\\langname}{''' + data['dictionary']['langname'] + '''}
\\newcommand{\\examplesep}{\\textbullet}
\\newcommand{\\etymsep}{\\textleftarrow}
\\newcommand{\\nativetext}[1]{\\textit{#1}}
\\newcommand{\\langtrans}[1]{`#1'}

\\begin{document}
\\title{'''+data['dictionary']['title']+'''}
\\author{''' + data['dictionary']['author'] + '''}
\\date{\\displaydate{startdate} - \\today}
\\frontmatter
\\begin{titlingpage}
  \\maketitle
\\end{titlingpage}
\\mainmatter

''' + output + '''

\\backmatter
% bibliography, glossary and index would go here.

\\end{document}''')