#!/usr/bin/perl
# details.cgi
# Display list of nginx details

use strict;
use warnings;
require './nginx-lib.pl';
&ReadParse();

&ui_print_header($title, "Server Details", "");

  while ( my ($key, $value) = each(%nginfo) ) {
    print "$key => $value<br>";
  }

&ui_print_footer("$return", "nginx index");