{-# LANGUAGE RecordWildCards #-}    -- per utilitzar fields

import Data.Char (isUpper)
import Data.List (nub, isInfixOf)
import Data.List.Split (splitOn)    -- cal instal·lar: cabal install split
import Data.String.Utils (strip)    -- cal instal·lar: cabal install MissingH
import Data.Maybe (mapMaybe, fromMaybe)


type Programa = [ Regla ]

data Regla = Regla { _cap::Atom, _cos::[ Atom ] }

instance Show Regla where
    show (Regla { _cap = x, _cos = y }) = "\nRegla { _cap = " ++ show x ++ ", _cos = " ++ show y ++ " }"       -- show para poder comprobar que el parse se había hecho bien

data Atom = Atom { _nomPredicat::String, _termes::[ Term ] }
    deriving (Eq, Show)

data Term = Var String | Sym String
   deriving (Eq, Show)

type Sustitucio = [ (Term, Term) ]     -- [(variable, constant), (variable, constant), ...]

type BaseConeixement = [ Atom ]


-- PARSER: Funciones del parser del programa ----------------------------------------------------------------------------

-- funciones de splitOn-------------------------------------

-- corta un string por "end.", es decir, separa las reglas de las query
cortarEntrada :: String -> [String]
cortarEntrada entrada = map (strip) (splitOn "end." entrada)

-- corta un string por ".", es decir, separa las lineas del programa
cortarLinea :: String -> [String]
cortarLinea entrada = map (strip) (splitOn "." (init entrada))

-- corta un string por "=>", es decir, separa el cos y el cap de las reglas
cortarPred :: String -> [String]
cortarPred linea = map (strip) (splitOn "=>" linea)

-- corta un string por " ", es decir, separa por palabras
cortarCap :: String -> [String]
cortarCap pred = map (strip) (splitOn " " pred)

-- corta un string por "&", es decir, separa los distintos atomos del cuerpo de una regla
cortarCos :: String -> [String]
cortarCos pred = map (strip) (splitOn "&" pred)

-- funciones de montar estructuras de datos-----------------

-- monta el programa, ya sean las reglas o las query
montarPrograma :: [[String]] -> Programa
montarPrograma r = map montarRegla r

-- monta un atomo en concreto
montarCap :: [String] -> Atom
montarCap (x:xs) = Atom { _nomPredicat = x, _termes = montarTermes xs }

-- monta los terminos de un atomo
montarTermes :: [String] -> [Term]
montarTermes [] = []
montarTermes (x:xs)
    | isUpper (head x) = Var x : montarTermes xs
    | otherwise = Sym x : montarTermes xs

-- monta una regla, ya sea un hecho sin cos, o una regla normal
montarRegla :: [String] -> Regla
montarRegla (x:[]) = Regla { _cap = montarCap (cortarCap x), _cos = [] }
montarRegla (x:xs:[]) = Regla { _cap = montarCap (cortarCap xs), _cos = map montarCap (map cortarCap (cortarCos x)) }
--------------------------------------------------------------------------------------------------------------------------


-- CONSECUENCIA: genera la siguiente base de conocimiento usando las reglas del programa ---------------------------------

consequencia :: Programa -> BaseConeixement -> BaseConeixement
consequencia [] kb = kb
consequencia (r:rs) kb = nub(avaluaRegla kb r ++ consequencia rs kb)

--------------------------------------------------------------------------------------------------------------------------


-- AVALUA REGLA: evalua las reglas con una base de conocimiento para generar nuevos atomos ground ------------------------

-- manda a evaluar todos los atomos del cuerpo de la regla con la base de conocimiento empezando por una lista de
-- sustituciones vacia devuelve la base de conocimiento formada por los atomos ground sin repeticiones sacados de la evaluacion 
avaluaRegla :: BaseConeixement -> Regla -> BaseConeixement
avaluaRegla kb r
    | sublist (_cos r) kb = [_cap r]
    | otherwise = nub(sonGround(map (\x -> (sustitueix (_cap r) x)) (miraCos kb (_cos r) [])) )

-- retorna solo los atomos que son ground 
sonGround :: [Atom] -> [Atom]
sonGround [] = []
sonGround (a:as)
    | esGround (_termes a) = [a] ++ sonGround as
    | otherwise = sonGround as

-- devuelve true si el atomo es ground (es decir, si todos los terminos son simbolos)
esGround :: [Term] -> Bool
esGround [] = True
esGround (Var t:ts) = False
esGround (Sym t:ts) = esGround ts

-- manda a evaluar todos los atomos con la base de conocimiento y la lista de sustituciones que saca el atomo que se ha evaluado antes
-- empezando con una lista vacia en el primero
miraCos :: BaseConeixement -> [Atom] -> [Sustitucio] -> [Sustitucio]
miraCos kb [] s = s
miraCos kb (a:as) s = miraCos kb as (avaluaAtom kb a s)

-- función auxiliar que determina si una lista es sublista de otra
sublist :: Eq a => [a] -> [a] -> Bool
sublist [] [] = True
sublist _ [] = False
sublist [] _ = True
sublist (x:xs) y
    | elem x y = sublist xs y
    | otherwise = False
---------------------------------------------------------------------------------------------------------------------------


-- AVALUA ATOM: avaluacion de Atom en una base de conocimiento ------------------------------------------------------------

-- en la primera visita la lista de sustituciones esta vacia y hay que generar todas las posibles sustituciones en ese
-- atomo con la base de conocimiento actual
avaluaAtom :: BaseConeixement -> Atom -> [ Sustitucio ] -> [ Sustitucio ]
avaluaAtom kb a [] = (mapMaybe (\x -> (unifica a x)) kb)
avaluaAtom kb a s = (avaluaAux kb a s)

-- si no es la primer atomo de la regla que se evalua se comprueban las sustituciones de la lista y se van descartando las
-- que no cuadran
avaluaAux :: BaseConeixement -> Atom -> [ Sustitucio ] -> [ Sustitucio ]
avaluaAux kb a [] = []
avaluaAux kb a (s:ss) = (map (s ++) (mapMaybe (\x -> (unifica (sustitueix a s) x)) kb)) ++ avaluaAux kb a ss
---------------------------------------------------------------------------------------------------------------------------


-- UNIFICACION: comprueba si dos atomos se pueden unificar (segun la definicion del enunciado) y genera su sustitución
-- en caso afirmativo. Si no genera Nothing

-- saca Nothing si los atomos no se puede unificar y Just Sustitucio en el caso de que si se pueda
unifica :: Atom -> Atom -> Maybe Sustitucio
unifica a1 a2
    | _nomPredicat a1 /= _nomPredicat a2 = Nothing
    | uni (_termes a1) (_termes a2) w = Just w
    | otherwise = Nothing
    where w = (unisub (_termes a1) (_termes a2))

-- dado dos listas de terminos, las recorre. Si el termino de la primera lista es una variable devuelve su sustitucion por
-- el simbolo de la segunda lista
unisub :: [Term] -> [Term] -> Sustitucio
unisub [] [] = []
unisub [] _ = []
unisub _ [] = []
unisub ((Sym x):xs) (y:ys) = unisub xs ys
unisub ((Var x):xs) (y:ys) = (Var x,y) : unisub xs ys

-- dadas dos listas de terminos y una sustitucion devuelve true si se pueden unificar
uni :: [Term] -> [Term] -> Sustitucio -> Bool
uni [] [] _ = True
uni [] _ _ = False
uni _ [] _ = False
uni (Sym x:xs) (Sym y:ys) s = x==y && uni xs ys s
uni (x:xs) (y:ys) s = uigual x y s && uni xs ys s

-- devuelve true si el primer termino puede ser sustituido por el segundo
uigual :: Term -> Term -> Sustitucio -> Bool
uigual x y [] = True
uigual x y ((u,v):ss)
    | u==x && v/=y = False
    | otherwise = uigual x y ss
--------------------------------------------------------------------------------------------------------------------------


-- SUSTITUCION: aplica la sustitución al atomo usando la funcion auxiliar sub --------------------------------------------

-- sustituye las variables del atomo que aparezcan en la sustitucion y devuelve el atomo sustituido
sustitueix :: Atom -> Sustitucio -> Atom
sustitueix a [] = a
sustitueix a s = Atom { _nomPredicat = (_nomPredicat a), _termes = (map (\x -> sub x s) (_termes a)) }

-- sustituye un termino si este es una variable que aparece en la sustitucion
sub :: Term -> Sustitucio -> Term
sub (Sym t) _ = Sym t
sub t [] = t
sub (Var t) ((Var x, Sym y):xs)
    | x==t = Sym y
    | otherwise = sub (Var t) xs


sustitucioBuida :: Sustitucio
sustitucioBuida = []
--------------------------------------------------------------------------------------------------------------------------


-- GENERAR SOLUCION: -----------------------------------------------------------------------------------------------------

-- genera el resultado de las queries
generaResult :: BaseConeixement -> BaseConeixement -> Programa -> BaseConeixement
generaResult kbi kbf pr
    | (sublist kbf kbi) = kbi
    | otherwise = (generaResult kbf (consequencia pr kbf) pr)

-- mira si la query es de true o false o de posibles sustituciones
soluciona :: BaseConeixement -> Atom -> IO ()
soluciona kb c = do
    if (_termes c) == []
    then trueOrFalse kb c
    else sacarSol kb c

-- muestra las posibles soluciones de una query
sacarSol :: BaseConeixement -> Atom -> IO ()
sacarSol kb c = do
    putStrLn $ show (mapMaybe (\x -> (unifica c x)) kb)

-- indica si la query es cierta o falsa
trueOrFalse :: BaseConeixement -> Atom -> IO ()
trueOrFalse kb c = do
    if (elem c kb)
    then putStrLn "true"
    else putStrLn "false"

-- computar las query
trabaja :: Programa -> Programa -> IO ()
trabaja pr [] = putStrLn "\nTodas las query finalizadas!"
trabaja pr (q:qu) = do
    let kb0 = []
    let kbf = generaResult kb0 (consequencia (pr ++ [q]) kb0) (pr ++ [q])
    soluciona kbf (_cap q)
    trabaja pr qu
--------------------------------------------------------------------------------------------------------------------------


-- MAIN: main del programa -----------------------------------------------------------------------------------------------
main :: IO ()
main = do
    entrada <- getContents
    let t = cortarEntrada entrada
    let r = cortarLinea (head t)
    let q = cortarLinea (t !! 1)
    let p = map cortarPred r
    let qu = map cortarPred q
    let pr = montarPrograma p
    let query = montarPrograma qu
    
    trabaja pr query
--------------------------------------------------------------------------------------------------------------------------

