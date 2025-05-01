<template>
  <div class="container">
    <div v-if="errorMessage.length > 0">
      <div class="col">
        <h1>{{ errorMessage }}</h1>
      </div>
    </div>
    <div v-else-if="weekNum > 0">
      <div class="row">
        <div class="col text-center">
          <h1 class="mb-5">Congratulations to our week {{ weekNum - 1 }} winners!</h1>
          <div class="row justify-content-center">
            <div class="col-12 col-md-4">
              <div class="card px-0 mb-4">
                <div class="card-header">
                  First Place 🏆
                </div>
                <ul class="list-group list-group-flush">
                  <li v-for="song in firstPlace" class="list-group-item">{{ song }}</li>
                </ul>
              </div>
            </div>
            <div v-if="firstPlace.length === 1" class="col-12 col-md-4">
              <div class="card px-0 mb-4">
                <div class="card-header">
                  Second Place 🥈
                </div>
                <ul class="list-group list-group-flush">
                  <li v-for="song in secondPlace" class="list-group-item">{{ song }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <!-- Theme Banner -->
        <div v-if="theme" class="row">
          <div class="col col-10 col-sm-6 offset-1 offset-sm-3">
            <div class="card px-0 mb-4">
              <div class="card-header text-white text-center">
                <h2 class="mb-0">Week {{ weekNum - 1 }} Theme</h2>
              </div>
              <div class="card-body text-center">
                <h3 class="card-title">{{ theme }}</h3>
                <p class="card-text">{{ themeDescription }}</p>
              </div>
            </div>
          </div>
        </div>
        <!-- Chart Card -->
        <div class="row-md-4 mb-4">
          <div class="card h-100">
            <div class="card-header">
              <h4>Week {{ weekNum - 1 }} Voting Results</h4>
            </div>
            <div class="card-body">
              <div id="chart">
                <CanvasJSChart :options="chartOptions" />
              </div>
            </div>
          </div>
        </div>

        <!-- Guessing Data Card -->
        <div class="row-md-4 mb-4">
          <div class="card h-100">
            <div class="card-header">
              <h4>Guessing Data</h4>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table">
                  <thead>
                    <tr>
                      <th scope="col">Who ye be</th>
                      <th scope="col">Number of Correct Guesses</th>
                      <th scope="col" v-for="guess in guessingData[0].guesses"
                        :key="guess.song + '-' + guess.submitter_guess">{{ guess.song }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="guesser in guessingData" :key="guesser.id">
                      <th scope="row">{{ guesser.name }}</th>
                      <td>{{ guesser.num_correct_guesses }}</td>
                      <td v-for="guess in guesser.guesses" :class="{ 'correct-guess': guess.correct }">
                        {{ guess.submitter_guess }}
                      </td>
                    </tr>
                    <tr>
                      <th scope="row">Correct Guesses</th>
                      <td></td>
                      <td v-for="guess in guessingData[0].guesses">
                        {{ songCorrectMatches[guess.song] }}
                      </td>
                    </tr>
                    <tr>
                      <th scope="row">Average</th>
                      <td>{{ avg_num_correct_guesses }}</td>
                      <td v-for="guess in guessingData[0].guesses">
                        {{ ((songCorrectMatches[guess.song] / guessingData[0].guesses.length)*100).toFixed(0) + "%" }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- Who Dun It Card -->
        <div class="row-md-4 mb-4">
          <div class="card h-100">
            <div class="card-header">
              <h4>Who Dun It?</h4>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table">
                  <thead>
                    <tr>
                      <th scope="col" class="text-start text-md-center">Submitter</th>
                      <th scope="col" class="text-start text-md-center">Song</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="song in allSongs" :key="song.submitter">
                      <td class="text-start text-md-center">{{ song.submitter }}</td>
                      <td class="text-start text-md-center">{{ song.name }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { toRaw } from "vue";
import api from "@/shared/api";
export default {
  name: "Results",
  props: {
    sotwId: {
      type: Number,
      default: 0,
    },
    weekNum: {
      type: Number,
      defaut: 0,
    },
  },
  computed: {
    songCorrectMatches() {
      const vm = this;
      let songsCorrect = {};
      for (const key in vm.allSongs) {
        songsCorrect[vm.allSongs[key].name] = 0;
      }
      for (let guesser of vm.guessingData) {
        for (let i=0; i < guesser.guesses.length; i++) {
          let guess = guesser.guesses[i]

          songsCorrect[guess.song] += guess.correct;
        }
      }
      return songsCorrect;
    }
  },
  data() {
    return {
      firstPlace: [],
      secondPlace: [],
      firstPlaceVotes: 0,
      secondPlaceVotes: 0,
      allSongs: [],
      guessingData: [{ guesses: { song: "", submitter_guess: "" } }],
      chartOptions: {},
      errorMessage: "",
      avg_num_correct_guesses: 0,
      theme: "",
      themeDescription: "",
    };
  },
  mounted() {
    const vm = this;
    vm.getResults(vm.weekNum);
  },
  methods: {
    getResults(weekNum) {
      const vm = this;
      // get results (if available)
      if (weekNum > 1) {
        weekNum -= 1;
      }
      api.methods
        .apiGetResults(vm.sotwId, weekNum)
        .then((res) => {
          if ("message" in res.data) {
            vm.errorMessage = res.data.message;
          } else {
            vm.firstPlace = toRaw(JSON.parse(res.data.first_place));
            vm.secondPlace = toRaw(JSON.parse(res.data.second_place));
            vm.allSongs = toRaw(JSON.parse(res.data.all_songs));
            vm.guessingData = toRaw(JSON.parse(res.data.guessing_data));
            vm.theme = res.data.theme;
            vm.themeDescription = res.data.theme_description;
            // get average guesses
            let total_correct_guesses = 0
            vm.guessingData.forEach(guesser => {
              total_correct_guesses += guesser.num_correct_guesses;
            });
            vm.avg_num_correct_guesses = Math.round((total_correct_guesses / vm.guessingData.length) * 100) / 100;
            
            vm.buildChart();
          }
        })
        .catch((err) => {
          console.log("ERROR", err);
        });

      return vm.weekNum;
    },
    toolTipFormatter(e) {
      let content = "";
      let dataPoint = e.entries[0].dataPoint;

      content += "Votes: " + dataPoint.y + "<br/>";
      content += "Submitter(s): ";
      dataPoint.submitters.forEach((s, i) => {
        content += s
        if (i != dataPoint.submitters.length - 1) {
          content += ", "
        }
      });
      content += "<br/>"
      content += "Voters:<br/>";
      dataPoint.voters.forEach((v) => {
        content += v + "<br/>";
      });

      return content;
    },
    buildChart() {
      const vm = this;
      // data points
      let dataPoints = [];
      let chartSongs = {};
      for (const key in vm.allSongs) {
        if (!(vm.allSongs[key].name in chartSongs)) {
          chartSongs[vm.allSongs[key].name] = {
            voters: [],
            submitters: [],
          }
        }
        chartSongs[vm.allSongs[key].name].voters = chartSongs[vm.allSongs[key].name].voters.concat(vm.allSongs[key].voters);
        chartSongs[vm.allSongs[key].name].submitters.push(vm.allSongs[key].submitter);
      }
      Object.keys(chartSongs).reverse().forEach((name) => {
        dataPoints.push({
          label: name,
          y: chartSongs[name].voters.length,
          voters: chartSongs[name].voters,
          submitters: chartSongs[name].submitters,
        });

        if (vm.firstPlace.indexOf(chartSongs[name].name) != -1) {
          vm.firstPlaceVotes = chartSongs[name].voters.length;
        } else if (vm.secondPlace.indexOf(chartSongs[name].name) != -1) {
          vm.secondPlaceVotes = chartSongs[name].voters.length;
        }
      });

      // chart options
      vm.chartOptions = {
        theme: "dark1",
        backgroundColor: "transparent",
        animationsEnabled: true,
        exportEnabled: true,
        axisX: {
          labelTextAlign: "right",
          labelFontSize: 12,
          labelWrap: false,
          interval: 1,
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
  },
  watch: {
    weekNum(newVal, oldVal) {
      this.getResults(newVal);
    }
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
