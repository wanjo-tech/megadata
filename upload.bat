python -m pip install -U -i https://pypi.tuna.tsinghua.edu.cn/simple twine
python -m twine upload --verbose dist/*
if %errorlevel% == 0 (
del /f /q dist\*
del /f /q /s *.pyc
)
