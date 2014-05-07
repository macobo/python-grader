import turtle
import os
import time
import random
import subprocess

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
CREATE_GIF_SH = os.path.join(CURRENT_FOLDER, "creategif.sh")

def take_picture(canvas, filename):
    canvas.postscript(file=filename)

def execute_file(file):
    exec(file.read(), {})

class Counter():
    def __init__(self):
        self.snapshot = 0
        
    def take_picture(self, root_prefix):
        filename = root_prefix + "{:03d}.ps".format(self.snapshot)
        take_picture(
            turtle.getcanvas(), 
            filename)
        self.snapshot += 1

def make_turtle_gif(user_program, output_file, snapshot_delay, frame_delay):
    def tick():
        #print("snip")
        counter.take_picture(root_prefix)
        root.after(snapshot_delay, tick)

    # prefix for temporary files
    root_prefix = ".temp_shot-%s-%03d-" % \
            (time.strftime("%Y%m%d%H%M%S"), random.randrange(1000))
    # do a last picture when we're done
    counter = Counter()
    turtle.exitonclick = lambda: counter.take_picture(root_prefix)

    root = turtle.getcanvas()._root()
    root.after(snapshot_delay, tick)
    # start the users program
    execute_file(user_program)

    print("Creating gif", output_file, repr(root_prefix))
    subprocess.call(
        [CREATE_GIF_SH, root_prefix, output_file, str(frame_delay)])

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert what a program draws using turtle to an animated gif')
    parser.add_argument('program_path', 
        type=argparse.FileType('r'),
        help="Path to a program that uses turtle")
    parser.add_argument('output_path',
        help="File path for the output gif")
    parser.add_argument('-s', '--snapshot_delay', type=int, default=500,
        metavar="delay", help="How often to take a snapshot (in ms)")
    parser.add_argument('-f', '--frame_delay', type=int, default=20,
        metavar="delay", help="Delay between frames in gif")

    args = parser.parse_args()
    make_turtle_gif(
        args.program_path, 
        args.output_path,
        args.snapshot_delay,
        args.frame_delay)