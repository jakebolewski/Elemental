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
void Copy( const Matrix<T>& A, Matrix<T>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy"))
    const Int height = A.Height();
    const Int width = A.Width();
    B.Resize( height, width ); 

    const Int ALDim = A.LDim();
    const Int BLDim = B.LDim();
    const T* ABuf = A.LockedBuffer();
    T* BBuf = B.Buffer();
    EL_PARALLEL_FOR
    for( Int j=0; j<width; ++j )
        MemCopy( &BBuf[j*BLDim], &ABuf[j*ALDim], height );
}

template<typename S,typename T>
void Copy( const Matrix<S>& A, Matrix<T>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy"))
    EntrywiseMap( A, B, function<T(S)>(&Caster<S,T>::Cast) );
}

template<typename T,Dist U,Dist V>
inline void Copy( const AbstractDistMatrix<T>& A, DistMatrix<T,U,V>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy"))
    B = A;
}

// Datatype conversions should not be very common, and so it is likely best to
// avoid explicitly instantiating every combination
template<typename S,typename T,Dist U,Dist V>
inline void Copy( const AbstractDistMatrix<S>& A, DistMatrix<T,U,V>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy"))
    if( A.Grid() == B.Grid() && A.ColDist() == U && A.RowDist() == V )
    {
        if( !B.RootConstrained() )
            B.SetRoot( A.Root() );
        if( !B.ColConstrained() )
            B.AlignCols( A.ColAlign() );
        if( !B.RowConstrained() )
            B.AlignRows( A.RowAlign() );
        if( A.Root() == B.Root() && 
            A.ColAlign() == B.ColAlign() && A.RowAlign() == B.RowAlign() )
        {
            B.Resize( A.Height(), A.Width() );
            Copy( A.LockedMatrix(), B.Matrix() );
            return;
        }
    }
    DistMatrix<S,U,V> BOrig(A.Grid());
    BOrig.AlignWith( B );
    BOrig = A;
    B.Resize( A.Height(), A.Width() );
    Copy( BOrig.LockedMatrix(), B.Matrix() );
}

template<typename T,Dist U,Dist V>
inline void Copy
( const AbstractBlockDistMatrix<T>& A, BlockDistMatrix<T,U,V>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy"))
    B = A;
}

// Datatype conversions should not be very common, and so it is likely best to
// avoid explicitly instantiating every combination
template<typename S,typename T,Dist U,Dist V>
inline void Copy
( const AbstractBlockDistMatrix<S>& A, BlockDistMatrix<T,U,V>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy"))
    if( A.Grid() == B.Grid() && A.ColDist() == U && A.RowDist() == V )
    {
        if( !B.RootConstrained() )
            B.SetRoot( A.Root() );
        if( !B.ColConstrained() )
            B.AlignColsWith( A.DistData() );
        if( !B.RowConstrained() )
            B.AlignRowsWith( A.DistData() );
        if( A.Root() == B.Root() && 
            A.ColAlign() == B.ColAlign() && 
            A.RowAlign() == B.RowAlign() && 
            A.ColCut() == B.ColCut() &&
            A.RowCut() == B.RowCut() )
        {
            B.Resize( A.Height(), A.Width() );
            Copy( A.LockedMatrix(), B.Matrix() );
            return;
        }
    }
    BlockDistMatrix<S,U,V> BOrig(A.Grid());
    BOrig.AlignWith( B );
    BOrig = A;
    B.Resize( A.Height(), A.Width() );
    Copy( BOrig.LockedMatrix(), B.Matrix() );
}

template<typename S,typename T>
void Copy( const AbstractDistMatrix<S>& A, AbstractDistMatrix<T>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy"))
    #define GUARD(CDIST,RDIST) B.ColDist() == CDIST && B.RowDist() == RDIST
    #define PAYLOAD(CDIST,RDIST) \
        auto& BCast = dynamic_cast<DistMatrix<T,CDIST,RDIST>&>(B); \
        Copy( A, BCast );
    #include "El/macros/GuardAndPayload.h"
}

template<typename S,typename T>
void Copy( const AbstractBlockDistMatrix<S>& A, AbstractBlockDistMatrix<T>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy"))
    #define GUARD(CDIST,RDIST) B.ColDist() == CDIST && B.RowDist() == RDIST
    #define PAYLOAD(CDIST,RDIST) \
        auto& BCast = dynamic_cast<BlockDistMatrix<T,CDIST,RDIST>&>(B); \
        Copy( A, BCast );
    #include "El/macros/GuardAndPayload.h"
}

