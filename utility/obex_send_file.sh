#!/usr/bin/expect
  exp_internal 1
  set address [lindex $argv 0]
  set file_path [lindex $argv 1]
  set prompt "#"
  spawn obexctl
  sleep 2
  expect -re $prompt
  send "connect $address\r"
  sleep 5
  send "send $file_path\r"
  sleep 2
  send "quit\r"