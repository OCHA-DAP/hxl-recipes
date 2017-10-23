Quick Charts
============

Recipes
-------

Definition
----------
`HDX <https://data.humdata.org/>`_ Quick Charts use `JSON <https://en.wikipedia.org/wiki/JSON>`_ configuration files to define different kinds of charts to offer to users. Each configuration file is a recipe consisting of a list of bites, individual blueprints for making charts from `HXL-tagged data <http://hxlstandard.org/>`_.

Terminology
-----------
+----------------+----------------------------------------------------------------------------------------------------------------------+
| Term           | Definition                                                                                                           |
+================+======================================================================================================================+
| HXL Bite       | A bite is one element of a dashboard such as a key figure, pie chart or bar chart                                    |
+----------------+----------------------------------------------------------------------------------------------------------------------+
| HXL Ingredient | The requirements of the HXL dataset to make the HXL bite.  If the ingredients are not there, the bite cannot be made |
+----------------+----------------------------------------------------------------------------------------------------------------------+
| HXL Recipe     | How you use the ingredients to make the bite.                                                                        |
+----------------+----------------------------------------------------------------------------------------------------------------------+
| HXL Cookbook   | The library of HXL bites (ingredients + recipes)                                                                     |
+----------------+----------------------------------------------------------------------------------------------------------------------+

Structure
---------
The `JSON <https://en.wikipedia.org/wiki/JSON>`_ config file is more a bite generator, this means that we can specify more than one aggregated function. We could do a json bite definition for each aggregate function (count, distinct-count or sum), but it is easier/simpler to put all of them there and let the system compute all possibilities. In specific cases (e.g 3w, HNOs, FTS) the recipe could be very simple in order to generate a limited number of bites tailored to each file type.

Recipe Example
--------------
Here is an example of a recipe (json) - list of bites(dictionaries):

.. code-block:: json
    :linenos:

 [
  {"name": "this is the first bite"},
  {"name": "this is the second bite"}
 ]

Simple Bite Example
-------------------
Here is an example of a simple bite to display a chart showing the total affected people grouped by country in a dataset:

.. code-block:: json
    :linenos:

 {
  "name": "Charts: Sum/count items for a value column grouped by aggregate columns",
  "description": "",
  "type": "chart",
  "ingredients": {
    "aggregateFunctions": [
      "sum",
    ],
    "aggregateColumns": [
      "#country",
      ],
    "valueColumns": [
      "#affected",
      ]
  }
 }

Bite Example
------------
Here is an example of a more complex bite to display a chart showing the total affected/inneed/reached/targeted/individuals people grouped by administrative divisions of a country in a dataset:

.. code-block:: json
    :linenos:

 {
  "name": "Charts: Sum/count items for a value column grouped by aggregate columns",
  "description": "",
  "type": "chart",
  "ingredients": {
    "aggregateFunctions": [
      "sum",
      "count"
    ],
    "aggregateColumns": [
      "#country",
      "#adm1",
      "#adm2",
      "#adm3",
      "#adm4",
      "#adm5"
    ],
    "valueColumns": [
      "#affected",
      "#inneed",
      "#reached",
      "#targeted",
      "#population"
    ]
  }
 }

Fields [properties of a bite]
-----------------------------
**name**
    a short, generic description of the visualisation. Not currently in use, but will be used in menu item selection

**description**
    a longer, human-readable description of the visualisation. Not currently in use, but will be used in notes

**type**
    the type of visualisation to generate. The options include the following:

    * "**chart**" — display either a bar or pie chart, depending on the number of values to show.
    * "**key figure**" — display a single number (such as total people in need), optionally with units and description text.
    * "**timeseries**" — display the change in values over time.

