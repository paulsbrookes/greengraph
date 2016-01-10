from argparse import ArgumentParser
from greengraph import Greengraph
from matplotlib import pyplot as plt

def process():
    parser = ArgumentParser(description = "Plot the amount of green space \
        between two locations.")
    parser.add_argument('--steps', type=int, default=20, help='Number of steps \
        plotted. Default value = 20.')
    parser.add_argument('--out', default=False, help='Name of output \
        file. "*.png" or "*.pdf"')
    parser.add_argument('--start', type=str, default='London', help='Start \
        location for plot. Default location is London.')
    parser.add_argument('--end', type=str, default='Cambridge', help='End \
        location of plot. Default location is Cambridge.')
    arguments= parser.parse_args()
    mygraph=Greengraph(arguments.start, arguments.end)
    data = mygraph.green_between(arguments.steps)
    data_norm = [x/160000.0 for x in data]
    plt.plot(data_norm)
    plt.title('Green space between two locations.')
    plt.xlabel('Step')
    plt.ylabel('Fraction of green pixels')
    if arguments.out:
        plt.savefig(arguments.out)
    else:
        plt.show()

if __name__ == "__main__":
    process()
