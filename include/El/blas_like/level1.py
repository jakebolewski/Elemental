#
#  Copyright (c) 2009-2015, Jack Poulson
#  All rights reserved.
#
#  This file is part of Elemental and is under the BSD 2-Clause License, 
#  which can be found in the LICENSE file in the root directory, or at 
#  http://opensource.org/licenses/BSD-2-Clause
#
from ..core import *

from ctypes import CFUNCTYPE

# BLAS 1
# ======

# Axpy
# ----
lib.ElAxpy_i.argtypes = \
lib.ElAxpyDist_i.argtypes = \
lib.ElAxpySparse_i.argtypes = \
lib.ElAxpyDistSparse_i.argtypes = \
lib.ElAxpyDistMultiVec_i.argtypes = \
  [iType,c_void_p,c_void_p]

lib.ElAxpy_s.argtypes = \
lib.ElAxpyDist_s.argtypes = \
lib.ElAxpySparse_s.argtypes = \
lib.ElAxpyDistSparse_s.argtypes = \
lib.ElAxpyDistMultiVec_s.argtypes = \
  [sType,c_void_p,c_void_p]

lib.ElAxpy_d.argtypes = \
lib.ElAxpyDist_d.argtypes = \
lib.ElAxpySparse_d.argtypes = \
lib.ElAxpyDistSparse_d.argtypes = \
lib.ElAxpyDistMultiVec_d.argtypes = \
  [dType,c_void_p,c_void_p]

lib.ElAxpy_c.argtypes = \
lib.ElAxpyDist_c.argtypes = \
lib.ElAxpySparse_c.argtypes = \
lib.ElAxpyDistSparse_c.argtypes = \
lib.ElAxpyDistMultiVec_c.argtypes = \
  [cType,c_void_p,c_void_p]

lib.ElAxpy_z.argtypes = \
lib.ElAxpyDist_z.argtypes = \
lib.ElAxpySparse_z.argtypes = \
lib.ElAxpyDistSparse_z.argtypes = \
lib.ElAxpyDistMultiVec_z.argtypes = \
  [zType,c_void_p,c_void_p]

def Axpy(alphaPre,X,Y):
  if type(X) is not type(Y): raise Exception('Types of X and Y must match')
  if X.tag != Y.tag: raise Exception('Datatypes of X and Y must match')
  alpha = TagToType(X.tag)(alphaPre)
  args = [alpha,X.obj,Y.obj]
  if type(X) is Matrix:
    if   X.tag == iTag: lib.ElAxpy_i(*args)
    elif X.tag == sTag: lib.ElAxpy_s(*args)
    elif X.tag == dTag: lib.ElAxpy_d(*args)
    elif X.tag == cTag: lib.ElAxpy_c(*args)
    elif X.tag == zTag: lib.ElAxpy_z(*args)
    else: DataExcept()
  elif type(X) is DistMatrix:
    if   X.tag == iTag: lib.ElAxpyDist_i(*args)
    elif X.tag == sTag: lib.ElAxpyDist_s(*args)
    elif X.tag == dTag: lib.ElAxpyDist_d(*args)
    elif X.tag == cTag: lib.ElAxpyDist_c(*args)
    elif X.tag == zTag: lib.ElAxpyDist_z(*args)
    else: DataExcept()
  elif type(X) is SparseMatrix:
    if   X.tag == iTag: lib.ElAxpySparse_i(*args)
    elif X.tag == sTag: lib.ElAxpySparse_s(*args)
    elif X.tag == dTag: lib.ElAxpySparse_d(*args)
    elif X.tag == cTag: lib.ElAxpySparse_c(*args)
    elif X.tag == zTag: lib.ElAxpySparse_z(*args)
    else: DataExcept()
  elif type(X) is DistSparseMatrix:
    if   X.tag == iTag: lib.ElAxpyDistSparse_i(*args)
    elif X.tag == sTag: lib.ElAxpyDistSparse_s(*args)
    elif X.tag == dTag: lib.ElAxpyDistSparse_d(*args)
    elif X.tag == cTag: lib.ElAxpyDistSparse_c(*args)
    elif X.tag == zTag: lib.ElAxpyDistSparse_z(*args)
    else: DataExcept()
  elif type(X) is DistMultiVec:
    if   X.tag == iTag: lib.ElAxpyDistMultiVec_i(*args)
    elif X.tag == sTag: lib.ElAxpyDistMultiVec_s(*args)
    elif X.tag == dTag: lib.ElAxpyDistMultiVec_d(*args)
    elif X.tag == cTag: lib.ElAxpyDistMultiVec_c(*args)
    elif X.tag == zTag: lib.ElAxpyDistMultiVec_z(*args)
    else: DataExcept()
  else: TypeExcept()

# AxpyTrapezoid
# -------------
lib.ElAxpyTrapezoid_i.argtypes = \
lib.ElAxpyTrapezoidDist_i.argtypes = \
lib.ElAxpyTrapezoidSparse_i.argtypes = \
lib.ElAxpyTrapezoidDistSparse_i.argtypes = \
  [c_uint,iType,c_void_p,c_void_p,iType]

lib.ElAxpyTrapezoid_s.argtypes = \
lib.ElAxpyTrapezoidDist_s.argtypes = \
lib.ElAxpyTrapezoidSparse_s.argtypes = \
lib.ElAxpyTrapezoidDistSparse_s.argtypes = \
  [c_uint,sType,c_void_p,c_void_p,iType]

lib.ElAxpyTrapezoid_d.argtypes = \
lib.ElAxpyTrapezoidDist_d.argtypes = \
lib.ElAxpyTrapezoidSparse_d.argtypes = \
lib.ElAxpyTrapezoidDistSparse_d.argtypes = \
  [c_uint,dType,c_void_p,c_void_p,iType]

lib.ElAxpyTrapezoid_c.argtypes = \
lib.ElAxpyTrapezoidDist_c.argtypes = \
lib.ElAxpyTrapezoidSparse_c.argtypes = \
lib.ElAxpyTrapezoidDistSparse_c.argtypes = \
  [c_uint,cType,c_void_p,c_void_p,iType]

lib.ElAxpyTrapezoid_z.argtypes = \
lib.ElAxpyTrapezoidDist_z.argtypes = \
lib.ElAxpyTrapezoidSparse_z.argtypes = \
lib.ElAxpyTrapezoidDistSparse_z.argtypes = \
  [c_uint,zType,c_void_p,c_void_p,iType]

def AxpyTriangle(uplo,alphaPre,X,Y,offset=0):
  if type(X) is not type(Y): raise Exception('Types of X and Y must match')
  if X.tag != Y.tag: raise Exception('Datatypes of X and Y must match')
  alpha = TagToType(X.tag)(alphaPre)
  args = [uplo,alpha,X.obj,Y.obj,offset]
  if type(X) is Matrix:
    if   X.tag == iTag: lib.ElAxpyTriangle_i(*args)
    elif X.tag == sTag: lib.ElAxpyTriangle_s(*args)
    elif X.tag == dTag: lib.ElAxpyTriangle_d(*args)
    elif X.tag == cTag: lib.ElAxpyTriangle_c(*args)
    elif X.tag == zTag: lib.ElAxpyTriangle_z(*args)
    else: DataExcept()
  elif type(X) is DistMatrix:
    if   X.tag == iTag: lib.ElAxpyTriangleDist_i(*args)
    elif X.tag == sTag: lib.ElAxpyTriangleDist_s(*args)
    elif X.tag == dTag: lib.ElAxpyTriangleDist_d(*args)
    elif X.tag == cTag: lib.ElAxpyTriangleDist_c(*args)
    elif X.tag == zTag: lib.ElAxpyTriangleDist_z(*args)
    else: DataExcept()
  elif type(X) is SparseMatrix:
    if   X.tag == iTag: lib.ElAxpyTriangleSparse_i(*args)
    elif X.tag == sTag: lib.ElAxpyTriangleSparse_s(*args)
    elif X.tag == dTag: lib.ElAxpyTriangleSparse_d(*args)
    elif X.tag == cTag: lib.ElAxpyTriangleSparse_c(*args)
    elif X.tag == zTag: lib.ElAxpyTriangleSparse_z(*args)
    else: DataExcept()
  elif type(X) is DistSparseMatrix:
    if   X.tag == iTag: lib.ElAxpyTriangleDistSparse_i(*args)
    elif X.tag == sTag: lib.ElAxpyTriangleDistSparse_s(*args)
    elif X.tag == dTag: lib.ElAxpyTriangleDistSparse_d(*args)
    elif X.tag == cTag: lib.ElAxpyTriangleDistSparse_c(*args)
    elif X.tag == zTag: lib.ElAxpyTriangleDistSparse_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Column norms
# ------------
lib.ElColumnNormsDistMultiVec_s.argtypes = \
lib.ElColumnNormsDistMultiVec_d.argtypes = \
lib.ElColumnNormsDistMultiVec_c.argtypes = \
lib.ElColumnNormsDistMultiVec_z.argtypes = \
  [c_void_p,c_void_p]

def ColumnNorms(A):
  if type(A) is DistMultiVec:
    norms = Matrix(TagToType(Base(A.tag)))
    args = [A.obj,norms.obj]
    if   A.tag == sTag: lib.ElColumnNormsDistMultiVec_s(*args)
    elif A.tag == dTag: lib.ElColumnNormsDistMultiVec_d(*args)
    elif A.tag == cTag: lib.ElColumnNormsDistMultiVec_c(*args)
    elif A.tag == zTag: lib.ElColumnNormsDistMultiVec_z(*args)
    else: DataExcept()
    return norms
  else: TypeExcept()

# Concatenation
# -------------

# Horizontal concatenation
# ^^^^^^^^^^^^^^^^^^^^^^^^
lib.ElHCat_i.argtypes = \
lib.ElHCat_s.argtypes = \
lib.ElHCat_d.argtypes = \
lib.ElHCat_c.argtypes = \
lib.ElHCat_z.argtypes = \
lib.ElHCatDist_i.argtypes = \
lib.ElHCatDist_s.argtypes = \
lib.ElHCatDist_d.argtypes = \
lib.ElHCatDist_c.argtypes = \
lib.ElHCatDist_z.argtypes = \
lib.ElHCatSparse_i.argtypes = \
lib.ElHCatSparse_s.argtypes = \
lib.ElHCatSparse_d.argtypes = \
lib.ElHCatSparse_c.argtypes = \
lib.ElHCatSparse_z.argtypes = \
lib.ElHCatDistSparse_i.argtypes = \
lib.ElHCatDistSparse_s.argtypes = \
lib.ElHCatDistSparse_d.argtypes = \
lib.ElHCatDistSparse_c.argtypes = \
lib.ElHCatDistSparse_z.argtypes = \
lib.ElHCatDistMultiVec_i.argtypes = \
lib.ElHCatDistMultiVec_s.argtypes = \
lib.ElHCatDistMultiVec_d.argtypes = \
lib.ElHCatDistMultiVec_c.argtypes = \
lib.ElHCatDistMultiVec_z.argtypes = \
  [c_void_p,c_void_p,c_void_p]

def HCat(A,B):
  if type(A) is not type(B):
    raise Exception('Types of A and B must match')
  if A.tag != B.tag:
    raise Exception('Datatype of A and B must match')
  if type(A) is Matrix:
    C = Matrix(A.tag)
    args = [A.obj,B.obj,C.obj]
    if   A.tag == iTag: lib.ElHCat_i(*args)
    elif A.tag == sTag: lib.ElHCat_s(*args)
    elif A.tag == dTag: lib.ElHCat_d(*args)
    elif A.tag == cTag: lib.ElHCat_c(*args)
    elif A.tag == zTag: lib.ElHCat_z(*args)
    else: DataExcept()
    return C
  elif type(A) is DistMatrix:
    C = DistMatrix(A.tag,MC,MR,A.Grid())
    args = [A.obj,B.obj,C.obj]
    if   A.tag == iTag: lib.ElHCatDist_i(*args)
    elif A.tag == sTag: lib.ElHCatDist_s(*args)
    elif A.tag == dTag: lib.ElHCatDist_d(*args)
    elif A.tag == cTag: lib.ElHCatDist_c(*args)
    elif A.tag == zTag: lib.ElHCatDist_z(*args)
    else: DataExcept()
    return C
  elif type(A) is SparseMatrix: 
    C = SparseMatrix(A.tag)
    args = [A.obj,B.obj,C.obj]
    if   A.tag == iTag: lib.ElHCatSparse_i(*args)
    elif A.tag == sTag: lib.ElHCatSparse_s(*args)
    elif A.tag == dTag: lib.ElHCatSparse_d(*args)
    elif A.tag == cTag: lib.ElHCatSparse_c(*args)
    elif A.tag == zTag: lib.ElHCatSparse_z(*args)
    else: DataExcept()
    return C
  elif type(A) is DistSparseMatrix:
    C = DistSparseMatrix(A.tag,A.Comm())
    args = [A.obj,B.obj,C.obj]
    if   A.tag == iTag: lib.ElHCatDistSparse_i(*args)
    elif A.tag == sTag: lib.ElHCatDistSparse_s(*args)
    elif A.tag == dTag: lib.ElHCatDistSparse_d(*args)
    elif A.tag == cTag: lib.ElHCatDistSparse_c(*args)
    elif A.tag == zTag: lib.ElHCatDistSparse_z(*args)
    else: DataExcept()
    return C
  elif type(A) is DistMultiVec:
    C = DistMultiVec(A.tag,A.Comm())
    args = [A.obj,B.obj,C.obj]
    if   A.tag == iTag: lib.ElHCatDistMultiVec_i(*args)
    elif A.tag == sTag: lib.ElHCatDistMultiVec_s(*args)
    elif A.tag == dTag: lib.ElHCatDistMultiVec_d(*args)
    elif A.tag == cTag: lib.ElHCatDistMultiVec_c(*args)
    elif A.tag == zTag: lib.ElHCatDistMultiVec_z(*args)
    else: DataExcept()
    return C
  else: TypeExcept()

# Vertical concatenation
# ^^^^^^^^^^^^^^^^^^^^^^
lib.ElVCat_i.argtypes = \
lib.ElVCat_s.argtypes = \
lib.ElVCat_d.argtypes = \
lib.ElVCat_c.argtypes = \
lib.ElVCat_z.argtypes = \
lib.ElVCatDist_i.argtypes = \
lib.ElVCatDist_s.argtypes = \
lib.ElVCatDist_d.argtypes = \
lib.ElVCatDist_c.argtypes = \
lib.ElVCatDist_z.argtypes = \
lib.ElVCatSparse_i.argtypes = \
lib.ElVCatSparse_s.argtypes = \
lib.ElVCatSparse_d.argtypes = \
lib.ElVCatSparse_c.argtypes = \
lib.ElVCatSparse_z.argtypes = \
lib.ElVCatDistSparse_i.argtypes = \
lib.ElVCatDistSparse_s.argtypes = \
lib.ElVCatDistSparse_d.argtypes = \
lib.ElVCatDistSparse_c.argtypes = \
lib.ElVCatDistSparse_z.argtypes = \
lib.ElVCatDistMultiVec_i.argtypes = \
lib.ElVCatDistMultiVec_s.argtypes = \
lib.ElVCatDistMultiVec_d.argtypes = \
lib.ElVCatDistMultiVec_c.argtypes = \
lib.ElVCatDistMultiVec_z.argtypes = \
  [c_void_p,c_void_p,c_void_p]

