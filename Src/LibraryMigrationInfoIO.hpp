#ifndef GS_LIBRARY_MIGRATION_INFO_IO_HPP
#define GS_LIBRARY_MIGRATION_INFO_IO_HPP

#include "Location.hpp"
#include "LibraryMigrationInfo.hpp"
#include "ACAPI/Result.hpp"

namespace FC::LibraryMigrationInfoIO {

ACAPI::Result<std::vector<LibraryMigrationInfo>> ImportFrom (const IO::Location& csvFile);

}

#endif