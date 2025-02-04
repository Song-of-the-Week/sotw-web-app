<template>
    <div class="modal fade" :id="modalId" tabindex="-1" role="dialog" :aria-labelby="modalId"
      aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modalTitle }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            {{ modalBody }}
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" :class="['btn', btnClass]" @click="$emit('click')">{{ buttonText }}</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "SotwCreationModal",
    props: {
      modalId: {
        type: String,
        required: true
      },
      btnClass: {
        type: String,
        default: "btn-primary",
      },
      modalTitle: {
        type: String,
        default: "",
      },
      modalBody: {
        type: String,
        default: "",
      },
      buttonText: {
        type: String,
        default: "Confirm"
      },
      shouldShow: {
        type: Boolean,
        default: false
      }
    },
    emits: ['click', 'update:shouldShow'],
    data() {
      return {
        modal: null
      };
    },
    async mounted() {
      const vm = this;
      vm.modal = new window.bootstrap.Modal(document.getElementById(this.modalId))
      // Add event listener for when modal is hidden
      document.getElementById(this.modalId).addEventListener('hidden.bs.modal', () => {
        this.$emit('update:shouldShow', false)
      })
    },
    beforeUnmount() {
      const vm = this;
      // Remove event listener
      document.getElementById(this.modalId)?.removeEventListener('hidden.bs.modal', () => {
        this.$emit('update:shouldShow', false)
      })
      if (vm.modal) {
        vm.modal.dispose()
      }
    },
    watch: {
      shouldShow(newVal, oldVal) {
        if (newVal && this.modal) {
          this.modal.show()
        } else if (!newVal && this.modal) {
          this.modal.hide()
        }
      }
    },
    methods: {
      show() {
        this.$emit('update:shouldShow', true)
      },
      hide() {
        this.$emit('update:shouldShow', false)
      }
    }
  };
  </script>
  
  <style scoped lang="scss">
  p {
    font-size: 0.84rem;
    margin: 0;
  }
  </style>
