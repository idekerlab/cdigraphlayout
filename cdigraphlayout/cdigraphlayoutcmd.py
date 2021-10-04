#!/usr/bin/env python

import os
import sys
import argparse
import traceback
import json
import math
import re
import logging
from contextlib import redirect_stdout

import ndex2
import igraph


logger = logging.getLogger(__name__)


DEFAULT_BOX_SIZE = 550.0
"""
Default size of bounding box to fit layout
into
"""

DEFAULT_NODE_SIZE = 75.0
"""
Default node size used to calculate bounding
box
"""

CY_VISUAL_PROPERTIES_ASPECT = 'cyVisualProperties'
"""
Name of aspect containing visual properties where
node size can be extracted
"""


class Formatter(argparse.ArgumentDefaultsHelpFormatter,
                argparse.RawDescriptionHelpFormatter):
    pass


def _parse_arguments(desc, args):
    """
    Parses command line arguments

    :param desc: Description shown when -h is passed on
                 command line
    :type desc: str
    :param args: Arguments from command line
    :type args: list
    :return: Argument Parser
    :rtype: :py:class:`argparse.ArgumentParser`
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
    scalegroup = parser.add_mutually_exclusive_group()
    scalegroup.add_argument('--scale', type=float,
                            help='If set, overrides default and '
                                 'uniformly scales layout coordinates')
    scalegroup.add_argument('--fit_into', type=str,
                            help='If set, overrides default and uniformly '
                                 'adjusts layout coordinates to fit in'
                                 'bounding box passed in. Value should be a '
                                 'comma delimited list of floating point '
                                 'positions in format LEFT,TOP,RIGHT,BOTTOM '
                                 'ex: 0.0,0.0,500.0,600.0')
    return parser.parse_args(args)


def _get_node_size_from_cyvisual_properties(net_cx=None):
    """
    Gets node size from visual properties if it exists

    :param net_cx:
    :type net_cx: :py:class:`ndex2.nice_cx_network.NiceCXNetwork`
    :raises ValueError: If **net_cx** passed in is ``None``
    :return: Size of node as retrieved from cyVisualProperties
             aspect or None, if not found
    :rtype: float
    """
    if net_cx is None:
        raise ValueError('Network passed in cannot be None')

    v_props = net_cx.get_opaque_aspect(CY_VISUAL_PROPERTIES_ASPECT)
    if v_props is None:
        logger.debug('No ' + CY_VISUAL_PROPERTIES_ASPECT +
                     ' aspect found in network')
        return None
    for entry in v_props:
        if not entry['properties_of'] == 'nodes:default':
            continue

        return max(float(entry['properties']['NODE_WIDTH']),
                   float(entry['properties']['NODE_HEIGHT']),
                   float(entry['properties']['NODE_SIZE']))
    return None


def _get_bounding_box_based_on_node_size(net_cx=None):
    """
    Gets node size from visual properties if it exists and
    use that along with number of nodes to calculate a bounding
    box where upper left coordinate is 0,0 and lower right
    is the greater of ``DEFAULT_NODE_SIZE`` or square root
    of node size squared times number of nodes

    :param net_cx: Network to run layout on and get node
                   size from
    :type net_cx: :py:class:`ndex2.nice_cx_network.NiceCXNetwork`
    :return: Bounding box to fix network into
    :rtype: :py:class:`igraph.drawing.utils.BoundingBox`
    """
    if net_cx is None:
        raise ValueError('Network passed in cannot be None')

    num_nodes = len(net_cx.get_nodes())

    n_size = _get_node_size_from_cyvisual_properties(net_cx=net_cx)
    if n_size is None:
        n_size = DEFAULT_NODE_SIZE

    thesize = max(DEFAULT_BOX_SIZE,
                  math.sqrt(n_size * n_size * num_nodes))
    bbox = igraph.drawing.utils.BoundingBox(0, 0,
                                            thesize,
                                            thesize)
    return bbox


def _get_bounding_box_from_user_str(inputstr):
    """

    :param inputstr:
    :return:
    """
    if inputstr is None:
        return None
    split_input = re.split('\W*,\W*', inputstr)
    if len(split_input) != 4:
        raise ValueError('Could not parse bounding box coordinates '
                         'from input string: ' + inputstr)
    return igraph.drawing.utils.BoundingBox(split_input[0],
                                            split_input[1],
                                            split_input[2],
                                            split_input[3])


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
            bbox = None
            if theargs.scale is None and theargs.fit_into is None:
                bbox = _get_bounding_box_based_on_node_size(net_cx=net)
            else:
                if theargs.fit_into is not None:
                    bbox = _get_bounding_box_from_user_str(theargs.fit_into)

            netx = net.to_networkx(mode='default')
            del net

            g = igraph.Graph.from_networkx(netx)
            layout = g.layout(theargs.layout)

            # with logic above and mutually exclusive
            # group restriction in argparse we can
            # set scale if it has a value, otherwise
            # set the bounding box
            if theargs.scale is not None:
                layout.scale(theargs.scale)
            else:
                layout.fit_into(bbox)

            new_layout = []
            for x in range(len(layout.coords)):
                new_layout.append({
                    'node': g.vs[x]['_nx_name'],
                    'x': layout.coords[x][0],
                    'y': layout.coords[x][1]  # technically this should be flipped
                                              # with negative prefix,
                                              # but it makes --fit_into
                                              # confusing
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
    to standard out.
    
    NOTE: If neither, --scale or --fit_into are set then the layout
          coordinates are set to fit into the box where upper left
          corner is 0,0 and lower right corner is {DEF_BS},{DEF_BS} or 
          sqrt(size of node squared x number of nodes) where
          size of node is obtained from cyVisualProperties aspect
          or set to DEF_NS if not found. 
    """.format(DEF_NS=DEFAULT_NODE_SIZE,
               DEF_BS=DEFAULT_BOX_SIZE)
    theargs = _parse_arguments(desc, args[1:])
    try:
        return run_layout(theargs, sys.stdout, sys.stderr)
    except Exception as e:
        sys.stderr.write('\n\nCaught exception: ' + str(e))
        traceback.print_exc()
        return 2


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv))
