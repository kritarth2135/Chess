# Chess
This is a chess game made in python.

## Features
What you __can__ do now:
1. Import any game using a FEN string

What you __cannot__ do now:
1. Capture a piece
2. Play chance by chance
3. Move any piece (Although right now it ignores pieces in middle)

## How to play:
First, clone this repository and then run:
```
python main.py
```
If you want to overwrite default starting position, you can import a custom board by passing a fen string as an argument as follows:
```
python main.py "starting_fen"
```

## User input format
Input is taken as follows, __without__ any space in between
```
<starting_square>,<ending square>
```
A square is denoted by the following:
```
<rank><file>       // algebraic notation
```
where ranks (horizontal rows) are from 1 to 8 (bottom to top), and files (vertical columns) from A to H (left to right).

For example if you want to move your pawn from ``e2`` to ``e4`` then:
```
e2,e4
```
The inputs are case __insensitive__.
