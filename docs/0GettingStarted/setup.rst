Setup
=====

The Core
########

Helpfully, the core library includes a command line interface (CLI) that (amongst other things) can be used to set it up.

From your terminal, run :code:`iot-core`. You should see an output similar to that below. If you get that, you've installed the core correctly!

.. code-block:: bash

    $ iot-core

    Usage: iot-core [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      core
      env

      network
      status

We can then run :code:`iot-core network status` to see the current status of the network. Because we haven't set this up yet, it should mostly come back failed!

.. code-block:: bash

    $ iot-core network status

    Network Setup:
        ✓ Network Interface Selected
        ✗ Static IP Set Up
        ✗ Hostapd Set Up
        ✗ DNSMasq Set Up

    Network Status:
        ✗ Static IP Respected
        ✗ HostAPD Running
        ✗ DNSMasq Running

To solve these, we can run the automatic network setup tool: :code:`iot-core network setup`



To test the install, we can attempt to directly interact with the core.
Under the hood, the core is listening for TCP connections on socket 1102, so we can use the netcat utility to send it some data and see if it responds!

.. note::

    By default, the core listens on port 1102. This can be overridden by `setting the environment variable <https://wiki.debian.org/EnvironmentVariables>`_ :code:`ONEIOT_C_PORT`.

Start the netcat utility with

.. code-block:: bash

    $ nc localhost 1102

And then type :code:`heartbeat` and press return. If all has gone well, you should see the response :code:`OK`. You can then exit netcat with :code:`ctrl+c`.

The Library
###########

\\TODO

OneIoT Manager
##############

\\TODO
