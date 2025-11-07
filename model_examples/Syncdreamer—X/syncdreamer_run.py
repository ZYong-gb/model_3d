from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

mviews_pipe = pipeline(
            Tasks.image_to_3d,
            model='Damo_XR_Lab/Syncdreamer')
result = mviews_pipe('./test_img.png')