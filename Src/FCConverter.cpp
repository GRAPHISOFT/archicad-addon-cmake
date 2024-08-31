#include "FCConverter.hpp"

#include "ResourceIds.hpp"

#include "GSTime.hpp"

#include "LibraryMigrationInfoIO.hpp"

namespace {
	enum ConverterStrings {
		ConverterStringsResourceId = ID_FAVORITE_CONVERTER_CONVERTER_STRS,
		UniqueDestinationFolderNameBase = 1
	};
}

namespace FC {

Converter::Converter (const GS::UniString& sourceFolderPath,
					  const GS::UniString& destinationFolderPath) :
	sourceFolder (IO::Location (sourceFolderPath)),
	destinationFolder (GetUniqueDestinationFolder (destinationFolderPath))
{
	libpartPairsCsv = sourceFolder.GetLocation ();
	libpartPairsCsv.AppendToLocal (IO::Name ("favorite_converter_data"));
	libpartPairsCsv.AppendToLocal (IO::Name ("libpart_pairs.csv"));
}


Converter::~Converter () = default;

IO::Folder Converter::GetUniqueDestinationFolder (const GS::UniString& parentFolderPath)
{
	IO::Location workLocation = IO::Location (parentFolderPath);

	GS::UniString workString = RSGetIndString (ConverterStringsResourceId, UniqueDestinationFolderNameBase, ACAPI_GetOwnResModule ());
	workString.Append ("_");
	workString.Append (TIGetTimeString (TIGetTime ()));
	workString.ReplaceAll (" ", "_");
	workString.ReplaceAll (":", "_");
	workString.ReplaceAll ("/", "_");

	workLocation.AppendToLocal (IO::Name (workString));

	return IO::Folder (workLocation, IO::Folder::OnNotFound::Create);
}


void Converter::CopyToDestinationFolder ()
{
	auto copyOne = [&] (const IO::Name& name, bool isFolder) {
		if (isFolder || name.GetExtension () != "xml") {
			return;
		}
		sourceFolder.Copy (name, destinationFolder, name);
	};
	sourceFolder.Enumerate (copyOne);
}


void Converter::StartConversion ()
{

	/* ACAPI::Result<std::vector <LibraryMigrationInfo>> migrationInfo =  */LibraryMigrationInfoIO::ImportFrom (libpartPairsCsv);
	CopyToDestinationFolder ();
}

} // namespace FC