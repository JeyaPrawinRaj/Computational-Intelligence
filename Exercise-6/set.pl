% --- CORE SET OPERATIONS ---

member(X, [X|_]) :- !.
member(X, [_|T]) :- member(X, T).

union([], L, L).
union([H|T], L, R) :- member(H, L), !, union(T, L, R).
union([H|T], L, [H|R]) :- union(T, L, R).

intersection([], _, []).
intersection([H|T], L, [H|R]) :- member(H, L), !, intersection(T, L, R).
intersection([_|T], L, R) :- intersection(T, L, R).

difference([], _, []).
difference([H|T], L, R) :- member(H, L), !, difference(T, L, R).
difference([H|T], L, [H|R]) :- difference(T, L, R).

subset([], _).
subset([H|T], L) :- member(H, L), subset(T, L).

is_equal(L1, L2) :- subset(L1, L2), subset(L2, L1).

% --- MENU ---
run :-
    repeat,
    nl, write('--- SET OPERATIONS MENU ---'), nl,
    write('1. Member'), nl,
    write('2. Union'), nl,
    write('3. Intersection'), nl,
    write('4. Difference'), nl,
    write('5. Subset'), nl,
    write('6. Is Equal'), nl,
    write('7. Exit'), nl,
    write('Enter choice: '), read(Choice),
    do_choice(Choice),
    Choice == 7, !.

do_choice(1) :-
    write('Element: '), read(X),
    write('List: '), read(L),
    (member(X, L) -> write('Result: Yes'); write('Result: No')), nl, !.

do_choice(2) :-
    write('List 1: '), read(L1), write('List 2: '), read(L2),
    union(L1, L2, R), write(R), nl, !.

do_choice(3) :-
    write('List 1: '), read(L1), write('List 2: '), read(L2),
    intersection(L1, L2, R), write(R), nl, !.

do_choice(4) :-
    write('List 1: '), read(L1), write('List 2: '), read(L2),
    difference(L1, L2, R), write(R), nl, !.

do_choice(5) :-
    write('Subset: '), read(L1), write('Main List: '), read(L2),
    (subset(L1, L2) -> write('Yes'); write('No')), nl, !.

do_choice(6) :-
    write('List 1: '), read(L1), write('List 2: '), read(L2),
    (is_equal(L1, L2) -> write('Equal'); write('Not Equal')), nl, !.

do_choice(7) :-
    write('Exiting...'), nl, !.

do_choice(_) :-
    write('Invalid choice'), nl.
