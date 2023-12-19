
# if first argument is 'install'
if ($args[0] -eq 'install') {
    pip install ghastoolkit
    exit
}

python3 "$PSScriptRoot/summary.py" $args
