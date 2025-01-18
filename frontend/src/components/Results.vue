<template>
  <div class="container">
    <div v-if="errorMessage.length > 0">
      <div class="col">
        <h1>{{ errorMessage }}</h1>
      </div>
    </div>
    <div v-else-if="weekNum > 0">
      <div class="row">
        <div class="col">
          <h1 class="mb-5">Congratulations to our week {{ weekNum - 1 }} winners!</h1>
          <h2 v-if="firstPlace.length === 2">
            Tied for first place with {{ firstPlaceVotes }} votes each, we have {{ firstPlace[0] }} and
            {{ firstPlace[1] }}!
          </h2>
          <h2 v-else-if="firstPlace.length > 2">
            Tied for first place with {{ firstPlaceVotes }} votes each, we have
            <span v-for="(song, index) in firstPlace" :key="index">{{ song }}<span
                v-if="index === firstPlace.length - 1">!</span><span v-else-if="index === firstPlace.length - 2">, and
              </span><span v-else>, </span></span>
          </h2>
          <div v-else>
            <h2 class="mb-4">In first place with {{ firstPlaceVotes }} votes, we have {{ firstPlace[0] }}!</h2>
            <h3 v-if="secondPlace.length === 2">
              Tied for second place with {{ secondPlaceVotes }} votes each, we have {{ secondPlace[0] }} and
              {{ secondPlace[1] }}!
            </h3>
            <h3 v-else-if="secondPlace.length > 2">
              Tied for second place with {{ secondPlaceVotes }} votes each, we have
              <span v-for="(song, index) in secondPlace" :key="index">{{ song }}<span
                  v-if="index === secondPlace.length - 1">!</span><span v-else-if="index === secondPlace.length - 2">,
                  and </span><span v-else>, </span></span>
            </h3>
            <h3 v-else>In second place with {{ secondPlaceVotes }} votes, we have {{ secondPlace[0] }}!</h3>
          </div>
        </div>
      </div>
      <div class="row mt-5">
        <div class="col">
          <div id="chart">
            <CanvasJSChart :options="chartOptions" />
          </div>
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
              </tbody>
            </table>
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
      content += "Submitter: " + dataPoint.submitter + "<br/>";
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
      for (const key in vm.allSongs) {
        dataPoints.push({
          label: vm.allSongs[key].name,
          y: vm.allSongs[key].voters.length,
          voters: vm.allSongs[key].voters,
          submitter: vm.allSongs[key].submitter,
        });

        if (vm.firstPlace.indexOf(vm.allSongs[key].name) != -1) {
          vm.firstPlaceVotes = vm.allSongs[key].voters.length;
        } else if (vm.secondPlace.indexOf(vm.allSongs[key].name) != -1) {
          vm.secondPlaceVotes = vm.allSongs[key].voters.length;
        }
      }

      // chart options
      vm.chartOptions = {
        theme: "dark1",
        backgroundColor: "transparent",
        animationsEnabled: true,
        exportEnabled: true,
        // width: "100%",
        title: {
          text: "Voting Results",
        },
        axisX: {
          labelTextAlign: "right",
          labelFontSize: 12,
          labelWrap: false,    // Don't allow the label to wrap to multiple lines
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
