import argparse
import logging
import application
import maze

# TODO: implement queue?

# TODO: abstract things not in mouse

if __name__ == '__main__':
    loglevels = [
        'DEBUG',
        'INFO',
        'WARNING',
        'ERROR',
        'CRITICAL'
    ]

    parser = argparse.ArgumentParser(description='pygame template')
    parser.add_argument('-l', '--logging', type=str, required=False, default='ERROR', dest='logging', choices=loglevels)
    parser.add_argument('-m', '--maze', type=str, required=False, default=None, dest='maze')
    args = parser.parse_args()

    loglevel = getattr(logging, args.logging, None)
    logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s %(name)s %(message)s')

    a = application.App(maze.load_maze(args.maze))
    a.on_execute()