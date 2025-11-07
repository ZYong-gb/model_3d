#!bin/bsah

cd /home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test

# conda activate LeRes

export PYTHONPATH="/home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test"

/mnt/data2/work/miniconda3/envs/LeRes/bin/python ./tools/test_shape.py --load_ckpt res50.pth --backbone resnet50