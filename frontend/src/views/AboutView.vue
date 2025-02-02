<template>
  <div class="about">
    <div class="container mb-4">
      <div class="w-50 mx-auto mb-4 text-center">
        <h1 class="mt-3">About Song of the Week</h1>
      </div>
    </div>
    <div class="container mb-4">
      <div class="w-75 mx-auto mb-4">
        <div class="accordion" id="aboutAccordion">
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse1" aria-expanded="false" aria-controls="collapse1">
                What is Song of the Week? 🗓️
              </button>
            </h2>
            <div id="collapse1" class="accordion-collapse collapse" data-bs-parent="#aboutAccordion">
              <div class="accordion-body">
                <p>
                  Song of the Week is meant to be a friendly competition where you and your friends can finally
                  determine who
                  has the best music taste through democracy!</p>
                <p>
                  It allows you to introduce your friends to new
                  music and learn more about them as you go along, creating a deeper understanding and connection
                  between you,
                  forming a bond that will last lifetimes or something, but it's mostly about winning.
                </p>
              </div>
            </div>
          </div>

          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse2" aria-expanded="false" aria-controls="collapse2">
                How does it work? 🤨
              </button>
            </h2>
            <div id="collapse2" class="accordion-collapse collapse" data-bs-parent="#aboutAccordion">
              <div class="accordion-body">
                <p>
                  Every week, you and whoever else is a part of your Song of the Week competition submit a song
                  anonymously in a
                  survey. Once everyone has submitted a song, a Spotify playlist composed of everyone's submission is
                  created
                  and made available to everyone in the competition.
                </p>
                <p>
                  Over the course of the next week, you and your friends will listen to the playlist and fill out the
                  next survey before the week ends. Each survey (except for the very
                  first one) will have you pick your favorite two songs from the playlist that week (votes for your own
                  song are
                  not counted for that song), match each of the players in the competition with one of the songs in the
                  playlist, and submit a new song for next week's playlist.
                </p>

                <p>
                  The results of the previous week's survey will be
                  shown on a day chosen by the Song of the Week competition creator. Once everyone has submitted a
                  response and you will see
                  song(s) got the most votes, which players got the most and least correct matches, and a breakdown of
                  who voted
                  for which song and who made each guess. The top voted song(s) each week will be added to a Song of the
                  Year
                  playlist available to everyone. The next playlist and a new survey will also be released with the
                  previous
                  week's results, and thus, the circle of Song of the Week continues.
                </p>
              </div>
            </div>
          </div>

          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse3" aria-expanded="false" aria-controls="collapse3">
                How many songs win each week? 🏆
              </button>
            </h2>
            <div id="collapse3" class="accordion-collapse collapse" data-bs-parent="#aboutAccordion">
              <div class="accordion-body">
                <p> The top two songs every week will win, unless there are ties. If there are ties for first, all songs
                  tied for first will make the
                  Song of the Year playlist, and no second place songs will be added. Likewise, if one song receives the
                  most votes but there is a tie
                  for second, all second place songs will make the Song of the Year.</p>
                <p> TL;DR - At least 2, but more if there are ties. </p>
              </div>
            </div>
          </div>

          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse7" aria-expanded="false" aria-controls="collapse3">
                Can I submit more than one song? 🤠
              </button>
            </h2>
            <div id="collapse7" class="accordion-collapse collapse" data-bs-parent="#aboutAccordion">
              <div class="accordion-body">
                <p>Absolutely not.</p>
              </div>
            </div>
          </div>

          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse4" aria-expanded="false" aria-controls="collapse3">
                Do I need a Spotify account? 🇸🇪
              </button>
            </h2>
            <div id="collapse4" class="accordion-collapse collapse" data-bs-parent="#aboutAccordion">
              <div class="accordion-body">
                <p>Yes. In addition, you must make sure your account is linked before attempting to join a Song of the
                  Week competition.</p>
              </div>
            </div>
          </div>

          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse5" aria-expanded="false" aria-controls="collapse3">
                How much does it cost? 🤑
              </button>
            </h2>
            <div id="collapse5" class="accordion-collapse collapse" data-bs-parent="#aboutAccordion">
              <div class="accordion-body">
                <p>Nothing at all! This is a hobby project and we do not plan to monetize it. Unless...?</p>
              </div>
            </div>
          </div>

          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse6" aria-expanded="false" aria-controls="collapse3">
                Are you going to sell my data? 😳
              </button>
            </h2>
            <div id="collapse6" class="accordion-collapse collapse" data-bs-parent="#aboutAccordion">
              <div class="accordion-body">
                <p>Absolutely not.</p>
              </div>
            </div>
          </div>

          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse8" aria-expanded="false" aria-controls="collapse3">
                Is this open source? 🧑‍💻
              </button>
            </h2>
            <div id="collapse8" class="accordion-collapse collapse" data-bs-parent="#aboutAccordion">
              <div class="accordion-body">
                <p><a href="https://github.com/orgs/Song-of-the-Week/repositories" class="text-primary text-decoration-none">Yes!</a></p>
              </div>
            </div>
          </div>

          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse9" aria-expanded="false" aria-controls="collapse3">
                Do you not have anything better to do with your time? 🤔
              </button>
            </h2>
            <div id="collapse9" class="accordion-collapse collapse" data-bs-parent="#aboutAccordion">
              <div class="accordion-body">
                <p>Absolutely not.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView'
};
</script>