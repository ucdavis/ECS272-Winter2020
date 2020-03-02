<template>
  <div id="app">
    <StatusBar title="COVID-19 News & Spread"/>
    <div class="main-content">
      <Map :data="null" style="grid-area: main"/>
      <TwitterFeed :data="twitter" :date="date" style="grid-area: side1"/>
      <NewsFeed :data="news" :date="date" style="grid-area: side2"/>
      <WordCloud :data="null" style="grid-area: side3"/>
      <TimeControl :data="null" :date="date" style="grid-area: control"/>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'

import StatusBar from './components/StatusBar.vue'
import WordCloud from './components/WordCloud.vue'
import Map from './components/Map.vue'
import TimeControl from './components/TimeControl.vue'
import TwitterFeed from './components/TwitterFeed.vue'
import NewsFeed from './components/NewsFeed.vue'

export default {
  name: 'App',
  components: {
    StatusBar,
    WordCloud,
    Map,
    TimeControl,
    TwitterFeed,
    NewsFeed
  },
  data() {
    return {
      twitter: null,
      news: null,
    }
  },
  created() {
    this.date = new Date()
    this.date.setUTCMonth(1, 20)
    console.log(this.date)

    d3.json('/data/twitter.json')
      .then((data) => {
        this.twitter = data.tweets
      })

    d3.json('/data/news.json')
      .then((data) => {
        this.news = data
      })
  }
}
</script>

<style>
body {
  background-color: #05192B;
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
  display: grid;
  grid-template-columns: 1fr 3fr 400px 400px 1fr;
  grid-template-rows: 25vh 25vh 15vh 20vh;
  grid-template-areas: 
  ". main side1 side2 ."
  ". main side1 side2 ."
  ". main side3 side3 ."
  ". control side3 side3 ."
  ". . . . .";
  grid-column-gap: 10px;
  grid-row-gap: 15px;
  padding: 40px 0 0 0;
}

.content-panel {
  display: inline-block;
  padding: 10px;
  background-color: #242A3D;
  border-radius: 4px;
  -webkit-box-shadow: 0px 0px 8px 1px rgba(0, 0, 0, 0.2);
  box-shadow: 0px 0px 8px 1px rgba(0, 0, 0, 0.2);
}

</style>
