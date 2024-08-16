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

		FavoritesConverterToolGuideLinkId = 20
	};

	enum ToolGuideLinkStrings {
		ToolGuideLinkId = 1
	};

	virtual void PanelResized (const DG::PanelResizeEvent& ev) override;

	virtual void ButtonClicked (const DG::ButtonClickEvent& ev) override;
	
	virtual void StaticTextClicked (const DG::StaticTextClickEvent& ev) override;

	DG::Button		convertButton;
	DG::Button		cancelButton;
	DG::Separator	separator;
	UD::LinkText	toolGuideLink;
};

} // namespace FC

#endif // GS_FAVORITE_COVNERTER_DIALOG_HPP