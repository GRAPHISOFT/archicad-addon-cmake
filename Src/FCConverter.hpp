#ifndef GS_FAVORITE_COVNERTER_CONVERTER_HPP
#define GS_FAVORITE_COVNERTER_CONVERTER_HPP

#include "Folder.hpp"

namespace FC {

class Converter {
public:
	Converter (const GS::UniString& sourceFolderPath,
			   const GS::UniString& destinationFolderPath);

	virtual ~Converter ();

	void StartConversion ();

private:
	IO::Folder GetUniqueDestinationFolder (const GS::UniString& parentFolderPath);

	void CopyToDestinationFolder ();

	IO::Folder sourceFolder;
	IO::Folder destinationFolder;
	IO::Location libpartPairsCsv;
};

} // namespace FC

#endif // GS_FAVORITE_COVNERTER_CONVERTER_HPP