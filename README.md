# synctextranslator

This is a package providing a shell script to convert the linenumbers from a source file to the resulting file and vice versa.
The main task is to serve as a synctex glueing program between various editors and viewers.

## supported editors
### Visual Studio Code
For now only `Visual Studio Code` is supported, which is available using the target `vscode`.
It can be configured to support synctextranslator using the `.vscode/settings.json` file with the following content:
```
{
    "latex-workshop.view.pdf.viewer": "external",
    "latex-workshop.view.pdf.external.synctex.command": "synctextranslator",
    "latex-workshop.view.pdf.external.synctex.args": [
        "%LINE%",
		"%TEX%",
		"viewer",
    ],
    "latex-workshop.showContextMenu": true,
}
```

## supported viewers
### Okular
The pdf viewer `okular` can be configured to fully support syntextranslator under Settings > Configure Okular > Editor > Custom Text Editor:
`synctextranslator %l %f editor`
Both `okular` and `zathura` are fully supported, their names serve as targets.

## configuration
Each file that should be used with `synctextranslator` must contain a section similar to this:
```
% synctextranslator
% directory = /home/benedikt/Entwicklung/scientific_report/
% tex_source = Template.tex
% tex_file = _build/scientific_report.tex
% pdf_file = _build/scientific_report.pdf
```

`directory` is optional, but then filenames have to be absolute.
The script compares `tex_source` and `tex_file` line by line and creates a map.
It then calls the appropriate viewer of editor to update the cursor position.

The call of this script should follow the pattern:
`synctextranslator <linenumber> <texfile> <target>`
- Linenumber is the linenumber that has been given by the editor or the viewer respectively.
- Texfile may be either the source or the generated tex file, it must however contain the described section.
- target is one of the known targets

## Meta targets
Special targets are available if they are defined in a file in the `.config` directory:
`~/.config/synctextranslator.conf`. The two targets `editor` and `viewer` can be used:
```
[DEFAULT]
editor = vscode
viewer = okular
```
