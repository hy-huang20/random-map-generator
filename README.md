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

The width/height of this generated map has both been set to 700, and the scale of each one rectangle has been set to 700 // 50 = 14. If you want to reset it, you can change the value of WIDTH(=700) Literal in main.py, HEIGHT(=700) Literal in main.py, and MAP_SIZE(=50) in random_map.py.