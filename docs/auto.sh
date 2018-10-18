#!/bin/bash
for file in ./*.html
do
  wkhtmltopdf "$file" "$file.pdf"
done
