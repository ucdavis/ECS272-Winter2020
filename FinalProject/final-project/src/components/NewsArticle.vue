<template>
<div class="article" v-on:click="articleClicked()">
    <b>{{data.headline}}</b>
    <br><br>
    {{data.journal}}, {{data['time-stamp']}}
</div>
</template>

<script>
export default {
    name: 'NewsArticle',
    props: {
        data: Object
    },
    methods: {
        articleClicked() {
            window.open(this.data.url, '_blank');
        }
    }
}
</script>

<style scoped>
.article {
    margin: 10px;
    padding: 15px;
    border-radius: 5px;
    background-color: #fff;
    color: #000;
    cursor: pointer;
}
</style>