void Copy( const Graph& A, Graph& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy [Graph]"))
    const Int numSources = A.NumSources();
    const Int numTargets = A.NumTargets();

    B.Resize( numSources, numTargets );
    // Directly assign instead of queueing up the individual edges
    B.sources_ = A.sources_;
    B.targets_ = A.targets_;
    B.consistent_ = A.consistent_;
    B.edgeOffsets_ = A.edgeOffsets_;
    B.MakeConsistent();
}

void Copy( const Graph& A, DistGraph& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy [Graph/DistGraph]"))
    const Int numSources = A.NumSources();
    const Int numTargets = A.NumTargets();

    B.SetComm( mpi::COMM_SELF );
    B.Resize( numSources, numTargets );
    // Directly assign instead of queueing up the individual edges
    B.sources_ = A.sources_;
    B.targets_ = A.targets_;
    B.consistent_ = A.consistent_;
    B.localEdgeOffsets_ = A.edgeOffsets_;
    B.MakeConsistent();
}

void Copy( const DistGraph& A, Graph& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy [DistGraph/Graph]"))
    const Int numSources = A.NumSources();
    const Int numTargets = A.NumTargets();
    mpi::Comm comm = A.Comm();
    if( mpi::Size(comm) != 1 )
        LogicError("Cannot yet construct sequential graph from distributed");

    B.Resize( numSources, numTargets );
    // Directly assign instead of queueing up the individual edges
    B.sources_ = A.sources_;
    B.targets_ = A.targets_;
    B.consistent_ = A.consistent_;
    B.edgeOffsets_ = A.localEdgeOffsets_;
    B.MakeConsistent();
}

void Copy( const DistGraph& A, DistGraph& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy [DistGraph]"))
    const Int numSources = A.NumSources();
    const Int numTargets = A.NumTargets();
    
    B.SetComm( A.Comm() );
    B.Resize( numSources, numTargets );
    // Directly assign instead of queueing up the individual edges
    B.sources_ = A.sources_;
    B.targets_ = A.targets_;
    B.consistent_ = A.consistent_;
    B.localEdgeOffsets_ = A.localEdgeOffsets_;
    B.MakeConsistent();
}

void CopyFromRoot( const DistGraph& distGraph, Graph& graph )
{
    DEBUG_ONLY(CallStackEntry cse("CopyFromRoot"))
    const mpi::Comm comm = distGraph.Comm();
    const int commSize = mpi::Size( comm );
    const int commRank = mpi::Rank( comm );

    const int numLocalEdges = distGraph.NumLocalEdges();
    vector<int> edgeSizes(commSize);
    mpi::AllGather( &numLocalEdges, 1, edgeSizes.data(), 1, comm );
    vector<int> edgeOffsets;
    const int numEdges = Scan( edgeSizes, edgeOffsets );

    graph.Resize( distGraph.NumSources(), distGraph.NumTargets() );
    graph.Reserve( numEdges );
    graph.sources_.resize( numEdges );
    graph.targets_.resize( numEdges );
    mpi::Gather
    ( distGraph.LockedSourceBuffer(), numLocalEdges,
      graph.SourceBuffer(), edgeSizes.data(), edgeOffsets.data(), 
      commRank, comm );
    mpi::Gather
    ( distGraph.LockedTargetBuffer(), numLocalEdges,
      graph.TargetBuffer(), edgeSizes.data(), edgeOffsets.data(), 
      commRank, comm );
    graph.MakeConsistent();
}

void CopyFromNonRoot( const DistGraph& distGraph, int root )
{
    DEBUG_ONLY(CallStackEntry cse("CopyFromRoot"))
    const mpi::Comm comm = distGraph.Comm();
    const int commSize = mpi::Size( comm );
    const int commRank = mpi::Rank( comm );
    if( commRank == root )
        LogicError("Root called CopyFromNonRoot");

    const int numLocalEdges = distGraph.NumLocalEdges();
    vector<int> edgeSizes(commSize);
    mpi::AllGather( &numLocalEdges, 1, edgeSizes.data(), 1, comm );
    vector<int> edgeOffsets;
    Scan( edgeSizes, edgeOffsets );

    mpi::Gather
    ( distGraph.LockedSourceBuffer(), numLocalEdges,
      (Int*)0, edgeSizes.data(), edgeOffsets.data(), root, comm );
    mpi::Gather
    ( distGraph.LockedTargetBuffer(), numLocalEdges,
      (Int*)0, edgeSizes.data(), edgeOffsets.data(), root, comm );
}

