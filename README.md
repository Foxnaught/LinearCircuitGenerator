# LinearCircuitGenerator
Given a number of resistors or elements this program will output the number of possible ways in which these elements can be combined in series or parallel to form unique networks. This does not account for bridging, it only counts networks that can be formed by one or more parallel-series networks.

LinearV4.py is the latest version of the file to generate networks. It represents a network as a series of nested 1-dimensional lists. Each element is represented by a 1. By counting the "level" that each list is on we can know if the list's elements are in series or parallel. The outer most list represents a set of elements in series. The second nested list represents elements in parallel. The third nested list represents elements in series. Etc.

LinearV4.py does not generate all networks it only generates half. This is because any unique network has a counterpart that can be obtained simply by placing the whole list representation into another list. This alternates each parallel list to a series list and vice versa.
Therefore to obtain the total number it simply calculates one half and multiples the number by 2. If you would like to obtain the other networks simply nest each list representation as one element in another list.

CircuitRenderer.py is a rendered programmed in pygame that will load networks from linearV4.py and display them. Since linearV4.py only generates half of the networks the renderer will only show half of them. If you would like to view the other half simply nest each representation into another list and feed it into the renderer function.
