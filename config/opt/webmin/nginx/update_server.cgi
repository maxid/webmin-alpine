#!/usr/bin/perl
# Update virtual servers (enable, disable, delete)

require './nginx-lib.pl';
&ReadParse();


my @serv = split(/\0/,$in{'d'});
my $dir = "$config{'virt_dir'}";
my $link_dir = "$config{'link_dir'}";
my $action = $in{'action'};

if ($action eq '_none') {
  return &redirect("");
}

foreach (@serv) {
  my $file = "$dir/$_";

  if ($action eq 'enable') {
    # create symlink
    my $err = &create_webfile_link($file);
    &error($err) if ($err);
  }

  if ($action eq 'disable') {
    # remove symlink
    my $err = &delete_webfile_link($file);
    &error($err) if ($err);
  }

  if ($action eq 'delete') {
    # delete file
    unlink($file);
    # test if file was deleted
    if (-e $file) {
      &error("The virtual server $_ was not deleted.");
    }
    # remove symlink
    my $err = &delete_webfile_link($file);
    &error($err) if ($err);
  }

  &webmin_log($action, 'nginx_server', $file);
}

$config{'messages'} = $text{'msg_reload'};
save_module_config();
&redirect("");
