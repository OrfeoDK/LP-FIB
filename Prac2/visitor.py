import sys
from turtle3d import Turtle3D
# Generated from logo3d.g by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .logo3dParser import logo3dParser
else:
    from logo3dParser import logo3dParser

# This class defines a complete generic visitor for a parse tree produced by logo3dParser.


class visitor(ParseTreeVisitor):
    # Inicialización del visitor y sus atributos, donde r es el root de la función y pa es el array con el procedimiento por el que empezar y sus parámetros
    # No iniciaremos la tortuga hasta que no se llame una función de ésta
    # var es la pila con los diccionarios de variables de cada procedimiento y procdefs son los procedimientos definidos en el programa con su número de variables
    def __init__(self, r, pa):
        self.turtle = None
        self.procdefs = dict()
        self.var = [{}]
        self.procact = pa
        self.rt = r
        self.first = True
        self.impr = False

    # Visit a parse tree produced by logo3dParser#root.
    def visitRoot(self, ctx: logo3dParser.RootContext):
        # Devuelve el boolean impr, que será cierto si la tortuga ha sido inicializada
        l = list(ctx.getChildren())
        self.visit(l[0])
        return self.impr

    # Visit a parse tree produced by logo3dParser#block.
    def visitBlock(self, ctx: logo3dParser.BlockContext):
        l = list(ctx.getChildren())
        # Si es la primera vez que entramos en la función, nos guardamos todas las funciones declaradas en el diccionario procdefs. Si alguna se repite sacamos un error.
        if self.first:
            for i in range(len(l)):
                if l[i].getChild(1).getText() in self.procdefs.keys():
                    raise Exception("Error: Repetició de procediment ja definit")
                j = 3
                while l[i].getChild(j).getText() != ')':
                    j += 1
                self.procdefs[l[i].getChild(1).getText()] = j - 3
            self.first = False
        # Buscamos el procedimiento procact entre los procesos definidos para ejecutarlo. Si no esta definido, sacamos un error.
        aux = -1
        for i in range(len(l)):
            if self.procact[0] == l[i].getChild(1).getText():
                aux = i
                i = len(l)
        if aux != -1:
            self.visit(l[aux])
        else:
            raise Exception("Error: Crida a procediment no definit")
        # Cuando finaliza el procedimiento, hacemos pop del diccionario donde se encontraban sus variables en la variable var
        self.var.pop()

    # Visit a parse tree produced by logo3dParser#procedureDef.
    def visitProcedureDef(self, ctx: logo3dParser.ProcedureDefContext):
        l = list(ctx.getChildren())
        # Comprovamos si el procedimiento tiene parámetros y los guardamos en el diccionario que se encuentra en el top de la pila var
        if not ctx.far and not ctx.car:
            for i in range(len(l)):
                if str(type(l[i])) == '<class \'logo3dParser.logo3dParser.StatementContext\'>':
                    self.visit(l[i])
        elif not ctx.car:
            self.var[-1][self.visit(ctx.far)] = self.procact[1]
            for i in range(len(l)):
                if str(type(l[i])) == '<class \'logo3dParser.logo3dParser.StatementContext\'>':
                    self.visit(l[i])
        else:
            x = self.procdefs[self.procact[0]] + 3
            for j in range(3, x):
                self.var[-1][self.visit(l[j])] = self.procact[j-2]
            for i in range(len(l)):
                if str(type(l[i])) == '<class \'logo3dParser.logo3dParser.StatementContext\'>':
                    self.visit(l[i])

    # Visit a parse tree produced by logo3dParser#farg.
    def visitFarg(self, ctx: logo3dParser.FargContext):
        # El primer argumento de un procedimiento
        l = list(ctx.getChildren())
        return self.visit(l[0])

    # Visit a parse tree produced by logo3dParser#carg.
    def visitCarg(self, ctx: logo3dParser.CargContext):
        # El segundo argumento de un procedimiento, el cual viene precedido por una coma
        l = list(ctx.getChildren())
        return self.visit(l[1])

    # Visit a parse tree produced by logo3dParser#statement.
    def visitStatement(self, ctx: logo3dParser.StatementContext):
        l = list(ctx.getChildren())
        self.visit(l[0])

    # Visit a parse tree produced by logo3dParser#assignment.
    def visitAssignment(self, ctx: logo3dParser.AssignmentContext):
        # Guardamos el valor asignado a la variable que pertoca en el diccionario del procedimiento
        l = list(ctx.getChildren())
        self.var[-1][l[0].getText()] = self.visit(l[2])

    # Visit a parse tree produced by logo3dParser#lectura.
    def visitLectura(self, ctx: logo3dParser.LecturaContext):
        # Leemos y guardamos el valor en la variable que pertoca en el diccionario del procedimiento
        l = list(ctx.getChildren())
        self.var[-1][l[1].getText()] = float(input())

    # Visit a parse tree produced by logo3dParser#escritura.
    def visitEscritura(self, ctx: logo3dParser.EscrituraContext):
        # Escribimos por pantalla la expresión que pertoca
        l = list(ctx.getChildren())
        print(self.visit(l[1]))

    # Visit a parse tree produced by logo3dParser#stateif.
    def visitStateif(self, ctx: logo3dParser.StateifContext):
        l = list(ctx.getChildren())
        # Asignamos a x la posición donde comienza el ELSE, si es que existe
        x = -1
        for i in range(len(l)):
                if l[i].getText() == 'ELSE':
                    x = i
        # Si x es mayor o igual a zero, realizaremos un if y un else. En caso contrario se tratará de un simple if. En ambos casos visitaremos sus statements
        if x >= 0:
            if self.visit(l[1]):
                for i in range(x):
                    if str(type(l[i])) == '<class \'logo3dParser.logo3dParser.StatementContext\'>':
                        self.visit(l[i])
            else:
                for i in range(x, len(l)):
                    if str(type(l[i])) == '<class \'logo3dParser.logo3dParser.StatementContext\'>':
                        self.visit(l[i])
        else:
            if self.visit(l[1]):
                for i in range(len(l)):
                    if str(type(l[i])) == '<class \'logo3dParser.logo3dParser.StatementContext\'>':
                        self.visit(l[i])

    # Visit a parse tree produced by logo3dParser#statewhile.
    def visitStatewhile(self, ctx: logo3dParser.StatewhileContext):
        # Realizaremos el while, visitando todos sus statements mientras se cumpla la condición
        l = list(ctx.getChildren())
        while self.visit(l[1]):
            for i in range(len(l)):
                if str(type(l[i])) == '<class \'logo3dParser.logo3dParser.StatementContext\'>':
                    self.visit(l[i])

    # Visit a parse tree produced by logo3dParser#statefor.
    def visitStatefor(self, ctx: logo3dParser.StateforContext):
        # Si el inicio o final del for se trata de una variable, la cogeremos del diccionario del procedimiento. En caso contrario, cogeremos el valor en forma de entero
        l = list(ctx.getChildren())
        if l[3].getText() in self.var[-1].keys():
            x = int(self.var[-1][l[3].getText()])
        else:
            x = int(l[3].getText())
        if l[5].getText() in self.var[-1].keys():
            y = int(self.var[-1][l[5].getText()])
        else:
            y = int(l[5].getText())
        # Realizaremos el for desde el inicio hasta el final, visitando todos sus statements. Guardaremos la variable k con su valor, actualizandola en cada iteración del bucle, en el diccionario del procedimiento
        for k in range(x, y):
            self.var[-1][l[1].getText()] = k
            for i in range(len(l)):
                if str(type(l[i])) == '<class \'logo3dParser.logo3dParser.StatementContext\'>':
                    self.visit(l[i])

    # Visit a parse tree produced by logo3dParser#procedureCall.
    def visitProcedureCall(self, ctx: logo3dParser.ProcedureCallContext):
        l = list(ctx.getChildren())
        norm = True
        # Comprobaremos si la llamada a la función se corresponde con alguna función de la tortuga.
        # En caso afirmativo, la ejecutaremos si el número de parámetros es el correcto. También pondremos norm a false, indicando que no es un procedimiento normal.
        # Además, si el boolean impr no era true, lo pondremos a true e inicializaremos la tortuga.
        # Si el procedimiento no se corresponde con ninguno de la tortuga y no está definido, sacaremos un error
        if l[0].getText() == 'color':
            if len(l) == 6:
                norm = False
                if not self.impr:
                    self.impr = True
                    self.turtle = Turtle3D()
                x = self.visit(l[2])
                y = self.visit(l[3])
                z = self.visit(l[4])
                self.turtle.color(x, y, z)
            else:
                raise Exception("Error: Nombre de parametres incorrectes")
        elif l[0].getText() == 'forward':
            if len(l) == 4:
                norm = False
                if not self.impr:
                    self.impr = True
                    self.turtle = Turtle3D()
                x = self.visit(l[2])
                self.turtle.forward(x)
            else:
                raise Exception("Error: Nombre de parametres incorrectes")
        elif l[0].getText() == 'backward':
            if len(l) == 4:
                norm = False
                if not self.impr:
                    self.impr = True
                    self.turtle = Turtle3D()
                x = self.visit(l[2])
                self.turtle.backward(x)
            else:
                raise Exception("Error: Nombre de parametres incorrectes")
        elif l[0].getText() == 'right':
            if len(l) == 4:
                norm = False
                if not self.impr:
                    self.impr = True
                    self.turtle = Turtle3D()
                x = self.visit(l[2])
                self.turtle.right(x)
            else:
                raise Exception("Error: Nombre de parametres incorrectes")
        elif l[0].getText() == 'left':
            if len(l) == 4:
                norm = False
                if not self.impr:
                    self.impr = True
                    self.turtle = Turtle3D()
                x = self.visit(l[2])
                self.turtle.left(x)
            else:
                raise Exception("Error: Nombre de parametres incorrectes")
        elif l[0].getText() == 'down':
            if len(l) == 4:
                norm = False
                if not self.impr:
                    self.impr = True
                    self.turtle = Turtle3D()
                x = self.visit(l[2])
                self.turtle.down(x)
            else:
                raise Exception("Error: Nombre de parametres incorrectes")
        elif l[0].getText() == 'up':
            if len(l) == 4:
                norm = False
                if not self.impr:
                    self.impr = True
                    self.turtle = Turtle3D()
                x = self.visit(l[2])
                self.turtle.up(x)
            else:
                raise Exception("Error: Nombre de parametres incorrectes")
        elif l[0].getText() == 'show':
            if len(l) == 3:
                norm = False
                if not self.impr:
                    self.impr = True
                    self.turtle = Turtle3D()
                self.turtle.show()
            else:
                raise Exception("Error: Nombre de parametres incorrectes")
        elif l[0].getText() == 'hide':
            if len(l) == 3:
                norm = False
                if not self.impr:
                    self.impr = True
                    self.turtle = Turtle3D()
                self.turtle.hide()
            else:
                raise Exception("Error: Nombre de parametres incorrectes")
        elif l[0].getText() == 'home':
            if len(l) == 3:
                norm = False
                if not self.impr:
                    self.impr = True
                    self.turtle = Turtle3D()
                self.turtle.home()
            else:
                raise Exception("Error: Nombre de parametres incorrectes")
        elif l[0].getText() not in self.procdefs.keys():
            raise Exception("Error: Crida a procediment no definit")
        # Si el procedimiento no es de la tortuga comprobaremos que el número de parémetros sea el correcto y en caso contrario abortaremos con un error.
        # También sacaremos un error si el nombre de alguno de estos está repetido
        # Si no detectamos ningún error, asignaremos al array procact el nombre del procedimiento y sus parámetros, pondremos un diccionario de variables vacio en la pila var y visitaremos la raiz para que este se ejecute
        if norm:
            j = 2
            while l[j].getText() != ')':
                k = 2
                while l[k].getText() != ')':
                    if j != k:
                        if l[j].getText() == l[k].getText() or ',' + l[j].getText() == l[k].getText():
                            raise Exception("Error: Noms de parametres formals repetits")
                    k += 1
                j += 1
            if self.procdefs[l[0].getText()] != j - 2:
                raise Exception("Error: Nombre de parametres incorrectes")
            if not ctx.far and not ctx.car:
                self.procact = [l[0].getText()]
            elif not ctx.car:
                self.procact = [l[0].getText(), self.visit(ctx.far)]
            else:
                self.procact = [l[0].getText(), self.visit(ctx.far)]
            for i in range(len(l)):
                if str(type(l[i])) == '<class \'logo3dParser.logo3dParser.CargContext\'>':
                    self.procact.append(self.visit(l[i]))
            self.var.append({})
            self.visit(self.rt)

    # Visit a parse tree produced by logo3dParser#MultDivExpr.
    def visitMultDivExpr(self, ctx: logo3dParser.MultDivExprContext):
        # Realizaremos o multiplicación o división, devolviendo el valor resultante. Si la división es entre 0, abortaremos con un error
        l = list(ctx.getChildren())
        if l[1].getText() == '*':
            return self.visit(l[0]) * self.visit(l[2])
        elif l[2].getText() == '0':
            raise ZeroDivisionError("Error: divisio per 0")
        else:
            return self.visit(l[0]) / self.visit(l[2])

    # Visit a parse tree produced by logo3dParser#atomExpr.
    def visitAtomExpr(self, ctx: logo3dParser.AtomExprContext):
        l = list(ctx.getChildren())
        return self.visit(l[0])

    # Visit a parse tree produced by logo3dParser#natomExpr.
    def visitNatomExpr(self, ctx: logo3dParser.NatomExprContext):
        # Devolveremos el número real negativo
        l = list(ctx.getChildren())
        return float('-' + l[1].getText())

    # Visit a parse tree produced by logo3dParser#SumResExpr.
    def visitSumResExpr(self, ctx: logo3dParser.SumResExprContext):
        # Realizaremos o suma o resta, devolviendo el valor resultante.
        l = list(ctx.getChildren())
        if l[1].getText() == '+':
            return self.visit(l[0]) + self.visit(l[2])
        else:
            return self.visit(l[0]) - self.visit(l[2])

    # Visit a parse tree produced by logo3dParser#relationExpr.
    def visitRelationExpr(self, ctx: logo3dParser.RelationExprContext):
        # Devolveremos el resultado de las comparaciones >, <, >= Y <=
        l = list(ctx.getChildren())
        if l[1].getText() == '>':
            return self.visit(l[0]) > self.visit(l[2])
        elif l[1].getText() == '<':
            return self.visit(l[0]) < self.visit(l[2])
        elif l[1].getText() == '>=':
            return self.visit(l[0]) >= self.visit(l[2])
        else:
            return self.visit(l[0]) <= self.visit(l[2])

    # Visit a parse tree produced by logo3dParser#equalExpr.
    def visitEqualExpr(self, ctx: logo3dParser.EqualExprContext):
        # Devolveremos el resultado de las comparaciones == y !=
        l = list(ctx.getChildren())
        if l[1].getText() == '==':
            return self.visit(l[0]) == self.visit(l[2])
        else:
            return self.visit(l[0]) != self.visit(l[2])

    # Visit a parse tree produced by logo3dParser#numberAtom.
    def visitNumberAtom(self, ctx: logo3dParser.NumberAtomContext):
        # Devolveremos el valor del número real
        l = list(ctx.getChildren())
        return float(l[0].getText())

    # Visit a parse tree produced by logo3dParser#boolAtom.
    def visitBoolAtom(self, ctx: logo3dParser.BoolAtomContext):
        # Devolveremos el valor del booleano, ya sea true o false
        l = list(ctx.getChildren())
        if l[0].getText() == 'TRUE':
            return True
        else:
            return False

    # Visit a parse tree produced by logo3dParser#idAtom.
    def visitIdAtom(self, ctx: logo3dParser.IdAtomContext):
        # Devolveremos el valor de la variable almacenado en el diccionario del procedimiento, si ésta se encuentra en él. En caso contrario, devolveremos el nombre de la variable
        l = list(ctx.getChildren())
        if l[0].getText() in self.var[-1].keys():
            return float(self.var[-1][l[0].getText()])
        else:
            return l[0].getText()

del logo3dParser
