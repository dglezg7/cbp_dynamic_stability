The Consequence of Higher Eccentricity in K47 A and B.
=====

Overview
-----

We show how the rise of the initial binary eccentricity increases in semi-major axis and represent that
binary eccentricities beyond 0.236 render Kepler 47 b unstable at some point during the dynamic evolution. 
The simulations run in order to produce this figure is an extension from the 
`Kepler47b <https://github.com/dglezg7/cbp_dynamic_stability/tree/master/kepler47b>`_ 
subdirectory. All initial conditions and modules are kept the identical compared the the Kepler47b directory, 
except in here we vary the initial binary eccentricity from 0.10 to 0.49.


===================   ============
**Date**              04/15/20
**Author**            David Graham
**Modules**           binary eqtide stellar
**Approx. runtime**   42 hours total
===================   ============
 
Running the script.
----

To create the data (make sure you have at least the python3 version), you must first run:

.. code-block:: bash

    python K47_Eccentricities.py

If you would like to have audio played on the K47_Eccentricities.py script, move any of the desired .wav files from 
the K47_Eccentrcities/audio/DesiredLanguage to the K47_Eccentricities directory. In order for the audio to play, you
must move the .wav files before playing the script. You may also stop and play the K47_Eccentricities.py script at 
any time and continue to run the script again from the most recently incomplete simulation.

When you have at least a few data points or when the previous script is finished, you may run in another terminal:  

.. code-block:: bash

    python makeplot.py <pdf | png>

and you may run the makeplot.py script repeatedly as the data points are being collected

Expected image
-----
.. |acrit| replace:: a\ :sub:`crit`\
.. |acbp| replace:: a\ :sub:`CBP`\
.. |ebin| replace:: e\ :sub:`star`\

.. figure:: K47_Eccentricities.png?raw=True 
K47b may only maintain its dynamic stability throughout the evolution when the initial binary eccentricity is below 0.236. The top panel represents the maximum difference between |acrit| and |acbp| in its entire long-term evolution. If |acrit| - |acbp| is less than zero, the dynamic stability limit never engulfs K47b. The middle panel shows the time in which |acrit| crosses into |acbp| during each simulation's history. The maximum instability time is 33.6 Myrs at |ebin| = 0.236 and drops as the initial |ebin| increases. The bottom panel shows when each of the binary stars tidally lock during each simulation. Tidal lock time for K47B is constant compared to the initial |ebin|, however the tidal lock time for K47A jumps from 69.3 Myrs at |ebin| = 0.19 to 3.93 Gyrs at |ebin| = 0.20 and decreases to zero as the initial |ebin| increases.

