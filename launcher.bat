@echo off
title StormTools Builder.py
color 8

echo installing requirements.txt ...
pip install -r requirements.txt
echo running builder.py ...
python builder.py
