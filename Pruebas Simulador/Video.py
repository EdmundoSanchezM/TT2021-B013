from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

in_loc = os.path.join(__location__, "ESCOMmp4.mp4")
out_loc = os.path.join(__location__, "ESCOMx3dot560FPS.mp4")

# Import video clip
clip = VideoFileClip(in_loc)
print("fps: {}".format(clip.fps))

# Modify the FPS
clip = clip.set_fps(clip.fps * 3)

# Apply speed up
final = clip.fx(vfx.speedx, 3.5)
print("fps: {}".format(final.fps))

# Save video clip
final.write_videofile(out_loc)