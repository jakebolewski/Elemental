/*
   Copyright (c) 2009-2014, Jack Poulson
   All rights reserved.

   This file is part of Elemental and is under the BSD 2-Clause License, 
   which can be found in the LICENSE file in the root directory, or at 
   http://opensource.org/licenses/BSD-2-Clause
*/
#pragma once
#ifndef ELEM_BIDIAG_PANELL_HPP
#define ELEM_BIDIAG_PANELL_HPP

#include ELEM_AXPY_INC
#include ELEM_CONJUGATE_INC
#include ELEM_SCALE_INC
#include ELEM_GEMV_INC

#include ELEM_REFLECTOR_INC

namespace elem {
namespace bidiag {

template<typename F> 
inline void
PanelL
( DistMatrix<F>& A, 
  DistMatrix<F,MD,STAR>& tP,
  DistMatrix<F,MD,STAR>& tQ,
  DistMatrix<F>& X, 
  DistMatrix<F>& Y,
  DistMatrix<F,MC,STAR>& AColPan_MC_STAR,
  DistMatrix<F,STAR,MR>& ARowPan_STAR_MR )
{
    DEBUG_ONLY(
        CallStackEntry cse("bidiag::PanelL");
        if( A.Grid() != tP.Grid() || tP.Grid() != tQ.Grid() || 
            tQ.Grid() != X.Grid() || X.Grid() != Y.Grid() ||
            Y.Grid() != AColPan_MC_STAR.Grid() || 
            Y.Grid() != ARowPan_STAR_MR.Grid() )
            LogicError("Grids must match");
        const Int panelSize = X.Width();
        if( A.Height() > A.Width() )
            LogicError("A must be at least as wide as it is tall");
        if( A.Height() != X.Height() )
            LogicError("A and X must be the same height");
        if( A.Width() != Y.Height() )
            LogicError("Y must be the same height as A's width");
        if( X.Height() < panelSize )
            LogicError("X must be a column panel");
        if( Y.Width() != panelSize )
            LogicError("Y is the wrong width");
        if( A.ColAlign() != X.ColAlign() || 
            A.RowAlign() != X.RowAlign() )
            LogicError("A and X must be aligned");
        if( A.ColAlign() != Y.ColAlign() || A.RowAlign() != Y.RowAlign() )
            LogicError("A and Y must be aligned");
    )
    LogicError("This routine is not yet written");
}

} // namespace bidiag
} // namespace elem

#endif // ifndef ELEM_BIDIAG_PANELL_HPP