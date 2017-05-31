import cx_Freeze
import sys, os

executables = [cx_Freeze.Executable("snake.py")] 

if getattr(sys, "frozen", False):
    # frozen
    DIRECTORY = os.path.dirname(sys.executable)
else:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))

IMAGES = os.path.join(DIRECTORY, "images") 



cx_Freeze.setup(
    name ="Snake",
    options = {"build_exe": {"packages" : ["pygame", "sys", "os", "random"], "include_files":[os.path.join(IMAGES, "snake.png"), os.path.join(IMAGES, "apple.png")]}},
    description = "Snake, written by Rasmus Bergström",
    executables = executables
)

