#!/usr/bin/perl
# index.cgi
# Display a list of all virtual servers, and links for various types

use HTML::Entities;
require './nginx-lib.pl';
&ReadParse();

# add virtual servers
my @virts = &get_servers();
foreach $v (@virts) {
  $idx = &indexof($v, @$conf);
  $sn = basename($v);
  $status = '<span style="color:darkgreen">' . $text{'status_enabled'} . '</span>';
  if (!-e "$config{'link_dir'}/$sn") {
    $status = $text{'status_disabled'};
  }
  push(@vidx, $sn);
  push(@vstatus, "$status");
  push(@vname, $sn);
  push(@vlink, "edit_server.cgi?editfile=$sn");
  push(@vroot, &find_directives($v, 'root'));
  push(@vurl, encode_entities(&find_directives($v, 'server_name')));
}

# Page header
&ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1, undef,
  &restart_button() . "<br>".
  &help_search_link("nginx", "man", "doc", "google"), undef, undef,
  &text('index_version', $nginfo{'version'}));

print '<div style="background:#fffdba; padding:10px; margin:20px 0;">' . $config{'messages'} . '</div>' if $config{'messages'};
$config{'messages'} = '';
save_module_config();
&ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1);

@tabs = (['global', 'Global Configuration'], ['existing', 'Existing Virtual Hosts'], ['create', 'Create Virtual Host']);

print ui_tabs_start(\@tabs, 'mode', 'existing');

print ui_tabs_start_tab('mode', 'global');
  $global_icon = { "icon" => "images/nginx_edit.png",
    "name" => $text{'gl_edit'},
    "link" => "edit_server.cgi?editfile=$config{'nginx_conf'}" };
  $proxy_icon = { "icon" => "images/edit_proxy.png",
    "name" => $text{'gl_proxy'},
    "link" => "edit_server.cgi?editfile=proxy.conf" };
  $det_icon = { "icon" => "images/nginx_details.png",
    "name" => $text{'gl_details'},
    "link" => "details.cgi" };
  &config_icons($global_icon, $proxy_icon, $det_icon);
print ui_tabs_end_tab('mode', 'global');

print ui_tabs_start_tab('mode', 'existing');
  @links = ( );
  push(@links, &select_all_link("d"), &select_invert_link("d"));
  print &ui_form_start("update_server.cgi", "get");
  print &ui_links_row(\@links);
  print &ui_columns_start([
    $text{'index_select'},
    $text{'index_status'},
    $text{'index_name'},
#     $text{'index_addr'},
#     $text{'index_port'},
    $text{'index_root'},
    $text{'index_url'} ], 100);
  for($i=0; $i<@vname; $i++) {
    my @cols;
    push(@cols, "$vstatus[$i]");
    push(@cols, "<a href=\"$vlink[$i]\">$vname[$i]</a>");
#     push(@cols, &html_escape($vaddr[$i]));
#     push(@cols, &html_escape($vport[$i]));
    push(@cols, &html_escape($vroot[$i]));
    push(@cols, "<a href=\"//$vurl[$i]\">$vurl[$i]</a>");
    print &ui_checked_columns_row(\@cols, undef,"d", $vidx[$i]);
  }
  print &ui_columns_end();
  print &ui_links_row(\@links);
  print &ui_select("action", "",
    [ ['_none', $text{'opt_select'}], ['enable', $text{'opt_enable'}], ['disable', $text{'opt_disable'}], ['delete', $text{'opt_delete'}] ]);
  print &ui_form_end([ [ "submit", $text{'btn_submit'} ] ]);
print ui_tabs_end_tab('mode', 'existing');

print ui_tabs_start_tab('mode', 'create');
  #plain open document creation here
  print &ui_form_start("create_server.cgi", "form-data");

    print &ui_table_start($text{'index_create'}, undef, 2);
    print &ui_table_row("Server Name",
      &ui_textbox("newserver", undef, 40));

    print &ui_table_row("Config",
      &ui_textarea("directives", undef, 25, 80, undef, undef,"style='width:100%'"));

    print &ui_table_row("",
      &ui_submit($text{'save'}));

    print &ui_table_end();
  print &ui_form_end();
print ui_tabs_end_tab('mode', 'create');

print ui_tabs_end();

ui_print_footer("/", $text{'index'});
