<template>
    <div id="map-content-panel" class="content-panel">
      <div>
          <h3>MAP</h3>
          <div id="map-container"></div>
      </div>
  </div>
</template>

<script>
import MapVis from '../js/vis/map_vis.js'

export default {
    name: 'Map',
    props: {
        data: Array,
        date: Date
    },
    data() {
        return {
            map_vis: null,
            map_vis_dimensions: {
                width: 0,
                height: 0,
                margin: { left: 150, right: 20, top: 20, bottom: 50 }
            },
        }
    },
    watch: {
        data(newVal) {
            if (newVal != null) {
                this.init()
            }
        }
    },
    created() {
        this.$root.$on('time-control-slider-changed', this.timeControlSliderChanged)
    },
    destroyed() {
        this.$root.$off('time-control-slider-changed', this.timeControlSliderChanged)
    },
    methods: {
        init() {
            this.map_vis_dimensions.width = document.getElementById('map-content-panel').offsetWidth
            this.map_vis_dimensions.height = document.getElementById('map-content-panel').offsetHeight - 95

            this.map_vis = new MapVis(this.data, 'map-container', this.map_vis_dimensions)
        },
        timeControlSliderChanged(value) {
            if (this.map_vis != null) {
                this.map_vis.update(value)
            }
        },
    },
}
</script>

<style>

</style>