<template>
  <div class="row">
    <div class="col">
      <div class="input-group">
        <span class="input-group-text">Day</span>
        <select v-model="day" @change="emitInput" class="form-control">
          <option value="0">Sunday</option>
          <option value="1">Monday</option>
          <option value="2">Tuesday</option>
          <option value="3">Wednesday</option>
          <option value="4">Thursday</option>
          <option value="5">Friday</option>
          <option value="6">Saturday</option>
        </select>
        <span class="input-group-text">Time</span>
        <select v-model="hour" @change="emitInput" class="form-control hour-select">
          <option value="0">0</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
          <option value="6">6</option>
          <option value="7">7</option>
          <option value="8">8</option>
          <option value="9">9</option>
          <option value="10">10</option>
          <option value="11">11</option>
          <option value="12">12</option>
          <option value="13">13</option>
          <option value="14">14</option>
          <option value="15">15</option>
          <option value="16">16</option>
          <option value="17">17</option>
          <option value="18">18</option>
          <option value="19">19</option>
          <option value="20">20</option>
          <option value="21">21</option>
          <option value="22">22</option>
          <option value="23">23</option>
        </select>
        <span class="input-group-text">:</span>
        <select v-model="minute" @change="emitInput" class="form-control minute-select">
          <option value="0">00</option>
          <option value="1">01</option>
          <option value="2">02</option>
          <option value="3">03</option>
          <option value="4">04</option>
          <option value="5">05</option>
          <option value="6">06</option>
          <option value="7">07</option>
          <option value="8">08</option>
          <option value="9">09</option>
          <option value="10">10</option>
          <option value="11">11</option>
          <option value="12">12</option>
          <option value="13">13</option>
          <option value="14">14</option>
          <option value="15">15</option>
          <option value="16">16</option>
          <option value="17">17</option>
          <option value="18">18</option>
          <option value="19">19</option>
          <option value="20">20</option>
          <option value="21">21</option>
          <option value="22">22</option>
          <option value="23">23</option>
          <option value="24">24</option>
          <option value="25">25</option>
          <option value="26">26</option>
          <option value="27">27</option>
          <option value="28">28</option>
          <option value="29">29</option>
          <option value="30">30</option>
          <option value="31">31</option>
          <option value="32">32</option>
          <option value="33">33</option>
          <option value="34">34</option>
          <option value="35">35</option>
          <option value="36">36</option>
          <option value="37">37</option>
          <option value="38">38</option>
          <option value="39">39</option>
          <option value="40">40</option>
          <option value="41">41</option>
          <option value="42">42</option>
          <option value="43">43</option>
          <option value="44">44</option>
          <option value="45">45</option>
          <option value="46">46</option>
          <option value="47">47</option>
          <option value="48">48</option>
          <option value="49">49</option>
          <option value="50">50</option>
          <option value="51">51</option>
          <option value="52">52</option>
          <option value="53">53</option>
          <option value="54">54</option>
          <option value="55">55</option>
          <option value="56">56</option>
          <option value="57">57</option>
          <option value="58">58</option>
          <option value="59">59</option>
        </select>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col">
      <div class="input-group">
        <span class="input-group-text">Timezone</span>
        <select v-model="selectedTimezone" @change="emitInput" class="form-control timezone-select">
          <option v-for="tz in allTimezones" :key="tz" :value="tz">{{ tz }}</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment-timezone';
export default {
  name: "DayTimePicker",
  props: {
    resultsDayTime: { type: Date, default: new Date() },
    resultsTimezone: { type: String, default: moment.tz.guess() }
  },
  data() {
    return {
      day: 0,
      hour: 0,
      minute: 0,
      allTimezones: moment.tz.names(),
      selectedTimezone: null,
    };
  },
  mounted() {
    const vm = this;
    vm.day = vm.resultsDayTime.getDay();
    vm.hour = vm.resultsDayTime.getHours();
    vm.minute = vm.resultsDayTime.getMinutes();

    vm.selectedTimezone = vm.resultsTimezone;

    document.getElementById("sotwCreationModal").addEventListener("hide.bs.modal", function (_) {
      vm.day = vm.resultsDayTime.getDay();
      vm.hour = vm.resultsDayTime.getHours();
      vm.minute = vm.resultsDayTime.getMinutes();
    });
    vm.emitInput();
  },
  methods: {
    emitInput() {
      const vm = this;
      // hard coded to April 1907 (when the first of the month was a Sunday)
      vm.$emit("input-day-time", { date: new Date(1907, 3, vm.day, vm.hour, vm.minute), timezone: vm.selectedTimezone });
    },
  },
};
</script>

<style scoped lang="scss">
.bi:hover {
  cursor: pointer;
}

.hour-select {
  max-width: 3rem;
}

.minute-select {
  max-width: 4rem;
}

// .timezone-select {
//   max-width: 10ch;
// }</style>
