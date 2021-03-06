Type guessing
--------------------

BiblioPixel can often guess the name of the class you mean from the file or
module that it's in.  This saves a lot of repetitive typing

This happens in two cases:

+ If there is only one class in the file or module
+ or if there is exactly one class in the file or module whose name is
  "basically the same" as the file or module name

Two names are *basically the same* if they are the same when you throw away
all punctuation and make them lower case - so ``HelloWorld``\ , ``HELLO_WORLD``
and ``hello_world`` are canonically the same.

-------------------

**Example 1**\ :  Simple animation, Absolute Typename

.. code-block:: yaml

       animation: bibliopixel.animation.sequence.Sequence

For convenience, if the whole class section is a string, it's the ``typename``\ :

**Example 2**\ :  Relative Typename

.. code-block:: yaml

       animation: .sequence.Sequence

**Example 3**\ :  Relative Typename with type guessing

.. code-block:: yaml

       animation: .sequence


.. bp-code-block:: footer

   shape: [64, 14]
   animation:
     typename: $bpa.strip.PartyMode
     colors: [blue, violet, magenta]
