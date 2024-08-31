#include "LibraryMigrationInfo.hpp"

namespace FC {

LibraryMigrationInfo::LibraryMigrationInfo (GS::Guid aclibGuid, GS::UniString aclibName, GS::Guid libpackGuid, GS::UniString libpack, GS::UniString libpackName) :
	aclibGuid (aclibGuid), aclibName (aclibName), libpackGuid (libpackGuid), libpack (libpack), libpackName (libpackName)
{
}

LibraryMigrationInfo::~LibraryMigrationInfo () {}

GS::Guid LibraryMigrationInfo::GetAclibGuid () const
{
	return aclibGuid;
}

GS::UniString LibraryMigrationInfo::GetAclibName () const
{
	return aclibName;
}

GS::Guid LibraryMigrationInfo::GetLibpackGuid () const
{
	return libpackGuid;
}

GS::UniString LibraryMigrationInfo::GetLibpack () const
{
	return libpack;
}

GS::UniString LibraryMigrationInfo::GetLibpackName () const
{
	return libpackName;
}

}