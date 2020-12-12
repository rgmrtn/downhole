# Downhole

Downhole is (aims to be) a collection of python utilities for dealing with geological drill data.

## Usage

```python
from downhole.survey import min_curv

# provide lists of floats to dip_data, depth_data, azm_data (survey data)
# provide projected x, y, z coordinates
# result is a list for each x,y,z coordinates of the drill path
min_curv(dip_data, depth_data, azm_data, x, y, z)

```