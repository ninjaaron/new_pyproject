#!/bin/sh
black --check {src_dir}
status=$?
if [ "$status" -ne 0 ]; then
  echo run black
fi
exit "$status"
