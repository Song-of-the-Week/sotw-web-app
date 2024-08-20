<template>
  <div class="modal fade" id="alertModal" tabindex="-1" role="dialog" aria-labelby="alertModal" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ header }}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>{{ message }}</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="callback()">Okay</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AlertModal",
  props: {
    alertModal: {
      default: null,
    },
    header: {
      type: String,
      default: "Alert!",
    },
    message: {
      type: String,
      default: "This is an alert.",
    },
    callback: {
      type: String,
      default: null,
    },
  },
  methods: {
    callback() {
      const vm = this;
      if (vm.callback != null) {
        this.$emit(vm.callback);
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
p {
  font-size: 0.84rem;
  margin: 0;
}
</style>
