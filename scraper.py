#!/usr/local/bin/python

import argparse
import datetime
from subprocess import call

URL = "http://kexp.org/playlist/"
date_format = "%d/%d/%d/%s"
file_format = "%d-%02d-%02d-%02d.html"

def scrape_year(outdir, year):
  for month in range(1, 13):
    for day in range(1, 32):
      #morning
      for hour in range(1, 13):
        scrape(outdir, year, month, day, hour, "am")
        scrape(outdir, year, month, day, hour, "pm")

def scrape(outdir, year, month, day, hour, pm):
  time = str(hour) + pm
  timestamp = date_format % (year, month, day, time)
  url = URL + timestamp

  if hour == 12 and pm == "am":
    hour = 0
  elif pm == "pm" and hour < 12:
    hour += 12

  filename = file_format % (year, month, day, hour)

  if outdir:
    cmd = "curl %s > %s/%s" % (url, outdir, filename)
  else:
    cmd = "curl %s > %s" % (url, filename)
  print cmd
  call(cmd, shell=True)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Downloads an entire year of KEXP playlist data, one hour at a time.")
  parser.add_argument("year", type=int, help="The year to scrape.")
  parser.add_argument("--outdir", type=str, help="The directory to place the scrape in.")

  args = parser.parse_args()

  print "scraping", args.year
  scrape_year(args.outdir, args.year)
