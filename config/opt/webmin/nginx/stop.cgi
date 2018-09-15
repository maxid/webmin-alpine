#!/usr/bin/perl
# stop.cgi
# Stop the running nginx server

require './nginx-lib.pl';
&ReadParse();

my $err = &stop_nginx();
&error($err) if ($err);
sleep(1);
&webmin_log("stop");
&redirect($in{'redir'});