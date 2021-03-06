/*
   Copyright (c) 2009-2012, Jack Poulson, Lexing Ying, and 
   The University of Texas at Austin.
   All rights reserved.

   Copyright (c) 2013, Jack Poulson, Lexing Ying, and Stanford University.
   All rights reserved.

   Copyright (c) 2013-2014, Jack Poulson and 
   The Georgia Institute of Technology.
   All rights reserved.

   Copyright (c) 2014-2015, Jack Poulson and Stanford University.
   All rights reserved.
   
   This file is part of Elemental and is under the BSD 2-Clause License, 
   which can be found in the LICENSE file in the root directory, or at 
   http://opensource.org/licenses/BSD-2-Clause
*/
#include "El.hpp"

namespace El {

template<typename F>
void DiagonalSolve
( const SymmNodeInfo& info, const SymmFront<F>& front, 
  MatrixNode<F>& X )
{
    DEBUG_ONLY(CallStackEntry cse("DiagonalSolve"))

    const Int numChildren = info.children.size();
    for( Int c=0; c<numChildren; ++c )
        DiagonalSolve( *info.children[c], *front.children[c], *X.children[c] );

    if( PivotedFactorization(front.type) )
        QuasiDiagonalSolve
        ( LEFT, LOWER, front.diag, front.subdiag, 
          X.matrix, front.isHermitian );
    else
        DiagonalSolve( LEFT, NORMAL, front.diag, X.matrix, true );
}

template<typename F>
void DiagonalSolve
( const DistSymmNodeInfo& info, const DistSymmFront<F>& front, 
  DistMultiVecNode<F>& X )
{
    DEBUG_ONLY(CallStackEntry cse("DiagonalSolve"))

    if( front.child == nullptr )
    {
        DiagonalSolve( *info.duplicate, *front.duplicate, *X.duplicate );
        return;
    }
    DiagonalSolve( *info.child, *front.child, *X.child );

    if( PivotedFactorization(front.type) )
        QuasiDiagonalSolve
        ( LEFT, LOWER, front.diag, front.subdiag, X.matrix, front.isHermitian );
    else
        DiagonalSolve( LEFT, NORMAL, front.diag, X.matrix, true );
}

template<typename F>
void DiagonalSolve
( const DistSymmNodeInfo& info, const DistSymmFront<F>& front, 
  DistMatrixNode<F>& X )
{
    DEBUG_ONLY(CallStackEntry cse("DiagonalSolve"))

    if( front.child == nullptr )
    {
        DiagonalSolve( *info.duplicate, *front.duplicate, *X.duplicate );
        return;
    }
    DiagonalSolve( *info.child, *front.child, *X.child );

    if( PivotedFactorization(front.type) )
        QuasiDiagonalSolve
        ( LEFT, LOWER, front.diag, front.subdiag, X.matrix, front.isHermitian );
    else
        DiagonalSolve( LEFT, NORMAL, front.diag, X.matrix, true );
}

#define PROTO(F) \
  template void DiagonalSolve \
  ( const SymmNodeInfo& info, const SymmFront<F>& front, \
    MatrixNode<F>& X ); \
  template void DiagonalSolve \
  ( const DistSymmNodeInfo& info, const DistSymmFront<F>& front, \
    DistMultiVecNode<F>& X ); \
  template void DiagonalSolve \
  ( const DistSymmNodeInfo& info, const DistSymmFront<F>& front, \
    DistMatrixNode<F>& X );

#define EL_NO_INT_PROTO
#include "El/macros/Instantiate.h"

} // namespace El
