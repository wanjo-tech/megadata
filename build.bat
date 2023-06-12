call conda activate megadata

python -m build

@rem python setup.py sdist bdist_wheel
@rem echo pip install dist/megadata-x.x.x.tar.gz