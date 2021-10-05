===================================================
CDAPS igraph layout
===================================================


Dependencies
------------

* Docker_
* `make <https://www.gnu.org/software/make/>`_ (to build)
* Python (to build)

Building
--------

To build the Docker_ container run the following:

.. code-block::

   git clone https://github.com/idekerlab/cdigraphlayout
   cd cdigraphlayout
   make dockerbuild

To build a pip_ installable package run the following:

.. code-block::

    git clone https://github.com/idekerlab/cdigraphlayout
    cd cdigraphlayout
    make dist

    # to install
    pip install dist/cdigraphlayout*whl


Run **make** command with no arguments to see other build/deploy options including creation of Docker image

.. code-block::

   make

Output:

.. code-block::

   clean                remove all build, test, coverage and Python artifacts
   clean-build          remove build artifacts
   clean-pyc            remove Python file artifacts
   clean-test           remove test and coverage artifacts
   lint                 check style with flake8
   test                 run tests quickly with the default Python
   test-all             run tests on every Python version with tox
   coverage             check code coverage quickly with the default Python
   docs                 generate Sphinx HTML documentation, including API docs
   servedocs            compile the docs watching for changes
   testrelease          package and upload a TEST release
   release              package and upload a release
   dist                 builds source and wheel package
   install              install the package to the active Python's site-packages
   dockerbuild          build docker image and store in local repository
   dockerpush           push image to dockerhub


Usage via Docker
------------------

The fragment below downloads a small network From NDEx_ and
runs the layout on it via the command line. The output
to standard out is the cartesianLayout_ aspect.

.. note::

    The fragment of code below assumes Docker is installed and working and ``make dockerbuild`` was run on the repo
    to build a docker container.

.. code-block::

    wget https://www.ndexbio.org/v2/network/36ac0907-78c3-11e8-a4bf-0ac135e8bacf
    docker run --rm -v `pwd`:`pwd` coleslawndex/cdigraphlayout:0.0.1 `pwd`/36ac0907-78c3-11e8-a4bf-0ac135e8bacf

**Example Output:**

.. code-block::

    [{"node": 0, "x": 242.56889787616825, "y": 28.655392478413916},
     {"node": 1, "x": 251.52727037575158, "y": 4.193109677073721},
     {"node": 2, "x": 224.8682718448992, "y": 182.1879797546074},
     {"node": 3, "x": 300.958265923956, "y": 42.387712457396404},
     {"node": 4, "x": 210.09683745556438, "y": 0.0},
     {"node": 5, "x": 182.04628565762079, "y": 22.819559638911386},
     {"node": 6, "x": 294.27174726092863, "y": 12.136299460986265},
     {"node": 7, "x": 150.08778222453932, "y": 273.2021063448339}, {"node": 8, "x": 18.88290216787732, "y": 291.19126713552293}, {"node": 9, "x": 230.17621761645904, "y": 245.63956874046983}, {"node": 10, "x": 220.64944396590622, "y": 277.5325910602439}, {"node": 11, "x": 226.5620092198507, "y": 321.62593135879024}, {"node": 12, "x": 208.66587872560012, "y": 292.4369464265172}, {"node": 13, "x": 87.03122440526637, "y": 295.78009472025053}, {"node": 14, "x": 97.8268837943514, "y": 322.19209240776075}, {"node": 15, "x": 146.1154222761311, "y": 299.9749078016687}, {"node": 16, "x": 131.50718172664338, "y": 271.8881815771321}, {"node": 17, "x": 160.48182607088415, "y": 320.22426883406547}, {"node": 18, "x": 136.4213701359282, "y": 246.6646752514475}, {"node": 19, "x": 168.82353828706954, "y": 288.0805347602935}, {"node": 20, "x": 157.73662049259798, "y": 244.30125907573466}, {"node": 21, "x": 179.53444253317417, "y": 314.47486478572023}, {"node": 22, "x": 271.3917573386482, "y": 314.9529350700328}, {"node": 23, "x": 296.7193199560536, "y": 298.23474027188587}, {"node": 24, "x": 115.18476251984012, "y": 94.15740453051642}, {"node": 25, "x": 149.900133245134, "y": 192.2460859390774}, {"node": 27, "x": 301.96229165818755, "y": 232.87957016686605}, {"node": 28, "x": 294.17381017179616, "y": 216.4433079229556}, {"node": 30, "x": 243.8490429563948, "y": 208.49083246090458}, {"node": 31, "x": 263.88805282409646, "y": 220.36566265275152}, {"node": 32, "x": 236.10033094698906, "y": 71.32432517584289}, {"node": 33, "x": 284.4550992937104, "y": 152.72210983138905}, {"node": 34, "x": 242.84039050541554, "y": 135.91246045990442}, {"node": 35, "x": 184.67785361607753, "y": 258.9081183538586}, {"node": 36, "x": 302.78238164943116, "y": 161.25850166725377}, {"node": 37, "x": 376.14957137071247, "y": 162.7132417267205}, {"node": 38, "x": 531.1170978321227, "y": 213.82742845364209}, {"node": 39, "x": 375.92377799283634, "y": 218.8123668523585}, {"node": 40, "x": 375.2977317341929, "y": 87.3716585862779}, {"node": 41, "x": 284.4635762179885, "y": 489.48440794539323}, {"node": 42, "x": 200.67221776856357, "y": 424.9581817593903}, {"node": 43, "x": 223.6532369784539, "y": 485.8695192250316}, {"node": 44, "x": 322.7980192707836, "y": 466.6405101479979}, {"node": 45, "x": 328.04301928243933, "y": 550.0}, {"node": 46, "x": 139.05153857459027, "y": 446.4883089359671}, {"node": 47, "x": 268.3665698016949, "y": 438.51825752369734}, {"node": 49, "x": 283.06136747684616, "y": 277.2944589088132}, {"node": 50, "x": 84.58302292202993, "y": 123.33269856488926}]

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _NDEx: https://www.ndexbio.org
.. _cartesianLayout: https://home.ndexbio.org/data-model/#cart_layout
.. _Docker: https://www.docker.com/
.. _pip: https://pypi.org/project/pip/