# Song of the Week Web Application Introduction
Song of the Week is a casual competition my friends and I have created to get to know each other's music tastes and to add a little competition to our lives every week. The way song of the week works is every week the participants submit a song that gets added to a shared playlist on Spotify that we all listen to over the following week. Then, we all fill out a Google form where we vote for our two favorite songs from this week's playlist, guess who submitted each song, and then submit a song for the next week's playlist. Additionally, we all eagerly await the results from each week's survey to see which song(s) won by votes (and thus will be added to the song of the year playlist), who submitted what songs, and who was the best and worst at guessing who submitted each song. As it stands, song of the week is facilitated by one of my friends who creates the Google form, creates the playlists, and posts the results of the Google form in our Discord server every week. This project aims to take the process of this friendly competition off of a single person's shoulders.

While this project is currently a work in progress, it will eventually be a web application built with Vue, Python, FastAPI, PostgreSQL, Celery, Redis, Nginx, and docker to containerize each piece all hosted on an AWS EC2 instance. These are the initial goals to get this set up for use by my friends. The web app will allow users to fill out the weekly survey, view weekly and older results, view weekly and older playlists as well as individualized playlists per user, and view and query raw data for individual analysis.

## Makefile

To run the application locally, run the following:
```bash
    make docker-build
    make docker-up
```