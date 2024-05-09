# Wandrer
Inspired by [Wandrer](https://wandrer.earth), like in this Strava activity description that shows the number of new miles:  

<img src="https://github.com/dsleo/wandrer/blob/main/img/strava.png" width="90%" height="auto">

The goal is to determine whether any segments within a newly Strava activity have been ridden or run before.  

To accomplish this, we propose two strategies:

* Geometrical Approach: By examining the geographical relationship between historical and new activity path segments, we get previously untraveled routes.

* Lexical Approach: We simply compare the historical and new activity Strava segment names. It's that easy.

## How To
Have a look at this [Example notebook](https://github.com/dsleo/wandrer/blob/main/notebooks/Example.ipynb)

## Clean this
Okay I was first thinking to store and index all segments and then do a neighbour search BUT it's not clear how to best do this: for two segment A = (a1, a2) and B=(b1, b2) I should get the minimum distance of (A,B) and (A, B-reversed) as ordering matters. Not clear how to set up an appropriate threshold of distance as "close enough" between segment also...

I could do without the neighbour search entirely and just do searchsorted, if we replace each segment by its mid-point. Scalar ftw. Natural distance threshold here. If segments are about 500m, then we could use something 250m and 500m ?