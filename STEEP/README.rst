Comparing Radius of Gyration Evolution between the CTL and CPL Model
=====

Overview
-----

We show the long-term evolution on the dynamics of binary stars with initial conditions obtained from
`Fleming (2018) <https://ui.adsabs.harvard.edu/abs/2018ApJ...858...86F/abstract>`_
in which we show how the radius of gyration affects the critical semi-major axis, orbital period, and
the eccentricity of the binary stars over five billion years. With each model, we ran simulations in
which one scenario has the radius of gyration evolution on and another where the evolution is off.


===================   ============
**Date**              12/15/19
**Author**            David Graham
**Modules**           eqtide stellar
**Approx. runtime**   40 min total
===================   ============
 
Running the script.
----

In each ``STEEP`` sub-folder, run the following:

.. code-block:: bash

    vplanet vpl.in

Then in the ``STEEP_CTL`` folder run:  

.. code-block:: bash

    python makeplot.py <pdf | png>

Expected image
-----

.. figure:: STEEP.png?raw=True 
In solid lines we have the CPL model and in dashed lines the CTL model. The "bluer" colors are the 
simulations with radius of gyration evolution turned on while the "redder" colors are simulations 
with radius of gyration evolution turned off, that is, the radius of gyration is stays as a constant.

