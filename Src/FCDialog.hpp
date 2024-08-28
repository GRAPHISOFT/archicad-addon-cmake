#ifndef GS_FAVORITE_COVNERTER_DIALOG_HPP
#define GS_FAVORITE_COVNERTER_DIALOG_HPP

#include "ResourceIds.hpp"

#include "DGModule.hpp"
#include "UDLinkText.hpp"

namespace FC {

class Dialog :	public DG::ModalDialog,
				public DG::PanelObserver,
				public DG::ButtonItemObserver,
				public DG::CompoundItemObserver,
				public UD::LinkTextObserver
{
public:
	Dialog ();

	virtual ~Dialog ();

private:
	enum DialogResourceIds {
		DialogResourceId = ID_FAVORITE_CONVERTER_DLG,
		ConvertButtonId = 1,
		CancelButtonId = 2,
		SeparatorId = 3,

		FavoritesConverterToolGuideLinkId = 20,

		SourceFolderTextEditId = 22,
		BrowseSourceFolderButtonId = 23,
		DestinationFolderTextEditId = 25,
		BrowseDestinationFolderButtonId = 26,

		ConversionFinishedTextId = 27,
		ConversionFinishedMoreDetailsTextId = 28,
		ConversionLogFileLinkId = 29,
		ParameterChangesFileLinkId = 30
	};

	enum ToolGuideLinkStrings {
		ToolGuideLinkId = 1
	};

	void HideFinishRelatedItems ();
	void ShowResult ();

	void Convert ();

	GS::UniString BrowseFolder ();

	void BrowseSourceFolder ();
	void BrowseDestinationFolder ();

	virtual void PanelResized (const DG::PanelResizeEvent& ev) override;
	virtual void ButtonClicked (const DG::ButtonClickEvent& ev) override;
	virtual void StaticTextClicked (const DG::StaticTextClickEvent& ev) override;

	DG::Button		convertButton;
	DG::Button		cancelButton;
	
	DG::Separator	separator;
	
	UD::LinkText	toolGuideLink;
	
	DG::TextEdit	sourceFolderTextEdit;
	DG::Button		browseSourceFolderButton;
	DG::TextEdit	destinationFolderTextEdit;
	DG::Button		browseDestinationFolderButton;

	DG::LeftText	conversionFinishedText;
	DG::LeftText	conversionFinishedMoreDetailsText;
	
	UD::LinkText	conversionLogFileLink;
	UD::LinkText	parameterChangesFileLink;
};

} // namespace FC

#endif // GS_FAVORITE_COVNERTER_DIALOG_HPP