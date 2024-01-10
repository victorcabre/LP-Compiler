set -x

source lpVenv/bin/activate;
antlr4 -Dlanguage=Python3 -no-listener -visitor pandaQ.g4