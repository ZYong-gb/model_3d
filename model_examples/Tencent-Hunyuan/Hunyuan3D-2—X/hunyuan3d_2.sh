cd /mnt/data2/zy_2025/model_store_dir/Tencent-Hunyuan
git clone git@github.com:Tencent-Hunyuan/Hunyuan3D-2.git

cd /mnt/data2/zy_2025/model_store_dir/Tencent-Hunyuan/Hunyuan3D-2
pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
# for texture
cd hy3dgen/texgen/custom_rasterizer
python3 setup.py install
cd ../../..
cd hy3dgen/texgen/differentiable_renderer
bash compile_mesh_painter.sh OR python3 setup.py install (on Windows)