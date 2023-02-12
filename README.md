## Random Map Generator

This project provides a Random Map Generator, which generates a random map. In the map, you can surely find the path between any two points.

Moreover, this project also shows you the performance of several algorithms:

- Breadth First Search

- Depth First Search

- Iterative Deepening Search

- Bidirectional Breadth First Search

- Bidirectional Depth First Search

- Bidirectional Iterative Deepening Search

- Uniform Cost Search

- Greedy Best First Search

- A Star Search

- Bidirectional A Star Search

- Iterative Deepening A Star Search

This project is based on python, and you should install pygame module and numpy module beforehand.

```
pip install -r requirements.txt
```

To run this project, you can input the following content in your commander:

```
python main.py
```

The width/height of this generated map has both been set to 700 (pixels), and the scale of each one rectangle has been set to 14 (=700 // 50). The relationship is:

```
WIDTH = HEIGHT
```

```
rectangle_scale = WIDTH // MAP_SIZE
```

If you want to reset them, you can change the value of WIDTH(=700) Literal in main.py, HEIGHT(=700) Literal in main.py, and MAP_SIZE(=50) Literal in random_map.py. You should always keep them as integers.

Here are several examples:

Bidirectional Breadth First Search

![Bidirectional Breadth First Search](/images/Bidirectional-Breadth-First-Search.png)

A Star Search

![A Star Search](/images/A-Star-Search.png)