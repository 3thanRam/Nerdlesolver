numbs=set("0123456789")
operators=set("+-/*=")

def safe_eval(expr):
    try:
        # Evaluate the expression to see if it's mathematically correct
        return eval(expr, {"__builtins__": None}, {"abs": abs, "int": int, "float": float})
    except:# Raises an exception if the expression is invalid
        return None


def validateeq(equation):
    """tests to see if an equation is valid.
    First tests if there is a left and right part.
    Then if each part is a valid expression.
    Finally if they are equal

    Args:
        equation (list[str]): equation as list of characters

    Returns:
        bool: validity of an equation
    """
    eqsplit="".join(equation).split("=")
    if len(eqsplit)!=2:
        return False
    left,right=eqsplit
    if any(op in right for op in operators):
        return False
    leftres=safe_eval(left)
    rightres=safe_eval(right)
    return (leftres) and (rightres) and (float(leftres)==float(rightres))
    

    
    
def testconfig(testequation,vals):
    
    equ=testequation.copy()
    count=0
    
    for ic,char in enumerate(testequation):
        if char=="?":
            equ[ic]=vals[count]
            count+=1
    return validateeq(equ)
