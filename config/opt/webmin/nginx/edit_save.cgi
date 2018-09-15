#!/usr/bin/perl
# edit_save.cgi
# Save manually entered directives

require './nginx-lib.pl';
&ReadParseMime();

my $file = $in{'editfile'};

&lock_file($file);
$temp = &transname();
&copy_source_dest($file, $temp);
$in{'directives'} =~ s/\r//g;
$in{'directives'} =~ s/\s+$//;
@dirs = split(/\n/, $in{'directives'});
$lref = &read_file_lines($file);
if (!defined($start)) {
	$start = 0;
	$end = @$lref - 1;
	}
splice(@$lref, $start, $end-$start+1, @dirs);
&flush_file_lines();
if ($config{'test_manual'}) {
	$err = &test_config();
	if ($err) {
		&copy_source_dest($temp, $file);
		&error(&text('manual_etest', "<pre>$err</pre>"));
		}
}
unlink($temp);
&unlock_file($file);
&webmin_log("edit", "nginx_server", $file, \%in);

$config{'messages'} = $text{'msg_reload'};
save_module_config();
&redirect("$return");