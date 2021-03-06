/*
   Copyright (c) 2009-2015, Jack Poulson
   All rights reserved.

   This file is part of Elemental and is under the BSD 2-Clause License, 
   which can be found in the LICENSE file in the root directory, or at 
   http://opensource.org/licenses/BSD-2-Clause
*/
#include "El.hpp"

namespace El {

template<typename T>
void GCDMatrix( Matrix<T>& G, Int m, Int n )
{
    DEBUG_ONLY(CallStackEntry cse("GCDMatrix"))
    G.Resize( m, n );
    auto gcdFill = []( Int i, Int j ) { return T(GCD(i+1,j+1)); };
    IndexDependentFill( G, function<T(Int,Int)>(gcdFill) );
}

template<typename T>
void GCDMatrix( AbstractDistMatrix<T>& G, Int m, Int n )
{
    DEBUG_ONLY(CallStackEntry cse("GCDMatrix"))
    G.Resize( m, n );
    auto gcdFill = []( Int i, Int j ) { return T(GCD(i+1,j+1)); };
    IndexDependentFill( G, function<T(Int,Int)>(gcdFill) );
}

template<typename T>
void GCDMatrix( AbstractBlockDistMatrix<T>& G, Int m, Int n )
{
    DEBUG_ONLY(CallStackEntry cse("GCDMatrix"))
    G.Resize( m, n );
    auto gcdFill = []( Int i, Int j ) { return T(GCD(i+1,j+1)); };
    IndexDependentFill( G, function<T(Int,Int)>(gcdFill) );
}

#define PROTO(T) \
  template void GCDMatrix( Matrix<T>& G, Int m, Int n ); \
  template void GCDMatrix( AbstractDistMatrix<T>& G, Int m, Int n ); \
  template void GCDMatrix( AbstractBlockDistMatrix<T>& G, Int m, Int n );

#define EL_ENABLE_QUAD
#include "El/macros/Instantiate.h"

} // namespace El
