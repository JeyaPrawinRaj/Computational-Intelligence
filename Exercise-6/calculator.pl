% --- Separate Predicates (Functions) ---
add_vals(X, Y, R) :- R is X + Y.
sub_vals(X, Y, R) :- R is X - Y.
mul_vals(X, Y, R) :- R is X * Y.
div_vals(X, Y, R) :- R is X / Y.
mod_vals(X, Y, R) :- R is X mod Y.

% --- Main Menu ---
calculator :-
    nl, write('--- PROLOG CALCULATOR ---'), nl,
    write('1. Addition'), nl,
    write('2. Subtraction'), nl,
    write('3. Multiplication'), nl,
    write('4. Division'), nl,
    write('5. Modulo'), nl,
    write('6. Exit'), nl,
    write('Select Choice (1-6): '), read(Choice),
    switch_case(Choice).

% --- Switch Case Logic ---

switch_case(1) :-
    write('Enter Num 1: '), read(X),
    write('Enter Num 2: '), read(Y),
    add_vals(X, Y, Res),
    write('Result: '), write(X), write(' + '), write(Y), write(' = '), write(Res), nl,
    calculator.

switch_case(2) :-
    write('Enter Num 1: '), read(X),
    write('Enter Num 2: '), read(Y),
    sub_vals(X, Y, Res),
    write('Result: '), write(X), write(' - '), write(Y), write(' = '), write(Res), nl,
    calculator.

switch_case(3) :-
    write('Enter Num 1: '), read(X),
    write('Enter Num 2: '), read(Y),
    mul_vals(X, Y, Res),
    write('Result: '), write(X), write(' * '), write(Y), write(' = '), write(Res), nl,
    calculator.

switch_case(4) :-
    write('Enter Num 1: '), read(X),
    write('Enter Num 2: '), read(Y),
    (Y \= 0 ->
        (div_vals(X, Y, Res), write('Result: '), write(X), write(' / '), write(Y), write(' = '), write(Res), nl) ;
        (write('Error: Division by zero!'), nl)
    ),
    calculator.

switch_case(5) :-
    write('Enter Num 1: '), read(X),
    write('Enter Num 2: '), read(Y),
    (Y \= 0 ->
        (mod_vals(X, Y, Res), write('Remainder: '), write(Res), nl) ;
        (write('Error: Modulo by zero!'), nl)
    ),
    calculator.

switch_case(6) :-
    write('Goodbye!'), nl.

switch_case(_) :-
    write('Invalid Option.'), nl,
    calculator.