**ingredients**
    a `JSON <https://en.wikipedia.org/wiki/JSON>`_ object (dictionary) containing instructions for creating the visualisation. The object has the following properties:

    * "**chart**" — display either a bar or pie chart, depending on the number of values to show.
    * "**key figure**" — display a single number (such as total people in need), optionally with units and description text.
    * "**timeseries**" — display the change in values over time.
    **aggregateFunctions**
        a `JSON <https://en.wikipedia.org/wiki/JSON>`_ array of functions to use to generate summary (aggregate) data from the original dataset. HDX Quick Charts will offer each of these to the user as a separate option. The following functions are available:

        * "**count**" — display the total number of times each unique value appears (e.g. the number of activities for each prefecture in a 3W) - number of rows in the file for the specified criteria
        * "**distinct-count**" — display the total number of unique values in a column listed in value-columns associated with each unique value in a column listed in aggregate-columns (e.g. the number of unique provinces in each country).
        * "**sum**" — add up figures in a column listed in value-columns for each unique value in a column listed in aggregate-columns (e.g. the total number of people in need in each country).
    **aggregateColumns**
        the columns that can be used to group the results (any given chart will use just one of the columns). The value is a `JSON <https://en.wikipedia.org/wiki/JSON>`_ array of HXL `tag patterns <https://github.com/HXLStandard/hxl-proxy/wiki/Tag-patterns>`_ used to match actual hashtags in the document, e.g. "[#adm1", "#adm2"]. When this property is missing, or no columns match the `tag patterns <https://github.com/HXLStandard/hxl-proxy/wiki/Tag-patterns>`_, the aggregate function will use the entire document without grouping the results.
    **valueColumns** (required)
        the columns to visualise. The value is a `JSON <https://en.wikipedia.org/wiki/JSON>`_ array of HXL `tag patterns <https://github.com/HXLStandard/hxl-proxy/wiki/Tag-patterns>`_ used to match actual hashtags in the document, e.g. "[#affected", "#inneed"].

How widgets are created
-----------------------
The “Quick Charts” engine checks for each bite in the recipe in the columns (aggregated or value) and compares with the files’ HXL tags. From all the HXL tags in the file, the engine keeps only the one specified in the bite and builds all the available options. The “Quick Charts” engine cooks and delivers more than 1 bite with 2 inputs: recipe (HDX or external) and data (ingredients).

Each visualization/widget can be of 3 types:

**Chart**
    It displays either a bar or pie chart, depending on the number of values to show. If there are no more than 4, the engine will draw a pie chart.
**Key figure**
    It displays a single number (such as total people in need), optionally with units, prefix, postfix  and description text.
**Timeseries**
    It displays the change in values over time.

Create your own recipe
----------------------

Users can build their own recipes using specific columns and starting from `HDX recipes <https://github.com/OCHA-DAP/hxl-recipes>`_ that are hosted on GitHub and they should keep in mind that there a several restrictions:
 * There are three(3) types of charts that are supported (bar/pie chart, timeseries, key figure)
 * There are three (3) function that are supported to aggregate the values: count, distinct-count, sum

Note. Users can use any column as aggregate or value types, but testing is required.
After creating the recipe, it needs to be stored on an public URL (unrestricted access) and to be added at end of the quick charts url. See next session how to use it.


How to use
----------

When calling a Quick Chart you could use the HDX default recipe or specify it via “recipeUrl” parameter.
This is an example of use:

**3w recipe**
	`https://github.com/OCHA-DAP/hxl-recipes/blob/master/recipes/3w/recipe.json <https://github.com/OCHA-DAP/hxl-recipes/blob/master/recipes/3w/recipe.json>`_

**Charts with 3w recipe**
https://data.humdata.org/hxlpreview/show;url=http%3A%2F%2Fdata.humdata.org%2Fdataset%2Fd7ab89e4-bcb2-4127-be3c-5e8cf804ffd3%2Fresource%2F1ac80d41-4fd0-4f65-8f04-2cd98f4c09b1%2Fdownload%2Fmali_3wop_juin-2017.xls;**recipeUrl=https%3A%2F%2Fraw.githubusercontent.com%2FOCHA-DAP%2Fhxl-recipes%2Fmaster%2Frecipes%2F3w%2Frecipe.json**

or link `here <https://data.humdata.org/hxlpreview/show;url=http%3A%2F%2Fdata.humdata.org%2Fdataset%2Fd7ab89e4-bcb2-4127-be3c-5e8cf804ffd3%2Fresource%2F1ac80d41-4fd0-4f65-8f04-2cd98f4c09b1%2Fdownload%2Fmali_3wop_juin-2017.xls;recipeUrl=https%3A%2F%2Fraw.githubusercontent.com%2FOCHA-DAP%2Fhxl-recipes%2Fmaster%2Frecipes%2F3w%2Frecipe.json>`_

Note. The recipe Url must be escaped (one public service can be found `here <https://meyerweb.com/eric/tools/dencoder/>`__ )
