<template>
  <div class="about">
    <CContainer class="mb-4">
      <div class="w-50 mx-auto mb-4 text-center">
      <h1 class="mt-3">About Song of the Week</h1>
      </div>
      </CContainer>
    <CContainer class="mb-4">
          <div class="w-75 mx-auto mb-4">
          <CAccordion>
            <CAccordionItem :item-key="1">
              <CAccordionHeader>
                What is Song of the Week?
              </CAccordionHeader>
              <CAccordionBody>
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
              </CAccordionBody>
            </CAccordionItem>
            <CAccordionItem :item-key="2">
              <CAccordionHeader>
                How Does It Work?
              </CAccordionHeader>
              <CAccordionBody>
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
              </CAccordionBody>
            </CAccordionItem>
            <CAccordionItem :item-key="3">
              <CAccordionHeader>
                How Many Songs Win Each Week?
              </CAccordionHeader>
              <CAccordionBody>
                <p>
                  The top two songs every week will win, unless there are ties. If there are ties for first, all songs
                  tied for first will make the
                  Song of the Year playlist, and no second place songs will be added. Likewise, if one song receives the
                  most votes but there is a tie
                  for second, all second place songs will make the Song of the Year.
                </p>
              </CAccordionBody>
            </CAccordionItem>

            <CAccordionItem :item-key="4">
              <CAccordionHeader>
                Do I Need A Spotify Account?
              </CAccordionHeader>
              <CAccordionBody>
                <p>
                  Yes. In addition, you must make sure your account is linked before attempting to join a Song of the
                  Week competition.
                </p>
              </CAccordionBody>
            </CAccordionItem>

            <CAccordionItem :item-key="5">
              <CAccordionHeader>
                How Much Does It Cost?
              </CAccordionHeader>
              <CAccordionBody>
                <p>
                  Nothing at all! This is a hobby project and we do not plan to monetize it. Unless...?
                </p>
              </CAccordionBody>
            </CAccordionItem>

            <CAccordionItem :item-key="6">
              <CAccordionHeader>
                Are You Going to Sell My Data?
              </CAccordionHeader>
              <CAccordionBody>
                <p>
                  Absolutely not.
                </p>
              </CAccordionBody>
            </CAccordionItem>

            <CAccordionItem :item-key="7">
              <CAccordionHeader>
                Is This Open Source?
              </CAccordionHeader>
              <CAccordionBody>
                  <p>
                    <a href="https://github.com/orgs/Song-of-the-Week/repositories" class="text-primary text-decoration-none">Yes!</a>
                  </p>
              </CAccordionBody>
            </CAccordionItem>

            <CAccordionItem :item-key="8">
              <CAccordionHeader>
                Do You Not Have Anything Better to Do With Your Time?
              </CAccordionHeader>
              <CAccordionBody>
                  <p>
                    Absolutely not.
                  </p>
              </CAccordionBody>
            </CAccordionItem>
          </CAccordion>
          </div>
        </CContainer>
  </div>
</template>

<script>
import {
  CAccordion,
  CAccordionItem,
  CAccordionBody,
  CButton,
  CAccordionHeader,
  CContainer,
} from '@coreui/vue';

export default {
  name: 'ContainerExample',
  components: {
    CAccordion,
    CAccordionItem,
    CAccordionBody,
    CButton,
    CAccordionHeader,
    CContainer,
  },
};
</script>