# dungeons-and-diagrams-solver
Solver for Last Call BBS "Dungeons and Diagrams" game

Takes in mazes of the form
```
// The Corroded Corridors
* 4 2 4 2 3 4 2 6
3 _ m _ _ _ _ m _
6 _ _ _ _ _ _ _ _
0 _ _ _ _ _ _ _ m
5 _ _ _ _ _ _ _ _
4 _ _ _ _ m _ _ _
0 _ _ _ _ _ _ _ m
6 _ _ _ _ _ _ _ _
3 _ m _ _ _ _ m _
```

And outputs solutions like:

```
┌───┬─────────────────┐
│ * │ 4 2 4 2 3 4 2 6 │
├───┼─────────────────┤
│ 3 │ # m # _ _ _ m # │
│ 6 │ # _ # _ # # # # │
│ 0 │ _ _ _ _ _ _ _ m │
│ 5 │ _ # _ # # # _ # │
│ 4 │ _ # _ # m # _ # │
│ 0 │ _ _ _ _ _ _ _ m │
│ 6 │ # _ # _ # # # # │
│ 3 │ # m # _ _ _ m # │
└───┴─────────────────┘
```