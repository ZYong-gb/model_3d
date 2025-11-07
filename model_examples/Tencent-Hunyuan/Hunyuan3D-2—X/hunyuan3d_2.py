from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained('Tencent-Hunyuan/Hunyuan3D-2')
mesh = pipeline(image='assets/demo.png')[0]