<template>
  <div class="content-panel">
      <div>
          <h3>TIMECONTROL ({{date.toUTCString()}})</h3>
      </div>
  </div>
</template>

<script>
export default {
    name: 'TimeControl',
    props: {
        data: Object,
        date: Date
    }
}
</script>

<style scoped>

</style>