from argparse import ArgumentParser
from greengraph import Greengraph
from matplotlib import pyplot as plt

if __name__ == "__main__":
    parser = ArgumentParser(description = "Plot the amount of green space \
        between two locations")
    parser.add_argument('--start')
    parser.add_argument('--end')
    parser.add_argument('--steps')
    parser.add_argument('--out')
    arguments= parser.parse_args()
    if not arguments.steps:
        arguments.steps = 20
    mygraph=Greengraph(arguments.start, arguments.end)
    data = mygraph.green_between(arguments.steps)
    plt.plot(data)
    plt.title('Green space versus location.')
    plt.xlabel('Step.')
    plt.ylabel('Number of green pixels.')
    if arguments.out:
        plt.savefig(arguments.out)
    else:
        plt.show()
