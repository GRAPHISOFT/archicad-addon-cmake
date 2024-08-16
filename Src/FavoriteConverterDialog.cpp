#include "FavoriteConverterDialog.hpp"

#include "DefaultProgramRunner.hpp"

namespace FC {

Dialog::Dialog () :
    DG::ModalDialog (ACAPI_GetOwnResModule (), DialogResourceId, ACAPI_GetOwnResModule ()),
    convertButton (GetReference (), ConvertButtonId),
    cancelButton (GetReference (), CancelButtonId),
    separator (GetReference (), SeparatorId),
    toolGuideLink (GetReference (), FavoritesConverterToolGuideLinkId)
{
    AttachToAllItems (*this);
    Attach (*this);

	toolGuideLink.SetLink (RSGetIndString (ID_FAVORITE_CONVERTER_TOOL_GUIDE_LINK_STRS, ToolGuideLinkId, ACAPI_GetOwnResModule ()));
}


Dialog::~Dialog ()
{
    Detach (*this);
    DetachFromAllItems (*this);
}


void Dialog::PanelResized (const DG::PanelResizeEvent& ev)
{
    BeginMoveResizeItems ();
    convertButton.Move (ev.GetHorizontalChange (), ev.GetVerticalChange ());
    cancelButton.Move (ev.GetHorizontalChange (), ev.GetVerticalChange ());
    separator.Resize(0, ev.GetVerticalChange ());
    EndMoveResizeItems ();
}


void Dialog::ButtonClicked (const DG::ButtonClickEvent& ev)
{
    if (ev.GetSource () == &convertButton) {
        PostCloseRequest (DG::ModalDialog::Accept);
    } else if (ev.GetSource () == &cancelButton) {
        PostCloseRequest (DG::ModalDialog::Cancel);
    }
}


void Dialog::StaticTextClicked (const DG::StaticTextClickEvent& ev)
{
    if (ev.GetSource () == &toolGuideLink) {
		OSUtils::OpenWithDefaultBrowser (toolGuideLink.GetLinkTarget ());
	}
}

} // namespace FC