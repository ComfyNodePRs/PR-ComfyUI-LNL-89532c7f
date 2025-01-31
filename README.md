# Frame Selector & Sequence Selection Node for ComfyUI
The Late Night Labs (LNL) Frame Selector node for ComfyUI is aimed at enhancing video interaction within the ComfyUI framework. It enables users to upload, playback, and perform basic In/Out on video files directly within the ComfyUI environment.

## Features
- Video Upload and Playback: Users can upload video files and utilize standard playback controls including Play, Pause, Scrub, and Rewind.
- Editing Tools: The node offers simple editing capabilities such as setting In/Out points for selecting specific video sections, frame selection for detailed editing, and outputting frames with handles for further processing.

## Structure
The project is structured into two main components: the web directory, containing front-end JavaScript and CSS files, and the modules directory, containing back-end Python scripts.

### Web Directory
- eventHandlers.js: Manages event handling for video playback and editing features.
- nodes.js: Defines the Load Video Node structure and integration within ComfyUI.
- utils.js: Contains utility functions for video processing and manipulation.
- widgets.js: Implements UI components for video editing.
- styles.js: Handles dynamic styling of the video node elements.
- css/lnlNodes.css: Provides styling for the Load Video Node components.
- images/: Contains icons used for playback and editing controls.

### Modules Directory
- server.py: Back-end server implementation for handling video upload and processing.
- utils.py: Back-end utility functions supporting video editing features.
- nodes.py: Defines the server-side representation of the Load Video Node.

## Installation
1. Ensure you have ComfyUI and its dependencies installed.
2. Clone this repo into custom_nodes:
```
$ cd ComfyUI/custom_nodes
$ git clone https://github.com/latenightlabs/ComfyUI-LNL.git
```

Install dependencies (not needed if you have ffmpeg for AnimateDiff):
```
$ cd ComfyUI-LNL
$ pip install -r requirements.txt
```

# To use the Load Video Node:

<img width="330" alt="image" src="https://github.com/latenightlabs/ComfyUI-LNL/assets/157748925/0b1be661-44b5-441b-aba4-17a479ddd96c">

## Inputs
1. Choose Video to Upload: Select a video file for processing (in this case, 'input/logo.mp4').

## Outputs
Options include:

1. Current image: Current frame being viewed.
2. Image Batch (in/out): Select a range of frames to process based on in and out points.
3. Frame count (rel): Display the count of frames relative to in and out points.
4. Frame count (abs): Absolute count of frames in the uploaded video.
5. Current frame (rel): The current frame number relative to in and out points.
6. Current frame (abs): The absolute frame number within the entire video.
7. Frame rate: FPS in the uploaded video.
8. Audio: Pass audio track if desired.

## Playback Controls

<img width="330" alt="image" src="https://github.com/latenightlabs/ComfyUI-LNL/assets/157748925/42f2987e-b4a5-433b-a2d1-0fd33eed03ed">

### Timeline Scrubber
1. Shows the current frame number out of the total number of frames (in this instance, frame 66 of 149).
2. In Point is green
3. Out Point is red
Note: In and Out point is set with the playback controls or in the input fields.


### Media Controls left to right:
1. Takes the user to the very first frame of the video.
2. Set 'in_point'.
3. Takes the user to the 'in_point', which is the frame set as the starting point for a selected range.
4. Steps backward by one frame, moving the current frame to the previous frame in the video.
5. Plays the video from the current frame forward.
6. _Not visible while Play button is displayed: Pause the playback at the current frame._
7. Steps forward by one frame at a time.
8. Takes the user to the 'out_point', the frame set as the ending point for a selected range.
9. Sets the 'out_point'.
10. Jumps to the very last frame of the video.

### Numeric Input Fields and Controls:

1. current_frame: Displays the current frame number and allows you to jump to a specific frame.
2. in_point and out_point: Fields for setting the start and end points for a range of frames for focused editing of a frame range.
3. select_every_nth_frame: Specify a pattern for selecting frames (e.g., every 2nd frame, every 3rd frame, etc.).


## Credits
This project uses parts of code and some ideas from the following repositories:
[ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)
[ComfyUI-VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite)
Make sure to check them out, they both offer awesome tool suites!

We also use icons for player controls supplied by [Icons8](https://icons8/com).


# Contributing
Contributions to the Load Video Node project are welcome. Please 

# License
This project is licensed under the GNU General Public License.
