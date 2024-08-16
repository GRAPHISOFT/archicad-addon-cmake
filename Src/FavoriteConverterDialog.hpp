#ifndef GS_FAVORITE_COVNERTER_DIALOG_HPP
#define GS_FAVORITE_COVNERTER_DIALOG_HPP

#include "DGModule.hpp"
#include "ResourceIds.hpp"

namespace FC {

class Dialog :	public DG::ModalDialog,
						        public DG::PanelObserver,
						        public DG::ButtonItemObserver,
						        public DG::CompoundItemObserver
{
public:
	enum DialogResourceIds {
		DialogResourceId = ID_FAVORITE_CONVERTER_DLG,
		ConvertButtonId = 1,
		CancelButtonId = 2,
		SeparatorId = 3
	};

	Dialog ();

	virtual ~Dialog ();

private:
	virtual void PanelResized (const DG::PanelResizeEvent& ev) override;

	virtual void ButtonClicked (const DG::ButtonClickEvent& ev) override;

	DG::Button		convertButton;
	DG::Button		cancelButton;
	DG::Separator	separator;
};

} // namespace FC

#endif // GS_FAVORITE_COVNERTER_DIALOG_HPP