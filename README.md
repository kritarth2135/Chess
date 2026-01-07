# Chess
This is a chess engine implemented in python.

## Features
What you __can__ do now:
1. Import any game using a FEN string
2. Move any piece
3. Capture any piece
4. Check the king

What you __cannot__ do now:
1. Checkmate the king
2. Castle
3. En passant capture

## How to play:
First, clone this repository and then run:
```
python main.py
```
If you want to overwrite default starting position, you can import a custom board by passing a fen string as an argument as follows:
```
python main.py "starting_fen"
```
By default game will starts in GUI, if you want to debug and run in CLI use the ``-c`` flag like below:
```
python main.py -c
```
## How to play
Just drag and drop a piece to move it.

## How to give user input in CLI
Input is taken as follows, __with__ space in between
```
<starting_square> <ending square>
```
A square is denoted by the following:
```
<rank><file>       // algebraic notation
```
where ranks (horizontal rows) are from 1 to 8 (bottom to top), and files (vertical columns) from A to H (left to right).

For example if you want to move your pawn from ``e2`` to ``e4`` then:
```
e2 e4
```
The inputs are case __insensitive__.
