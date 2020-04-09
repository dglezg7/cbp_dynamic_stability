Dynamic Constraints on the Habitable Zone of Binary Stars
=====

Overview
-----

We model the critical semi-major axis of p-type identical binary stars and how the dynamic stability limits for each binary
eccentricity prevent planets from surviving in their habitable zones.

===================   ============
**Date**              14/12/19
**Author**            David Graham
**Approx. runtime**   15 seconds
===================   ============

We combine the obtained expression of the critical semi-major axis from 
`Holman & Wiegert (1999) <https://ui.adsabs.harvard.edu/abs/1999AJ....117..621H/abstract>`_ 
and overlapped them with the habitable zone limits from 
`Kopparapu (2013) <https://ui.adsabs.harvard.edu/abs/2013ApJ...765..131K/abstract>`_
where the inner limit of the HZ is the runaway greenhouse effect and the outer limit is the
maximum greenhouse effect. 
 
Running the script.
----

.. code-block:: bash

    python CBP_HZ_plot.py <pdf | png>

Expected image
-----

.. figure:: HZ_CBP.png?raw=True
Orbital constraints placed on circumbinary planets orbiting identical-mass binary stars while 
showing the habitable zone for binary star systems between 0.1 to 0.5 solar masses. Each critical 
semi-major axis line in the plot shows how higher binary eccentricities create a higher restriction 
in which the circumbinary planet may become dynamically stable.
