#!/bin/sh

file_name="123.py"

touch "$file_name"

echo "#!/usr/bin/python" > $file_name
