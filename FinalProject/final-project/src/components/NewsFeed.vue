<template>
  <div class="content-panel">
      <div style="overflow: hidden; height:100%">
          <h3>News Feed</h3>
          <div class="scroll">
              <NewsArticle v-for="article in getNews(null)" :key="article.url" :data="article" />
          </div>
      </div>
  </div>
</template>

<script>
import NewsArticle from './NewsArticle'

export default {
    name: 'NewsFeed',
    components: {
        NewsArticle
    },
    props: {
        data: Array,
        date: Date
    },
    methods: {
        getNews(limit) {
            if (this.data == null) {
                return []
            }

            var result = this.data.filter(e => {
                var news_date = new Date(e['time-stamp'])
                return (news_date.getUTCMonth() == this.date.getUTCMonth()) &&
                (news_date.getUTCDate() == this.date.getUTCDate()) &&
                (news_date.getUTCFullYear() == this.date.getUTCFullYear())
            })

            if (limit != null) {
                return result.slice(0,limit)
            } else {
                return result
            }
        }
    }
}
</script>

<style scoped>
.scroll {
    padding:10px;
    overflow-x: hidden;
    overflow-y: scroll;
    display: flex; 
    flex-direction: column;
    height: calc(100% - 95px);
    /* Below lines hide the scroll bar */
    width: 100%;
    padding-right: 17px;
    box-sizing: content-box;
}
</style>