% -------- FACTS --------
american(west).
enemy(nono, america).

owns(nono, m1).
missile(m1).

% -------- RULES --------
weapon(X) :- missile(X).
hostile(X) :- enemy(X, america).

sells(west, nono, X) :-
    missile(X),
    owns(nono, X).

criminal(X) :-
    american(X),
    sells(X, Y, Z),
    weapon(Z),
    hostile(Y).
