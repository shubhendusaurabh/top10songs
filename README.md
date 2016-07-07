top10songs
==========

Top 10 Songs

A Simple Django app built while learning django

[Top10Songs](http://www.top10songs.co.in "Top10Songs")

Workflow
========
*  heroku pg:backups capture
*  curl -o latest.dump `heroku pg:backups public-url`
*  cat latest.dump | docker exec -i api_postgres_1 pg_restore --verbose --clean --no-acl --no-owner -U postgres -d postgres