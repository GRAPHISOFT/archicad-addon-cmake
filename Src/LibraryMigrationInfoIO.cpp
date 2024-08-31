#include "LibraryMigrationInfoIO.hpp"

#include <fstream>
#include <string>
#include <vector>
#include <sstream>

namespace FC {

namespace {

bool SkipHeader (std::ifstream& csv)
{
	std::string line;
	return static_cast<bool> (std::getline (csv, line));
}

}

ACAPI::Result<std::vector<LibraryMigrationInfo>> LibraryMigrationInfoIO::ImportFrom (const IO::Location& csvFile)
{
	GS::UniString path;
	csvFile.ToPath (&path);
	std::ifstream csv (path.ToCStr ().Get ());

	if (!csv) {
		GS::UniString error = GS::UniString::Printf ("The %T file is not exist", path.ToPrintf ());
		return {ACAPI::Error (Error, error.ToCStr ().Get ()), ACAPI_GetToken ()};
	}

	if (!SkipHeader (csv)) {
		GS::UniString error = GS::UniString::Printf ("The %T file is empty", path.ToPrintf ());
		return {ACAPI::Error (Error, error.ToCStr ().Get ()), ACAPI_GetToken ()};
	}

	std::vector<LibraryMigrationInfo> result;

	std::string line;
	for (UIndex rowNumber = 2; std::getline (csv, line); ++rowNumber) {
		std::stringstream lineStream (line);
		std::string aclibGuid, aclibName, libpackGuid, libpack, libpackName;

		if (std::getline (lineStream, aclibGuid, '|') &&
			std::getline (lineStream, aclibName, '|') &&
			std::getline (lineStream, libpackGuid, '|') &&
			std::getline (lineStream, libpack, '|') &&
			std::getline (lineStream, libpackName, '|'))
		{
			result.push_back (LibraryMigrationInfo (GS::Guid (aclibGuid.c_str ()),
													GS::UniString (aclibName),
													GS::Guid (libpackGuid.c_str ()),
													GS::UniString (libpack),
													GS::UniString (libpackName)));
		} else {
			GS::UniString error = GS::UniString::Printf ("The #%d row is not well formatted in the %T file", rowNumber, path.ToPrintf ());
			return {ACAPI::Error (Error, error.ToCStr ().Get ()), ACAPI_GetToken ()};
		}
	}

	return ACAPI::Ok (result);
}

}