template<typename T>
void Copy( const SparseMatrix<T>& A, SparseMatrix<T>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy [SparseMatrix]"))
    B = A;
}

template<typename S,typename T>
void Copy( const SparseMatrix<S>& A, SparseMatrix<T>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy"))
    EntrywiseMap( A, B, function<T(S)>(&Caster<S,T>::Cast) );
}

template<typename S,typename T>
void Copy( const SparseMatrix<S>& A, Matrix<T>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy"))
    Zeros( B, A.Height(), A.Width() );
    for( Int k=0; k<A.NumEntries(); ++k )
        B.Update( A.Row(k), A.Col(k), Caster<S,T>::Cast(A.Value(k)) );
}

template<typename T>
void Copy( const DistSparseMatrix<T>& A, DistSparseMatrix<T>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy [DistSparseMatrix]"))
    B = A;
}

template<typename S,typename T>
void Copy( const DistSparseMatrix<S>& A, DistSparseMatrix<T>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy"))
    EntrywiseMap( A, B, function<T(S)>(&Caster<S,T>::Cast) );
}

template<typename S,typename T>
void Copy( const DistSparseMatrix<S>& A, AbstractDistMatrix<T>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy"))
    const Int m = A.Height();
    const Int n = A.Width();
    mpi::Comm comm = A.Comm();
    const Int commSize = mpi::Size( comm ); 
    if( !mpi::Congruent( B.Grid().Comm(), comm ) )
        LogicError("Communicators of A and B must be congruent");
    if( B.CrossSize() != 1 || B.RedundantSize() != 1 )
        LogicError("Trivial cross and redundant communicators required");

    Zeros( B, m, n );

    // Compute the number of entries of A to send to each member of B
    // ==============================================================
    vector<int> sendCounts(commSize,0);
    for( Int k=0; k<A.NumLocalEntries(); ++k )
    {
        const Int i = A.Row(k);
        const Int j = A.Col(k);
        ++sendCounts[ B.Owner(i,j) ];
    }

    // Pack the triplets
    // =================
    vector<int> sendOffs;
    const int totalSend = Scan( sendCounts, sendOffs );
    vector<ValueIntPair<T>> sendBuf(totalSend);
    auto offs = sendOffs;
    for( Int k=0; k<A.NumLocalEntries(); ++k )
    {
        const Int i = A.Row(k);
        const Int j = A.Col(k);
        const T value = Caster<S,T>::Cast(A.Value(k));
        const int owner = B.Owner(i,j);
        sendBuf[offs[owner]].indices[0] = i;
        sendBuf[offs[owner]].indices[1] = j;
        sendBuf[offs[owner]].value = value;
        ++offs[owner];
    }

    // Exchange and unpack the triplets
    // ================================
    auto recvBuf = mpi::AllToAll( sendBuf, sendCounts, sendOffs, comm );
    for( auto& entry : recvBuf )
        B.UpdateLocal
        ( B.LocalRow(entry.indices[0]), B.LocalCol(entry.indices[1]), 
          entry.value );
}

template<typename T>
void CopyFromRoot( const DistSparseMatrix<T>& ADist, SparseMatrix<T>& A )
{
    DEBUG_ONLY(CallStackEntry cse("CopyFromRoot"))
    const mpi::Comm comm = ADist.Comm();
    const int commSize = mpi::Size( comm );
    const int commRank = mpi::Rank( comm );

    const int numLocalEntries = ADist.NumLocalEntries();
    vector<int> entrySizes(commSize);
    mpi::AllGather( &numLocalEntries, 1, entrySizes.data(), 1, comm );
    vector<int> entryOffs;
    const int numEntries = Scan( entrySizes, entryOffs );

    A.Resize( ADist.Height(), ADist.Width() );
    A.Reserve( numEntries );
    A.graph_.sources_.resize( numEntries );
    A.graph_.targets_.resize( numEntries );
    A.vals_.resize( numEntries );
    mpi::Gather
    ( ADist.LockedSourceBuffer(), numLocalEntries,
      A.SourceBuffer(), entrySizes.data(), entryOffs.data(), 
      commRank, comm );
    mpi::Gather
    ( ADist.LockedTargetBuffer(), numLocalEntries,
      A.TargetBuffer(), entrySizes.data(), entryOffs.data(), 
      commRank, comm );
    mpi::Gather
    ( ADist.LockedValueBuffer(), numLocalEntries,
      A.ValueBuffer(), entrySizes.data(), entryOffs.data(), 
      commRank, comm );
    A.MakeConsistent();
}

