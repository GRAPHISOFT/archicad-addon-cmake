#! /usr/bin/perl -w

use FindBin ;
use File::Spec::Functions qw(splitpath catfile updir);
use File::Copy;
use Cwd;
use feature 'unicode_strings';

#-----------------------------------------------------------------------
# Executes one GRC conversion command
#-----------------------------------------------------------------------
sub DoGRC ($$$$$$$)
{
	my ($tool, $headerDir, $sourceDir, $inputFile, $devKitDir, $destinationDir, $outputFile) = @_ ;
	my $incHeaderDir = catfile (Cwd::realpath ($devKitDir), "Support", "Inc");

	system ("mkdir -p \"" . $destinationDir . "\"") ;
	print "\t$inputFile\n";

	system ("xcrun clang -x c++ -E -P -DPREPROCESS_GRC -DGS_64BIT -Dmacintosh -DINT__APP -I \"" . $headerDir . "\" -I \"" . $incHeaderDir . "\" \"" . catfile ($sourceDir, $inputFile) . "\" > \"" . catfile ($destinationDir, $outputFile .".i") . "\"");
	system ($tool . " -m r -q utf8 utf16 -T M -n -i \"" . catfile ($destinationDir, $outputFile .".i") . "\" -p \"" . catfile ($sourceDir, "Images") . "\" -o \"" . catfile ($destinationDir, $outputFile) . "\" -w 2");
}


#-----------------------------------------------------------------------
# Convert GRC
#-----------------------------------------------------------------------
print "Converting resource files:\n";

my $devKitDir = catfile ($ARGV[0]);
my $makeResConvTool = "\"" . catfile (Cwd::realpath ($devKitDir), "Support", "Tools", "OSX", "ResConv") . "\"";

my $addOnResourcesPath = Cwd::realpath (catfile ($FindBin::Bin, updir ()));
my $addOnRootPath = Cwd::realpath (catfile ($addOnResourcesPath, updir ()));
my $resTarget = catfile ($ARGV[2]);
my $locResTarget = catfile ($resTarget, "English.lproj");
my $roFolder = catfile ($ARGV[1], "RO");
my $rfixFolder = catfile ($addOnResourcesPath, "RFIX");
my $rintFolder = catfile ($addOnResourcesPath, "RINT");
my $srcFolder = catfile ($addOnRootPath, "AddOn");

my @files;

opendir (DIR, $rfixFolder);
@files = readdir (DIR);
closedir (DIR);

foreach $path (@files) {
	($volume,$directories,$file) = splitpath ($path);
	DoGRC ($makeResConvTool, $srcFolder, $rfixFolder, $file, $devKitDir, $roFolder, $file . ".ro") if ($file =~ /.*\.grc$/i);
}

opendir (DIR, $rintFolder);
@files = readdir (DIR);
closedir (DIR);

foreach $path (@files) {
	($volume,$directories,$file) = splitpath ($path);
	DoGRC ($makeResConvTool, $srcFolder, $rintFolder, $file, $devKitDir, $roFolder, $file . ".ro") if ($file =~ /.*\.grc$/i);
}

opendir (DIR, $roFolder);
@files = readdir (DIR);
closedir (DIR);

system ("mkdir -p \"" . $locResTarget . "\"") ;

foreach $file (@files) {
	if ($file =~ /.*\.tif$/) {
		copy (catfile ($roFolder, $file), $resTarget);
	} elsif ($file =~ /.*\.rsrd$/) {
		copy (catfile ($roFolder, $file), $locResTarget);
	}
}

my $locStrings = catfile ($locResTarget, "Localizable.strings");

# create the output Localizable.strings file
open (OFILE, ">:encoding(UTF-16LE)", $locStrings) or die "Can't create $locStrings: $!";
my $buf = "\x{feff}";
print OFILE $buf;

printf "\t=> Localizable.strings\n";

# collect all files from the RO folder
opendir (DIR, $roFolder);
@files = readdir (DIR);
closedir (DIR);

# enable slurp mode
undef $/;

foreach $file (@files) {
	if ($file =~ /.*\.strings$/) {
		printf "\t\t$file\n";
		my $stringsFile = catfile ($roFolder, $file);
		if ((stat ($stringsFile))[7] > 2) {		# check file size
			open (IFILE, "<:encoding(UTF-16LE)", $stringsFile) or die "Can't open $stringsFile: $!";

			# skip byte order mark
			read (IFILE, $buf, 1);
			if ($buf ne "\x{feff}") {
				print OFILE $buf;
			}

			my $content = <IFILE>;
			close (IFILE);

			print OFILE $content;
		}
	}
}

close (OFILE) or die "Can't close $locStrings: $!";

print "done.\n";
