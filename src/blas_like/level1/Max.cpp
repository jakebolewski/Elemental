/*
   Copyright (c) 2009-2015, Jack Poulson
   All rights reserved.

   This file is part of Elemental and is under the BSD 2-Clause License, 
   which can be found in the LICENSE file in the root directory, or at 
   http://opensource.org/licenses/BSD-2-Clause
*/
#include "El.hpp"

namespace El {

template<typename Real>
ValueInt<Real>
VectorMax( const Matrix<Real>& x )
{
    DEBUG_ONLY(CallStackEntry cse("VectorMax"))
    const Int m = x.Height();
    const Int n = x.Width();
    DEBUG_ONLY(
        if( m != 1 && n != 1 )
            LogicError("Input should have been a vector");
    )
    ValueInt<Real> pivot;
    if( Min(m,n) == 0 )
    {
        pivot.value = 0;
        pivot.index = -1;    
        return pivot;
    }

    pivot.value = x.Get(0,0);
    pivot.index = 0;
    if( n == 1 )
    {
        for( Int i=1; i<m; ++i )
        {
            const Real value = x.Get(i,0);
            if( value > pivot.value )
            {
                pivot.value = value;
                pivot.index = i;
            }
        }
    }
    else
    {
        for( Int j=1; j<n; ++j )
        {
            const Real value = x.Get(0,j);
            if( value > pivot.value )
            {
                pivot.value = value;
                pivot.index = j;
            }
        }
    }
    return pivot;
}

template<typename Real>
ValueInt<Real>
VectorMax( const AbstractDistMatrix<Real>& x )
{
    DEBUG_ONLY(CallStackEntry cse("VectorMax"))
    const Int m = x.Height();
    const Int n = x.Width();
    DEBUG_ONLY(
        if( m != 1 && n != 1 )
            LogicError("Input should have been a vector");
        if( !x.Grid().InGrid() )
            LogicError("viewing processes are not allowed");
    )
    ValueInt<Real> pivot;
    if( Min(m,n) == 0 )
    {
        pivot.value = 0;
        pivot.index = -1;
        return pivot;
    }
 
    ValueInt<Real> localPivot;
    localPivot.value = x.Get(0,0);
    localPivot.index = 0;
    if( x.Participating() )
    {
        if( n == 1 )
        {
            if( x.RowRank() == x.RowAlign() )
            {
                const Int mLocal = x.LocalHeight();
                for( Int iLoc=0; iLoc<mLocal; ++iLoc )
                {
                    const Real value = x.GetLocal(iLoc,0);
                    if( value > localPivot.value )
                    {
                        localPivot.value = value;
                        localPivot.index = x.GlobalRow(iLoc);
                    }
                }
            }
        }
        else
        {
            if( x.ColRank() == x.ColAlign() )
            {
                const Int nLocal = x.LocalWidth();
                for( Int jLoc=0; jLoc<nLocal; ++jLoc )
                {
                    const Real value = x.GetLocal(0,jLoc);
                    if( value > localPivot.value )
                    {
                        localPivot.value = value;
                        localPivot.index = x.GlobalCol(jLoc);
                    }
                }
            }
        }
        pivot = mpi::AllReduce
                ( localPivot, mpi::MaxLocOp<Real>(), x.DistComm() );
    }
    mpi::Broadcast( pivot.index, x.Root(), x.CrossComm() );
    mpi::Broadcast( pivot.value, x.Root(), x.CrossComm() );
    return pivot;
}

template<typename Real>
ValueInt<Real> VectorMax( const DistMultiVec<Real>& x )
{
    DEBUG_ONLY(CallStackEntry cse("VectorMax"))
    const Int height = x.Height();
    DEBUG_ONLY(
        if( x.Width() != 1 )
            LogicError("Input should have been a vector");
    )
    mpi::Comm comm = x.Comm();
    ValueInt<Real> pivot;
    if( height == 0 )
    {
        pivot.value = 0;
        pivot.index = -1;
        return pivot;
    }

    // Get a lower-bound for the maximum entry of the matrix to avoid cases
    // where a process does not own any data
    // =====================================================================
    const Real maxNorm = MaxNorm( x );
    ValueInt<Real> localPivot;
    localPivot.value = -maxNorm;
    localPivot.index = 0;
    const Int mLocal = x.LocalHeight();
    for( Int iLoc=0; iLoc<mLocal; ++iLoc )
    {
        const Real value = x.GetLocal(iLoc,0);
        if( value > localPivot.value )
        {
            localPivot.value = value;
            localPivot.index = x.GlobalRow(iLoc);
        }
    }
    pivot = mpi::AllReduce( localPivot, mpi::MaxLocOp<Real>(), comm );
    return pivot;
}

template<typename Real>
ValueIntPair<Real> Max( const Matrix<Real>& A )
{
    DEBUG_ONLY(CallStackEntry cse("Max"))
    const Int m = A.Height();
    const Int n = A.Width();

    ValueIntPair<Real> pivot;
    if( Min(m,n) == 0 )
    {
        pivot.value = 0;
        pivot.indices[0] = -1;
        pivot.indices[1] = -1;
        return pivot;
    }

    pivot.value = A.Get(0,0);
    pivot.indices[0] = 0;
    pivot.indices[1] = 0;
    for( Int j=0; j<n; ++j )
    {
        for( Int i=0; i<m; ++i )
        {
            const Real value = A.Get(i,j);
            if( value > pivot.value )
            {
                pivot.value = value;
                pivot.indices[0] = i;
                pivot.indices[1] = j;
            }
        }
    }
    return pivot;
}

template<typename Real>
ValueIntPair<Real> Max( const AbstractDistMatrix<Real>& A )
{
    DEBUG_ONLY(
        CallStackEntry cse("Max");
        if( !A.Grid().InGrid() )
            LogicError("Viewing processes are not allowed");
    )
    ValueIntPair<Real> pivot;
    if( Min(A.Height(),A.Width()) == 0 )
    {
        pivot.value = 0;
        pivot.indices[0] = -1;
        pivot.indices[1] = -1;
        return pivot;
    }

    ValueIntPair<Real> localPivot;
    localPivot.value = A.Get(0,0);
    localPivot.indices[0] = 0;
    localPivot.indices[1] = 0;
    if( A.Participating() )
    {
        // Store the index/value of the local pivot candidate
        const Int mLocal = A.LocalHeight();
        const Int nLocal = A.LocalWidth();
        for( Int jLoc=0; jLoc<nLocal; ++jLoc )
        {
            const Int j = A.GlobalCol(jLoc);
            for( Int iLoc=0; iLoc<mLocal; ++iLoc )
            {
                const Real value = A.GetLocal(iLoc,jLoc);
                if( value > localPivot.value )
                {
                    const Int i = A.GlobalRow(iLoc);
                    localPivot.value = value;
                    localPivot.indices[0] = i;
                    localPivot.indices[1] = j;
                }
            }
        }

        // Compute and store the location of the new pivot
        pivot = mpi::AllReduce
                ( localPivot, mpi::MaxLocPairOp<Real>(), A.DistComm() );
    }
    mpi::Broadcast( pivot.indices, 2, A.Root(), A.CrossComm() );
    mpi::Broadcast( pivot.value, A.Root(), A.CrossComm() );
    return pivot;
}

template<typename Real>
ValueIntPair<Real> SymmetricMax( UpperOrLower uplo, const Matrix<Real>& A )
{
    DEBUG_ONLY(
        CallStackEntry cse("SymmetricMax");
        if( A.Height() != A.Width() )
            LogicError("A must be square");
    )
    const Int n = A.Width();
    ValueIntPair<Real> pivot;
    if( n == 0 )
    {
        pivot.value = 0;
        pivot.indices[0] = -1;
        pivot.indices[1] = -1;
        return pivot;
    }

    pivot.value = A.Get(0,0);
    pivot.indices[0] = 0;
    pivot.indices[1] = 0;
    if( uplo == LOWER )
    {
        for( Int j=0; j<n; ++j )
        {
            for( Int i=j; i<n; ++i )
            {
                const Real value = A.Get(i,j);
                if( value > pivot.value )
                {
                    pivot.value = value;
                    pivot.indices[0] = i;
                    pivot.indices[1] = j;
                }
            }
        }
    }
    else
    {
        for( Int j=0; j<n; ++j ) 
        { 
            for( Int i=0; i<=j; ++i )
            {
                const Real value = A.Get(i,j);
                if( value > pivot.value )
                {
                    pivot.value = value;
                    pivot.indices[0] = i;
                    pivot.indices[1] = j;
                }
            }
        }
    }
    return pivot;
}

template<typename Real>
ValueIntPair<Real>
SymmetricMax( UpperOrLower uplo, const AbstractDistMatrix<Real>& A )
{
    DEBUG_ONLY(
        CallStackEntry cse("SymmetricMax");
        if( A.Height() != A.Width() )
            LogicError("A must be square");
        if( !A.Grid().InGrid() )
            LogicError("Viewing processes are not allowed");
    )
    const Int mLocal = A.LocalHeight();
    const Int nLocal = A.LocalWidth();

    ValueIntPair<Real> pivot;
    if( A.Height() == 0 )
    {
        pivot.value = 0;
        pivot.indices[0] = -1;
        pivot.indices[1] = -1;
        return pivot;
    }

    ValueIntPair<Real> localPivot;
    localPivot.value = A.Get(0,0);
    localPivot.indices[0] = 0;
    localPivot.indices[1] = 0;
    if( A.Participating() )
    {
        if( uplo == LOWER )
        {
            for( Int jLoc=0; jLoc<nLocal; ++jLoc )
            {
                const Int j = A.GlobalCol(jLoc);
                const Int mLocBefore = A.LocalRowOffset(j);
                for( Int iLoc=mLocBefore; iLoc<mLocal; ++iLoc )
                {
                    const Real value = A.GetLocal(iLoc,jLoc);
                    if( value > localPivot.value )
                    {
                        const Int i = A.GlobalRow(iLoc);
                        localPivot.value = value;
                        localPivot.indices[0] = i;
                        localPivot.indices[1] = j;
                    }
                }
            }
        }
        else
        {
            for( Int jLoc=0; jLoc<nLocal; ++jLoc )
            {
                const Int j = A.GlobalCol(jLoc);
                const Int mLocBefore = A.LocalRowOffset(j+1);
                for( Int iLoc=0; iLoc<mLocBefore; ++iLoc )
                {
                    const Real value = A.GetLocal(iLoc,jLoc);
                    if( value > localPivot.value )
                    {
                        const Int i = A.GlobalRow(iLoc);
                        localPivot.value = value;
                        localPivot.indices[0] = i;
                        localPivot.indices[1] = j;
                    }
                }
            }
        }

        // Compute and store the location of the new pivot
        pivot = mpi::AllReduce
                ( localPivot, mpi::MaxLocPairOp<Real>(), A.DistComm() );
    }
    mpi::Broadcast( pivot.indices, 2, A.Root(), A.CrossComm() );
    mpi::Broadcast( pivot.value, A.Root(), A.CrossComm() );
    return pivot;
}

#define PROTO(Real) \
  template ValueInt<Real> VectorMax( const Matrix<Real>& x ); \
  template ValueInt<Real> VectorMax( const AbstractDistMatrix<Real>& x ); \
  template ValueInt<Real> VectorMax( const DistMultiVec<Real>& x ); \
  template ValueIntPair<Real> Max( const Matrix<Real>& x ); \
  template ValueIntPair<Real> Max( const AbstractDistMatrix<Real>& x ); \
  template ValueIntPair<Real> SymmetricMax \
  ( UpperOrLower uplo, const Matrix<Real>& A ); \
  template ValueIntPair<Real> SymmetricMax \
  ( UpperOrLower uplo, const AbstractDistMatrix<Real>& A );

#define EL_NO_COMPLEX_PROTO
#define EL_ENABLE_QUAD
#include "El/macros/Instantiate.h"

} // namespace El
