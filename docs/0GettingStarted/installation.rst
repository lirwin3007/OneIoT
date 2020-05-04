Installation
============

OneIoT is super simple to set up! To follow this guide you will need:

 - Raspberry Pi 3 or 4 *(Other models are untested, but may work)*
 - At least 1 OneIoT device
 - An additional way of networking your pi

.. note:: An aditional way of networking your pi is required since the onboard wifi is taken up with the OneIoT network - you can connect your pi to the internet through another WiFi dongle, or with a wired ethernet cable

Once you've got all of the above, we can begin!

A quick bit of theory
#####################

Before we dive into setting everything up, it might be useful to examine a little bit of theory on how OneIoT works. Let's start by defining a few key terms.

**OneIoT Networks**

A OneIoT network consists of a number of **OneIoT Devices** and one **OneIoT Controller**.
The *OneIoT Controller* is responsible for creating and maintaining communication links between itself and the *OneIoT Devices* in the network.
Its possible, and potentially benificial to have more than 1 OneIoT network. An example of when this is encouraged would be having two seperate OneIoT networks for your home and your garage.
In this situation, it would probably be quite difficult to position your *OneIoT Controller* such that it can cover your house and garage with a network.
In the future, it will be possible to get these 2 networks talking.

**OneIoT Devices**

A OneIoT device is any device that can connect to a **OneIoT controller** using the OneIoT protocol.
At the moment, the only OneIoT devices in existance are the ESP-32 based OneIoT boards.
OneIoT devices can be interfaced with the outside world through their GPIO pins, and can be read from and have instructions sent to them by their *OneIoT controller*.
Usually

**OneIoT Controllers**

A OneIoT Controller is the device responsible for maintaining connections to all of the OneIoT Devices in it's network.
At the minute, the only example of a OneIoT controller is a raspberry pi running the software that we will install later in this document.

Setting up a controller
#######################

We're going to be using a raspberry pi as a controller.
In this walkthrough, we'll assume that you're using a fresh Raspbian Buster image, available from the `Raspberry Pi website <https://www.raspberrypi.org/downloads/raspbian/>`_.

Updating and Upgrading
~~~~~~~~~~~~~~~~~~~~~~

It's important that you're up to date - to make sure your system is fully up to date, run

.. code-block:: bash

    $ sudo apt-get update
    $ sudo apt-get upgrade

Installing the Core Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~

OneIoT has one central core library that handles communication with all devices.
This is run all the time in the background waiting for commands.
Importantly, there is only one process running the core library. If you, the user, wants to access OneIoT devices from 2 separate processes, those processes each interact with the one core library process that handles communication with each device and reports back to the user process.

If you want, you can interact with the core library directly - we'll do just that to test it once we have set it up - but we've created the OneIoT python library to interact with the core on your behalf so everything is nicely wrapped up in Python classes and functions. We'll get to this later though.

There are a number of different ways to install the core library:

.. tabs::

    .. tab:: Using Pip

        Using pip is the simplest way to install the core library.

        .. tabs::

            .. group-tab:: Python 3

                .. code-block:: bash

                    $ sudo pip3 install oneiot-core

            .. group-tab:: Python 2 (Not recommended)

                .. code-block:: bash

                    $ sudo pip install oneiot-core

    .. tab:: From Source

        :code:`\\TODO`
