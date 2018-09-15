#!/usr/bin/perl
# edit_server.cgi
# Display a text box for manually editing directives

require './nginx-lib.pl';
&ReadParse();

my $dir = "$config{'virt_dir'}";
my $file = "$dir/$in{'editfile'}";
if (!-e $file) {
  $file = "$in{'editfile'}";
}
if (!-e $file) {
  $file = "$config{'nginx_dir'}/$in{'editfile'}";
}

&ui_print_header($title, $text{'manual_title'}, "");
print &text('manual_header', "<tt>$file</tt>"),"<p>\n";

# textbox form
print &ui_form_start("edit_save.cgi", "form-data");
print &ui_hidden("editfile", $file),"\n";

$lref = &read_file_lines($file);
if (!defined($start)) {
	$start = 0;
	$end = @$lref - 1;
	}
for($i=$start; $i<=$end; $i++) {
	$buf .= $lref->[$i]."\n";
	}
print &ui_textarea("directives", $buf, 25, 80, undef, undef,"style='width:100%'"),"<br>\n";
print &ui_submit($text{'save'});
print &ui_form_end();

&ui_print_footer("$return", "server listing");