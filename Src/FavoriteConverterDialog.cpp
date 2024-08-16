#include "FavoriteConverterDialog.hpp"

namespace FC {

Dialog::Dialog () :
    DG::ModalDialog (ACAPI_GetOwnResModule (), DialogResourceId, ACAPI_GetOwnResModule ()),
    convertButton (GetReference (), ConvertButtonId),
    cancelButton (GetReference (), CancelButtonId),
    separator (GetReference (), SeparatorId)
{
    AttachToAllItems (*this);
    Attach (*this);
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

} // namespace FC