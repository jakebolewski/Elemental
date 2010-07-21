/*
   Copyright (C) 2009-2010 Jack Poulson <jack.poulson@gmail.com>

   This file is part of Elemental.

   Elemental is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   Elemental is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with Elemental.  If not, see <http://www.gnu.org/licenses/>.
*/
#include "elemental/blas_internal.hpp"
#include "elemental/lapack_internal.hpp"
using namespace std;
using namespace elemental;

// On exit, the upper triangle of A is overwritten by R, and the Householder
// transforms that determine Q are stored below the diagonal of A with an 
// implicit one on the diagonal. 
//
// In the complex case, the column-vector s stores the unit-magnitude complex 
// rotations that map the norms of the implicit Householder vectors to their
// coefficient:  
//                tau_j = 2 psi_j / ( u_j^H u_j ),
// where psi_j is the j'th entry of s and u_j is the j'th unscaled Householder
// reflector.

template<typename R>
void
elemental::lapack::QR
( DistMatrix<R,MC,MR>& A )
{
#ifndef RELEASE
    PushCallStack("lapack::QR");
#endif
    const Grid& g = A.GetGrid();

    // Matrix views
    DistMatrix<R,MC,MR>
        ATL(g), ATR(g),  A00(g), A01(g), A02(g),  ALeftPan(g), ARightPan(g),
        ABL(g), ABR(g),  A10(g), A11(g), A12(g),
                         A20(g), A21(g), A22(g);

    PartitionDownLeftDiagonal
    ( A, ATL, ATR,
         ABL, ABR, 0 );
    while( ( ATL.Height() < A.Height() && ATL.Width() < A.Width() ) )
    {
        RepartitionDownDiagonal
        ( ATL, /**/ ATR,  A00, /**/ A01, A02,
         /*************/ /******************/
               /**/       A10, /**/ A11, A12,
          ABL, /**/ ABR,  A20, /**/ A21, A22 );

        ALeftPan.View2x1
        ( A11,
          A21 );

        ARightPan.View2x1
        ( A12,
          A22 );

        //--------------------------------------------------------------------//
        lapack::internal::PanelQR( ALeftPan );
        lapack::UT( Left, Lower, Normal, 0, ALeftPan, ARightPan );
        //--------------------------------------------------------------------//

        SlidePartitionDownDiagonal
        ( ATL, /**/ ATR,  A00, A01, /**/ A02,
               /**/       A10, A11, /**/ A12,
         /*************/ /******************/
          ABL, /**/ ABR,  A20, A21, /**/ A22 );
    }
#ifndef RELEASE
    PopCallStack();
#endif
}

#ifndef WITHOUT_COMPLEX
template<typename R>
void
elemental::lapack::QR
( DistMatrix<complex<R>,MC,MR  >& A, 
  DistMatrix<complex<R>,MD,Star>& t )
{
#ifndef RELEASE
    PushCallStack("lapack::QR");
    if( A.GetGrid() != t.GetGrid() )
        throw logic_error( "A and s must be distributed over the same grid." );
#endif
    const Grid& g = A.GetGrid();
#ifndef RELEASE
    if( t.Viewing() && 
        (t.Height() != min(A.Height(),A.Width()) || t.Width() != 1) )
        throw logic_error
              ( "t must be a column vector of the same height as the minimum "
                "dimension of A." );
    if( !t.AlignedWithDiag( A ) )
        throw logic_error( "t must be aligned with A's main diagonal." );
#endif
    typedef complex<R> C;
    if( !t.Viewing() )
    {
        if( !t.ConstrainedColAlignment() )
            t.AlignWithDiag( A );
        t.ResizeTo( min(A.Height(),A.Width()), 1 );
    }

    // Matrix views
    DistMatrix<C,MC,MR>
        ATL(g), ATR(g),  A00(g), A01(g), A02(g),  ALeftPan(g), ARightPan(g),
        ABL(g), ABR(g),  A10(g), A11(g), A12(g),
                         A20(g), A21(g), A22(g);
    DistMatrix<C,MD,Star>
        tT(g),  t0(g),
        tB(g),  t1(g),
                t2(g);

    PartitionDownLeftDiagonal
    ( A, ATL, ATR,
         ABL, ABR, 0 );
    PartitionDown
    ( t, tT,
         tB, 0 );
    while( ( ATL.Height() < A.Height() && ATL.Width() < A.Width() ) )
    {
        RepartitionDownDiagonal
        ( ATL, /**/ ATR,  A00, /**/ A01, A02,
         /*************/ /******************/
               /**/       A10, /**/ A11, A12,
          ABL, /**/ ABR,  A20, /**/ A21, A22 );

        RepartitionDown
        ( tT,  t0,
         /**/ /**/
               t1,
          tB,  t2 );

        ALeftPan.View2x1
        ( A11,
          A21 );

        ARightPan.View2x1
        ( A12,
          A22 );

        //--------------------------------------------------------------------//
        lapack::internal::PanelQR( ALeftPan, t1 );
        lapack::UT( Left, Lower, Normal, 0, ALeftPan, t1, ARightPan );
        //--------------------------------------------------------------------//

        SlidePartitionDownDiagonal
        ( ATL, /**/ ATR,  A00, A01, /**/ A02,
               /**/       A10, A11, /**/ A12,
         /*************/ /******************/
          ABL, /**/ ABR,  A20, A21, /**/ A22 );

        SlidePartitionDown
        ( tT,  t0,
               t1,
         /**/ /**/
          tB,  t2 );
    }
#ifndef RELEASE
    PopCallStack();
#endif
}
#endif

template void
elemental::lapack::QR
( DistMatrix<float,MC,MR>& A );

template void
elemental::lapack::QR
( DistMatrix<double,MC,MR>& A );

#ifndef WITHOUT_COMPLEX
template void
elemental::lapack::QR
( DistMatrix<scomplex,MC,MR  >& A,
  DistMatrix<scomplex,MD,Star>& t );

template void
elemental::lapack::QR
( DistMatrix<dcomplex,MC,MR  >& A,
  DistMatrix<dcomplex,MD,Star>& t );
#endif
