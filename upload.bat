condat activate megadata

python -m twine upload --verbose dist/*
if %errorlevel% == 0 (
del /f /q dist\*
del /f /q /s *.pyc
)
