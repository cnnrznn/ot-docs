if !has(python)
        com! -nargs=* Werk echoerr "Error: Werk requires vim compiled with +python"
        finish
endif

com! -nargs=* Werk py Werk.command(<f-args>)

python << EOF

import document

EOF