def VCat(A,B):
  if type(A) is not type(B):
    raise Exception('Types of A and B must match')
  if A.tag != B.tag:
    raise Exception('Datatype of A and B must match')
  if type(A) is Matrix:
    C = Matrix(A.tag)
    args = [A.obj,B.obj,C.obj]
    if   A.tag == iTag: lib.ElVCat_i(*args)
    elif A.tag == sTag: lib.ElVCat_s(*args)
    elif A.tag == dTag: lib.ElVCat_d(*args)
    elif A.tag == cTag: lib.ElVCat_c(*args)
    elif A.tag == zTag: lib.ElVCat_z(*args)
    else: DataExcept()
    return C
  elif type(A) is DistMatrix:
    C = DistMatrix(A.tag,MC,MR,A.Grid())
    args = [A.obj,B.obj,C.obj]
    if   A.tag == iTag: lib.ElVCatDist_i(*args)
    elif A.tag == sTag: lib.ElVCatDist_s(*args)
    elif A.tag == dTag: lib.ElVCatDist_d(*args)
    elif A.tag == cTag: lib.ElVCatDist_c(*args)
    elif A.tag == zTag: lib.ElVCatDist_z(*args)
    else: DataExcept()
    return C
  elif type(A) is SparseMatrix: 
    C = SparseMatrix(A.tag)
    args = [A.obj,B.obj,C.obj]
    if   A.tag == iTag: lib.ElVCatSparse_i(*args)
    elif A.tag == sTag: lib.ElVCatSparse_s(*args)
    elif A.tag == dTag: lib.ElVCatSparse_d(*args)
    elif A.tag == cTag: lib.ElVCatSparse_c(*args)
    elif A.tag == zTag: lib.ElVCatSparse_z(*args)
    else: DataExcept()
    return C
  elif type(A) is DistSparseMatrix:
    C = DistSparseMatrix(A.tag,A.Comm())
    args = [A.obj,B.obj,C.obj]
    if   A.tag == iTag: lib.ElVCatDistSparse_i(*args)
    elif A.tag == sTag: lib.ElVCatDistSparse_s(*args)
    elif A.tag == dTag: lib.ElVCatDistSparse_d(*args)
    elif A.tag == cTag: lib.ElVCatDistSparse_c(*args)
    elif A.tag == zTag: lib.ElVCatDistSparse_z(*args)
    else: DataExcept()
    return C
  elif type(A) is DistMultiVec:
    C = DistMultiVec(A.tag,A.Comm())
    args = [A.obj,B.obj,C.obj]
    if   A.tag == iTag: lib.ElVCatDistMultiVec_i(*args)
    elif A.tag == sTag: lib.ElVCatDistMultiVec_s(*args)
    elif A.tag == dTag: lib.ElVCatDistMultiVec_d(*args)
    elif A.tag == cTag: lib.ElVCatDistMultiVec_c(*args)
    elif A.tag == zTag: lib.ElVCatDistMultiVec_z(*args)
    else: DataExcept()
    return C
  else: TypeExcept()

# Conjugate
# ---------
lib.ElConjugate_c.argtypes = \
lib.ElConjugate_z.argtypes = \
lib.ElConjugateDist_c.argtypes = \
lib.ElConjugateDist_z.argtypes = \
  [c_void_p]

def Conjugate(A):
  args = [A.obj]
  if type(A) is Matrix:
    if   A.tag == cTag: lib.ElConjugate_c(*args)
    elif A.tag == zTag: lib.ElConjugate_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == cTag: lib.ElConjugateDist_c(*args)
    elif A.tag == zTag: lib.ElConjugateDist_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Copy
# ----
lib.ElCopy_s.argtypes = \
lib.ElCopy_d.argtypes = \
lib.ElCopy_c.argtypes = \
lib.ElCopy_z.argtypes = \
lib.ElCopyDist_s.argtypes = \
lib.ElCopyDist_d.argtypes = \
lib.ElCopyDist_c.argtypes = \
lib.ElCopyDist_z.argtypes = \
lib.ElCopyGraph.argtypes = \
lib.ElCopyDistGraph.argtypes = \
lib.ElCopySparse_i.argtypes = \
lib.ElCopySparse_s.argtypes = \
lib.ElCopySparse_d.argtypes = \
lib.ElCopySparse_c.argtypes = \
lib.ElCopySparse_z.argtypes = \
lib.ElCopySparseToDense_i.argtypes = \
lib.ElCopySparseToDense_s.argtypes = \
lib.ElCopySparseToDense_d.argtypes = \
lib.ElCopySparseToDense_c.argtypes = \
lib.ElCopySparseToDense_z.argtypes = \
lib.ElCopyDistSparse_i.argtypes = \
lib.ElCopyDistSparse_s.argtypes = \
lib.ElCopyDistSparse_d.argtypes = \
lib.ElCopyDistSparse_c.argtypes = \
lib.ElCopyDistSparse_z.argtypes = \
lib.ElCopyDistSparseToDense_i.argtypes = \
lib.ElCopyDistSparseToDense_s.argtypes = \
lib.ElCopyDistSparseToDense_d.argtypes = \
lib.ElCopyDistSparseToDense_c.argtypes = \
lib.ElCopyDistSparseToDense_z.argtypes = \
lib.ElCopyDistMultiVec_i.argtypes = \
lib.ElCopyDistMultiVec_s.argtypes = \
lib.ElCopyDistMultiVec_d.argtypes = \
lib.ElCopyDistMultiVec_c.argtypes = \
lib.ElCopyDistMultiVec_z.argtypes = \
  [c_void_p,c_void_p]

def Copy(A,B):
  if A.tag != B.tag:
    raise Exception('Copying between datatypes is not yet supported in Python')
  args = [A.obj,B.obj]
  if type(A) is Matrix:
    if type(B) is not Matrix:
      raise Exception('Expected B to be a Matrix')
    if   B.tag == iTag: lib.ElCopy_i(*args)
    elif B.tag == sTag: lib.ElCopy_s(*args)
    elif B.tag == dTag: lib.ElCopy_d(*args)
    elif B.tag == cTag: lib.ElCopy_c(*args)
    elif B.tag == zTag: lib.ElCopy_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if type(B) is not DistMatrix:
      raise Exception('Expected B to be a DistMatrix')
    if   B.tag == iTag: lib.ElCopyDist_i(*args)
    elif B.tag == sTag: lib.ElCopyDist_s(*args)
    elif B.tag == dTag: lib.ElCopyDist_d(*args)
    elif B.tag == cTag: lib.ElCopyDist_c(*args)
    elif B.tag == zTag: lib.ElCopyDist_z(*args)
    else: DataExcept()
  elif type(A) is Graph:
    if type(B) is not Graph:
      raise Exception('Expected B to be a Graph')
    lib.ElCopyGraph(*args)
  elif type(A) is DistGraph:
    if type(B) is not DistGraph:
      raise Exception('Expected B to be a DistGraph')
    lib.ElCopyDistGraph(*args)
  elif type(A) is SparseMatrix:
    if type(B) is SparseMatrix:
      if   A.tag == iTag: lib.ElCopySparse_i(*args)
      elif A.tag == sTag: lib.ElCopySparse_s(*args)
      elif A.tag == dTag: lib.ElCopySparse_d(*args)
      elif A.tag == cTag: lib.ElCopySparse_c(*args)
      elif A.tag == zTag: lib.ElCopySparse_z(*args)
      else: DataExcept()
    elif type(B) is Matrix:
      if   A.tag == iTag: lib.ElCopySparseToDense_i(*args)
      elif A.tag == sTag: lib.ElCopySparseToDense_s(*args)
      elif A.tag == dTag: lib.ElCopySparseToDense_d(*args)
      elif A.tag == cTag: lib.ElCopySparseToDense_c(*args)
      elif A.tag == zTag: lib.ElCopySparseToDense_z(*args)
      else: DataExcept()
    else:
      raise Exception('Expected B to be a (Sparse)Matrix')
  elif type(A) is DistSparseMatrix:
    if type(B) is DistSparseMatrix:
      if   A.tag == iTag: lib.ElCopyDistSparse_i(*args)
      elif A.tag == sTag: lib.ElCopyDistSparse_s(*args)
      elif A.tag == dTag: lib.ElCopyDistSparse_d(*args)
      elif A.tag == cTag: lib.ElCopyDistSparse_c(*args)
      elif A.tag == zTag: lib.ElCopyDistSparse_z(*args)
      else: DataExcept()
    elif type(B) is DistMatrix:
      if   A.tag == iTag: lib.ElCopyDistSparseToDense_i(*args)
      elif A.tag == sTag: lib.ElCopyDistSparseToDense_s(*args)
      elif A.tag == dTag: lib.ElCopyDistSparseToDense_d(*args)
      elif A.tag == cTag: lib.ElCopyDistSparseToDense_c(*args)
      elif A.tag == zTag: lib.ElCopyDistSparseToDense_z(*args)
      else: DataExcept()
    else:
      raise Exception('Expected B to be a Dist(Sparse)Matrix')
  elif type(A) is DistMultiVec:
    if type(B) is not DistMultiVec:
      raise Exception('Expected B to be a DistMultiVec')
    if   A.tag == iTag: lib.ElCopyDistMultiVec_i(*args)
    elif A.tag == sTag: lib.ElCopyDistMultiVec_s(*args)
    elif A.tag == dTag: lib.ElCopyDistMultiVec_d(*args)
    elif A.tag == cTag: lib.ElCopyDistMultiVec_c(*args)
    elif A.tag == zTag: lib.ElCopyDistMultiVec_z(*args)
    else: DataExcept()
  else: TypeExcept()

lib.ElCopyGraphFromRoot.argtypes = \
lib.ElCopyMultiVecFromRoot_i.argtypes = \
lib.ElCopyMultiVecFromRoot_s.argtypes = \
lib.ElCopyMultiVecFromRoot_d.argtypes = \
lib.ElCopyMultiVecFromRoot_c.argtypes = \
lib.ElCopyMultiVecFromRoot_z.argtypes = \
  [c_void_p,c_void_p]

def CopyFromRoot(ADist,ASeq):
  args = [ADist.obj,ASeq.obj]
  if type(ADist) is DistGraph:
    if type(ASeq) is not Graph:
      raise Exception("Expected the result to be a Graph")
    lib.ElCopyGraphFromRoot(*args)
  elif type(ADist) is DistSparseMatrix:
    if type(ASeq) is not SparseMatrix:
      raise Exception("Expected the result to be a SparseMatrix")
    if ASeq.tag != ADist.tag:
      raise Exception("Expected the result to be of the same type")
    if   ADist.tag == iTag: lib.ElCopySparseMatrixFromRoot_i(*args)
    elif ADist.tag == sTag: lib.ElCopySparseMatrixFromRoot_s(*args)
    elif ADist.tag == dTag: lib.ElCopySparseMatrixFromRoot_d(*args)
    elif ADist.tag == cTag: lib.ElCopySparseMatrixFromRoot_c(*args)
    elif ADist.tag == zTag: lib.ElCopySparseMatrixFromRoot_z(*args)
    else: DataExcept()
  elif type(ADist) is DistMultiVec:
    if type(ASeq) is not Matrix:
      raise Exception("Expected the result to be a Matrix")
    if ASeq.tag != ADist.tag:
      raise Exception("Expected the result to be of the same type")
    if   ADist.tag == iTag: lib.ElCopyMultiVecFromRoot_i(*args)
    elif ADist.tag == sTag: lib.ElCopyMultiVecFromRoot_s(*args)
    elif ADist.tag == dTag: lib.ElCopyMultiVecFromRoot_d(*args)
    elif ADist.tag == cTag: lib.ElCopyMultiVecFromRoot_c(*args)
    elif ADist.tag == zTag: lib.ElCopyMultiVecFromRoot_z(*args)
    else: DataExcept()
  else: TypeExcept()

lib.ElCopyMultiVecFromNonRoot_i.argtypes = \
lib.ElCopyMultiVecFromNonRoot_s.argtypes = \
lib.ElCopyMultiVecFromNonRoot_d.argtypes = \
lib.ElCopyMultiVecFromNonRoot_c.argtypes = \
lib.ElCopyMultiVecFromNonRoot_z.argtypes = \
lib.ElCopyGraphFromNonRoot.argtypes = \
  [c_void_p,c_int]

def CopyFromNonRoot(ADist,root=0):
  args = [ADist.obj,root]
  if type(ADist) is DistGraph:
    lib.ElCopyGraphFromNonRoot(*args)
  elif type(ADist) is DistSparseMatrix:
    if   ADist.tag == iTag: lib.ElCopySparseMatrixFromNonRoot_i(*args)
    elif ADist.tag == sTag: lib.ElCopySparseMatrixFromNonRoot_s(*args)
    elif ADist.tag == dTag: lib.ElCopySparseMatrixFromNonRoot_d(*args)
    elif ADist.tag == cTag: lib.ElCopySparseMatrixFromNonRoot_c(*args)
    elif ADist.tag == zTag: lib.ElCopySparseMatrixFromNonRoot_z(*args)
    else: DataExcept()
  elif type(ADist) is DistMultiVec:
    if   ADist.tag == iTag: lib.ElCopyMultiVecFromNonRoot_i(*args)
    elif ADist.tag == sTag: lib.ElCopyMultiVecFromNonRoot_s(*args)
    elif ADist.tag == dTag: lib.ElCopyMultiVecFromNonRoot_d(*args)
    elif ADist.tag == cTag: lib.ElCopyMultiVecFromNonRoot_c(*args)
    elif ADist.tag == zTag: lib.ElCopyMultiVecFromNonRoot_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Diagonal scale
# --------------
lib.ElDiagonalScale_i.argtypes = \
lib.ElDiagonalScale_s.argtypes = \
lib.ElDiagonalScale_d.argtypes = \
lib.ElDiagonalScaleDist_i.argtypes = \
lib.ElDiagonalScaleDist_s.argtypes = \
lib.ElDiagonalScaleDist_d.argtypes = \
lib.ElDiagonalScaleSparse_i.argtypes = \
lib.ElDiagonalScaleSparse_s.argtypes = \
lib.ElDiagonalScaleSparse_d.argtypes = \
lib.ElDiagonalScaleDistSparse_i.argtypes = \
lib.ElDiagonalScaleDistSparse_s.argtypes = \
lib.ElDiagonalScaleDistSparse_d.argtypes = \
  [c_uint,c_void_p,c_void_p]

lib.ElDiagonalScale_c.argtypes = \
lib.ElDiagonalScale_z.argtypes = \
lib.ElDiagonalScaleDist_c.argtypes = \
lib.ElDiagonalScaleDist_z.argtypes = \
lib.ElDiagonalScaleSparse_c.argtypes = \
lib.ElDiagonalScaleSparse_z.argtypes = \
lib.ElDiagonalScaleDistSparse_c.argtypes = \
lib.ElDiagonalScaleDistSparse_z.argtypes = \
  [c_uint,c_uint,c_void_p,c_void_p]

def DiagonalScale(side,orient,d,A):
  if d.tag != A.tag: raise Exception('Matrix datatypes must match')
  args = [side,d.obj,A.obj]
  argsCpx = [side,orient,d.obj,A.obj]
  if type(A) is Matrix:
    if type(d) is not Matrix:
      raise Exception('Expected d to be a Matrix')
    if   A.tag == iTag: lib.ElDiagonalScale_i(*args)
    elif A.tag == sTag: lib.ElDiagonalScale_s(*args)
    elif A.tag == dTag: lib.ElDiagonalScale_d(*args)
    elif A.tag == cTag: lib.ElDiagonalScale_c(*argsCpx)
    elif A.tag == zTag: lib.ElDiagonalScale_z(*argsCpx)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if type(d) is not DistMatrix:
      raise Exception('Expected d to be a DistMatrix')
    if   A.tag == iTag: lib.ElDiagonalScaleDist_i(*args)
    elif A.tag == sTag: lib.ElDiagonalScaleDist_s(*args)
    elif A.tag == dTag: lib.ElDiagonalScaleDist_d(*args)
    elif A.tag == cTag: lib.ElDiagonalScaleDist_c(*argsCpx)
    elif A.tag == zTag: lib.ElDiagonalScaleDist_z(*argsCpx)
    else: DataExcept()
  elif type(A) is SparseMatrix:
    if type(d) is not Matrix:
      raise Exception('Expected d to be a Matrix')
    if   A.tag == iTag: lib.ElDiagonalScaleSparse_i(*args)
    elif A.tag == sTag: lib.ElDiagonalScaleSparse_s(*args)
    elif A.tag == dTag: lib.ElDiagonalScaleSparse_d(*args)
    elif A.tag == cTag: lib.ElDiagonalScaleSparse_c(*argsCpx)
    elif A.tag == zTag: lib.ElDiagonalScaleSparse_z(*argsCpx)
    else: DataExcept()
  elif type(A) is DistSparseMatrix:
    if type(d) is not DistMultiVec:
      raise Exception('Expected d to be a DistMultiVec')
    if   A.tag == iTag: lib.ElDiagonalScaleDistSparse_i(*args)
    elif A.tag == sTag: lib.ElDiagonalScaleDistSparse_s(*args)
    elif A.tag == dTag: lib.ElDiagonalScaleDistSparse_d(*args)
    elif A.tag == cTag: lib.ElDiagonalScaleDistSparse_c(*argsCpx)
    elif A.tag == zTag: lib.ElDiagonalScaleDistSparse_z(*argsCpx)
    else: DataExcept()
  else: TypeExcept()

