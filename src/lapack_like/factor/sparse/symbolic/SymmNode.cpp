/*
   Copyright 2009-2011, Jack Poulson.
   All rights reserved.

   Copyright 2011-2012, Jack Poulson, Lexing Ying, and 
   The University of Texas at Austin.
   All rights reserved.

   Copyright 2013, Jack Poulson, Lexing Ying, and Stanford University.
   All rights reserved.

   Copyright 2013-2014, Jack Poulson and The Georgia Institute of Technology.
   All rights reserved.

   Copyright 2014-2015, Jack Poulson and Stanford University.
   All rights reserved.
   
   This file is part of Elemental and is under the BSD 2-Clause License, 
   which can be found in the LICENSE file in the root directory, or at 
   http://opensource.org/licenses/BSD-2-Clause
*/
#include "El.hpp"

namespace El {

SymmNode::SymmNode( SymmNode* parentNode )
: parent(parentNode), duplicate(nullptr)
{ }

SymmNode::SymmNode( DistSymmNode* duplicateNode )
: parent(nullptr), duplicate(duplicateNode)
{
    size = duplicate->size;
    off = duplicate->off;
    lowerStruct = duplicate->lowerStruct;
}

SymmNode::~SymmNode()
{
    if( uncaught_exception() )
    {
        cerr << "Uncaught exception" << endl;
        DEBUG_ONLY(DumpCallStack())
        return;
    }

    for( const SymmNode* child : children )
        delete child;
}

} // namespace El
