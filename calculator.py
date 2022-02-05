import numpy as np

def simultaneousEq(x1,y1,c1,x2,y2,c2):
  A=np.array([[x1,y1],[x2,y2]],dtype=np.float)
  B=np.array([c1,c2],dtype=np.float)
  print(A,B)
  C=np.linalg.solve(A,B)
  return (C)

def quadraticEq(A,B,C):
  coeff=np.array([A,B,C])
  roots=np.roots(coeff)
  return(roots)