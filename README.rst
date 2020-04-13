nc
====

🎨 Extensible color names in Python 🎨

EXAMPLES:

.. code-block:: python
   import nc

   for c in nc.red, nc.light_green, nc.DarkGrey, nc.puce:
       print(c, '=', *c)

    # Red = 255 0 0
    # Light green = 144 238 144
    # Dark grey = 85 85 85
    # Puce = 204 136 153
