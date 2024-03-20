#Calculator that takes in expressions set with spaces between each number or operation
#Returns the calculated value
#AdvancedCalculator takes in an expression with variables and can compute the value of the expression

class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          


class Stack:
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__


    def isEmpty(self):
        return self.top == None

    def __len__(self): 
        count = 0
        current = self.top
        while current:
            current = current.next
            count +=1
        return count

    def push(self,value):
        newNode = Node(value)
        if self.isEmpty() ==False:
            newNode.next = self.top
        self.top = newNode

     
    def pop(self):
        if self.isEmpty():
            return None
        popNode = self.top
        self.top = popNode.next
        return popNode.value


    def peek(self):
        if self.isEmpty():
            return None
        return self.top.value



class Calculator:
    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):
        string = txt.strip()
        try:
            float(string)
            return True
        except ValueError:
            return False





    def _getPostfix(self, txt):
        opdict = {'^': 7, "*" : 6, "/": 6, "+": 5, "-":5, "(" :4, "[":3,"{":2,"<":1, None: 0, ')':-4, ']':-3, '}':-2, '>':-1}
        txt = txt.strip()
        lst = txt.split(" ")
        pf = ""
        valid = self.isValidInput(txt,opdict,lst)
        postfixStack = Stack() # method must use postfixStack to compute the postfix expression
        if valid:
            for index in range(len(lst)):
                item = lst[index]
                if self._isNumber(item):
                    pf += f" {float(item)}" #if its a number --> straight to pf
                    #check to see if the item next to it is a open bracket because that implies multiplication
                    if index != len(lst)-1 and (opdict[lst[index+1]]>0 and opdict[lst[index+1]]<5):
                        postfixStack.push('*')
                elif item == "^" and postfixStack.peek() == "^": #if its a exponent at the top and your putting another one in don't pop
                    postfixStack.push(item)                    
                else: #if not a number -->prep for the stack
                    operationValue = opdict[item]
                    if postfixStack.isEmpty() or (operationValue<5 and operationValue>0):
                        postfixStack.push(item) #if stack is empty or its a bracket put item in
                    elif(operationValue<0): #if its a closing Bracket
                        while opdict[postfixStack.peek()] != (-1* operationValue): #while its open bracket match isnt found
                            if opdict[postfixStack.peek()]>4: #if its a proper operation it gets into the stack
                                pf += f" {postfixStack.pop()}"
                            else: #otherwise just get rid of it
                                postfixStack.pop()
                        postfixStack.pop() #pop the last open bracket
                        if index != len(lst)-1 and opdict[lst[index+1]]>0 and opdict[lst[index+1]]<5: #if implied multiplication is happening between two sets of brackets
                            postfixStack.push('*')
                    else:
                        while operationValue<opdict[postfixStack.peek()]: #pops everything with greater precidence
                            pf += f" {postfixStack.pop()}"
                        if operationValue == opdict[postfixStack.peek()]: #pop-push for equal precidence (NEED TO IMPLEMENT FOR PARENTHESIS)
                            pf += f" {postfixStack.pop()}"
                            postfixStack.push(item) 
                        else: #if its greater than just push on top of stack
                            postfixStack.push(item)            
        else:
            return None

        #Empty everything else in the stack and put it at the end of pf
        while postfixStack.isEmpty() == False:
            pf += f" {postfixStack.pop()}"                   

        pf = pf.strip()
        return pf







    def isValidInput(self, txt, opdict,lst):
        s = Stack()
        validP = True
        is_open = {'(': 1, '[': 2, '{': 3, '<': 4}
        is_close = {')': 1, ']': 2, '}': 3, '>': 4}
        size = len(txt)
        i = 0
        #check for balanced parenthesis
        while validP and i < size:
            current = txt[i]
            if current in is_open:
              s.push(current)
            elif current in is_close:
              if s.isEmpty():
                validP = False
              else:
                top_parenthesis = s.pop()
                validP = is_open[top_parenthesis] == is_close[current]
            i += 1
        validP = s.isEmpty() and validP

        #check for unsupported operators
        validOp = True
        for index in range(len(lst)):
            item = lst[index]
            if item not in opdict and self._isNumber(item)==False: #Invalid Operation Check
                validOp = False
            if index != len(lst)-1 and self._isNumber(item)==True and self._isNumber(lst[index+1])==True: #checks for nums next to eachother
                validOp = False
            if item in opdict and opdict[item]>0 and index != len(lst)-1:
                if lst[index+1] in opdict and opdict[lst[index+1]]>4 and opdict[lst[index+1]]<7: #checks for invalid ops next to eachother
                    validOp = False

        if lst[len(lst)-1] in opdict and opdict[lst[len(lst)-1]]>=0: #checks if the last item is an invalid op
            validOp = False

        if validP == False or validOp == False:
            return False
        else:
            return True
        








    @property
    def calculate(self):
        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None

        calcStack = Stack()   #use calcStack to compute the  expression
        pf = self._getPostfix(self.getExpr)
        if pf == None:
            return None
        lst = pf.split(" ")
        num1 = None
        num2 = None
        result = None
        for item in lst:
            if self._isNumber(item):
                calcStack.push(item)
            else:
                num1 = float(calcStack.pop())
                num2 = float(calcStack.pop())
                if item == "*":
                    result = num1 * num2
                elif item == "/":
                    result = num2/num1
                elif item == "+":
                    result = num1 + num2
                elif item == "-":
                    result = num2-num1
                elif item == "^":
                    result = num2 ** num1
                calcStack.push(result)

        return calcStack.pop()

        
        
class AdvancedCalculator:
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        return word[0].isalpha() and word.isalnum()
       

    def _replaceVariables(self, expr):
        lst = expr.split(" ")
        for i in range(len(lst)):
            item = lst[i]
            if self._isVariable(item):
                if item in self.states:
                    lst[i] = str(self.states[item])
                else:
                    return None
        return " ".join(lst)

        
    
    def calculateExpressions(self):
        self.states = {} 
        d = {}
        calcObj = Calculator()     #use calcObj to compute each expression
        lst = self.expressions.split(";")
        for item in lst:
            itemlst = item.split("=")
            if len(itemlst)==2:
                var = itemlst[0].strip()
                expr = itemlst[1].strip()
                exprRep = self._replaceVariables(expr)
                if exprRep == None:
                    self.states = {}
                    return None
                calcObj.setExpr(exprRep)
                self.states[var] = float(calcObj.calculate)
                d[item] = self.states.copy()
            elif "return" in item:
                expr = item.split("return")[1].strip()
                exprRep = self._replaceVariables(expr)
                if exprRep == None:
                    self.states = {}
                    return None
                calcObj.setExpr(exprRep)
                d["_return_"]= float(calcObj.calculate)


        return d


















