# dungeons-and-diagrams-solver
Solver for Last Call BBS "Dungeons and Diagrams" game

Takes in mazes of the form
```
// Tutorial level
* 4 1 4 1 2 1
3 _ _ _ _ _ c
1 _ _ _ _ _ _
1 m _ _ _ _ _
5 _ _ _ _ _ _
2 _ _ _ _ _ m
1 m _ _ _ _ _
```

And outputs solutions like:

```
┌───┬─────────────┐
│ * │ 4 1 4 1 2 1 │
├───┼─────────────┤
│ 3 │ # # # _ _ c │
│ 1 │ # _ _ _ _ _ │
│ 1 │ m _ # _ _ _ │
│ 5 │ # _ # # # # │
│ 2 │ # _ _ _ # m │
│ 1 │ m _ # _ _ _ │
└───┴─────────────┘
```