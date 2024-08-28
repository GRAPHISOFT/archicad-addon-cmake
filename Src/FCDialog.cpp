#include "FCDialog.hpp"

#include "FCConverter.hpp"

#include "DefaultProgramRunner.hpp"
#include "DGFolderDialog.hpp"

namespace FC {

Dialog::Dialog () :
    DG::ModalDialog (ACAPI_GetOwnResModule (), DialogResourceId, ACAPI_GetOwnResModule ()),
    convertButton (GetReference (), ConvertButtonId),
    cancelButton (GetReference (), CancelButtonId),
    separator (GetReference (), SeparatorId),
    
    toolGuideLink (GetReference (), FavoritesConverterToolGuideLinkId),
    
    sourceFolderTextEdit (GetReference (), SourceFolderTextEditId),
    browseSourceFolderButton (GetReference (), BrowseSourceFolderButtonId),
    destinationFolderTextEdit (GetReference (), DestinationFolderTextEditId),
    browseDestinationFolderButton (GetReference (), BrowseDestinationFolderButtonId),

    conversionFinishedText (GetReference (), ConversionFinishedTextId),
    conversionFinishedMoreDetailsText (GetReference (), ConversionFinishedMoreDetailsTextId),
    conversionLogFileLink (GetReference (), ConversionLogFileLinkId),
    parameterChangesFileLink (GetReference (), ParameterChangesFileLinkId)
{
    AttachToAllItems (*this);
    Attach (*this);

	toolGuideLink.SetLink (RSGetIndString (ID_FAVORITE_CONVERTER_TOOL_GUIDE_LINK_STRS, ToolGuideLinkId, ACAPI_GetOwnResModule ()));

    HideFinishRelatedItems ();
}


Dialog::~Dialog ()
{
    Detach (*this);
    DetachFromAllItems (*this);
}


void Dialog::HideFinishRelatedItems ()
{
    conversionFinishedText.Hide ();
    conversionFinishedMoreDetailsText.Hide ();
    conversionLogFileLink.Hide ();
    parameterChangesFileLink.Hide ();
}


void Dialog::ShowResult ()
{
    conversionFinishedText.Show ();
    conversionFinishedMoreDetailsText.Show ();
    conversionLogFileLink.Show ();
    parameterChangesFileLink.Show ();
}


void Dialog::Convert ()
{
    Converter converter (sourceFolderTextEdit.GetText (),
                         destinationFolderTextEdit.GetText ());
    converter.StartConversion ();
    ShowResult ();
}


GS::UniString Dialog::BrowseFolder ()
{
    DG::FolderDialog folderDialog;
    if (!folderDialog.Invoke ())
        return GS::EmptyUniString;

    return folderDialog.GetFolder ().ToDisplayText ();
}


void Dialog::BrowseSourceFolder ()
{
    const GS::UniString browsedFolder = BrowseFolder ();
    sourceFolderTextEdit.SetText (browsedFolder);
}


void Dialog::BrowseDestinationFolder ()
{
    const GS::UniString browsedFolder = BrowseFolder ();
    destinationFolderTextEdit.SetText (browsedFolder);
}


void Dialog::PanelResized (const DG::PanelResizeEvent& ev)
{
    BeginMoveResizeItems ();

    convertButton.Move (ev.GetHorizontalChange (), ev.GetVerticalChange ());
    cancelButton.Move (ev.GetHorizontalChange (), ev.GetVerticalChange ());
    separator.Resize(0, ev.GetVerticalChange ());

    sourceFolderTextEdit.Resize (ev.GetHorizontalChange (), 0);
    browseSourceFolderButton.Move (ev.GetHorizontalChange (), 0);
    destinationFolderTextEdit.Resize (ev.GetHorizontalChange (), 0);
    browseDestinationFolderButton.Move (ev.GetHorizontalChange (), 0);

    EndMoveResizeItems ();
}


void Dialog::ButtonClicked (const DG::ButtonClickEvent& ev)
{
    if (ev.GetSource () == &convertButton) {
        Convert ();
    } else if (ev.GetSource () == &cancelButton) {
        PostCloseRequest (DG::ModalDialog::Cancel);
    } else if (ev.GetSource () == &browseSourceFolderButton) {
        BrowseSourceFolder ();
    } else if (ev.GetSource () == &browseDestinationFolderButton) {
        BrowseDestinationFolder ();
    }
}


void Dialog::StaticTextClicked (const DG::StaticTextClickEvent& ev)
{
    if (ev.GetSource () == &toolGuideLink) {
		OSUtils::OpenWithDefaultBrowser (toolGuideLink.GetLinkTarget ());
	} else if (ev.GetSource () == &conversionLogFileLink) {
        OSUtils::OpenWithDefaultProgram (conversionLogFileLink.GetLinkTarget ());
    } else if (ev.GetSource () == &parameterChangesFileLink) {
        OSUtils::OpenWithDefaultProgram (parameterChangesFileLink.GetLinkTarget ());
    }
}

} // namespace FC