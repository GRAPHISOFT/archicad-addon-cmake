#ifndef GS_LIBRARY_MIGRATION_INFO_HPP
#define GS_LIBRARY_MIGRATION_INFO_HPP

#include "Location.hpp"
#include "LibraryMigrationInfo.hpp"

namespace FC {

class LibraryMigrationInfo {
public:
	LibraryMigrationInfo (GS::Guid aclibGuid, GS::UniString aclibName, GS::Guid libpackGuid, GS::UniString libpack, GS::UniString libpackName);
	virtual ~LibraryMigrationInfo ();

	GS::Guid GetAclibGuid () const;
	GS::UniString GetAclibName () const;
	GS::Guid GetLibpackGuid () const;
	GS::UniString GetLibpack () const;
	GS::UniString GetLibpackName () const;

private:
	GS::Guid aclibGuid;
	GS::UniString aclibName;
	GS::Guid libpackGuid;
	GS::UniString libpack;
	GS::UniString libpackName;
};

}

#endif