template<typename T>
void CopyFromNonRoot( const DistSparseMatrix<T>& ADist, int root )
{
    DEBUG_ONLY(CallStackEntry cse("CopyFromRoot"))
    const mpi::Comm comm = ADist.Comm();
    const int commSize = mpi::Size( comm );
    const int commRank = mpi::Rank( comm );
    if( commRank == root )
        LogicError("Root called CopyFromNonRoot");

    const int numLocalEntries = ADist.NumLocalEntries();
    vector<int> entrySizes(commSize);
    mpi::AllGather( &numLocalEntries, 1, entrySizes.data(), 1, comm );
    vector<int> entryOffs;
    Scan( entrySizes, entryOffs );

    mpi::Gather
    ( ADist.LockedSourceBuffer(), numLocalEntries,
      (Int*)0, entrySizes.data(), entryOffs.data(), root, comm );
    mpi::Gather
    ( ADist.LockedTargetBuffer(), numLocalEntries,
      (Int*)0, entrySizes.data(), entryOffs.data(), root, comm );
    mpi::Gather
    ( ADist.LockedValueBuffer(), numLocalEntries,
      (T*)0, entrySizes.data(), entryOffs.data(), root, comm );
}

template<typename T>
void Copy( const DistMultiVec<T>& A, DistMultiVec<T>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy [DistMultiVec]"))
    B.SetComm( A.Comm() );
    B.Resize( A.Height(), A.Width() );
    B.Matrix() = A.LockedMatrix();
}

template<typename S,typename T>
void Copy( const DistMultiVec<S>& A, DistMultiVec<T>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy [DistMultiVec]"))
    EntrywiseMap( A, B, function<T(S)>(&Caster<S,T>::Cast) );
}

template<typename T>
void Copy( const DistMultiVec<T>& A, AbstractDistMatrix<T>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy [DistMultiVec -> ADM]"))
    const Int m = A.Height();
    const Int n = A.Width();
    const Int mLoc = A.LocalHeight();
    mpi::Comm comm = B.DistComm();
    const int commSize = mpi::Size(comm);
    if( B.CrossSize() != 1 || B.RedundantSize() != 1 )
        LogicError
        ("DistMultiVec -> ADM only supported with trivial cross and "
         "redundant sizes");

    B.Resize( m, n );
   
    // Compute the metadata
    // ====================
    vector<int> sendCounts(commSize,0);
    for( Int j=0; j<n; ++j )
        for( Int iLoc=0; iLoc<mLoc; ++iLoc )
            ++sendCounts[ B.Owner(A.GlobalRow(iLoc),j) ]; 

    // Pack
    // ====
    vector<int> sendOffs;
    const int totalSend = Scan( sendCounts, sendOffs );
    vector<ValueIntPair<T>> sendBuf(totalSend);
    auto offs = sendOffs;
    for( Int j=0; j<n; ++j )
    {
        for( Int iLoc=0; iLoc<mLoc; ++iLoc )
        {
            const Int i = A.GlobalRow(iLoc);
            const int owner = B.Owner(i,j);
            sendBuf[offs[owner]].indices[0] = i;
            sendBuf[offs[owner]].indices[1] = j;
            sendBuf[offs[owner]].value = A.GetLocal(iLoc,j);
            ++offs[owner];
        }
    }

    // Exchange and unpack
    // ===================
    auto recvBuf = mpi::AllToAll( sendBuf, sendCounts, sendOffs, comm );
    for( auto& entry : recvBuf )
        B.Set( entry.indices[0], entry.indices[1], entry.value );
}

