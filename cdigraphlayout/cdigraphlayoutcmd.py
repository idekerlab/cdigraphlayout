#!/usr/bin/env python

import os
import sys
import argparse
import traceback
import json
import math

from contextlib import redirect_stdout

import ndex2
import igraph


class Formatter(argparse.ArgumentDefaultsHelpFormatter,
                argparse.RawDescriptionHelpFormatter):
    pass


def _parse_arguments(desc, args):
    """
    Parses command line arguments
    :param desc:
    :param args:
    :return:
    """
    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=Formatter)
    parser.add_argument('input',
                        help='CX file')
    parser.add_argument('--layout', default='auto',
                        choices=['auto', 'circle', 'drl', 'fr',
                                 'kk', 'lgl', 'random', 'rt',
                                 'rt_circular'],
                        help='Layout algorithm to use. '
                             'For description see https://igraph.org/python/'
                             'doc/tutorial/tutorial.html#layout-algorithms')
    return parser.parse_args(args)


def _get_bounding_box_based_on_node_size(net_cx=None):
    """
    Gets node size from visual properties if it exists
    :param net_cx:
    :return: Bounding box to fix network into
    :rtype: :py:class:`igraph.drawing.utils.BoundingBox`
    """
    num_nodes = len(net_cx.get_nodes())

    v_props = net_cx.get_opaque_aspect('cyVisualProperties')
    if v_props is None:
        return None

    for entry in v_props:
        if not entry['properties_of'] == 'nodes:default':
            continue

        n_size = max(float(entry['properties']['NODE_WIDTH']),
                     float(entry['properties']['NODE_HEIGHT']),
                     float(entry['properties']['NODE_SIZE']))

        thesize = max(550.0,
                      math.sqrt(n_size * n_size * num_nodes))
        bbox = igraph.drawing.utils.BoundingBox(0, 0,
                                                thesize,
                                                thesize)
        return bbox
    return None


def run_layout(theargs, out_stream=sys.stdout,
               err_stream=sys.stderr):
    """
    Runs networkx Spring layout

    :param theargs: Holds attributes from argparse
    :type theargs: `:py:class:`argparse.Namespace`
    :param out_stream: stream for standard output
    :type out_stream: file like object
    :param err_stream: stream for standard error output
    :type err_stream: file like object
    :return: 0 upon success otherwise error
    :rtype: int
    """

    if theargs.input is None or not os.path.isfile(theargs.input):
        err_stream.write(str(theargs.input) + ' is not a file')
        return 3

    if os.path.getsize(theargs.input) == 0:
        err_stream.write(str(theargs.input) + ' is an empty file')
        return 4

    try:
        with redirect_stdout(sys.stderr):
            net = ndex2.create_nice_cx_from_file(theargs.input)

            bbox = _get_bounding_box_based_on_node_size(net_cx=net)
            netx = net.to_networkx(mode='default')
            del net
            g = igraph.Graph.from_networkx(netx)

            layout = g.layout(theargs.layout)

            if bbox is not None:
                layout.fit_into(bbox)

            new_layout = []
            for x in range(len(layout.coords)):
                new_layout.append({
                    'node': g.vs[x]['_nx_name'],
                    'x': layout.coords[x][0],
                    'y': -layout.coords[x][1]
                })

            # write value of cartesianLayout aspect to output stream
            json.dump(new_layout, out_stream)
        return 0
    except Exception as e:
        err_stream.write(str(e))
        return 5
    finally:
        err_stream.flush()
        out_stream.flush()


def main(args):
    """
    Main entry point for program
    :param args: command line arguments usually :py:const:`sys.argv`
    :return: 0 for success otherwise failure
    :rtype: int
    """
    desc = """
    Runs igraph layout on command line, sending cartesianLayout aspect
    to standard out
    """
    theargs = _parse_arguments(desc, args[1:])
    try:
        return run_layout(theargs, sys.stdout, sys.stderr)
    except Exception as e:
        sys.stderr.write('\n\nCaught exception: ' + str(e))
        traceback.print_exc()
        return 2


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv))
