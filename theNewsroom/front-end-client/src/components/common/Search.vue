<template>
<v-dialog d-flex elevation="0" v-model="show" width="1000px" height="500px">
    <v-card class="flex-wrap text-justify justify-space-between">
        <v-card-title class="headline"> <strong>Search</strong>: {{this.keyword}}</v-card-title>
        <v-divider />
        <h2 class="subheading grey--text text-center" v-if="results.length == 0">Sorry, your search returned no results!</h2>
        <v-card-actions v-else>
            <v-flex align-center xs12>
                <v-data-table :mobile-breakpoint="0" :headers="headers" :items="results" :sort-by="['topicofarticlesByTopicId.totalCount']" :sort-desc="[true]">
                    <template v-slot:item="{ item }">
                        <tr @click="rowClicked(item)">
                            <td class="subheading text-center" v-text="item.topicofarticlesByTopicId.totalCount" />
                            <td class="subheading text-center" v-text="item.name" />
                        </tr>
                    </template>
                </v-data-table>
            </v-flex>
        </v-card-actions>
        <v-divider />
        <v-card-actions>
            <v-row dense>
                <v-spacer />
                <v-btn rounded depressed @click.stop="close">
                    Close
                </v-btn>
                <HelpSearch />
            </v-row>
        </v-card-actions>
    </v-card>
    <Popup v-model="popup" />
</v-dialog>
</template>

<script>
import {
    mapState,
    mapMutations
} from 'vuex';

import Popup from "./Popup"
import HelpSearch from "./HelpSearch"

import SEARCH_FOR_TOPIC from '../../graphql/SearchForTopic.gql'

export default {
    props: {
        value: Boolean
    },
    components: {
        Popup,
        HelpSearch
    },
    computed: {
        ...mapState(['keyword']),
        show: {
            get() {
                return this.value
            },
            set(value) {
                this.$emit('input', value)
            }
        }
    },
    methods: {
        ...mapMutations([
            'openTopic',
        ]),
        open(topic) {
            this.popup = true
            this.openTopic(topic)
        },
        close() {
            this.show = false
        },
        rowClicked(topic) {
            this.open(topic)
            console.log(topic);
        },
    },
    data: () => ({
        popup: false,
        results: [],
        headers: [{
                text: '# Articles',
                value: 'topicofarticlesByTopicId.totalCount',
                width: "30%",
                align: 'center',
            },
            {
                text: 'Topic',
                value: 'name',
                width: "100%",
                align: 'center',
            }
        ],
    }),
    apollo: {
        results: {
            query: SEARCH_FOR_TOPIC,
            variables() {
                return {
                    keyword: this.keyword
                }
            },
            update(data) {
                return data.allTopics.nodes;
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
    background: rgb(243, 245, 245);
}
.item:hover {
    background: rgb(239, 240, 240);
}
</style>
