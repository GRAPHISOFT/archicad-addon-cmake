#include "FCDialog.hpp"


static const GSResID AddOnInfoID			= ID_ADDON_INFO;
	static const Int32 AddOnNameID			= 1;
	static const Int32 AddOnDescriptionID	= 2;

static const short FavoriteConverterMenuID			= ID_FAVORITE_CONVERTER_MENU;
	static const Int32 FavoriteConverterSubMenuID	= 1;


static GSErrCode MenuCommandHandler (const API_MenuParams *menuParams)
{
	switch (menuParams->menuItemRef.menuResID) {
		case FavoriteConverterMenuID:
			switch (menuParams->menuItemRef.itemIndex) {
				case FavoriteConverterSubMenuID:
					{
						FC::Dialog dialog;
						dialog.Invoke ();
					}
					break;
			}
			break;
	}
	return NoError;
}


API_AddonType CheckEnvironment (API_EnvirParams* envir)
{
	envir->addOnInfo.name = RSGetIndString (AddOnInfoID, AddOnNameID, ACAPI_GetOwnResModule ());
	envir->addOnInfo.description = RSGetIndString (AddOnInfoID, AddOnDescriptionID, ACAPI_GetOwnResModule ());

	return APIAddon_Normal;
}


GSErrCode RegisterInterface (void)
{
	return ACAPI_MenuItem_RegisterMenu (FavoriteConverterMenuID, 0, MenuCode_Tools, MenuFlag_Default);
}


GSErrCode Initialize (void)
{
	return ACAPI_MenuItem_InstallMenuHandler (FavoriteConverterMenuID, MenuCommandHandler);
}


GSErrCode FreeData (void)
{
	return NoError;
}
