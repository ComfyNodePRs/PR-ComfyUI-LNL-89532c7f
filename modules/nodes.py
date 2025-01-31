import os

import torch
import numpy as np

from .utils import lnl_cv_frame_generator, lnl_get_audio, lnl_lazy_eval

import folder_paths

"""
Attribution: ComfyUI-VideoHelperSuite

Portions of this code are adapted from GitHub repository `https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite`,
which is licensed under the GNU General Public License version 3 (GPL-3.0):

"""
class FrameSelector:

    supported_video_extensions =  ['webm', 'mp4', 'mkv']

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = []
        for f in os.listdir(input_dir):
            if os.path.isfile(os.path.join(input_dir, f)):
                file_parts = f.split('.')
                if len(file_parts) > 1 and (file_parts[-1] in FrameSelector.supported_video_extensions):
                    files.append(f"input/{f}")
        return {
            "required": {
                "video_path": (sorted(files),),
            },
            "hidden": {
                "prompt": "PROMPT",
                "unique_id": "UNIQUE_ID"
            },
        }

    RETURN_TYPES = ("IMAGE", "IMAGE", "INT", "INT", "INT", "INT", "INT", "VHS_AUDIO",)
    RETURN_NAMES = ("Current image", "Image Batch (in/out)", "Frame count (rel)", "Frame count (abs)", "Current frame (rel)", "Current frame (abs)", "Frame rate", "audio",)
    OUTPUT_NODE = True
    CATEGORY = "LNL"
    FUNCTION = "process_video"

    def __getImageBatch(self, full_video_path, frames_to_process, select_every_nth_frame, starting_frame):
        generatedImages = lnl_cv_frame_generator(full_video_path, frames_to_process, starting_frame, select_every_nth_frame)
        (width, height, target_frame_time) = next(generatedImages)
        width = int(width)
        height = int(height)

        imageBatch = torch.from_numpy(np.fromiter(generatedImages, np.dtype((np.float32, (height, width, 3)))))
        if len(imageBatch) == 0:
            raise RuntimeError("No frames generated")
        return (imageBatch, target_frame_time)

    def process_video(
        self,
        video_path,
        prompt=None,
        unique_id=None
    ):
        prompt_inputs = prompt[unique_id]["inputs"]
        full_video_path = os.path.join(folder_paths.base_path, video_path)

        in_point = prompt_inputs["in_out_point_slider"]["startMarkerFrame"]
        out_point = prompt_inputs["in_out_point_slider"]["endMarkerFrame"]
        current_frame = prompt_inputs["in_out_point_slider"]["currentFrame"]
        total_frames = prompt_inputs["in_out_point_slider"]["totalFrames"]
        frame_rate = prompt_inputs["in_out_point_slider"]["frameRate"]

        select_every_nth_frame = prompt_inputs["select_every_nth_frame"]

        frames_to_process = out_point - in_point + 1
        starting_frame = in_point - 1

        (current_image, _) = self.__getImageBatch(full_video_path, 1, 1, current_frame - 1)
        (in_out_images, target_frame_time) = self.__getImageBatch(full_video_path, frames_to_process, select_every_nth_frame, starting_frame)

        audio = lambda: lnl_get_audio(full_video_path, starting_frame * target_frame_time,
                               frames_to_process*target_frame_time*select_every_nth_frame)

        return (
            current_image,
            in_out_images,
            frames_to_process,
            total_frames,
            current_frame - in_point + 1,
            current_frame,
            frame_rate,
            lnl_lazy_eval(audio),
        )

class FrameSelectorV2(FrameSelector):

    RETURN_TYPES = ("IMAGE", "IMAGE", "INT", "INT", "STRING", "INT", "INT", "INT", "INT", "INT", "VHS_AUDIO",)
    RETURN_NAMES = ("Current image", "Image Batch (in/out)", "Frame in", "Frame out", "Filename", "Frame count (rel)", "Frame count (abs)", "Current frame (rel)", "Current frame (abs)", "Frame rate", "audio",)
    OUTPUT_NODE = True
    CATEGORY = "LNL"
    FUNCTION = "process_video"

    def process_video(
        self,
        video_path,
        prompt=None,
        unique_id=None
    ):
        prompt_inputs = prompt[unique_id]["inputs"]
        in_point = prompt_inputs["in_out_point_slider"]["startMarkerFrame"]
        out_point = prompt_inputs["in_out_point_slider"]["endMarkerFrame"]

        result = super().process_video(video_path, prompt, unique_id)
        return result[:2] + (in_point, out_point, video_path,) + result[2:]

NODE_CLASS_MAPPINGS = {
    "LNL_FrameSelectorV2": FrameSelectorV2,
    "LNL_FrameSelector": FrameSelector,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LNL_FrameSelectorV2": "LNL Frame Selector V2",
    "LNL_FrameSelector": "LNL Frame Selector [Deprecated] ⛔️",
}