# Diagonal scale trapezoid
# ------------------------
lib.ElDiagonalScaleTrapezoid_i.argtypes = \
lib.ElDiagonalScaleTrapezoid_s.argtypes = \
lib.ElDiagonalScaleTrapezoid_d.argtypes = \
lib.ElDiagonalScaleTrapezoidDist_i.argtypes = \
lib.ElDiagonalScaleTrapezoidDist_s.argtypes = \
lib.ElDiagonalScaleTrapezoidDist_d.argtypes = \
lib.ElDiagonalScaleTrapezoidSparse_i.argtypes = \
lib.ElDiagonalScaleTrapezoidSparse_s.argtypes = \
lib.ElDiagonalScaleTrapezoidSparse_d.argtypes = \
lib.ElDiagonalScaleTrapezoidDistSparse_i.argtypes = \
lib.ElDiagonalScaleTrapezoidDistSparse_s.argtypes = \
lib.ElDiagonalScaleTrapezoidDistSparse_d.argtypes = \
  [c_uint,c_uint,c_void_p,c_void_p,iType]

lib.ElDiagonalScaleTrapezoid_c.argtypes = \
lib.ElDiagonalScaleTrapezoid_z.argtypes = \
lib.ElDiagonalScaleTrapezoidDist_c.argtypes = \
lib.ElDiagonalScaleTrapezoidDist_z.argtypes = \
lib.ElDiagonalScaleTrapezoidSparse_c.argtypes = \
lib.ElDiagonalScaleTrapezoidSparse_z.argtypes = \
lib.ElDiagonalScaleTrapezoidDistSparse_c.argtypes = \
lib.ElDiagonalScaleTrapezoidDistSparse_z.argtypes = \
  [c_uint,c_uint,c_uint,c_void_p,c_void_p,iType]

def DiagonalScaleTrapezoid(side,uplo,orient,d,A,offset=0):
  if d.tag != A.tag: raise Exception('Matrix datatypes must match')
  args = [side,uplo,d.obj,A.obj,offset]
  argsCpx = [side,uplo,orient,d.obj,A.obj,offset]
  if type(A) is Matrix:
    if type(d) is not Matrix:
      raise Exception('Expected d to be a Matrix')
    if   A.tag == iTag: lib.ElDiagonalScaleTrapezoid_i(*args)
    elif A.tag == sTag: lib.ElDiagonalScaleTrapezoid_s(*args)
    elif A.tag == dTag: lib.ElDiagonalScaleTrapezoid_d(*args)
    elif A.tag == cTag: lib.ElDiagonalScaleTrapezoid_c(*argsCpx)
    elif A.tag == zTag: lib.ElDiagonalScaleTrapezoid_z(*argsCpx)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if type(d) is not DistMatrix:
      raise Exception('Expected d to be a DistMatrix')
    if   A.tag == iTag: lib.ElDiagonalScaleTrapezoidDist_i(*args)
    elif A.tag == sTag: lib.ElDiagonalScaleTrapezoidDist_s(*args)
    elif A.tag == dTag: lib.ElDiagonalScaleTrapezoidDist_d(*args)
    elif A.tag == cTag: lib.ElDiagonalScaleTrapezoidDist_c(*argsCpx)
    elif A.tag == zTag: lib.ElDiagonalScaleTrapezoidDist_z(*argsCpx)
    else: DataExcept()
  elif type(A) is SparseMatrix:
    if type(d) is not Matrix:
      raise Exception('Expected d to be a Matrix')
    if   A.tag == iTag: lib.ElDiagonalScaleTrapezoidSparse_i(*args)
    elif A.tag == sTag: lib.ElDiagonalScaleTrapezoidSparse_s(*args)
    elif A.tag == dTag: lib.ElDiagonalScaleTrapezoidSparse_d(*args)
    elif A.tag == cTag: lib.ElDiagonalScaleTrapezoidSparse_c(*argsCpx)
    elif A.tag == zTag: lib.ElDiagonalScaleTrapezoidSparse_z(*argsCpx)
    else: DataExcept()
  elif type(A) is DistSparseMatrix:
    if type(d) is not DistMultiVec:
      raise Exception('Expected d to be a DistMultiVec')
    if   A.tag == iTag: lib.ElDiagonalScaleTrapezoidDistSparse_i(*args)
    elif A.tag == sTag: lib.ElDiagonalScaleTrapezoidDistSparse_s(*args)
    elif A.tag == dTag: lib.ElDiagonalScaleTrapezoidDistSparse_d(*args)
    elif A.tag == cTag: lib.ElDiagonalScaleTrapezoidDistSparse_c(*argsCpx)
    elif A.tag == zTag: lib.ElDiagonalScaleTrapezoidDistSparse_z(*argsCpx)
    else: DataExcept()
  else: TypeExcept()

# Diagonal solve
# --------------
lib.ElDiagonalSolve_s.argtypes = \
lib.ElDiagonalSolve_d.argtypes = \
lib.ElDiagonalSolveDist_s.argtypes = \
lib.ElDiagonalSolveDist_d.argtypes = \
lib.ElDiagonalSolveSparse_s.argtypes = \
lib.ElDiagonalSolveSparse_d.argtypes = \
lib.ElDiagonalSolveDistSparse_s.argtypes = \
lib.ElDiagonalSolveDistSparse_d.argtypes = \
  [c_uint,c_void_p,c_void_p]

lib.ElDiagonalSolve_c.argtypes = \
lib.ElDiagonalSolve_z.argtypes = \
lib.ElDiagonalSolveDist_c.argtypes = \
lib.ElDiagonalSolveDist_z.argtypes = \
lib.ElDiagonalSolveSparse_c.argtypes = \
lib.ElDiagonalSolveSparse_z.argtypes = \
lib.ElDiagonalSolveDistSparse_c.argtypes = \
lib.ElDiagonalSolveDistSparse_z.argtypes = \
  [c_uint,c_uint,c_void_p,c_void_p]

def DiagonalSolve(side,orient,d,A):
  if d.tag != A.tag: raise Exception('Matrix datatypes must match')
  args = [side,d.obj,A.obj]
  argsCpx = [side,orient,d.obj,A.obj]
  if type(A) is Matrix:
    if type(d) is not Matrix:
      raise Exception('Expected d to be a Matrix')
    if   A.tag == sTag: lib.ElDiagonalSolve_s(*args)
    elif A.tag == dTag: lib.ElDiagonalSolve_d(*args)
    elif A.tag == cTag: lib.ElDiagonalSolve_c(*argsCpx)
    elif A.tag == zTag: lib.ElDiagonalSolve_z(*argsCpx)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if type(d) is not DistMatrix:
      raise Exception('Expected d to be a DistMatrix')
    if   A.tag == sTag: lib.ElDiagonalSolveDist_s(*args)
    elif A.tag == dTag: lib.ElDiagonalSolveDist_d(*args)
    elif A.tag == cTag: lib.ElDiagonalSolveDist_c(*argsCpx)
    elif A.tag == zTag: lib.ElDiagonalSolveDist_z(*argsCpx)
    else: DataExcept()
  elif type(A) is SparseMatrix:
    if type(d) is not Matrix:
      raise Exception('Expected d to be a Matrix')
    if   A.tag == sTag: lib.ElDiagonalSolveSparse_s(*args)
    elif A.tag == dTag: lib.ElDiagonalSolveSparse_d(*args)
    elif A.tag == cTag: lib.ElDiagonalSolveSparse_c(*argsCpx)
    elif A.tag == zTag: lib.ElDiagonalSolveSparse_z(*argsCpx)
    else: DataExcept()
  elif type(A) is DistSparseMatrix:
    if type(d) is not DistMultiVec:
      raise Exception('Expected d to be a DistMultiVec')
    if   A.tag == sTag: lib.ElDiagonalSolveDistSparse_s(*args)
    elif A.tag == dTag: lib.ElDiagonalSolveDistSparse_d(*args)
    elif A.tag == cTag: lib.ElDiagonalSolveDistSparse_c(*argsCpx)
    elif A.tag == zTag: lib.ElDiagonalSolveDistSparse_z(*argsCpx)
    else: DataExcept()
  else: TypeExcept()

# Dot
# ---
lib.ElDot_i.argtypes = \
lib.ElDotDist_i.argtypes = \
lib.ElDotDistMultiVec_i.argtypes = \
  [c_void_p,c_void_p,POINTER(iType)]

lib.ElDot_s.argtypes = \
lib.ElDotDist_s.argtypes = \
lib.ElDotDistMultiVec_s.argtypes = \
  [c_void_p,c_void_p,POINTER(sType)]

lib.ElDot_d.argtypes = \
lib.ElDotDist_d.argtypes = \
lib.ElDotDistMultiVec_d.argtypes = \
  [c_void_p,c_void_p,POINTER(dType)]

lib.ElDot_c.argtypes = \
lib.ElDotDist_c.argtypes = \
lib.ElDotDistMultiVec_c.argtypes = \
  [c_void_p,c_void_p,POINTER(cType)]

lib.ElDot_z.argtypes = \
lib.ElDotDist_z.argtypes = \
lib.ElDotDistMultiVec_z.argtypes = \
  [c_void_p,c_void_p,POINTER(zType)]

