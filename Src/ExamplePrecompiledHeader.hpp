#ifndef GS_EXAMPLE_PRECOMPILED_HEADER_HPP
#define GS_EXAMPLE_PRECOMPILED_HEADER_HPP

#include <GSNew.hpp>
#include <GSMalloc.hpp>

#if defined (macintosh)
namespace std {
    void *GS_realloc (void *userData, size_t newSize);
}
#endif

#include <limits.h>
#include <math.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <vector>
#include <unordered_map>
#include <memory>

#if defined(WINDOWS)
#include "Win32Interface.hpp"
#endif

#include "APIEnvir.h"
#include "ACAPinc.h"

#endif // GS_EXAMPLE_PRECOMPILED_HEADER_HPP
