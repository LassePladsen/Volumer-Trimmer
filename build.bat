$echo off
pyinstaller --onefile --noconsole --icon "E:\Lasse\Dokumenter\Dev\Python prosjekter\FFmpeg Volumer-Trimmer\data\icon.ico" --add-data "E:\Lasse\Dokumenter\Dev\Python prosjekter\FFmpeg Volumer-Trimmer\data;data" -n "Volumer & Trimmer" main.py

