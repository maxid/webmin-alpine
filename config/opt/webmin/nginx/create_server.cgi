#!/usr/bin/perl
# create_server.cgi
# Create a new virtual host.

require './nginx-lib.pl';
&ReadParseMime();


my $dir = "$config{'virt_dir'}";
my $link_dir = "$config{'link_dir'}";
my $file = "$dir/$in{'newserver'}";
if (-e $file) {
  &error("This file already exists.");
}

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

my $err = &test_config();
&error($err."config errors, probably with your newest host.") if ($err);

unlink($temp);
&unlock_file($file);
&webmin_log("create", "nginx_server", $file, \%in);

if ($link_dir) {
	# create symlink for Debian style
	&create_webfile_link($file);

	if (!-e "$link_dir/$in{'newserver'}") {
		&error("Symlink couldn't be created.");
	}
}

&redirect("");