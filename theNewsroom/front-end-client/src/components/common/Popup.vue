<template>
    <v-dialog d-flex elevation="0" v-model="show" width="1000px" height="500px">
        <v-card class=" flex-wrap text-justify justify-space-between">
            <v-card-title class="headline font-weight-bold" v-text='current_topic.name' />
            <v-divider />
            <v-card-title class="subheading">
                Related Topics
            </v-card-title>
            <v-card-actions>
                <v-row dense>
                    <v-col v-for="(topic, index) in topics" :key="index" md=6>
                        <v-btn color="rgb(230, 235, 255)" rounded width=100% depressed @click.stop="nextTopic(topic)" v-text='topic.name' />
                    </v-col>
                </v-row>
            </v-card-actions>
            <v-divider />
            <v-card-title class="subheading">
                Top Articles
            </v-card-title>
            <v-list depressed rounded >
                    <v-list-item class="item align-items=center" v-for="article in articles" :key="article.id" depressed @click='open(article)'>
                        <v-list-item-title v-text='article.articleByArticleId.title.slice(0, 100)' />
                    </v-list-item>
            </v-list>
            <v-divider />
            <v-card-actions>
                <v-row dense>
                    <v-btn v-if='isSelected' rounded depressed @click='removeSelected(current_topic)'>
                        Remove
                    </v-btn>
                    <v-btn  v-else rounded depressed @click='add(current_topic)'>
                        Add
                    </v-btn>
                    <v-spacer />
                    <v-btn  v-if='!isRoot' rounded depressed @click="previousTopic">
                        Previous
                    </v-btn>
                    <v-btn  rounded depressed @click.stop="close">
                        Close
                    </v-btn>
                    <HelpPopup />
                </v-row>
            </v-card-actions>
        </v-card>
        <Article v-model="article" />
        <Replace v-model="replace" />
    </v-dialog>
</template>

<script>
import {
    mapGetters,
    mapState,
    mapMutations
} from 'vuex';

import HelpPopup from "./HelpPopup";
import Article from "./Article";
import Replace from "./Replace";

import ALL_TOPICS_WITH_FILTER from '../../graphql/TopicsAndArticleCount.gql'
import TOP_ARTICLES_FROM_TOPIC from '../../graphql/TopArticlesFromTopic.gql'

export default {
    props: {
        value: Boolean
    },
    components: {
        HelpPopup,
        Article,
        Replace
    },
    computed: {
        ...mapState(['popups', 'selected', 'current_topic']),
        ...mapGetters(['isRoot', 'numSelected', 'isSelected', 'getPopups']),
        show: {
            get() {
                return this.value
            },
            set(value) {
                this.$emit('input', value)
            }
        }
    },
    data: () => ({
        article: false,
        topics: [],
        articles: [],
        replace: false
    }),
    apollo: {
        topics: {
            query: ALL_TOPICS_WITH_FILTER,
            variables() {
                return {
                    limit: 6
                }
            },
            update(data) {
                return data.allTopics.nodes;
            }
        },
        articles: {
            query: TOP_ARTICLES_FROM_TOPIC,
            variables() {
                var id
                if (this.current_topic.id == null) {
                    id = 1
                } else {
                    id = this.current_topic.id
                }
                return {
                    topicId: id
                }
            },
            update(data) {
                return data.topicById.topicofarticlesByTopicId.nodes;
            }
        }
    },
    methods: {
        ...mapMutations([
            'addSelected',
            'removeSelected',
            'openTopic',
            'nextTopic',
            'previousTopic',
            'closeTopic',
            'openArticle'
        ]),
        close() {
            this.show = false
            this.closeTopic()
        },
        open(article) {
            this.article = true
            this.openArticle(article)
        },
        add(topic) {
            if (this.numSelected == 5) {
                this.replace = true
            } else {
                this.addSelected(topic)
            }
        }
    },
}

</script>
<style scoped>
.v-list-item {
    justify-content: center !important;
    flex-direction: row !important;
    text-align: center !important;
    align-items: center !important;
}
.item {
    background: rgb(230, 235, 255);

}
.item:hover {
     background:rgb(222, 229, 255);

}
</style>