template<typename T>
void Copy( const AbstractDistMatrix<T>& A, DistMultiVec<T>& B )
{
    DEBUG_ONLY(CallStackEntry cse("Copy [ADM -> DistMultiVec]"))
    const Int m = A.Height();
    const Int n = A.Width();
    const Int mLoc = A.LocalHeight();
    const Int nLoc = A.LocalWidth();
    mpi::Comm comm = B.Comm();
    const int commSize = mpi::Size(comm);
    if( A.CrossSize() != 1 || A.RedundantSize() != 1 )
        LogicError
        ("ADM -> DistMultiVec only supported with trivial cross and "
         "redundant sizes");

    B.Resize( m, n );
   
    // Compute the metadata
    // ====================
    vector<int> sendCounts(commSize,0);
    for( Int jLoc=0; jLoc<nLoc; ++jLoc )
        for( Int iLoc=0; iLoc<mLoc; ++iLoc )
            ++sendCounts[ B.RowOwner(A.GlobalRow(iLoc)) ]; 

    // Pack
    // ====
    vector<int> sendOffs;
    const int totalSend = Scan( sendCounts, sendOffs );
    vector<ValueIntPair<T>> sendBuf(totalSend);
    auto offs = sendOffs;
    for( Int jLoc=0; jLoc<nLoc; ++jLoc )
    {
        const Int j = A.GlobalCol(jLoc);
        for( Int iLoc=0; iLoc<mLoc; ++iLoc )
        {
            const Int i = A.GlobalRow(iLoc);
            const int owner = B.RowOwner(i);
            sendBuf[offs[owner]].indices[0] = i;
            sendBuf[offs[owner]].indices[1] = j;
            sendBuf[offs[owner]].value = A.GetLocal(iLoc,jLoc);
            ++offs[owner];
        }
    }

    // Exchange and unpack
    // ===================
    auto recvBuf = mpi::AllToAll( sendBuf, sendCounts, sendOffs, comm );
    for( auto& entry : recvBuf )
        B.SetLocal
        ( entry.indices[0]-B.FirstLocalRow(), entry.indices[1], entry.value );
}

template<typename T>
void CopyFromRoot( const DistMultiVec<T>& XDist, Matrix<T>& X )
{
    DEBUG_ONLY(CallStackEntry cse("CopyFromRoot"))
    const mpi::Comm comm = XDist.Comm();
    const int commSize = mpi::Size( comm );
    const int commRank = mpi::Rank( comm );

    const Int m = XDist.Height();
    const Int n = XDist.Width();
    const int numLocalEntries = XDist.LocalHeight()*n;
    vector<int> entrySizes(commSize);
    mpi::AllGather( &numLocalEntries, 1, entrySizes.data(), 1, comm );
    vector<int> entryOffs;
    const int numEntries = Scan( entrySizes, entryOffs );

    vector<T> recvBuf( numEntries );
    X.Resize( m, n, Max(m,1) );
    const auto& XDistLoc = XDist.LockedMatrix();
    if( XDistLoc.Height() == XDistLoc.LDim() )
    {
        mpi::Gather
        ( XDistLoc.LockedBuffer(), numLocalEntries,
          recvBuf.data(), entrySizes.data(), entryOffs.data(), 
          commRank, comm );
    }
    else
    {
        vector<T> sendBuf( numLocalEntries );
        for( Int jLoc=0; jLoc<XDistLoc.Width(); ++jLoc )
            for( Int iLoc=0; iLoc<XDistLoc.Height(); ++iLoc )
                sendBuf[iLoc+jLoc*XDistLoc.Height()] = XDistLoc.Get(iLoc,jLoc);
        mpi::Gather
        ( sendBuf.data(), numLocalEntries,
          recvBuf.data(), entrySizes.data(), entryOffs.data(), 
          commRank, comm );
    }
    for( Int q=0; q<commSize; ++q )
    {
        const Int iOff = entryOffs[q]/n;
        const Int iSize = entrySizes[q]/n;
        for( Int t=0; t<entrySizes[q]; ++t )
            X.Set( iOff+(t%iSize), t/iSize, recvBuf[entryOffs[q]+t] );
    }
}

template<typename T>
void CopyFromNonRoot( const DistMultiVec<T>& XDist, int root )
{
    DEBUG_ONLY(CallStackEntry cse("CopyFromNonRoot"))
    const mpi::Comm comm = XDist.Comm();
    const int commSize = mpi::Size( comm );
    const int commRank = mpi::Rank( comm );
    if( commRank == root )
        LogicError("Called CopyFromNonRoot from root");

    const int numLocalEntries = XDist.LocalHeight()*XDist.Width();
    vector<int> entrySizes(commSize);
    mpi::AllGather( &numLocalEntries, 1, entrySizes.data(), 1, comm );
    vector<int> entryOffs;
    Scan( entrySizes, entryOffs );

    const auto& XDistLoc = XDist.LockedMatrix();
    if( XDistLoc.Height() == XDistLoc.LDim() )
    {
        mpi::Gather
        ( XDistLoc.LockedBuffer(), numLocalEntries,
          (T*)0, entrySizes.data(), entryOffs.data(), root, comm );
    }
    else
    {
        vector<T> sendBuf( numLocalEntries );
        for( Int jLoc=0; jLoc<XDistLoc.Width(); ++jLoc )
            for( Int iLoc=0; iLoc<XDistLoc.Height(); ++iLoc )
                sendBuf[iLoc+jLoc*XDistLoc.Height()] = XDistLoc.Get(iLoc,jLoc);
        mpi::Gather
        ( sendBuf.data(), numLocalEntries,
          (T*)0, entrySizes.data(), entryOffs.data(), root, comm );
    }
}

