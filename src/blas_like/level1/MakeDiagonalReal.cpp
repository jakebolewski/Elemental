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
void MakeDiagonalReal( Matrix<T>& A, Int offset )
{
    DEBUG_ONLY(CallStackEntry cse("MakeDiagonalReal"))
    const Int iStart = Max(-offset,0);
    const Int jStart = Max( offset,0);
    const Int diagLength = A.DiagonalLength(offset);
    for( Int k=0; k<diagLength; ++k )
    {
        const Int i = iStart + k;
        const Int j = jStart + k;
        A.MakeReal( i, j );
    }
}

template<typename T>
void MakeDiagonalReal( AbstractDistMatrix<T>& A, Int offset )
{
    DEBUG_ONLY(CallStackEntry cse("MakeDiagonalReal"))
    const Int height = A.Height();
    const Int localWidth = A.LocalWidth();
    Matrix<T>& ALoc = A.Matrix();
    for( Int jLoc=0; jLoc<localWidth; ++jLoc )
    {
        const Int j = A.GlobalCol(jLoc);
        const Int i = j - offset;
        if( i < height && A.IsLocal(i,j) )
        {
            const Int iLoc = A.LocalRow(i);
            ALoc.MakeReal( iLoc, jLoc );
        }
    }
}

template<typename T>
void MakeDiagonalReal( AbstractBlockDistMatrix<T>& A, Int offset )
{
    DEBUG_ONLY(CallStackEntry cse("MakeDiagonalReal"))
    const Int height = A.Height();
    const Int localWidth = A.LocalWidth();
    Matrix<T>& ALoc = A.Matrix();
    for( Int jLoc=0; jLoc<localWidth; ++jLoc )
    {
        const Int j = A.GlobalCol(jLoc);
        const Int i = j - offset;
        if( i < height && A.IsLocal(i,j) )
        {
            const Int iLoc = A.LocalRow(i);
            ALoc.MakeReal( iLoc, jLoc );
        }
    }
}

#define PROTO(T) \
  template void MakeDiagonalReal( Matrix<T>& A, Int offset ); \
  template void MakeDiagonalReal( AbstractDistMatrix<T>& A, Int offset ); \
  template void MakeDiagonalReal( AbstractBlockDistMatrix<T>& A, Int offset ); 

#define EL_ENABLE_QUAD
#include "El/macros/Instantiate.h"

} // namespace El
