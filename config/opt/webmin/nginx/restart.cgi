#!/usr/bin/perl
# reload.cgi
# reload nginx config file or restart nginx

require './nginx-lib.pl';
&ReadParse();

my $err = &test_config();
&error($err."will not reload") if ($err);
my $err = &reload_nginx();
&error($err) if ($err);
sleep(1);
&webmin_log("apply");
&redirect($in{'redir'});