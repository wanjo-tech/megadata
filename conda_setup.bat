echo assume conda at \app\miniconda3\condabin\conda

conda activate base

conda create -y -n megadata python==3.8

conda activate megadata

@rem python -m pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple twine build
python -m pip install --upgrade -i https://mirrors.cloud.tencent.com/pypi/simple twine build