def Dot(A,B):
  if type(A) is not type(B): raise Exception('Types of A and B must match')
  if A.tag != B.tag: raise Exception('Datatypes of A and B must match')
  prod = TagToType(A.tag)()
  args = [A.obj,B.obj,pointer(prod)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElDot_i(*args) 
    elif A.tag == sTag: lib.ElDot_s(*args)
    elif A.tag == dTag: lib.ElDot_d(*args)
    elif A.tag == cTag: lib.ElDot_c(*args)
    elif A.tag == zTag: lib.ElDot_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElDotDist_i(*args) 
    elif A.tag == sTag: lib.ElDotDist_s(*args)
    elif A.tag == dTag: lib.ElDotDist_d(*args)
    elif A.tag == cTag: lib.ElDotDist_c(*args)
    elif A.tag == zTag: lib.ElDotDist_z(*args)
    else: DataExcept()
  elif type(A) is DistMultiVec:
    if   A.tag == iTag: lib.ElDotDistMultiVec_i(*args) 
    elif A.tag == sTag: lib.ElDotDistMultiVec_s(*args)
    elif A.tag == dTag: lib.ElDotDistMultiVec_d(*args)
    elif A.tag == cTag: lib.ElDotDistMultiVec_c(*args)
    elif A.tag == zTag: lib.ElDotDistMultiVec_z(*args)
    else: DataExcept()
  else: TypeExcept()
  return prod.value

# Dotu
# ----
lib.ElDot_c.argtypes = \
lib.ElDotDist_c.argtypes = \
lib.ElDotDistMultiVec_c.argtypes = \
  [c_void_p,c_void_p,POINTER(cType)]

lib.ElDot_z.argtypes = \
lib.ElDotDist_z.argtypes = \
lib.ElDotDistMultiVec_z.argtypes = \
  [c_void_p,c_void_p,POINTER(zType)]

def Dotu(A,B):
  if type(A) is not type(B): raise Exception('Types of A and B must match')
  if A.tag != B.tag: raise Exception('Datatypes of A and B must match')
  prod = TagToType(A.tag)()
  args = [A.obj,B.obj,pointer(prod)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElDot_i(*args) 
    elif A.tag == sTag: lib.ElDot_s(*args)
    elif A.tag == dTag: lib.ElDot_d(*args)
    elif A.tag == cTag: lib.ElDotu_c(*args)
    elif A.tag == zTag: lib.ElDotu_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElDotDist_i(*args) 
    elif A.tag == sTag: lib.ElDotDist_s(*args)
    elif A.tag == dTag: lib.ElDotDist_d(*args)
    elif A.tag == cTag: lib.ElDotuDist_c(*args)
    elif A.tag == zTag: lib.ElDotuDist_z(*args)
    else: DataExcept()
  elif type(A) is DistMultiVec:
    if   A.tag == iTag: lib.ElDotDistMultiVec_i(*args) 
    elif A.tag == sTag: lib.ElDotDistMultiVec_s(*args)
    elif A.tag == dTag: lib.ElDotDistMultiVec_d(*args)
    elif A.tag == cTag: lib.ElDotuDistMultiVec_c(*args)
    elif A.tag == zTag: lib.ElDotuDistMultiVec_z(*args)
    else: DataExcept()
  else: TypeExcept()
  return prod.value

# Entrywise fill
# --------------
lib.ElEntrywiseFill_i.argtypes = \
lib.ElEntrywiseFillDist_i.argtypes = \
lib.ElEntrywiseFillDistMultiVec_i.argtypes = \
  [c_void_p,CFUNCTYPE(iType)]

lib.ElEntrywiseFill_s.argtypes = \
lib.ElEntrywiseFillDist_s.argtypes = \
lib.ElEntrywiseFillDistMultiVec_s.argtypes = \
  [c_void_p,CFUNCTYPE(sType)]

lib.ElEntrywiseFill_d.argtypes = \
lib.ElEntrywiseFillDist_d.argtypes = \
lib.ElEntrywiseFillDistMultiVec_d.argtypes = \
  [c_void_p,CFUNCTYPE(dType)]

lib.ElEntrywiseFill_c.argtypes = \
lib.ElEntrywiseFillDist_c.argtypes = \
lib.ElEntrywiseFillDistMultiVec_c.argtypes = \
  [c_void_p,CFUNCTYPE(cType)]

lib.ElEntrywiseFill_z.argtypes = \
lib.ElEntrywiseFillDist_z.argtypes = \
lib.ElEntrywiseFillDistMultiVec_z.argtypes = \
  [c_void_p,CFUNCTYPE(zType)]

def EntrywiseFill(A,fill):
  cFill = CFUNCTYPE(TagToType(A.tag))(fill)
  args = [A.obj,cFill]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElEntrywiseFill_i(*args)
    elif A.tag == sTag: lib.ElEntrywiseFill_s(*args)
    elif A.tag == dTag: lib.ElEntrywiseFill_d(*args)
    elif A.tag == cTag: lib.ElEntrywiseFill_c(*args)
    elif A.tag == zTag: lib.ElEntrywiseFill_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElEntrywiseFillDist_i(*args)
    elif A.tag == sTag: lib.ElEntrywiseFillDist_s(*args)
    elif A.tag == dTag: lib.ElEntrywiseFillDist_d(*args)
    elif A.tag == cTag: lib.ElEntrywiseFillDist_c(*args)
    elif A.tag == zTag: lib.ElEntrywiseFillDist_z(*args)
    else: DataExcept()
  elif type(A) is DistMultiVec:
    if   A.tag == iTag: lib.ElEntrywiseFillDistMultiVec_i(*args)
    elif A.tag == sTag: lib.ElEntrywiseFillDistMultiVec_s(*args)
    elif A.tag == dTag: lib.ElEntrywiseFillDistMultiVec_d(*args)
    elif A.tag == cTag: lib.ElEntrywiseFillDistMultiVec_c(*args)
    elif A.tag == zTag: lib.ElEntrywiseFillDistMultiVec_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Entrywise map
# -------------
lib.ElEntrywiseMap_i.argtypes = \
lib.ElEntrywiseMapDist_i.argtypes = \
lib.ElEntrywiseMapSparse_i.argtypes = \
lib.ElEntrywiseMapDistSparse_i.argtypes = \
lib.ElEntrywiseMapDistMultiVec_i.argtypes = \
  [c_void_p,CFUNCTYPE(iType,iType)]

lib.ElEntrywiseMap_s.argtypes = \
lib.ElEntrywiseMapDist_s.argtypes = \
lib.ElEntrywiseMapSparse_s.argtypes = \
lib.ElEntrywiseMapDistSparse_s.argtypes = \
lib.ElEntrywiseMapDistMultiVec_s.argtypes = \
  [c_void_p,CFUNCTYPE(sType,sType)]

lib.ElEntrywiseMap_d.argtypes = \
lib.ElEntrywiseMapDist_d.argtypes = \
lib.ElEntrywiseMapSparse_d.argtypes = \
lib.ElEntrywiseMapDistSparse_d.argtypes = \
lib.ElEntrywiseMapDistMultiVec_d.argtypes = \
  [c_void_p,CFUNCTYPE(dType,dType)]

lib.ElEntrywiseMap_c.argtypes = \
lib.ElEntrywiseMapDist_c.argtypes = \
lib.ElEntrywiseMapSparse_c.argtypes = \
lib.ElEntrywiseMapDistSparse_c.argtypes = \
lib.ElEntrywiseMapDistMultiVec_c.argtypes = \
  [c_void_p,CFUNCTYPE(cType,cType)]

lib.ElEntrywiseMap_z.argtypes = \
lib.ElEntrywiseMapDist_z.argtypes = \
lib.ElEntrywiseMapSparse_z.argtypes = \
lib.ElEntrywiseMapDistSparse_z.argtypes = \
lib.ElEntrywiseMapDistMultiVec_z.argtypes = \
  [c_void_p,CFUNCTYPE(zType,zType)]

def EntrywiseMap(A,mapFunc):
  cMap = CFUNCTYPE(TagToType(A.tag),TagToType(A.tag))(mapFunc)
  args = [A.obj,cMap]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElEntrywiseMap_i(*args)
    elif A.tag == sTag: lib.ElEntrywiseMap_s(*args)
    elif A.tag == dTag: lib.ElEntrywiseMap_d(*args)
    elif A.tag == cTag: lib.ElEntrywiseMap_c(*args)
    elif A.tag == zTag: lib.ElEntrywiseMap_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElEntrywiseMapDist_i(*args)
    elif A.tag == sTag: lib.ElEntrywiseMapDist_s(*args)
    elif A.tag == dTag: lib.ElEntrywiseMapDist_d(*args)
    elif A.tag == cTag: lib.ElEntrywiseMapDist_c(*args)
    elif A.tag == zTag: lib.ElEntrywiseMapDist_z(*args)
    else: DataExcept()
  elif type(A) is SparseMatrix:
    if   A.tag == iTag: lib.ElEntrywiseMapSparse_i(*args)
    elif A.tag == sTag: lib.ElEntrywiseMapSparse_s(*args)
    elif A.tag == dTag: lib.ElEntrywiseMapSparse_d(*args)
    elif A.tag == cTag: lib.ElEntrywiseMapSparse_c(*args)
    elif A.tag == zTag: lib.ElEntrywiseMapSparse_z(*args)
    else: DataExcept()
  elif type(A) is DistSparseMatrix:
    if   A.tag == iTag: lib.ElEntrywiseMapDistSparse_i(*args)
    elif A.tag == sTag: lib.ElEntrywiseMapDistSparse_s(*args)
    elif A.tag == dTag: lib.ElEntrywiseMapDistSparse_d(*args)
    elif A.tag == cTag: lib.ElEntrywiseMapDistSparse_c(*args)
    elif A.tag == zTag: lib.ElEntrywiseMapDistSparse_z(*args)
    else: DataExcept()
  elif type(A) is DistMultiVec:
    if   A.tag == iTag: lib.ElEntrywiseMapDistMultiVec_i(*args)
    elif A.tag == sTag: lib.ElEntrywiseMapDistMultiVec_s(*args)
    elif A.tag == dTag: lib.ElEntrywiseMapDistMultiVec_d(*args)
    elif A.tag == cTag: lib.ElEntrywiseMapDistMultiVec_c(*args)
    elif A.tag == zTag: lib.ElEntrywiseMapDistMultiVec_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Fill
# ----
lib.ElFill_i.argtypes = \
lib.ElFillDist_i.argtypes = \
  [c_void_p,iType]

lib.ElFill_s.argtypes = \
lib.ElFillDist_s.argtypes = \
  [c_void_p,sType]

lib.ElFill_d.argtypes = \
lib.ElFillDist_d.argtypes = \
  [c_void_p,dType]

lib.ElFill_c.argtypes = \
lib.ElFillDist_c.argtypes = \
  [c_void_p,cType]

lib.ElFill_z.argtypes = \
lib.ElFillDist_z.argtypes = \
  [c_void_p,zType]

def Fill(A,alphaPre):
  alpha = TagToType(A.tag)(alphaPre)
  args = [A.obj,alpha]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElFill_i(*args)
    elif A.tag == sTag: lib.ElFill_s(*args)
    elif A.tag == dTag: lib.ElFill_d(*args)
    elif A.tag == cTag: lib.ElFill_c(*args)
    elif A.tag == zTag: lib.ElFill_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElFillDist_i(*args)
    elif A.tag == sTag: lib.ElFillDist_s(*args)
    elif A.tag == dTag: lib.ElFillDist_d(*args)
    elif A.tag == cTag: lib.ElFillDist_c(*args)
    elif A.tag == zTag: lib.ElFillDist_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Fill diagonal
# ------------
lib.ElFillDiagonal_i.argtypes = \
lib.ElFillDiagonalDist_i.argtypes = \
  [c_void_p,iType,iType]

lib.ElFillDiagonal_s.argtypes = \
lib.ElFillDiagonalDist_s.argtypes = \
  [c_void_p,sType,iType]

lib.ElFillDiagonal_d.argtypes = \
lib.ElFillDiagonalDist_d.argtypes = \
  [c_void_p,dType,iType]

lib.ElFillDiagonal_c.argtypes = \
lib.ElFillDiagonalDist_c.argtypes = \
  [c_void_p,cType,iType]

lib.ElFillDiagonal_z.argtypes = \
lib.ElFillDiagonalDist_z.argtypes = \
  [c_void_p,zType,iType]

def FillDiagonal(A,alphaPre,offset=0):
  alpha = TagToType(A.tag)(alphaPre)
  args = [A.obj,alpha,offset]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElFillDiagonal_i(*args)
    elif A.tag == sTag: lib.ElFillDiagonal_s(*args)
    elif A.tag == dTag: lib.ElFillDiagonal_d(*args)
    elif A.tag == cTag: lib.ElFillDiagonal_c(*args)
    elif A.tag == zTag: lib.ElFillDiagonal_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElFillDiagonalDist_i(*args)
    elif A.tag == sTag: lib.ElFillDiagonalDist_s(*args)
    elif A.tag == dTag: lib.ElFillDiagonalDist_d(*args)
    elif A.tag == cTag: lib.ElFillDiagonalDist_c(*args)
    elif A.tag == zTag: lib.ElFillDiagonalDist_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Full
# ----
lib.ElFull_i.argtypes = \
lib.ElFull_s.argtypes = \
lib.ElFull_d.argtypes = \
lib.ElFull_c.argtypes = \
lib.ElFull_z.argtypes = \
lib.ElFullDist_i.argtypes = \
lib.ElFullDist_s.argtypes = \
lib.ElFullDist_d.argtypes = \
lib.ElFullDist_c.argtypes = \
lib.ElFullDist_z.argtypes = \
  [c_void_p,c_void_p]

def Full(A,B):
  if A.tag != B.tag: 
    raise Exception("Expected A and B to have the same datatype")
  args = [A.obj,B.obj]
  if type(A) is SparseMatrix:
    if type(B) is not Matrix:
      raise Exception("Expected B to be a Matrix")
    if   A.tag == iTag: lib.ElFull_i(*args)
    elif A.tag == sTag: lib.ElFull_s(*args)
    elif A.tag == dTag: lib.ElFull_d(*args)
    elif A.tag == cTag: lib.ElFull_c(*args)
    elif A.tag == zTag: lib.ElFull_z(*args)
    else: DataExcept()
  elif type(A) is DistSparseMatrix:
    if type(B) is not DistMatrix:
      raise Exception("Expected B to be a DistMatrix")
    if   A.tag == iTag: lib.ElFullDist_i(*args)
    elif A.tag == sTag: lib.ElFullDist_s(*args)
    elif A.tag == dTag: lib.ElFullDist_d(*args)
    elif A.tag == cTag: lib.ElFullDist_c(*args)
    elif A.tag == zTag: lib.ElFullDist_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Get diagonal
# ------------
# TODO

# Get submatrix
# -------------
lib.ElGetSubmatrixSparse_i.argtypes = \
lib.ElGetSubmatrixSparse_s.argtypes = \
lib.ElGetSubmatrixSparse_d.argtypes = \
lib.ElGetSubmatrixSparse_c.argtypes = \
lib.ElGetSubmatrixSparse_z.argtypes = \
lib.ElGetSubmatrixDistSparse_i.argtypes = \
lib.ElGetSubmatrixDistSparse_s.argtypes = \
lib.ElGetSubmatrixDistSparse_d.argtypes = \
lib.ElGetSubmatrixDistSparse_c.argtypes = \
lib.ElGetSubmatrixDistSparse_z.argtypes = \
lib.ElGetSubmatrixDistMultiVec_i.argtypes = \
lib.ElGetSubmatrixDistMultiVec_s.argtypes = \
lib.ElGetSubmatrixDistMultiVec_d.argtypes = \
lib.ElGetSubmatrixDistMultiVec_c.argtypes = \
lib.ElGetSubmatrixDistMultiVec_z.argtypes = \
  [c_void_p,IndexRange,IndexRange,c_void_p]

def GetSubmatrix(A,I,J):
  if type(A) is SparseMatrix:
    ASub = SparseMatrix(A.tag)
    args = [A.obj,I,J,ASub.obj]
    if   A.tag == iTag: lib.ElGetSubmatrixSparse_i(*args)
    elif A.tag == sTag: lib.ElGetSubmatrixSparse_s(*args)
    elif A.tag == dTag: lib.ElGetSubmatrixSparse_d(*args)
    elif A.tag == cTag: lib.ElGetSubmatrixSparse_c(*args)
    elif A.tag == zTag: lib.ElGetSubmatrixSparse_z(*args)
    else: DataExcept()
    return ASub
  elif type(A) is DistSparseMatrix:
    ASub = DistSparseMatrix(A.tag,A.Comm())
    args = [A.obj,I,J,ASub.obj]
    if   A.tag == iTag: lib.ElGetSubmatrixDistSparse_i(*args)
    elif A.tag == sTag: lib.ElGetSubmatrixDistSparse_s(*args)
    elif A.tag == dTag: lib.ElGetSubmatrixDistSparse_d(*args)
    elif A.tag == cTag: lib.ElGetSubmatrixDistSparse_c(*args)
    elif A.tag == zTag: lib.ElGetSubmatrixDistSparse_z(*args)
    else: DataExcept()
    return ASub
  elif type(A) is DistMultiVec:
    ASub = DistMultiVec(A.tag,A.Comm())
    args = [A.obj,I,J,ASub.obj]
    if   A.tag == iTag: lib.ElGetSubmatrixDistMultiVec_i(*args)
    elif A.tag == sTag: lib.ElGetSubmatrixDistMultiVec_s(*args)
    elif A.tag == dTag: lib.ElGetSubmatrixDistMultiVec_d(*args)
    elif A.tag == cTag: lib.ElGetSubmatrixDistMultiVec_c(*args)
    elif A.tag == zTag: lib.ElGetSubmatrixDistMultiVec_z(*args)
    else: DataExcept()
    return ASub
  else: TypeExcept()

# Hadamard
# --------
lib.ElHadamard_i.argtypes = \
lib.ElHadamard_s.argtypes = \
lib.ElHadamard_d.argtypes = \
lib.ElHadamard_c.argtypes = \
lib.ElHadamard_z.argtypes = \
lib.ElHadamardDist_i.argtypes = \
lib.ElHadamardDist_s.argtypes = \
lib.ElHadamardDist_d.argtypes = \
lib.ElHadamardDist_c.argtypes = \
lib.ElHadamardDist_z.argtypes = \
  [c_void_p,c_void_p,c_void_p]

def Hadamard(A,B,C):
  if type(A) is not type(B) or type(B) is not type(C):
    raise Exception('Matrix types must match')
  if A.tag != B.tag or B.tag != C.tag:
    raise Exception('Matrix datatypes must match')
  args = [A.obj,B.obj,C.obj]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElHadamard_i(*args)
    elif A.tag == sTag: lib.ElHadamard_s(*args)
    elif A.tag == dTag: lib.ElHadamard_d(*args)
    elif A.tag == cTag: lib.ElHadamard_c(*args)
    elif A.tag == zTag: lib.ElHadamard_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElHadamardDist_i(*args)
    elif A.tag == sTag: lib.ElHadamardDist_s(*args)
    elif A.tag == dTag: lib.ElHadamardDist_d(*args)
    elif A.tag == cTag: lib.ElHadamardDist_c(*args)
    elif A.tag == zTag: lib.ElHadamardDist_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Hilbert-Schmidt
# ---------------
lib.ElHilbertSchmidt_i.argtypes = \
lib.ElHilbertSchmidtDist_i.argtypes = \
lib.ElHilbertSchmidtDistMultiVec_i.argtypes = \
  [c_void_p,c_void_p,POINTER(iType)]

lib.ElHilbertSchmidt_s.argtypes = \
lib.ElHilbertSchmidtDist_s.argtypes = \
lib.ElHilbertSchmidtDistMultiVec_s.argtypes = \
  [c_void_p,c_void_p,POINTER(sType)]

lib.ElHilbertSchmidt_d.argtypes = \
lib.ElHilbertSchmidtDist_d.argtypes = \
lib.ElHilbertSchmidtDistMultiVec_d.argtypes = \
  [c_void_p,c_void_p,POINTER(dType)]

lib.ElHilbertSchmidt_c.argtypes = \
lib.ElHilbertSchmidtDist_c.argtypes = \
lib.ElHilbertSchmidtDistMultiVec_c.argtypes = \
  [c_void_p,c_void_p,POINTER(cType)]

lib.ElHilbertSchmidt_z.argtypes = \
lib.ElHilbertSchmidtDist_z.argtypes = \
lib.ElHilbertSchmidtDistMultiVec_z.argtypes = \
  [c_void_p,c_void_p,POINTER(zType)]

def HilbertSchmidt(A,B):
  if type(A) is type(B): raise Exception('Matrix types must match')
  if A.tag != B.tag: raise Exception('Datatypes must match')
  prod = TagToType(A.tag)()
  args = [A.obj,B.obj,pointer(prod)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElHilbertSchmidt_i(*args)
    elif A.tag == sTag: lib.ElHilbertSchmidt_s(*args)
    elif A.tag == dTag: lib.ElHilbertSchmidt_d(*args)
    elif A.tag == cTag: lib.ElHilbertSchmidt_c(*args)
    elif A.tag == zTag: lib.ElHilbertSchmidt_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElHilbertSchmidtDist_i(*args)
    elif A.tag == sTag: lib.ElHilbertSchmidtDist_s(*args)
    elif A.tag == dTag: lib.ElHilbertSchmidtDist_d(*args)
    elif A.tag == cTag: lib.ElHilbertSchmidtDist_c(*args)
    elif A.tag == zTag: lib.ElHilbertSchmidtDist_z(*args)
    else: DataExcept()
  elif type(A) is DistMultiVec:
    if   A.tag == iTag: lib.ElHilbertSchmidtDistMultiVec_i(*args)
    elif A.tag == sTag: lib.ElHilbertSchmidtDistMultiVec_s(*args)
    elif A.tag == dTag: lib.ElHilbertSchmidtDistMultiVec_d(*args)
    elif A.tag == cTag: lib.ElHilbertSchmidtDistMultiVec_c(*args)
    elif A.tag == zTag: lib.ElHilbertSchmidtDistMultiVec_z(*args)
    else: DataExcept()
  else: TypeExcept()
  return prod.value

# Index dependent fill
# --------------------
lib.ElIndexDependentFill_i.argtypes = \
lib.ElIndexDependentFillDist_i.argtypes = \
  [c_void_p,CFUNCTYPE(iType,iType,iType)]

lib.ElIndexDependentFill_s.argtypes = \
lib.ElIndexDependentFillDist_s.argtypes = \
  [c_void_p,CFUNCTYPE(sType,iType,iType)]

lib.ElIndexDependentFill_d.argtypes = \
lib.ElIndexDependentFillDist_d.argtypes = \
  [c_void_p,CFUNCTYPE(dType,iType,iType)]

lib.ElIndexDependentFill_c.argtypes = \
lib.ElIndexDependentFillDist_c.argtypes = \
  [c_void_p,CFUNCTYPE(cType,iType,iType)]

lib.ElIndexDependentFill_z.argtypes = \
lib.ElIndexDependentFillDist_z.argtypes = \
  [c_void_p,CFUNCTYPE(zType,iType,iType)]

def IndexDependentFill(A,fill):
  cFill = CFUNCTYPE(TagToType(A.tag),iType,iType)(fill)
  args = [A.obj,cFill]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElIndexDependentFill_i(*args)
    elif A.tag == sTag: lib.ElIndexDependentFill_s(*args)
    elif A.tag == dTag: lib.ElIndexDependentFill_d(*args)
    elif A.tag == cTag: lib.ElIndexDependentFill_c(*args)
    elif A.tag == zTag: lib.ElIndexDependentFill_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElIndexDependentFillDist_i(*args)
    elif A.tag == sTag: lib.ElIndexDependentFillDist_s(*args)
    elif A.tag == dTag: lib.ElIndexDependentFillDist_d(*args)
    elif A.tag == cTag: lib.ElIndexDependentFillDist_c(*args)
    elif A.tag == zTag: lib.ElIndexDependentFillDist_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Index dependent map
# -------------------
lib.ElIndexDependentMap_i.argtypes = \
lib.ElIndexDependentMapDist_i.argtypes = \
  [c_void_p,CFUNCTYPE(iType,iType,iType,iType)]

lib.ElIndexDependentMap_s.argtypes = \
lib.ElIndexDependentMapDist_s.argtypes = \
  [c_void_p,CFUNCTYPE(sType,iType,iType,sType)]

lib.ElIndexDependentMap_d.argtypes = \
lib.ElIndexDependentMapDist_d.argtypes = \
  [c_void_p,CFUNCTYPE(dType,iType,iType,dType)]

lib.ElIndexDependentMap_c.argtypes = \
lib.ElIndexDependentMapDist_c.argtypes = \
  [c_void_p,CFUNCTYPE(cType,iType,iType,cType)]

lib.ElIndexDependentMap_z.argtypes = \
lib.ElIndexDependentMapDist_z.argtypes = \
  [c_void_p,CFUNCTYPE(zType,iType,iType,zType)]

def IndexDependentMap(A,mapFunc):
  typeA = TagToType(A)
  cMap = CFUNCTYPE(typeA,iType,iType,typeA)(mapFunc)
  args = [A.obj,cMap]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElIndexDependentMap_i(*args)
    elif A.tag == sTag: lib.ElIndexDependentMap_s(*args)
    elif A.tag == dTag: lib.ElIndexDependentMap_d(*args)
    elif A.tag == cTag: lib.ElIndexDependentMap_c(*args)
    elif A.tag == zTag: lib.ElIndexDependentMap_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElIndexDependentMapDist_i(*args)
    elif A.tag == sTag: lib.ElIndexDependentMapDist_s(*args)
    elif A.tag == dTag: lib.ElIndexDependentMapDist_d(*args)
    elif A.tag == cTag: lib.ElIndexDependentMapDist_c(*args)
    elif A.tag == zTag: lib.ElIndexDependentMapDist_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Kronecker product
# -----------------
lib.ElKronecker_i.argtypes = \
lib.ElKronecker_s.argtypes = \
lib.ElKronecker_d.argtypes = \
lib.ElKronecker_c.argtypes = \
lib.ElKronecker_z.argtypes = \
lib.ElKroneckerDist_i.argtypes = \
lib.ElKroneckerDist_s.argtypes = \
lib.ElKroneckerDist_d.argtypes = \
lib.ElKroneckerDist_c.argtypes = \
lib.ElKroneckerDist_z.argtypes = \
lib.ElKroneckerSparse_i.argtypes = \
lib.ElKroneckerSparse_s.argtypes = \
lib.ElKroneckerSparse_d.argtypes = \
lib.ElKroneckerSparse_c.argtypes = \
lib.ElKroneckerSparse_z.argtypes = \
lib.ElKroneckerDistSparse_i.argtypes = \
lib.ElKroneckerDistSparse_s.argtypes = \
lib.ElKroneckerDistSparse_d.argtypes = \
lib.ElKroneckerDistSparse_c.argtypes = \
lib.ElKroneckerDistSparse_z.argtypes = \
  [c_void_p,c_void_p,c_void_p]

def Kronecker(A,B,C):
  if type(A) is not type(B):
    raise Exception("Python interface assumes type(A) = type(B)")
  if A.tag != B.tag or B.tag != C.tag:
    raise Exception("Matrix datatypes must match")
  args = [A.obj,B.obj,C.obj]
  if type(C) is Matrix:
    if type(A) is not Matrix:
      LogicError("Assumed A and B were of type Matrix")
    if   A.tag == iTag: lib.ElHadamard_i(*args)
    elif A.tag == sTag: lib.ElHadamard_s(*args)
    elif A.tag == dTag: lib.ElHadamard_d(*args)
    elif A.tag == cTag: lib.ElHadamard_c(*args)
    elif A.tag == zTag: lib.ElHadamard_z(*args)
    else: DataExcept()
  elif type(C) is DistMatrix:
    if type(A) is not Matrix:
      LogicError("Assumed A and B were of type Matrix")
    if   A.tag == iTag: lib.ElHadamardDist_i(*args)
    elif A.tag == sTag: lib.ElHadamardDist_s(*args)
    elif A.tag == dTag: lib.ElHadamardDist_d(*args)
    elif A.tag == cTag: lib.ElHadamardDist_c(*args)
    elif A.tag == zTag: lib.ElHadamardDist_z(*args)
    else: DataExcept()
  elif type(C) is SparseMatrix:
    if type(A) is not SparseMatrix:
      LogicError("Assumed A and B were of type SparseMatrix")
    if   A.tag == iTag: lib.ElHadamardSparse_i(*args)
    elif A.tag == sTag: lib.ElHadamardSparse_s(*args)
    elif A.tag == dTag: lib.ElHadamardSparse_d(*args)
    elif A.tag == cTag: lib.ElHadamardSparse_c(*args)
    elif A.tag == zTag: lib.ElHadamardSparse_z(*args)
    else: DataExcept()
  elif type(C) is DistSparseMatrix:
    if type(A) is not SparseMatrix:
      LogicError("Assumed A and B were of type SparseMatrix")
    if   A.tag == iTag: lib.ElHadamardDistSparse_i(*args)
    elif A.tag == sTag: lib.ElHadamardDistSparse_s(*args)
    elif A.tag == dTag: lib.ElHadamardDistSparse_d(*args)
    elif A.tag == cTag: lib.ElHadamardDistSparse_c(*args)
    elif A.tag == zTag: lib.ElHadamardDistSparse_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Make symmetric/Hermitian
# ------------------------
lib.ElMakeSymmetric_i.argtypes = \
lib.ElMakeSymmetric_s.argtypes = \
lib.ElMakeSymmetric_d.argtypes = \
lib.ElMakeSymmetric_c.argtypes = \
lib.ElMakeSymmetric_z.argtypes = \
lib.ElMakeSymmetricDist_i.argtypes = \
lib.ElMakeSymmetricDist_s.argtypes = \
lib.ElMakeSymmetricDist_d.argtypes = \
lib.ElMakeSymmetricDist_c.argtypes = \
lib.ElMakeSymmetricDist_z.argtypes = \
lib.ElMakeSymmetricSparse_i.argtypes = \
lib.ElMakeSymmetricSparse_s.argtypes = \
lib.ElMakeSymmetricSparse_d.argtypes = \
lib.ElMakeSymmetricSparse_c.argtypes = \
lib.ElMakeSymmetricSparse_z.argtypes = \
lib.ElMakeSymmetricDistSparse_i.argtypes = \
lib.ElMakeSymmetricDistSparse_s.argtypes = \
lib.ElMakeSymmetricDistSparse_d.argtypes = \
lib.ElMakeSymmetricDistSparse_c.argtypes = \
lib.ElMakeSymmetricDistSparse_z.argtypes = \
  [c_uint,c_void_p]

lib.ElMakeHermitian_c.argtypes = \
lib.ElMakeHermitian_z.argtypes = \
lib.ElMakeHermitianDist_c.argtypes = \
lib.ElMakeHermitianDist_z.argtypes = \
lib.ElMakeHermitianSparse_c.argtypes = \
lib.ElMakeHermitianSparse_z.argtypes = \
lib.ElMakeHermitianDistSparse_c.argtypes = \
lib.ElMakeHermitianDistSparse_z.argtypes = \
  [c_uint,c_void_p]

def MakeSymmetric(uplo,A,conj=False):
  args = [uplo,A.obj]
  if type(A) is Matrix: 
    if   A.tag == iTag: lib.ElMakeSymmetric_i(*args)
    elif A.tag == sTag: lib.ElMakeSymmetric_s(*args)
    elif A.tag == dTag: lib.ElMakeSymmetric_d(*args)
    elif A.tag == cTag: 
      if conj: lib.ElMakeHermitian_c(*args)
      else:    lib.ElMakeSymmetric_c(*args)
    elif A.tag == zTag: 
      if conj: lib.ElMakeHermitian_z(*args)
      else:    lib.ElMakeSymmetric_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElMakeSymmetricDist_i(*args)
    elif A.tag == sTag: lib.ElMakeSymmetricDist_s(*args)
    elif A.tag == dTag: lib.ElMakeSymmetricDist_d(*args)
    elif A.tag == cTag: 
      if conj: lib.ElMakeHermitianDist_c(*args)
      else:    lib.ElMakeSymmetricDist_c(*args)
    elif A.tag == zTag: 
      if conj: lib.ElMakeHermitianDist_z(*args)
      else:    lib.ElMakeSymmetricDist_z(*args)
    else: DataExcept()
  elif type(A) is SparseMatrix:
    if   A.tag == iTag: lib.ElMakeSymmetricSparse_i(*args)
    elif A.tag == sTag: lib.ElMakeSymmetricSparse_s(*args)
    elif A.tag == dTag: lib.ElMakeSymmetricSparse_d(*args)
    elif A.tag == cTag:
      if conjugate: lib.ElMakeHermitianSparse_c(*args)
      else:         lib.ElMakeHermitianSparse_c(*args)
    elif A.tag == zTag:
      if conjugate: lib.ElMakeHermitianSparse_z(*args)
      else:         lib.ElMakeHermitianSparse_z(*args)
    else: DataExcept()
  elif type(A) is DistSparseMatrix:
    if   A.tag == iTag: lib.ElMakeSymmetricDistSparse_i(*args)
    elif A.tag == sTag: lib.ElMakeSymmetricDistSparse_s(*args)
    elif A.tag == dTag: lib.ElMakeSymmetricDistSparse_d(*args)
    elif A.tag == cTag:
      if conjugate: lib.ElMakeHermitianDistSparse_c(*args)
      else:         lib.ElMakeHermitianDistSparse_c(*args)
    elif A.tag == zTag:
      if conjugate: lib.ElMakeHermitianDistSparse_z(*args)
      else:         lib.ElMakeHermitianDistSparse_z(*args)
    else: DataExcept()
  else: TypeExcept()

def MakeHermitian(uplo,A):
  MakeSymmetric(uplo,A,True)

# Make real
# ---------
lib.ElMakeReal_c.argtypes = \
lib.ElMakeReal_z.argtypes = \
lib.ElMakeRealDist_c.argtypes = \
lib.ElMakeRealDist_z.argtypes = \
  [c_uint,c_void_p]

def MakeReal(uplo,A):
  args = [uplo,A.obj]
  if type(A) is Matrix:
    if   A.tag == cTag: lib.ElMakeReal_c(*args)
    elif A.tag == zTag: lib.ElMakeReal_z(*args)
  elif type(A) is DistMatrix:
    if   A.tag == cTag: lib.ElMakeRealDist_c(*args)
    elif A.tag == zTag: lib.ElMakeRealDist_z(*args)
  else: TypeExcept()

# Make trapezoidal
# ----------------
lib.ElMakeTrapezoidal_i.argtypes = \
lib.ElMakeTrapezoidal_s.argtypes = \
lib.ElMakeTrapezoidal_d.argtypes = \
lib.ElMakeTrapezoidal_c.argtypes = \
lib.ElMakeTrapezoidal_z.argtypes = \
lib.ElMakeTrapezoidalDist_i.argtypes = \
lib.ElMakeTrapezoidalDist_s.argtypes = \
lib.ElMakeTrapezoidalDist_d.argtypes = \
lib.ElMakeTrapezoidalDist_c.argtypes = \
lib.ElMakeTrapezoidalDist_z.argtypes = \
lib.ElMakeTrapezoidalSparse_i.argtypes = \
lib.ElMakeTrapezoidalSparse_s.argtypes = \
lib.ElMakeTrapezoidalSparse_d.argtypes = \
lib.ElMakeTrapezoidalSparse_c.argtypes = \
lib.ElMakeTrapezoidalSparse_z.argtypes = \
  [c_uint,c_void_p,iType]

def MakeTrapezoidal(uplo,A,offset=0):
  args = [uplo,A.obj,offset]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElMakeTrapezoidal_i(*args)
    elif A.tag == sTag: lib.ElMakeTrapezoidal_s(*args)
    elif A.tag == dTag: lib.ElMakeTrapezoidal_d(*args)
    elif A.tag == cTag: lib.ElMakeTrapezoidal_c(*args)
    elif A.tag == zTag: lib.ElMakeTrapezoidal_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElMakeTrapezoidalDist_i(*args)
    elif A.tag == sTag: lib.ElMakeTrapezoidalDist_s(*args)
    elif A.tag == dTag: lib.ElMakeTrapezoidalDist_d(*args)
    elif A.tag == cTag: lib.ElMakeTrapezoidalDist_c(*args)
    elif A.tag == zTag: lib.ElMakeTrapezoidalDist_z(*args)
    else: DataExcept()
  elif type(A) is SparseMatrix:
    if   A.tag == iTag: lib.ElMakeTrapezoidalSparse_i(*args)
    elif A.tag == sTag: lib.ElMakeTrapezoidalSparse_s(*args)
    elif A.tag == dTag: lib.ElMakeTrapezoidalSparse_d(*args)
    elif A.tag == cTag: lib.ElMakeTrapezoidalSparse_c(*args)
    elif A.tag == zTag: lib.ElMakeTrapezoidalSparse_z(*args)
    else: DataExcept()
  elif type(A) is DistSparseMatrix:
    if   A.tag == iTag: lib.ElMakeTrapezoidalDistSparse_i(*args)
    elif A.tag == sTag: lib.ElMakeTrapezoidalDistSparse_s(*args)
    elif A.tag == dTag: lib.ElMakeTrapezoidalDistSparse_d(*args)
    elif A.tag == cTag: lib.ElMakeTrapezoidalDistSparse_c(*args)
    elif A.tag == zTag: lib.ElMakeTrapezoidalDistSparse_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Max
# ---
class ValueInt_i(ctypes.Structure):
  _fields_ = [("value",iType),("index",iType)]
class ValueInt_s(ctypes.Structure):
  _fields_ = [("value",sType),("index",iType)]
class ValueInt_d(ctypes.Structure):
  _fields_ = [("value",dType),("index",iType)]
class ValueInt_c(ctypes.Structure):
  _fields_ = [("value",cType),("index",iType)]
class ValueInt_z(ctypes.Structure):
  _fields_ = [("value",zType),("index",iType)]
def TagToValueInt(tag):
  if   tag == iTag: return ValueInt_i()
  elif tag == sTag: return ValueInt_s()
  elif tag == dTag: return ValueInt_d()
  elif tag == cTag: return ValueInt_c()
  elif tag == zTag: return ValueInt_z()
  else: DataExcept()

class ValueIntPair_i(ctypes.Structure):
  _fields_ = [("value",iType),("indices",(iType*2))]
class ValueIntPair_s(ctypes.Structure):
  _fields_ = [("value",sType),("indices",(iType*2))]
class ValueIntPair_d(ctypes.Structure):
  _fields_ = [("value",dType),("indices",(iType*2))]
class ValueIntPair_c(ctypes.Structure):
  _fields_ = [("value",cType),("indices",(iType*2))]
class ValueIntPair_z(ctypes.Structure):
  _fields_ = [("value",zType),("indices",(iType*2))]
def TagToValueIntPair(tag):
  if   tag == iTag: return ValueIntPair_i()
  elif tag == sTag: return ValueIntPair_s()
  elif tag == dTag: return ValueIntPair_d()
  elif tag == cTag: return ValueIntPair_c()
  elif tag == zTag: return ValueIntPair_z()
  else: DataExcept()

lib.ElMax_i.argtypes = \
lib.ElMaxDist_i.argtypes = \
  [c_void_p,POINTER(ValueIntPair_i)]

lib.ElMax_s.argtypes = \
lib.ElMaxDist_s.argtypes = \
  [c_void_p,POINTER(ValueIntPair_s)]

lib.ElMax_d.argtypes = \
lib.ElMaxDist_d.argtypes = \
  [c_void_p,POINTER(ValueIntPair_d)]

def Max(A):
  pair = TagToValueIntPair(A.tag)
  args = [A.obj,pointer(pair)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElMax_i(*args) 
    elif A.tag == sTag: lib.ElMax_s(*args) 
    elif A.tag == dTag: lib.ElMax_d(*args) 
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElMaxDist_i(*args) 
    elif A.tag == sTag: lib.ElMaxDist_s(*args) 
    elif A.tag == dTag: lib.ElMaxDist_d(*args) 
    else: DataExcept()
  else: TypeExcept()
  return pair.value, pair.indices[0], pair.indices[1]

lib.ElSymmetricMax_i.argtypes = \
lib.ElSymmetricMaxDist_i.argtypes = \
  [c_uint,c_void_p,POINTER(ValueIntPair_i)]

lib.ElSymmetricMax_s.argtypes = \
lib.ElSymmetricMaxDist_s.argtypes = \
  [c_uint,c_void_p,POINTER(ValueIntPair_s)]

lib.ElSymmetricMax_d.argtypes = \
lib.ElSymmetricMaxDist_d.argtypes = \
  [c_uint,c_void_p,POINTER(ValueIntPair_d)]

def SymmetricMax(uplo,A):
  pair = TagToValueIntPair(A.tag)
  args = [uplo,A.obj,pointer(pair)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElSymmetricMax_i(*args) 
    elif A.tag == sTag: lib.ElSymmetricMax_s(*args) 
    elif A.tag == dTag: lib.ElSymmetricMax_d(*args) 
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElSymmetricMaxDist_i(*args) 
    elif A.tag == sTag: lib.ElSymmetricMaxDist_s(*args) 
    elif A.tag == dTag: lib.ElSymmetricMaxDist_d(*args) 
    else: DataExcept()
  else: TypeExcept()
  return pair.value, pair.indices[0], pair.indices[1]

lib.ElVectorMax_i.argtypes = \
lib.ElVectorMaxDist_i.argtypes = \
  [c_void_p,POINTER(ValueInt_i)]

lib.ElVectorMax_s.argtypes = \
lib.ElVectorMaxDist_s.argtypes = \
  [c_void_p,POINTER(ValueInt_s)]

lib.ElVectorMax_d.argtypes = \
lib.ElVectorMaxDist_d.argtypes = \
  [c_void_p,POINTER(ValueInt_d)]

def VectorMax(A):
  pair = TagToValueInt(A.tag)
  args = [A.obj,pointer(pair)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElVectorMax_i(*args) 
    elif A.tag == sTag: lib.ElVectorMax_s(*args) 
    elif A.tag == dTag: lib.ElVectorMax_d(*args) 
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElVectorMaxDist_i(*args) 
    elif A.tag == sTag: lib.ElVectorMaxDist_s(*args) 
    elif A.tag == dTag: lib.ElVectorMaxDist_d(*args) 
    else: DataExcept()
  else: TypeExcept()
  return pair.value, pair.index

# MaxAbs
# ------
lib.ElMaxAbs_i.argtypes = \
lib.ElMaxAbsDist_i.argtypes = \
  [c_void_p,POINTER(ValueIntPair_i)]

lib.ElMaxAbs_s.argtypes = \
lib.ElMaxAbs_c.argtypes = \
lib.ElMaxAbsDist_s.argtypes = \
lib.ElMaxAbsDist_c.argtypes = \
  [c_void_p,POINTER(ValueIntPair_s)]

lib.ElMaxAbs_d.argtypes = \
lib.ElMaxAbs_z.argtypes = \
lib.ElMaxAbsDist_d.argtypes = \
lib.ElMaxAbsDist_z.argtypes = \
  [c_void_p,POINTER(ValueIntPair_d)]

def MaxAbs(A):
  pair = TagToValueIntPair(Base(A.tag))
  args = [A.obj,pointer(pair)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElMaxAbs_i(*args) 
    elif A.tag == sTag: lib.ElMaxAbs_s(*args) 
    elif A.tag == dTag: lib.ElMaxAbs_d(*args) 
    elif A.tag == cTag: lib.ElMaxAbs_c(*args) 
    elif A.tag == zTag: lib.ElMaxAbs_z(*args) 
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElMaxAbsDist_i(*args) 
    elif A.tag == sTag: lib.ElMaxAbsDist_s(*args) 
    elif A.tag == dTag: lib.ElMaxAbsDist_d(*args) 
    elif A.tag == cTag: lib.ElMaxAbsDist_c(*args) 
    elif A.tag == zTag: lib.ElMaxAbsDist_z(*args) 
    else: DataExcept()
  else: TypeExcept()
  return pair.value, pair.indices[0], pair.indices[1]

lib.ElSymmetricMaxAbs_i.argtypes = \
lib.ElSymmetricMaxAbsDist_i.argtypes = \
  [c_uint,c_void_p,POINTER(ValueIntPair_i)]

lib.ElSymmetricMaxAbs_s.argtypes = \
lib.ElSymmetricMaxAbs_c.argtypes = \
lib.ElSymmetricMaxAbsDist_s.argtypes = \
lib.ElSymmetricMaxAbsDist_c.argtypes = \
  [c_uint,c_void_p,POINTER(ValueIntPair_s)]

lib.ElSymmetricMaxAbs_d.argtypes = \
lib.ElSymmetricMaxAbs_z.argtypes = \
lib.ElSymmetricMaxAbsDist_d.argtypes = \
lib.ElSymmetricMaxAbsDist_z.argtypes = \
  [c_uint,c_void_p,POINTER(ValueIntPair_d)]

def SymmetricMaxAbs(uplo,A):
  pair = TagToValueIntPair(Base(A.tag))
  args = [uplo,A.obj,pointer(pair)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElSymmetricMaxAbs_i(*args) 
    elif A.tag == sTag: lib.ElSymmetricMaxAbs_s(*args) 
    elif A.tag == dTag: lib.ElSymmetricMaxAbs_d(*args) 
    elif A.tag == cTag: lib.ElSymmetricMaxAbs_c(*args) 
    elif A.tag == zTag: lib.ElSymmetricMaxAbs_z(*args) 
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElSymmetricMaxAbsDist_i(*args) 
    elif A.tag == sTag: lib.ElSymmetricMaxAbsDist_s(*args) 
    elif A.tag == dTag: lib.ElSymmetricMaxAbsDist_d(*args) 
    elif A.tag == cTag: lib.ElSymmetricMaxAbsDist_c(*args) 
    elif A.tag == zTag: lib.ElSymmetricMaxAbsDist_z(*args) 
    else: DataExcept()
  else: TypeExcept()
  return pair.value, pair.indices[0], pair.indices[1]

lib.ElVectorMaxAbs_i.argtypes = \
lib.ElVectorMaxAbsDist_i.argtypes = \
  [c_void_p,POINTER(ValueInt_i)]

lib.ElVectorMaxAbs_s.argtypes = \
lib.ElVectorMaxAbsDist_s.argtypes = \
  [c_void_p,POINTER(ValueInt_s)]

lib.ElVectorMaxAbs_d.argtypes = \
lib.ElVectorMaxAbsDist_d.argtypes = \
  [c_void_p,POINTER(ValueInt_d)]

lib.ElVectorMaxAbs_c.argtypes = \
lib.ElVectorMaxAbsDist_c.argtypes = \
  [c_void_p,POINTER(ValueInt_s)]

lib.ElVectorMaxAbs_z.argtypes = \
lib.ElVectorMaxAbsDist_z.argtypes = \
  [c_void_p,POINTER(ValueInt_d)]

def VectorMaxAbs(A):
  pair = TagToValueInt(Base(A.tag))
  args = [A.obj,pointer(pair)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElVectorMaxAbs_i(*args) 
    elif A.tag == sTag: lib.ElVectorMaxAbs_s(*args) 
    elif A.tag == dTag: lib.ElVectorMaxAbs_d(*args) 
    elif A.tag == cTag: lib.ElVectorMaxAbs_c(*args) 
    elif A.tag == zTag: lib.ElVectorMaxAbs_z(*args) 
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElVectorMaxAbsDist_i(*args) 
    elif A.tag == sTag: lib.ElVectorMaxAbsDist_s(*args) 
    elif A.tag == dTag: lib.ElVectorMaxAbsDist_d(*args) 
    elif A.tag == cTag: lib.ElVectorMaxAbsDist_c(*args) 
    elif A.tag == zTag: lib.ElVectorMaxAbsDist_z(*args) 
    else: DataExcept()
  else: TypeExcept()
  return pair.value, pair.index

# Min
# ---
lib.ElMin_i.argtypes = \
lib.ElMinDist_i.argtypes = \
  [c_void_p,POINTER(ValueIntPair_i)]

lib.ElMin_s.argtypes = \
lib.ElMinDist_s.argtypes = \
  [c_void_p,POINTER(ValueIntPair_s)]

lib.ElMin_d.argtypes = \
lib.ElMinDist_d.argtypes = \
  [c_void_p,POINTER(ValueIntPair_d)]

def Min(A):
  pair = TagToValueIntPair(A.tag)
  args = [A.obj,pointer(pair)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElMin_i(*args) 
    elif A.tag == sTag: lib.ElMin_s(*args) 
    elif A.tag == dTag: lib.ElMin_d(*args) 
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElMinDist_i(*args) 
    elif A.tag == sTag: lib.ElMinDist_s(*args) 
    elif A.tag == dTag: lib.ElMinDist_d(*args) 
    else: DataExcept()
  else: TypeExcept()
  return pair.value, pair.indices[0], pair.indices[1]

lib.ElSymmetricMin_i.argtypes = \
lib.ElSymmetricMinDist_i.argtypes = \
  [c_uint,c_void_p,POINTER(ValueIntPair_i)]

lib.ElSymmetricMin_s.argtypes = \
lib.ElSymmetricMinDist_s.argtypes = \
  [c_uint,c_void_p,POINTER(ValueIntPair_s)]

lib.ElSymmetricMin_d.argtypes = \
lib.ElSymmetricMinDist_d.argtypes = \
  [c_uint,c_void_p,POINTER(ValueIntPair_d)]

def SymmetricMin(uplo,A):
  pair = TagToValueIntPair(A.tag)
  args = [uplo,A.obj,pointer(pair)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElSymmetricMin_i(*args) 
    elif A.tag == sTag: lib.ElSymmetricMin_s(*args) 
    elif A.tag == dTag: lib.ElSymmetricMin_d(*args) 
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElSymmetricMinDist_i(*args) 
    elif A.tag == sTag: lib.ElSymmetricMinDist_s(*args) 
    elif A.tag == dTag: lib.ElSymmetricMinDist_d(*args) 
    else: DataExcept()
  else: TypeExcept()
  return pair.value, pair.indices[0], pair.indices[1]

lib.ElVectorMin_i.argtypes = \
lib.ElVectorMinDist_i.argtypes = \
  [c_void_p,POINTER(ValueInt_i)]

lib.ElVectorMin_s.argtypes = \
lib.ElVectorMinDist_s.argtypes = \
  [c_void_p,POINTER(ValueInt_s)]

lib.ElVectorMin_d.argtypes = \
lib.ElVectorMinDist_d.argtypes = \
  [c_void_p,POINTER(ValueInt_d)]

def VectorMin(A):
  pair = TagToValueInt(A.tag)
  args = [A.obj,pointer(pair)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElVectorMin_i(*args) 
    elif A.tag == sTag: lib.ElVectorMin_s(*args) 
    elif A.tag == dTag: lib.ElVectorMin_d(*args) 
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElVectorMinDist_i(*args) 
    elif A.tag == sTag: lib.ElVectorMinDist_s(*args) 
    elif A.tag == dTag: lib.ElVectorMinDist_d(*args) 
    else: DataExcept()
  else: TypeExcept()
  return pair.value, pair.index

# MinAbs
# ------
lib.ElMinAbs_i.argtypes = \
lib.ElMinAbsDist_i.argtypes = \
  [c_void_p,POINTER(ValueIntPair_i)]

lib.ElMinAbs_s.argtypes = \
lib.ElMinAbsDist_s.argtypes = \
  [c_void_p,POINTER(ValueIntPair_s)]

lib.ElMinAbs_d.argtypes = \
lib.ElMinAbsDist_d.argtypes = \
  [c_void_p,POINTER(ValueIntPair_d)]

lib.ElMinAbs_c.argtypes = \
lib.ElMinAbsDist_c.argtypes = \
  [c_void_p,POINTER(ValueIntPair_s)]

lib.ElMinAbs_z.argtypes = \
lib.ElMinAbsDist_z.argtypes = \
  [c_void_p,POINTER(ValueIntPair_d)]

def MinAbs(A):
  pair = TagToValueIntPair(Base(A.tag))
  args = [A.obj,pointer(pair)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElMinAbs_i(*args) 
    elif A.tag == sTag: lib.ElMinAbs_s(*args) 
    elif A.tag == dTag: lib.ElMinAbs_d(*args) 
    elif A.tag == cTag: lib.ElMinAbs_c(*args) 
    elif A.tag == zTag: lib.ElMinAbs_z(*args) 
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElMinAbsDist_i(*args) 
    elif A.tag == sTag: lib.ElMinAbsDist_s(*args) 
    elif A.tag == dTag: lib.ElMinAbsDist_d(*args) 
    elif A.tag == cTag: lib.ElMinAbsDist_c(*args) 
    elif A.tag == zTag: lib.ElMinAbsDist_z(*args) 
    else: DataExcept()
  else: TypeExcept()
  return pair.value, pair.indices[0], pair.indices[1]

lib.ElSymmetricMinAbs_i.argtypes = \
lib.ElSymmetricMinAbsDist_i.argtypes = \
  [c_uint,c_void_p,POINTER(ValueIntPair_i)]

lib.ElSymmetricMinAbs_s.argtypes = \
lib.ElSymmetricMinAbsDist_s.argtypes = \
  [c_uint,c_void_p,POINTER(ValueIntPair_s)]

lib.ElSymmetricMinAbs_d.argtypes = \
lib.ElSymmetricMinAbsDist_d.argtypes = \
  [c_uint,c_void_p,POINTER(ValueIntPair_d)]

lib.ElSymmetricMinAbs_c.argtypes = \
lib.ElSymmetricMinAbsDist_c.argtypes = \
  [c_uint,c_void_p,POINTER(ValueIntPair_s)]

lib.ElSymmetricMinAbs_z.argtypes = \
lib.ElSymmetricMinAbsDist_z.argtypes = \
  [c_uint,c_void_p,POINTER(ValueIntPair_d)]

def SymmetricMinAbs(uplo,A):
  pair = TagToValueIntPair(Base(A.tag))
  args = [uplo,A.obj,pointer(pair)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElSymmetricMinAbs_i(*args) 
    elif A.tag == sTag: lib.ElSymmetricMinAbs_s(*args) 
    elif A.tag == dTag: lib.ElSymmetricMinAbs_d(*args) 
    elif A.tag == cTag: lib.ElSymmetricMinAbs_c(*args) 
    elif A.tag == zTag: lib.ElSymmetricMinAbs_z(*args) 
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElSymmetricMinAbsDist_i(*args) 
    elif A.tag == sTag: lib.ElSymmetricMinAbsDist_s(*args) 
    elif A.tag == dTag: lib.ElSymmetricMinAbsDist_d(*args) 
    elif A.tag == cTag: lib.ElSymmetricMinAbsDist_c(*args) 
    elif A.tag == zTag: lib.ElSymmetricMinAbsDist_z(*args) 
    else: DataExcept()
  else: TypeExcept()
  return pair.value, pair.indices[0], pair.indices[1]

lib.ElVectorMinAbs_i.argtypes = \
lib.ElVectorMinAbsDist_i.argtypes = \
  [c_void_p,POINTER(ValueInt_i)]

lib.ElVectorMinAbs_s.argtypes = \
lib.ElVectorMinAbsDist_s.argtypes = \
  [c_void_p,POINTER(ValueInt_s)]

lib.ElVectorMinAbs_d.argtypes = \
lib.ElVectorMinAbsDist_d.argtypes = \
  [c_void_p,POINTER(ValueInt_d)]

lib.ElVectorMinAbs_c.argtypes = \
lib.ElVectorMinAbsDist_c.argtypes = \
  [c_void_p,POINTER(ValueInt_s)]

lib.ElVectorMinAbs_z.argtypes = \
lib.ElVectorMinAbsDist_z.argtypes = \
  [c_void_p,POINTER(ValueInt_d)]

def VectorMinAbs(A):
  pair = TagToValueInt(Base(A.tag))
  args = [A.obj,pointer(pair)]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElVectorMinAbs_i(*args) 
    elif A.tag == sTag: lib.ElVectorMinAbs_s(*args) 
    elif A.tag == dTag: lib.ElVectorMinAbs_d(*args) 
    elif A.tag == cTag: lib.ElVectorMinAbs_c(*args) 
    elif A.tag == zTag: lib.ElVectorMinAbs_z(*args) 
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElVectorMinAbsDist_i(*args) 
    elif A.tag == sTag: lib.ElVectorMinAbsDist_s(*args) 
    elif A.tag == dTag: lib.ElVectorMinAbsDist_d(*args) 
    elif A.tag == cTag: lib.ElVectorMinAbsDist_c(*args) 
    elif A.tag == zTag: lib.ElVectorMinAbsDist_z(*args) 
    else: DataExcept()
  else: TypeExcept()
  return pair.value, pair.index

# Nrm2
# ----
lib.ElNrm2_s.argtypes = [c_void_p,POINTER(sType)]
lib.ElNrm2_d.argtypes = [c_void_p,POINTER(dType)]
lib.ElNrm2_c.argtypes = [c_void_p,POINTER(sType)]
lib.ElNrm2_z.argtypes = [c_void_p,POINTER(dType)]
lib.ElNrm2Dist_s.argtypes = [c_void_p,POINTER(sType)]
lib.ElNrm2Dist_d.argtypes = [c_void_p,POINTER(dType)]
lib.ElNrm2Dist_c.argtypes = [c_void_p,POINTER(sType)]
lib.ElNrm2Dist_z.argtypes = [c_void_p,POINTER(dType)]
lib.ElNrm2DistMultiVec_s.argtypes = [c_void_p,POINTER(sType)]
lib.ElNrm2DistMultiVec_d.argtypes = [c_void_p,POINTER(dType)]
lib.ElNrm2DistMultiVec_c.argtypes = [c_void_p,POINTER(sType)]
lib.ElNrm2DistMultiVec_z.argtypes = [c_void_p,POINTER(dType)]

def Nrm2(A):
  gamma = TagToType(Base(A.tag))()
  args = [A.obj,pointer(gamma)]
  if type(A) is Matrix:
    if   A.tag == sTag: lib.ElNrm2_s(*args)
    elif A.tag == dTag: lib.ElNrm2_d(*args)
    elif A.tag == cTag: lib.ElNrm2_c(*args)
    elif A.tag == zTag: lib.ElNrm2_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == sTag: lib.ElNrm2Dist_s(*args)
    elif A.tag == dTag: lib.ElNrm2Dist_d(*args)
    elif A.tag == cTag: lib.ElNrm2Dist_c(*args)
    elif A.tag == zTag: lib.ElNrm2Dist_z(*args)
    else: DataExcept()
  elif type(A) is DistMultiVec:
    if   A.tag == sTag: lib.ElNrm2DistMultiVec_s(*args)
    elif A.tag == dTag: lib.ElNrm2DistMultiVec_d(*args)
    elif A.tag == cTag: lib.ElNrm2DistMultiVec_c(*args)
    elif A.tag == zTag: lib.ElNrm2DistMultiVec_z(*args)
    else: DataExcept()
  else: TypeExcept()
  return gamma.value

# Scale
# -----
lib.ElScale_i.argtypes = [iType,c_void_p]
lib.ElScale_s.argtypes = [sType,c_void_p]
lib.ElScale_d.argtypes = [dType,c_void_p]
lib.ElScale_c.argtypes = [cType,c_void_p]
lib.ElScale_z.argtypes = [zType,c_void_p]
lib.ElScaleDist_i.argtypes = [iType,c_void_p]
lib.ElScaleDist_s.argtypes = [sType,c_void_p]
lib.ElScaleDist_d.argtypes = [dType,c_void_p]
lib.ElScaleDist_c.argtypes = [cType,c_void_p]
lib.ElScaleDist_z.argtypes = [zType,c_void_p]
lib.ElScaleSparse_i.argtypes = [iType,c_void_p]
lib.ElScaleSparse_s.argtypes = [sType,c_void_p]
lib.ElScaleSparse_d.argtypes = [dType,c_void_p]
lib.ElScaleSparse_c.argtypes = [cType,c_void_p]
lib.ElScaleSparse_z.argtypes = [zType,c_void_p]
lib.ElScaleDistSparse_i.argtypes = [iType,c_void_p]
lib.ElScaleDistSparse_s.argtypes = [sType,c_void_p]
lib.ElScaleDistSparse_d.argtypes = [dType,c_void_p]
lib.ElScaleDistSparse_c.argtypes = [cType,c_void_p]
lib.ElScaleDistSparse_z.argtypes = [zType,c_void_p]
lib.ElScaleDistMultiVec_i.argtypes = [iType,c_void_p]
lib.ElScaleDistMultiVec_s.argtypes = [sType,c_void_p]
lib.ElScaleDistMultiVec_d.argtypes = [dType,c_void_p]
lib.ElScaleDistMultiVec_c.argtypes = [cType,c_void_p]
lib.ElScaleDistMultiVec_z.argtypes = [zType,c_void_p]
def Scale(alphaPre,A):
  alpha = TagToType(A.tag)(alphaPre)
  args = [alpha,A.obj]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElScale_i(*args)
    elif A.tag == sTag: lib.ElScale_s(*args)
    elif A.tag == dTag: lib.ElScale_d(*args)
    elif A.tag == cTag: lib.ElScale_c(*args)
    elif A.tag == zTag: lib.ElScale_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElScaleDist_i(*args)
    elif A.tag == sTag: lib.ElScaleDist_s(*args)
    elif A.tag == dTag: lib.ElScaleDist_d(*args)
    elif A.tag == cTag: lib.ElScaleDist_c(*args)
    elif A.tag == zTag: lib.ElScaleDist_z(*args)
    else: DataExcept()
  elif type(A) is SparseMatrix:
    if   A.tag == iTag: lib.ElScaleSparse_i(*args)
    elif A.tag == sTag: lib.ElScaleSparse_s(*args)
    elif A.tag == dTag: lib.ElScaleSparse_d(*args)
    elif A.tag == cTag: lib.ElScaleSparse_c(*args)
    elif A.tag == zTag: lib.ElScaleSparse_z(*args)
    else: DataExcept()
  elif type(A) is DistSparseMatrix:
    if   A.tag == iTag: lib.ElScaleDistSparse_i(*args)
    elif A.tag == sTag: lib.ElScaleDistSparse_s(*args)
    elif A.tag == dTag: lib.ElScaleDistSparse_d(*args)
    elif A.tag == cTag: lib.ElScaleDistSparse_c(*args)
    elif A.tag == zTag: lib.ElScaleDistSparse_z(*args)
    else: DataExcept()
  elif type(A) is DistMultiVec:
    if   A.tag == iTag: lib.ElScaleDistMultiVec_i(*args)
    elif A.tag == sTag: lib.ElScaleDistMultiVec_s(*args)
    elif A.tag == dTag: lib.ElScaleDistMultiVec_d(*args)
    elif A.tag == cTag: lib.ElScaleDistMultiVec_c(*args)
    elif A.tag == zTag: lib.ElScaleDistMultiVec_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Scale trapezoid
# ---------------
lib.ElScaleTrapezoid_i.argtypes = [iType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoid_s.argtypes = [sType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoid_d.argtypes = [dType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoid_c.argtypes = [cType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoid_z.argtypes = [zType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidDist_i.argtypes = [iType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidDist_s.argtypes = [sType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidDist_d.argtypes = [dType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidDist_c.argtypes = [cType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidDist_z.argtypes = [zType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidSparse_i.argtypes = [iType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidSparse_s.argtypes = [sType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidSparse_d.argtypes = [dType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidSparse_c.argtypes = [cType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidSparse_z.argtypes = [zType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidDistSparse_i.argtypes = [iType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidDistSparse_s.argtypes = [sType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidDistSparse_d.argtypes = [dType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidDistSparse_c.argtypes = [cType,c_uint,c_void_p,iType]
lib.ElScaleTrapezoidDistSparse_z.argtypes = [zType,c_uint,c_void_p,iType]
def ScaleTrapezoid(alphaPre,uplo,A,offset=0):
  alpha = TagToType(A.tag)(alphaPre)
  args = [alpha,uplo,A.obj,offset]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElScaleTrapezoid_i(*args)
    elif A.tag == sTag: lib.ElScaleTrapezoid_s(*args)
    elif A.tag == dTag: lib.ElScaleTrapezoid_d(*args)
    elif A.tag == cTag: lib.ElScaleTrapezoid_c(*args)
    elif A.tag == zTag: lib.ElScaleTrapezoid_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElScaleTrapezoidDist_i(*args)
    elif A.tag == sTag: lib.ElScaleTrapezoidDist_s(*args)
    elif A.tag == dTag: lib.ElScaleTrapezoidDist_d(*args)
    elif A.tag == cTag: lib.ElScaleTrapezoidDist_c(*args)
    elif A.tag == zTag: lib.ElScaleTrapezoidDist_z(*args)
    else: DataExcept()
  elif type(A) is SparseMatrix:
    if   A.tag == iTag: lib.ElScaleTrapezoidSparse_i(*args)
    elif A.tag == sTag: lib.ElScaleTrapezoidSparse_s(*args)
    elif A.tag == dTag: lib.ElScaleTrapezoidSparse_d(*args)
    elif A.tag == cTag: lib.ElScaleTrapezoidSparse_c(*args)
    elif A.tag == zTag: lib.ElScaleTrapezoidSparse_z(*args)
    else: DataExcept()
  elif type(A) is DistSparseMatrix:
    if   A.tag == iTag: lib.ElScaleTrapezoidDistSparse_i(*args)
    elif A.tag == sTag: lib.ElScaleTrapezoidDistSparse_s(*args)
    elif A.tag == dTag: lib.ElScaleTrapezoidDistSparse_d(*args)
    elif A.tag == cTag: lib.ElScaleTrapezoidDistSparse_c(*args)
    elif A.tag == zTag: lib.ElScaleTrapezoidDistSparse_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Set diagonal
# ------------
# TODO

# Shift
# -----
lib.ElShift_i.argtypes = \
lib.ElShiftDist_i.argtypes = \
lib.ElShiftDistMultiVec_i.argtypes = \
  [c_void_p,iType]
lib.ElShift_s.argtypes = \
lib.ElShiftDist_s.argtypes = \
lib.ElShiftDistMultiVec_s.argtypes = \
  [c_void_p,sType]
lib.ElShift_d.argtypes = \
lib.ElShiftDist_d.argtypes = \
lib.ElShiftDistMultiVec_d.argtypes = \
  [c_void_p,dType]
lib.ElShift_c.argtypes = \
lib.ElShiftDist_c.argtypes = \
lib.ElShiftDistMultiVec_c.argtypes = \
  [c_void_p,cType]
lib.ElShift_z.argtypes = \
lib.ElShiftDist_z.argtypes = \
lib.ElShiftDistMultiVec_z.argtypes = \
  [c_void_p,zType]
def Shift(A,alphaPre):
  alpha = TagToType(A.tag)(alphaPre)
  args = [A.obj,alpha]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElShift_i(*args)
    elif A.tag == sTag: lib.ElShift_s(*args)
    elif A.tag == dTag: lib.ElShift_d(*args)
    elif A.tag == cTag: lib.ElShift_c(*args)
    elif A.tag == zTag: lib.ElShift_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElShiftDist_i(*args)
    elif A.tag == sTag: lib.ElShiftDist_s(*args)
    elif A.tag == dTag: lib.ElShiftDist_d(*args)
    elif A.tag == cTag: lib.ElShiftDist_c(*args)
    elif A.tag == zTag: lib.ElShiftDist_z(*args)
    else: DataExcept()
  elif type(A) is DistMultiVec:
    if   A.tag == iTag: lib.ElShiftDistMultiVec_i(*args)
    elif A.tag == sTag: lib.ElShiftDistMultiVec_s(*args)
    elif A.tag == dTag: lib.ElShiftDistMultiVec_d(*args)
    elif A.tag == cTag: lib.ElShiftDistMultiVec_c(*args)
    elif A.tag == zTag: lib.ElShiftDistMultiVec_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Shift diagonal
# --------------
lib.ElShiftDiagonal_i.argtypes = \
lib.ElShiftDiagonalDist_i.argtypes = \
lib.ElShiftDiagonalSparse_i.argtypes = \
lib.ElShiftDiagonalDistSparse_i.argtypes = \
  [c_void_p,iType,iType]
lib.ElShiftDiagonal_s.argtypes = \
lib.ElShiftDiagonalDist_s.argtypes = \
lib.ElShiftDiagonalSparse_s.argtypes = \
lib.ElShiftDiagonalDistSparse_s.argtypes = \
  [c_void_p,sType,iType]
lib.ElShiftDiagonal_d.argtypes = \
lib.ElShiftDiagonalDist_d.argtypes = \
lib.ElShiftDiagonalSparse_d.argtypes = \
lib.ElShiftDiagonalDistSparse_d.argtypes = \
  [c_void_p,dType,iType]
lib.ElShiftDiagonal_c.argtypes = \
lib.ElShiftDiagonalDist_c.argtypes = \
lib.ElShiftDiagonalSparse_c.argtypes = \
lib.ElShiftDiagonalDistSparse_c.argtypes = \
  [c_void_p,cType,iType]
lib.ElShiftDiagonal_z.argtypes = \
lib.ElShiftDiagonalDist_z.argtypes = \
lib.ElShiftDiagonalSparse_z.argtypes = \
lib.ElShiftDiagonalDistSparse_z.argtypes = \
  [c_void_p,zType,iType]

def ShiftDiagonal(A,alphaPre,offset=0):
  alpha = TagToType(A.tag)(alphaPre)
  args = [A.obj,alpha,offset]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElShiftDiagonal_i(*args)
    elif A.tag == sTag: lib.ElShiftDiagonal_s(*args)
    elif A.tag == dTag: lib.ElShiftDiagonal_d(*args)
    elif A.tag == cTag: lib.ElShiftDiagonal_c(*args)
    elif A.tag == zTag: lib.ElShiftDiagonal_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElShiftDiagonalDist_i(*args)
    elif A.tag == sTag: lib.ElShiftDiagonalDist_s(*args)
    elif A.tag == dTag: lib.ElShiftDiagonalDist_d(*args)
    elif A.tag == cTag: lib.ElShiftDiagonalDist_c(*args)
    elif A.tag == zTag: lib.ElShiftDiagonalDist_z(*args)
    else: DataExcept()
  elif type(A) is SparseMatrix:
    if   A.tag == iTag: lib.ElShiftDiagonalSparse_i(*args)
    elif A.tag == sTag: lib.ElShiftDiagonalSparse_s(*args)
    elif A.tag == dTag: lib.ElShiftDiagonalSparse_d(*args)
    elif A.tag == cTag: lib.ElShiftDiagonalSparse_c(*args)
    elif A.tag == zTag: lib.ElShiftDiagonalSparse_z(*args)
    else: DataExcept()
  elif type(A) is DistSparseMatrix:
    if   A.tag == iTag: lib.ElShiftDiagonalDistSparse_i(*args)
    elif A.tag == sTag: lib.ElShiftDiagonalDistSparse_s(*args)
    elif A.tag == dTag: lib.ElShiftDiagonalDistSparse_d(*args)
    elif A.tag == cTag: lib.ElShiftDiagonalDistSparse_c(*args)
    elif A.tag == zTag: lib.ElShiftDiagonalDistSparse_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Swap
# ----
lib.ElSwap_i.argtypes = [c_uint,c_void_p,c_void_p]
lib.ElSwap_s.argtypes = [c_uint,c_void_p,c_void_p]
lib.ElSwap_d.argtypes = [c_uint,c_void_p,c_void_p]
lib.ElSwap_c.argtypes = [c_uint,c_void_p,c_void_p]
lib.ElSwap_z.argtypes = [c_uint,c_void_p,c_void_p]
lib.ElSwapDist_i.argtypes = [c_uint,c_void_p,c_void_p]
lib.ElSwapDist_s.argtypes = [c_uint,c_void_p,c_void_p]
lib.ElSwapDist_d.argtypes = [c_uint,c_void_p,c_void_p]
lib.ElSwapDist_c.argtypes = [c_uint,c_void_p,c_void_p]
lib.ElSwapDist_z.argtypes = [c_uint,c_void_p,c_void_p]
def Swap(orient,X,Y):
  if type(X) is not type(Y): raise Exception('Matrix types must match')
  if X.tag != Y.tag: raise Exception('Matrix datatypes must match')
  args = [orient,X.obj,Y.obj]
  if type(X) is Matrix:
    if   A.tag == iTag: lib.ElSwap_i(*args)
    elif A.tag == sTag: lib.ElSwap_s(*args)
    elif A.tag == dTag: lib.ElSwap_d(*args)
    elif A.tag == cTag: lib.ElSwap_c(*args)
    elif A.tag == zTag: lib.ElSwap_z(*args)
    else: DataExcept()
  elif type(X) is DistMatrix:
    if   A.tag == iTag: lib.ElSwapDist_i(*args)
    elif A.tag == sTag: lib.ElSwapDist_s(*args)
    elif A.tag == dTag: lib.ElSwapDist_d(*args)
    elif A.tag == cTag: lib.ElSwapDist_c(*args)
    elif A.tag == zTag: lib.ElSwapDist_z(*args)
    else: DataExcept()
  else: TypeExcept()

lib.ElRowSwap_i.argtypes = [c_void_p,iType,iType]
lib.ElRowSwap_s.argtypes = [c_void_p,iType,iType]
lib.ElRowSwap_d.argtypes = [c_void_p,iType,iType]
lib.ElRowSwap_c.argtypes = [c_void_p,iType,iType]
lib.ElRowSwap_z.argtypes = [c_void_p,iType,iType]
lib.ElRowSwapDist_i.argtypes = [c_void_p,iType,iType]
lib.ElRowSwapDist_s.argtypes = [c_void_p,iType,iType]
lib.ElRowSwapDist_d.argtypes = [c_void_p,iType,iType]
lib.ElRowSwapDist_c.argtypes = [c_void_p,iType,iType]
lib.ElRowSwapDist_z.argtypes = [c_void_p,iType,iType]
def RowSwap(A,iTo,iFrom):
  args = [A.obj,iTo,iFrom]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElRowSwap_i(*args)
    elif A.tag == sTag: lib.ElRowSwap_s(*args)
    elif A.tag == dTag: lib.ElRowSwap_d(*args)
    elif A.tag == cTag: lib.ElRowSwap_c(*args)
    elif A.tag == zTag: lib.ElRowSwap_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElRowSwapDist_i(*args)
    elif A.tag == sTag: lib.ElRowSwapDist_s(*args)
    elif A.tag == dTag: lib.ElRowSwapDist_d(*args)
    elif A.tag == cTag: lib.ElRowSwapDist_c(*args)
    elif A.tag == zTag: lib.ElRowSwapDist_z(*args)
    else: DataExcept()
  else: TypeExcept()

lib.ElColSwap_i.argtypes = [c_void_p,iType,iType]
lib.ElColSwap_s.argtypes = [c_void_p,iType,iType]
lib.ElColSwap_d.argtypes = [c_void_p,iType,iType]
lib.ElColSwap_c.argtypes = [c_void_p,iType,iType]
lib.ElColSwap_z.argtypes = [c_void_p,iType,iType]
lib.ElColSwapDist_i.argtypes = [c_void_p,iType,iType]
lib.ElColSwapDist_s.argtypes = [c_void_p,iType,iType]
lib.ElColSwapDist_d.argtypes = [c_void_p,iType,iType]
lib.ElColSwapDist_c.argtypes = [c_void_p,iType,iType]
lib.ElColSwapDist_z.argtypes = [c_void_p,iType,iType]
def ColSwap(A,jTo,jFrom):
  args = [A.obj,jTo,jFrom]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElColSwap_i(*args)
    elif A.tag == sTag: lib.ElColSwap_s(*args)
    elif A.tag == dTag: lib.ElColSwap_d(*args)
    elif A.tag == cTag: lib.ElColSwap_c(*args)
    elif A.tag == zTag: lib.ElColSwap_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElColSwapDist_i(*args)
    elif A.tag == sTag: lib.ElColSwapDist_s(*args)
    elif A.tag == dTag: lib.ElColSwapDist_d(*args)
    elif A.tag == cTag: lib.ElColSwapDist_c(*args)
    elif A.tag == zTag: lib.ElColSwapDist_z(*args)
    else: DataExcept()
  else: TypeExcept()

lib.ElSymmetricSwap_i.argtypes = [c_uint,c_void_p,iType,iType]
lib.ElSymmetricSwap_s.argtypes = [c_uint,c_void_p,iType,iType]
lib.ElSymmetricSwap_d.argtypes = [c_uint,c_void_p,iType,iType]
lib.ElSymmetricSwap_c.argtypes = [c_uint,c_void_p,iType,iType]
lib.ElSymmetricSwap_z.argtypes = [c_uint,c_void_p,iType,iType]
lib.ElSymmetricSwapDist_i.argtypes = [c_uint,c_void_p,iType,iType]
lib.ElSymmetricSwapDist_s.argtypes = [c_uint,c_void_p,iType,iType]
lib.ElSymmetricSwapDist_d.argtypes = [c_uint,c_void_p,iType,iType]
lib.ElSymmetricSwapDist_c.argtypes = [c_uint,c_void_p,iType,iType]
lib.ElSymmetricSwapDist_z.argtypes = [c_uint,c_void_p,iType,iType]
def SymmetricSwap(uplo,A,jTo,jFrom):
  args = [uplo,A.obj,jTo,jFrom]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElSymmetricSwap_i(*args)
    elif A.tag == sTag: lib.ElSymmetricSwap_s(*args)
    elif A.tag == dTag: lib.ElSymmetricSwap_d(*args)
    elif A.tag == cTag: lib.ElSymmetricSwap_c(*args)
    elif A.tag == zTag: lib.ElSymmetricSwap_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElSymmetricSwapDist_i(*args)
    elif A.tag == sTag: lib.ElSymmetricSwapDist_s(*args)
    elif A.tag == dTag: lib.ElSymmetricSwapDist_d(*args)
    elif A.tag == cTag: lib.ElSymmetricSwapDist_c(*args)
    elif A.tag == zTag: lib.ElSymmetricSwapDist_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Transpose/Adjoint
# -----------------
lib.ElTranspose_i.argtypes = [c_void_p,c_void_p]
lib.ElTranspose_s.argtypes = [c_void_p,c_void_p]
lib.ElTranspose_d.argtypes = [c_void_p,c_void_p]
lib.ElTranspose_c.argtypes = [c_void_p,c_void_p]
lib.ElTranspose_z.argtypes = [c_void_p,c_void_p]
lib.ElTransposeDist_i.argtypes = [c_void_p,c_void_p]
lib.ElTransposeDist_s.argtypes = [c_void_p,c_void_p]
lib.ElTransposeDist_d.argtypes = [c_void_p,c_void_p]
lib.ElTransposeDist_c.argtypes = [c_void_p,c_void_p]
lib.ElTransposeDist_z.argtypes = [c_void_p,c_void_p]
lib.ElTransposeSparse_i.argtypes = [c_void_p,c_void_p]
lib.ElTransposeSparse_s.argtypes = [c_void_p,c_void_p]
lib.ElTransposeSparse_d.argtypes = [c_void_p,c_void_p]
lib.ElTransposeSparse_c.argtypes = [c_void_p,c_void_p]
lib.ElTransposeSparse_z.argtypes = [c_void_p,c_void_p]
lib.ElTransposeDistSparse_i.argtypes = [c_void_p,c_void_p]
lib.ElTransposeDistSparse_s.argtypes = [c_void_p,c_void_p]
lib.ElTransposeDistSparse_d.argtypes = [c_void_p,c_void_p]
lib.ElTransposeDistSparse_c.argtypes = [c_void_p,c_void_p]
lib.ElTransposeDistSparse_z.argtypes = [c_void_p,c_void_p]

lib.ElAdjoint_c.argtypes = [c_void_p,c_void_p]
lib.ElAdjoint_z.argtypes = [c_void_p,c_void_p]
lib.ElAdjointDist_c.argtypes = [c_void_p,c_void_p]
lib.ElAdjointDist_z.argtypes = [c_void_p,c_void_p]
lib.ElAdjointSparse_c.argtypes = [c_void_p,c_void_p]
lib.ElAdjointSparse_z.argtypes = [c_void_p,c_void_p]
lib.ElAdjointDistSparse_c.argtypes = [c_void_p,c_void_p]
lib.ElAdjointDistSparse_z.argtypes = [c_void_p,c_void_p]

def Transpose(A,B,conj=False):
  if A.tag != B.tag:
    raise Exception('Transposing between datatypes not yet supported in Python')
  if type(A) is not type(B): raise Exception('Matrix types must match')
  args = [A.obj,B.obj]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElTranspose_i(*args)
    elif A.tag == sTag: lib.ElTranspose_s(*args)
    elif A.tag == dTag: lib.ElTranspose_d(*args)
    elif A.tag == cTag:
      if conj: lib.ElAdjoint_c(*args)
      else:    lib.ElTranspose_c(*args)
    elif A.tag == zTag: 
      if conj: lib.ElAdjoint_z(*args)
      else:    lib.ElTranspose_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElTransposeDist_i(*args)
    elif A.tag == sTag: lib.ElTransposeDist_s(*args)
    elif A.tag == dTag: lib.ElTransposeDist_d(*args)
    elif A.tag == cTag:
      if conj: lib.ElAdjointDist_c(*args)
      else:    lib.ElTransposeDist_c(*args)
    elif A.tag == zTag: 
      if conj: lib.ElAdjointDist_z(*args)
      else:    lib.ElTransposeDist_z(*args)
    else: DataExcept()
  elif type(A) is SparseMatrix:
    if   A.tag == iTag: lib.ElTransposeSparse_i(*args)
    elif A.tag == sTag: lib.ElTransposeSparse_s(*args)
    elif A.tag == dTag: lib.ElTransposeSparse_d(*args)
    elif A.tag == cTag:
      if conj: lib.ElAdjointSparse_c(*args)
      else:    lib.ElTransposeSparse_c(*args)
    elif A.tag == zTag:
      if conj: lib.ElAdjointSparse_z(*args)
      else:    lib.ElTransposeSparse_z(*args)
    else: DataExcept()
  elif type(A) is DistSparseMatrix:
    if   A.tag == iTag: lib.ElTransposeDistSparse_i(*args)
    elif A.tag == sTag: lib.ElTransposeDistSparse_s(*args)
    elif A.tag == dTag: lib.ElTransposeDistSparse_d(*args)
    elif A.tag == cTag:
      if conj: lib.ElAdjointDistSparse_c(*args)
      else:    lib.ElTransposeDistSparse_c(*args)
    elif A.tag == zTag:
      if conj: lib.ElAdjointDistSparse_z(*args)
      else:    lib.ElTransposeDistSparse_z(*args)
    else: DataExcept()
  else: TypeExcept()

def Adjoint(A,B):
  Transpose(A,B,True)

# Real part
# ---------
# TODO: Version which returns the result instead?
lib.ElRealPart_i.argtypes = [c_void_p,c_void_p]
lib.ElRealPart_s.argtypes = [c_void_p,c_void_p]
lib.ElRealPart_d.argtypes = [c_void_p,c_void_p]
lib.ElRealPart_c.argtypes = [c_void_p,c_void_p]
lib.ElRealPart_z.argtypes = [c_void_p,c_void_p]
lib.ElRealPartDist_i.argtypes = [c_void_p,c_void_p]
lib.ElRealPartDist_s.argtypes = [c_void_p,c_void_p]
lib.ElRealPartDist_d.argtypes = [c_void_p,c_void_p]
lib.ElRealPartDist_c.argtypes = [c_void_p,c_void_p]
lib.ElRealPartDist_z.argtypes = [c_void_p,c_void_p]
def RealPart(A,AReal):
  if AReal.tag != Base(A.tag):
    raise Exception('AReal must have the base datatype of A')
  if type(A) is not type(AReal): raise Exception('Matrix types must match')
  args = [A.obj,AReal.obj]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElRealPart_i(*args)
    elif A.tag == sTag: lib.ElRealPart_s(*args)
    elif A.tag == dTag: lib.ElRealPart_d(*args)
    elif A.tag == cTag: lib.ElRealPart_c(*args)
    elif A.tag == zTag: lib.ElRealPart_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElRealPartDist_i(*args)
    elif A.tag == sTag: lib.ElRealPartDist_s(*args)
    elif A.tag == dTag: lib.ElRealPartDist_d(*args)
    elif A.tag == cTag: lib.ElRealPartDist_c(*args)
    elif A.tag == zTag: lib.ElRealPartDist_z(*args)
    else: DataExcept()
  else: TypeExcept()

# Imaginary part
# --------------
# TODO: Version which returns the result instead?
lib.ElImagPart_i.argtypes = [c_void_p,c_void_p]
lib.ElImagPart_s.argtypes = [c_void_p,c_void_p]
lib.ElImagPart_d.argtypes = [c_void_p,c_void_p]
lib.ElImagPart_c.argtypes = [c_void_p,c_void_p]
lib.ElImagPart_z.argtypes = [c_void_p,c_void_p]
lib.ElImagPartDist_i.argtypes = [c_void_p,c_void_p]
lib.ElImagPartDist_s.argtypes = [c_void_p,c_void_p]
lib.ElImagPartDist_d.argtypes = [c_void_p,c_void_p]
lib.ElImagPartDist_c.argtypes = [c_void_p,c_void_p]
lib.ElImagPartDist_z.argtypes = [c_void_p,c_void_p]
def ImagPart(A,AImag):
  if AImag.tag != Base(A.tag):
    raise Exception('AImag must have the base datatype of A')
  if type(A) is not type(AImag): raise Exception('Matrix types must match')
  args = [A.obj,AImag.obj]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElImagPart_i(*args)
    elif A.tag == sTag: lib.ElImagPart_s(*args)
    elif A.tag == dTag: lib.ElImagPart_d(*args)
    elif A.tag == cTag: lib.ElImagPart_c(*args)
    elif A.tag == zTag: lib.ElImagPart_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElImagPartDist_i(*args)
    elif A.tag == sTag: lib.ElImagPartDist_s(*args)
    elif A.tag == dTag: lib.ElImagPartDist_d(*args)
    elif A.tag == cTag: lib.ElImagPartDist_c(*args)
    elif A.tag == zTag: lib.ElImagPartDist_z(*args)
    else: DataExcept()
  else: TypeExcept()

# UpdateDiagonal
# --------------
# TODO

# Zero
# ----
lib.ElZero_i.argtypes = [c_void_p]
lib.ElZero_s.argtypes = [c_void_p]
lib.ElZero_d.argtypes = [c_void_p]
lib.ElZero_c.argtypes = [c_void_p]
lib.ElZero_z.argtypes = [c_void_p]
lib.ElZeroDist_i.argtypes = [c_void_p]
lib.ElZeroDist_s.argtypes = [c_void_p]
lib.ElZeroDist_d.argtypes = [c_void_p]
lib.ElZeroDist_c.argtypes = [c_void_p]
lib.ElZeroDist_z.argtypes = [c_void_p]
lib.ElZeroSparse_i.argtypes = [c_void_p]
lib.ElZeroSparse_s.argtypes = [c_void_p]
lib.ElZeroSparse_d.argtypes = [c_void_p]
lib.ElZeroSparse_c.argtypes = [c_void_p]
lib.ElZeroSparse_z.argtypes = [c_void_p]
lib.ElZeroDistSparse_i.argtypes = [c_void_p]
lib.ElZeroDistSparse_s.argtypes = [c_void_p]
lib.ElZeroDistSparse_d.argtypes = [c_void_p]
lib.ElZeroDistSparse_c.argtypes = [c_void_p]
lib.ElZeroDistSparse_z.argtypes = [c_void_p]
lib.ElZeroDistMultiVec_i.argtypes = [c_void_p]
lib.ElZeroDistMultiVec_s.argtypes = [c_void_p]
lib.ElZeroDistMultiVec_d.argtypes = [c_void_p]
lib.ElZeroDistMultiVec_c.argtypes = [c_void_p]
lib.ElZeroDistMultiVec_z.argtypes = [c_void_p]

def Zero(A):
  args = [A.obj]
  if type(A) is Matrix:
    if   A.tag == iTag: lib.ElZero_i(*args)
    elif A.tag == sTag: lib.ElZero_s(*args)
    elif A.tag == dTag: lib.ElZero_d(*args)
    elif A.tag == cTag: lib.ElZero_c(*args)
    elif A.tag == zTag: lib.ElZero_z(*args)
    else: DataExcept()
  elif type(A) is DistMatrix:
    if   A.tag == iTag: lib.ElZeroDist_i(*args)
    elif A.tag == sTag: lib.ElZeroDist_s(*args)
    elif A.tag == dTag: lib.ElZeroDist_d(*args)
    elif A.tag == cTag: lib.ElZeroDist_c(*args)
    elif A.tag == zTag: lib.ElZeroDist_z(*args)
    else: DataExcept()
  elif type(A) is SparseMatrix:
    if   A.tag == iTag: lib.ElZeroSparse_i(*args)
    elif A.tag == sTag: lib.ElZeroSparse_s(*args)
    elif A.tag == dTag: lib.ElZeroSparse_d(*args)
    elif A.tag == cTag: lib.ElZeroSparse_c(*args)
    elif A.tag == zTag: lib.ElZeroSparse_z(*args)
    else: DataExcept()
  elif type(A) is DistSparseMatrix:
    if   A.tag == iTag: lib.ElZeroDistSparse_i(*args)
    elif A.tag == sTag: lib.ElZeroDistSparse_s(*args)
    elif A.tag == dTag: lib.ElZeroDistSparse_d(*args)
    elif A.tag == cTag: lib.ElZeroDistSparse_c(*args)
    elif A.tag == zTag: lib.ElZeroDistSparse_z(*args)
    else: DataExcept()
  elif type(A) is DistMultiVec:
    if   A.tag == iTag: lib.ElZeroDistMultiVec_i(*args)
    elif A.tag == sTag: lib.ElZeroDistMultiVec_s(*args)
    elif A.tag == dTag: lib.ElZeroDistMultiVec_d(*args)
    elif A.tag == cTag: lib.ElZeroDistMultiVec_c(*args)
    elif A.tag == zTag: lib.ElZeroDistMultiVec_z(*args)
    else: DataExcept()
  else: TypeExcept()
