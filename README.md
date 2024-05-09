# Wandrer
Inspired by [Wandrer](https://wandrer.earth), 
<img src="https://github.com/dsleo/wandrer/blob/main/img/strava.jpg" width="50%" height="40%">

The goal is to determine whether any segments within a newly Strava activity have been ridden or run before.  

To accomplish this, we propose two strategies:

* Geometrical Approach: By examining the geographical relationship between historical and new activity path segments, we get previously untraveled routes.

* Lexical Approach: We simply compare the historical and new activity Strava segment names. It's that easy.

## How To
Have a look at this [Example notebook](https://github.com/dsleo/wandrer/blob/main/notebooks/Example.ipynb)