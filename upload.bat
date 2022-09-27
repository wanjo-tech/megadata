@rem python -m pip install twine
python -m twine upload dist/*
del /f /q dist\*
