
# Get the directory of this script
$ExtensionPath = Split-Path -parent $MyInvocation.MyCommand.Definition

# if first argument is 'install'
if ($args[0] -eq 'install') {
    pip install ghastoolkit
    exit
}

python3 "$ExtensionPath/summary.py" $args
