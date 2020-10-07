Dynamic stability limits influenced by Q Factors.
=====

Overview
-----

We use the CPL model to simulate different initial Q factors during a potential Kepler-47 time evolution. 
We chose the fiducial values of Kepler-47 from Graham et al. 2020 except we changed the initial binary
eccentricity to 0.20. We show how Q factors impact the evolution of critical semi-major axis, the eccentricity, 
and the orbital period. 


===================   ============
**Date**              10/07/20
**Author**            David Graham
**Modules**           binary eqtide stellar
**Approx. runtime**   15 minutes total
===================   ============
 
Running the script.
----

To create the data (make sure you have at least the python3 version), you must first run:

.. code-block:: bash

    python K47_tidalQs.py

If you would like to have audio played on the K47_tidalQs.py script, move any of the desired .wav files from 
the audio/DesiredLanguage to the Qfactors directory. In order for the audio to play, you must move the .wav files 
before playing the script. You are also free to create your own .wav files and input them into the Qfactors 
directory we well. You may also stop and play the K47_tidalQs.py script at any time and continue to run the script 
again from the most recently incomplete simulation.

When you have at least a few data points or when the previous script is finished, you may run in another terminal:  

.. code-block:: bash

    python makeplot.py <pdf | png>

and you may run the makeplot.py script repeatedly as the data points are being collected

Expected image
-----
.. |acrit| replace:: a\ :sub:`crit`\

.. figure:: Qfactor_CPL.png?raw=True 
The dynamic evolution of Kepler-47 binaries influenced by different initial Q factors using the CPL model. Redder curves represent low initial Q values while bluer curves represent higher Q values. We used the CPL model along with dynamic 
radius of gyration. Top: The binaries' dynamic stability limit time evolutions, |acrit|. Middle: The orbital period of Kepler-47B. Bottom: The eccentricity of Kepler-47B.  

