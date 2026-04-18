male(john). male(bob). male(jim).
female(mary). female(carol).

spouse(john, mary). spouse(mary, john).

parent(john, carol). parent(mary, carol).

father(X,Y) :- male(X), parent(X,Y).
mother(X,Y) :- female(X), parent(X,Y).

child(X,Y) :- parent(Y,X).

sibling(X,Y) :-
    parent(P,X), parent(P,Y),
    X \= Y.

brother(X,Y) :- male(X), sibling(X,Y).
sister(X,Y) :- female(X), sibling(X,Y).

grandparent(X,Y) :- parent(X,Z), parent(Z,Y).

uncle(X,Y) :-
    male(X),
    sibling(X,P),
    parent(P,Y).

relation(X, Y, 'Father') :- father(X, Y).
relation(X, Y, 'Mother') :- mother(X, Y).
relation(X, Y, 'Brother') :- brother(X, Y).
relation(X, Y, 'Sister') :- sister(X, Y).

what_is(X,Y) :-
    relation(X,Y,R),
    write(X), write(' is '), write(R), write(' of '), write(Y), nl.
