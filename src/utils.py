import argparse


def parse_bounds(arg):
    try:
        return [float(i) for i in arg.split(",")]
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Output bounds should be formatted as (xmin,ymin,xmax,ymax)"
        )
