/*
   Copyright (c) 2009-2015, Jack Poulson
   All rights reserved.

   This file is part of Elemental and is under the BSD 2-Clause License, 
   which can be found in the LICENSE file in the root directory, or at 
   http://opensource.org/licenses/BSD-2-Clause
*/
#include "El.hpp"
#include "El/config-internal.h"

namespace El {

template<typename G>
Memory<G>::Memory()
: size_(0), buffer_(nullptr)
{ }

template<typename G>
Memory<G>::Memory( size_t size )
: size_(0), buffer_(nullptr)
{ Require( size ); }

template<typename G>
Memory<G>::Memory( Memory<G>&& mem )
: size_(mem.size_), buffer_(nullptr)
{ ShallowSwap(mem); }

template<typename G>
Memory<G>& Memory<G>::operator=( Memory<G>&& mem )
{ ShallowSwap( mem ); return *this; }

template<typename G>
void Memory<G>::ShallowSwap( Memory<G>& mem )
{
    std::swap(size_,mem.size_);
    std::swap(buffer_,mem.buffer_);
}

template<typename G>
Memory<G>::~Memory() { delete[] buffer_; }

template<typename G>
G* Memory<G>::Buffer() const { return buffer_; }

template<typename G>
size_t  Memory<G>::Size() const { return size_; }

template<typename G>
G* Memory<G>::Require( size_t size )
{
    if( size > size_ )
    {
        delete[] buffer_;
#ifndef EL_RELEASE
        try {
#endif
            buffer_ = new G[size];
#ifndef EL_RELEASE
        } 
        catch( std::bad_alloc& e )
        {
            ostringstream os;
            os << "Failed to allocate " << size*sizeof(G) 
               << " bytes on process " << mpi::WorldRank() << endl;
            cerr << os.str();
            throw e;
        }
#endif
        size_ = size;
#ifdef EL_ZERO_INIT
        MemZero( buffer_, size_ );
#elif defined(EL_HAVE_VALGRIND)
        if( EL_RUNNING_ON_VALGRIND )
            MemZero( buffer_, size_ );
#endif
    }
    return buffer_;
}

template<typename G>
void Memory<G>::Release()
{  this->Empty(); }

template<typename G>
void Memory<G>::Empty()
{
    delete[] buffer_;
    size_ = 0;
    buffer_ = nullptr;
}

#define PROTO(T) \
  template class Memory<T>;

#define EL_ENABLE_QUAD
#include "El/macros/Instantiate.h"

} // namespace El
