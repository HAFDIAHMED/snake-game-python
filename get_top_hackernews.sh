#!/bin/bash

top_story=$(curl -s "https://news.ycombinator.com" | sed -n 's/.*<a href="\([^"]*\)" title=.*/\1/p' | head -n 1)
title=$(curl -s "https://news.ycombinator.com" | sed -n 's/.*title="\([^"]*\)".*/\1/p' | head -n 1)
points=$(curl -s "https://news.ycombinator.com" | sed -n 's/.*<span class="score">\([^<]*\)<\/span>.*/\1/p' | head -n 1)

echo "Top Story:"
echo "Title: $title"
echo "Link: $top_story"
echo "Points: $points"