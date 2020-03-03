<template>
  <div class="content-panel">
    <div>
      <h3>TIMECONTROL ({{date.toUTCString()}})</h3>
      <div class="slidecontainer">
        <input
          class="slider"
          id="date_slider"
          type="range"
          min="0"
          max="33"
          value="0"
          v-model="slider_value"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TimeControl",
  props: {
    data: Object,
    date: Date
  },
  data() {
      return {
          slider_value: 0
      }
  },
  watch: {
      slider_value() {
          this.$root.$emit('time-control-slider-changed', this.slider_value)
      }
  },
};
</script>

<style scoped>
</style>