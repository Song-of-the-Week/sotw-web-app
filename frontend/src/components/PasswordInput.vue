<template>
  <div class="input-group">
    <input
      v-if="showPassword"
      v-model="password"
      type="text"
      class="form-control"
      @input="emitInput()"
      aria-label="password input"
    />
    <input
      v-else
      v-model="password"
      type="password"
      class="form-control"
      @input="emitInput()"
      aria-label="password input"
    />
    <span type="text" class="input-group-text pointer">
      <i
        class="bi"
        :class="{ 'bi-eye': !showPassword, 'bi-eye-slash': showPassword }"
        @click="showPassword = !showPassword"
      ></i>
    </span>
  </div>
</template>

<script>
export default {
  name: "PasswordInput",
  data() {
    return {
      password: "",
      showPassword: false,
    };
  },
  mounted() {
    const vm = this;
    document.getElementById("loginModal").addEventListener("hide.bs.modal", function (event) {
      vm.password = "";
      vm.showPassword = "";
    });
  },
  methods: {
    emitInput() {
      const vm = this;
      vm.$emit("input-password", vm.password);
    },
  },
};
</script>

<style scoped lang="scss">
.bi:hover {
  cursor: pointer;
}
</style>