#define CONVERT(S,T) \
  template void Copy( const Matrix<S>& A, Matrix<T>& B ); \
  template void Copy \
  ( const DistSparseMatrix<S>& A, AbstractDistMatrix<T>& B ); \
  template void Copy \
  ( const AbstractDistMatrix<S>& A, AbstractDistMatrix<T>& B ); \
  template void Copy \
  ( const AbstractBlockDistMatrix<S>& A, AbstractBlockDistMatrix<T>& B ); \
  template void Copy( const SparseMatrix<S>& A, SparseMatrix<T>& B ); \
  template void Copy( const DistSparseMatrix<S>& A, DistSparseMatrix<T>& B ); \
  template void Copy( const SparseMatrix<S>& A, Matrix<T>& B ); \
  template void Copy( const DistMultiVec<S>& A, DistMultiVec<T>& B );

#define SAME(T) \
  CONVERT(T,T) \
  template void CopyFromRoot \
  ( const DistSparseMatrix<T>& ADist, SparseMatrix<T>& A ); \
  template void CopyFromNonRoot( const DistSparseMatrix<T>& ADist, int root ); \
  template void Copy( const DistMultiVec<T>& A, AbstractDistMatrix<T>& B ); \
  template void Copy( const AbstractDistMatrix<T>& A, DistMultiVec<T>& B ); \
  template void CopyFromRoot( const DistMultiVec<T>& ADist, Matrix<T>& A ); \
  template void CopyFromNonRoot( const DistMultiVec<T>& ADist, int root );

#define PROTO_INT(T) SAME(T) 

#define PROTO_REAL(Real) \
  SAME(Real) \
  CONVERT(Int,Real) \
  CONVERT(Real,Complex<Real>)

#define PROTO_COMPLEX(C) \
  SAME(C) \
  CONVERT(Int,C)

#ifdef EL_HAVE_QUAD

#define PROTO_FLOAT \
  PROTO_REAL(float) \
  CONVERT(float,double) \
  CONVERT(float,Quad) \
  CONVERT(float,Complex<double>) \
  CONVERT(float,Complex<Quad>)

#define PROTO_DOUBLE \
  PROTO_REAL(double) \
  CONVERT(double,float) \
  CONVERT(double,Quad) \
  CONVERT(double,Complex<float>) \
  CONVERT(double,Complex<Quad>)

#define PROTO_QUAD \
  PROTO_REAL(Quad) \
  CONVERT(Quad,float) \
  CONVERT(Quad,double) \
  CONVERT(Quad,Complex<float>) \
  CONVERT(Quad,Complex<double>)

#define PROTO_COMPLEX_FLOAT \
  PROTO_COMPLEX(Complex<float>) \
  CONVERT(Complex<float>,Complex<double>) \
  CONVERT(Complex<float>,Complex<Quad>)

#define PROTO_COMPLEX_DOUBLE \
  PROTO_COMPLEX(Complex<double>) \
  CONVERT(Complex<double>,Complex<float>) \
  CONVERT(Complex<double>,Complex<Quad>)

#define PROTO_COMPLEX_QUAD \
  PROTO_COMPLEX(Complex<Quad>) \
  CONVERT(Complex<Quad>,Complex<float>) \
  CONVERT(Complex<Quad>,Complex<double>)

#else

#define PROTO_FLOAT \
  PROTO_REAL(float) \
  CONVERT(float,double) \
  CONVERT(float,Complex<double>)

#define PROTO_DOUBLE \
  PROTO_REAL(double) \
  CONVERT(double,float) \
  CONVERT(double,Complex<float>)

#define PROTO_COMPLEX_FLOAT \
  PROTO_COMPLEX(Complex<float>) \
  CONVERT(Complex<float>,Complex<double>)

#define PROTO_COMPLEX_DOUBLE \
  PROTO_COMPLEX(Complex<double>) \
  CONVERT(Complex<double>,Complex<float>)

#endif

#define EL_ENABLE_QUAD
#include "El/macros/Instantiate.h"

} // namespace El
