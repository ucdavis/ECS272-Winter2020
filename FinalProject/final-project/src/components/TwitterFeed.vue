<template>
  <div class="content-panel">
      <div style="overflow: hidden">
          <h3>Twitter Feed</h3>
          <div class="scroll">
            <Tweet v-for="tweet in getTweets(5)" :key="tweet.tweet_id" :id="tweet.tweet_id" :options="{ cards: 'hidden', width: '350', align: 'center' }"/>
          </div>
      </div>
  </div>
</template>

<script>
import { Tweet } from 'vue-tweet-embed'

export default {
    name: 'TwitterFeed',
    components: {
        Tweet
    },
    props: {
        data: Array,
        date: Date
    },
    methods: {
        getTweets(limit) {
            if (this.data == null) {
                return []
            }
                        console.log(limit)

            return this.data.filter(e => {
                var tweet_date = new Date(e.timestamp * 1000)
                return (tweet_date.getUTCMonth() == this.date.getUTCMonth()) &&
                (tweet_date.getUTCDate() == this.date.getUTCDate()) &&
                (tweet_date.getUTCFullYear() == this.date.getUTCFullYear())
            })
            .sort((a, b) => {
                if (a.likes == b.likes)
                    return 0
                if (a.likes < b.likes)
                    return 1
                if (a.likes > b.likes)
                    return -1
            }).slice(0,limit)

        }
    }
}
</script>

<style scoped>
.scroll {
    padding:10px;
    overflow-x: hidden;
    overflow-y: scroll;
    max-height: 520px;
    /* Below lines hide the scroll bar */
    width: 100%;
    padding-right: 17px;
    box-sizing: content-box;
}
</style>