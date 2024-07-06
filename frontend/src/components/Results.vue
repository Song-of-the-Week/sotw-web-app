<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <h1 class="mb-5">Congratulations to our week {{ weekNum }} winners!</h1>
        <h2 v-if="firstPlace.length === 2">
          Tied for first place with {{ firstPlaceVotes }} votes each, we have {{ firstPlace[0] }} and
          {{ firstPlace[1] }}!
        </h2>
        <h2 v-else-if="firstPlace.length > 2">
          Tied for first place with {{ firstPlaceVotes }} votes each, we have
          <span v-for="(song, index) in firstPlace" :key="index"
            >{{ song }}<span v-if="index === firstPlace.length - 1">!</span
            ><span v-else-if="index === firstPlace.length - 2">, and </span><span v-else>, </span></span
          >
        </h2>
        <div v-else>
          <h2 class="mb-4">In first place with {{ firstPlaceVotes }} votes, we have {{ firstPlace[0] }}!</h2>
          <h3 v-if="secondPlace.length === 2">
            Tied for second place with {{ secondPlaceVotes }} votes each, we have {{ secondPlace[0] }} and
            {{ secondPlace[1] }}!
          </h3>
          <h3 v-else-if="secondPlace.length > 2">
            Tied for second place with {{ secondPlaceVotes }} votes each, we have
            <span v-for="(song, index) in secondPlace" :key="index"
              >{{ song }}<span v-if="index === secondPlace.length - 1">!</span
              ><span v-else-if="index === secondPlace.length - 2">, and </span><span v-else>, </span></span
            >
          </h3>
          <h3 v-else>In second place with {{ secondPlaceVotes }} votes, we have {{ secondPlace[0] }}!</h3>
        </div>
      </div>
    </div>
    <div class="row mt-5">
      <div class="col">
        <CanvasJSChart :options="chartOptions" />
      </div>
    </div>
    <div class="row mt-5">
      <div class="col">
        <h4>Guessing Data</h4>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th scope="col">Who ye be</th>
                <th scope="col">Number of Correct Guesses</th>
                <th scope="col" v-for="key in Object.keys(allSongs)" :key="key">{{ allSongs[key].name }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="guesser in guessingData" :key="guesser.id">
                <th scope="row">{{ guesser.name }}</th>
                <td>{{ guesser.numCorrectGuesses }}</td>
                <td
                  v-for="guess in guesser.guesses"
                  :class="{ 'correct-guess': guess.correct }"
                  :key="guess.submitterReal"
                >
                  {{ guess.submitterGuess }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Results",
  props: {
    weekId: {
      type: Number,
      defaut: 0,
    },
  },
  data() {
    return {
      weekNum: 0,
      firstPlace: [],
      secondPlace: [],
      firstPlaceVotes: 0,
      secondPlaceVotes: 0,
      allSongs: [],
      guessingData: [],
      chartOptions: {},
    };
  },
  mounted() {
    const vm = this;

    vm.firstPlace = ["Sample1", "Sample2", "Sample3"];
    vm.secondPlace = ["Sample1", "Sample2", "Sample3"];

    vm.allSongs = {
      0: { name: "sample1", voters: ["Dan", "Jan"], submitter: "Sam" },
      1: { name: "sample2", voters: ["Sam", "Dan"], submitter: "Jan" },
      2: { name: "sample3", voters: ["Jan", "Sam"], submitter: "Dan" },
    };

    vm.guessingData = [
      {
        id: 0,
        name: "Dan",
        guesses: [
          { song: "sample1", submitterGuess: "Jan", correct: false },
          { song: "sample2", submitterGuess: "Sam", correct: false },
          { song: "sample3", submitterGuess: "Dan", correct: true },
        ],
        numCorrectGuesses: 1,
      },
      {
        id: 1,
        name: "Sam",
        guesses: [
          { song: "sample1", submitterGuess: "Sam", correct: true },
          { song: "sample2", submitterGuess: "Jan", correct: true },
          { song: "sample3", submitterGuess: "Dan", correct: true },
        ],
        numCorrectGuesses: 3,
      },
      {
        id: 2,
        name: "Jan",
        guesses: [
          { song: "sample1", submitterGuess: "Dan", correct: false },
          { song: "sample2", submitterGuess: "Jan", correct: true },
          { song: "sample3", submitterGuess: "Sam", correct: false },
        ],
        numCorrectGuesses: 1,
      },
    ];

    // Chart Options
    let dataPoints = [];
    for (const key in vm.allSongs) {
      dataPoints.push({
        label: vm.allSongs[key].name,
        y: vm.allSongs[key].voters.length,
        voters: vm.allSongs[key].voters,
        submitter: vm.allSongs[key].submitter,
      });
    }

    vm.chartOptions = {
      theme: "dark1",
      backgroundColor: "transparent",
      animationsEnabled: true,
      exportEnabled: true,
      title: {
        text: "Voting Results",
      },
      axisX: {
        labelTextAlign: "right",
      },
      axisY: {
        interval: 1,
      },
      toolTip: {
        shared: true,
        content: vm.toolTipFormatter,
      },
      data: [
        {
          type: "bar",
          yValueFormatString: "#",
          dataPoints: dataPoints,
        },
      ],
    };
  },
  methods: {
    toolTipFormatter(e) {
      let content = "";
      let dataPoint = e.entries[0].dataPoint;

      content += "Votes: " + dataPoint.y + "<br/>";
      content += "Submitter: " + dataPoint.submitter + "<br/>";
      content += "Voters:<br/>";
      dataPoint.voters.forEach((v) => {
        content += v + "<br/>";
      });

      return content;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
th:first-child,
td:first-child {
  position: sticky;
  left: 0;
}
.table {
  min-width: 48rem;
}
.correct-guess {
  background-color: #32a852;
}
</style>
