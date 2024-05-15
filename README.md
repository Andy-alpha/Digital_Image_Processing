A simple project which implements RegionGrow and SplitMerge algorithm. Based on Python.
- [INSTALLATION](#installation)
- [DESCRIPTION](#description)
- [OPTIONS](#options)

# INSTALLATION

First you should install Python and `pip` for you system, whatever via Anaconda or other ways.

Then install numpy and opencv-python:
```
pip install --upgrade numpy opencv-python
```

To install it right away for all users (Windows, Linux, macOS, etc.), type:
```
git clone https://github.com/Andy-alpha/Digital_Image_Processing.git
cd Digital_Image_Processing/
```

# DESCRIPTION

Usage:
```
python main.py [-h] [-m 'r'|'s'] [-i /path/to/image] [-o /path/of/output.jpg]
               [--thresh INT] [--step STRIDE] [--select 'auto'|'manual']
               [-c CELL] [--max maxMean] [--min minVar]
```

# OPTIONS

```
-m, --mode: 'r'|'s' ('r' for 'regionGrow' and 's' for 'spiltMerge'")
-i, --image: /path/to/image.jpg
-o, --output: /path/of/output.jpg
--thresh: Threshold value for region growing (default=10).
--step: Stride/Intevals when choosing points automatically.
--select: 'auto'|'manual'
  (select whether you would like to choose points automatically or manually in 'regionGrow' mode)
-c, --cell:  The size of minimum split area.
--max: maxMean (default=80.0, the upper bound of mean value)
--min: （default=10.0, the lower bound of standard variation)
```
