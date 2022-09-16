I don't h

My local GPU doesn't support cuspatial, so I'm limited to reading the docs.
Looking at both documentations, I'd probably consider requesting direct GPU support for some of the GeoPandas Constructive Methods (https://geopandas.org/en/stable/docs/user_guide/geometric_manipulations.html#constructive-methods). For example, the GeoSeries simplify (https://geopandas.org/en/stable/docs/user_guide/geometric_manipulations.html#GeoSeries.simplify) and convex_hull https://geopandas.org/en/stable/docs/user_guide/geometric_manipulations.html#GeoSeries.convex_hull seem like common enough operations that it would make sense to consider an implementation that would take advantage of a GPU (instead of converting to and from a GeoPandas object).

i.e.:

**Is your feature request related to a problem? Please describe.**
I would like to be able to run common constructive methods directly on the GPU, without having to convert to and back from GeoPandas (CPU).

**Describe the solution you'd like**
Being able to execute methods equivalent to operations such as GeoPandas' [simplify](https://geopandas.org/en/stable/docs/user_guide/geometric_manipulations.html#GeoSeries.simplify) and [convex_hull](https://geopandas.org/en/stable/docs/user_guide/geometric_manipulations.html#GeoSeries.convex_hull) directly on the GPU

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.
Converting to GeoPandas and back (CPU)

**Additional context**
Add any other context, code examples, or references to existing implementations about the feature request here.





the following two feature requests: 

centroid
envelope


simplify