<template>
  <div id="app">
    <StatusBar title="ECS272 - Final Project"/>
    <div class="main-content">
      <Map :data="null" />
      <WordCloud :data="null" />
      <TwitterFeed :data="null" />
      <br>
      <TimeControl :data="null" />
    </div>
  </div>
</template>

<script>
import StatusBar from './components/StatusBar.vue'
import WordCloud from './components/WordCloud.vue'
import Map from './components/Map.vue'
import TimeControl from './components/TimeControl.vue'
import TwitterFeed from './components/TwitterFeed.vue'



export default {
  name: 'App',
  components: {
    StatusBar,
    WordCloud,
    Map,
    TimeControl,
    TwitterFeed
  }
}
</script>

<style>
body {
  background-color: #0e1924;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #FFF;
  margin-top: 60px;
}

h1 {
  font-size: 2em;
}

h2 {
  font-size: 1.5em;
}

h3 {
  font-size: 1.2em;
}

.main-content {
  padding: 20px 0;
}

.content-panel {
  display: inline-block;
  padding: 10px;
  margin: 10px;
  background-color: #182736;
  -webkit-box-shadow: 0px 0px 8px 1px rgba(0,0,0,0.5); 
  box-shadow: 0px 0px 8px 1px rgba(0,0,0,0.5);
}

</style>
