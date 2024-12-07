
**Let's check performance, because it's fun**

# Part 2

## Pypy

    User time (seconds): 375.55
    System time (seconds): 3.52
    Percent of CPU this job got: 99%
    Elapsed (wall clock) time (h:mm:ss or m:ss): 6:19.18
    Average shared text size (kbytes): 0
    Average unshared data size (kbytes): 0
    Average stack size (kbytes): 0
    Average total size (kbytes): 0
    Maximum resident set size (kbytes): 6271228
    Average resident set size (kbytes): 0
    Major (requiring I/O) page faults: 0
    Minor (reclaiming a frame) page faults: 1735697
    Voluntary context switches: 1
    Involuntary context switches: 2319

## Python

    User time (seconds): 1355.06
    System time (seconds): 4.06
    Percent of CPU this job got: 99%
    Elapsed (wall clock) time (h:mm:ss or m:ss): 22:39.53
    Average shared text size (kbytes): 0
    Average unshared data size (kbytes): 0
    Average stack size (kbytes): 0
    Average total size (kbytes): 0
    Maximum resident set size (kbytes): 7029344
    Average resident set size (kbytes): 0
    Major (requiring I/O) page faults: 0
    Minor (reclaiming a frame) page faults: 1822997
    Voluntary context switches: 1
    Involuntary context switches: 8738

## Fast (binary) Python (7.5x faster!)

    User time (seconds): 182.26
    System time (seconds): 1.09
    Percent of CPU this job got: 99%
    Elapsed (wall clock) time (h:mm:ss or m:ss): 3:03.42

### Pythonista on an iPad:

    >>> ELAPSED 120.86144995689392sec

    Faster than a Threadripper CPU. Oh well.


## Fast (binary) Pypy (3.37x faster than the Fast Python, 7x faster than the slow Pypy, 25x faster than the slow Python)

    User time (seconds): 54.60
    System time (seconds): 1.98
    Percent of CPU this job got: 99%
    Elapsed (wall clock) time (h:mm:ss or m:ss): 0:56.60
