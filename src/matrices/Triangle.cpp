/*
   Copyright (c) 2009-2015, Jack Poulson
   All rights reserved.

   This file is part of Elemental and is under the BSD 2-Clause License, 
   which can be found in the LICENSE file in the root directory, or at 
   http://opensource.org/licenses/BSD-2-Clause
*/
#include "El.hpp"

namespace El {

// The "triangle matrix" is defined to have the symbol:
//   f(z) = z^{-1} + 1/4 z^2.
// Please see 
//   L. Reichel and L. N. Trefethen, "Eigenvalues and pseudo-eigenvalues of 
//   "Toeplitz matrices", Linear Algebra Appl., 1992.

template<typename F> 
void Triangle( Matrix<F>& A, Int n )
{
    DEBUG_ONLY(CallStackEntry cse("Triangle"))
    if( n < 3 )
        LogicError("Must be at least 3x3 to have a second-order symbol");
    Zeros( A, n, n );
    FillDiagonal( A, F(1),       1 );
    FillDiagonal( A, F(1)/F(4), -2 );
}

template<typename F>
void Triangle( AbstractDistMatrix<F>& A, Int n )
{
    DEBUG_ONLY(CallStackEntry cse("Triangle"))
    if( n < 3 )
        LogicError("Must be at least 3x3 to have a second-order symbol");
    Zeros( A, n, n );
    FillDiagonal( A, F(1),       1 );
    FillDiagonal( A, F(1)/F(4), -2 );
}

template<typename F>
void Triangle( AbstractBlockDistMatrix<F>& A, Int n )
{
    DEBUG_ONLY(CallStackEntry cse("Triangle"))
    if( n < 3 )
        LogicError("Must be at least 3x3 to have a second-order symbol");
    Zeros( A, n, n );
    FillDiagonal( A, F(1),       1 );
    FillDiagonal( A, F(1)/F(4), -2 );
}

#define PROTO(F) \
  template void Triangle( Matrix<F>& A, Int n ); \
  template void Triangle( AbstractDistMatrix<F>& A, Int n ); \
  template void Triangle( AbstractBlockDistMatrix<F>& A, Int n );

#define EL_NO_INT_PROTO
#define EL_ENABLE_QUAD
#include "El/macros/Instantiate.h"

} // namespace El
