module Vector exposing (Vector, add, cross, distance, divide, dot, equivalent, magnitude, multiply, normalize, randomVector, similarity, subtract, vector, x, y)

import Random


type alias Vector =
    ( Float, Float )


equivalentErr =
    1.0e-6


vector : Float -> Float -> Vector
vector a b =
    ( a, b )


x : Vector -> Float
x =
    Tuple.first


y : Vector -> Float
y =
    Tuple.second


subtract : Vector -> Vector -> Vector
subtract p q =
    vector (x p - x q) (y p - y q)


add : Vector -> Vector -> Vector
add p q =
    vector (x p + x q) (y p + y q)


multiply : Float -> Vector -> Vector
multiply k p =
    vector (x p * k) (y p * k)


divide : Float -> Vector -> Vector
divide k p =
    vector (x p / k) (y p / k)


magnitude : Vector -> Float
magnitude p =
    sqrt (x p ^ 2 + y p ^ 2)


distance : Vector -> Vector -> Float
distance p q =
    magnitude (subtract p q)


normalize : Vector -> Vector
normalize p =
    divide (magnitude p) p


dot : Vector -> Vector -> Float
dot p q =
    (x p * x q) + (y p * y q)


cross : Vector -> Vector -> Float
cross p q =
    x p * y q - y p * x q


perpendicular : Vector -> Vector
perpendicular p =
    vector -(y p) (x p)


similarity : Vector -> Vector -> Float
similarity p q =
    dot p q / (magnitude p * magnitude q)


equivalent : Vector -> Vector -> Bool
equivalent p q =
    magnitude (subtract p q) < equivalentErr


randomVector : Vector -> Vector -> Random.Generator Vector
randomVector min max =
    Random.map2 vector
        (Random.float (x min) (x max))
        (Random.float (y min) (y max))
