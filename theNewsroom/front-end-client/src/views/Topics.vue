<template>
<div class="topics">
    <template>
        <v-container fluid>

            <v-layout wrap>
                <v-flex xs12 md4>
                    <v-card flat tile width='100%'>
                        <v-list flat rounded dense>
                            <v-list-group value="true" color="none">
                                <template v-slot:activator>
                                    <v-list-item-content>
                                        <v-list-item-title class='font-weight-light list-title'>Filters </v-list-item-title>
                                    </v-list-item-content>
                                </template>
                                <!-- Search -->
                                <v-list-item>
                                    <v-text-field @keyup.enter.native="searchTopic" dense rounded filled v-model="keyword" append-icon="mdi-magnify" label="Search for a topic" single-line hide-details />
                                    <Search v-model="search" />
                                </v-list-item>
                                <!-- Calendar -->
                                <v-list-item>
                                    <v-menu ref="menu" v-model="menu" :close-on-content-click="false" :return-value.sync="dates" transition="scale-transition" offset-y min-width="290px">
                                        <template v-slot:activator="{ on, attrs }">
                                            <v-text-field dense rounded filled v-model="dateRange" label="Select time period" append-icon="mdi-calendar" single-line hide-details readonly v-bind="attrs" v-on="on" />
                                        </template>
                                        <v-date-picker v-model="dates" :max='todaysDate' range no-title scrollable>
                                            <v-spacer />
                                            <v-btn text color="primary" @click="saveDates">
                                                OK
                                            </v-btn>
                                        </v-date-picker>
                                    </v-menu>
                                </v-list-item>
                                <!-- Media selection -->
                                <v-list-item>
                                    <v-text-field dense rounded filled v-model="media" append-icon="mdi-book-open-variant" label="Filter by media outlet" single-line hide-details />
                                </v-list-item>
                            </v-list-group>
                            <v-list-item>
                                <v-spacer />
                                <v-btn rounded depressed @click="reset">
                                    Reset </v-btn>
                                <HelpTopics />
                            </v-list-item>
                        </v-list>
                    </v-card>
                    <v-spacer />
                </v-flex>
                <v-spacer />
                <v-flex align-center xs12 md8>
                    <!-- At the moment, topics are shown in a data table with rows that contain a topic's name and number of articles. Datatables allow us with a lot of options for sorting and presenting data, and are more scalable for different screen resolutions than other data presentation methods -->
                    <v-data-table :mobile-breakpoint="0" :headers="headers" :items="topics" :sort-by="['topicofarticlesByTopicId.totalCount']" :sort-desc="[true]">
                        <template v-slot:item="{ item }">
                            <tr @click="rowClicked(item)">
                                <td> {{item.topicofarticlesByTopicId.totalCount}} </td>
                                <td>{{item.name}}</td>
                            </tr>
                        </template>
                    </v-data-table>
                </v-flex>
                <Popup v-model="popup" />
                <v-col />
            </v-layout>
        </v-container>
    </template>
</div>
</template>

<script>
import Popup from "../components/common/Popup"
import HelpTopics from "../components/common/HelpTopics"
import Search from "../components/common/Search"
import ALL_TOPICS_WITH_FILTER from '../graphql/TopicsAndArticleCount.gql'
import {
    mapMutations
} from 'vuex';

export default {
    name: "Topics",
    components: {
        Popup,
        HelpTopics,
        Search
    },

    data: () => ({
        search: false,
        popup: false,
        start_date: null,
        end_date: null,
        dates: [],
        keyword: '',
        menu: false,
        media: '',
        sortDesc: true,
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
        topics: [],

    }),
    apollo: {
        topics: {
            query: ALL_TOPICS_WITH_FILTER,
            variables() {
                return {
                        media: this.media,
                        from: this.start_date,
                        to: this.end_date,
                }
            },
            update(data) {
                return data.allTopics.nodes;
            }
        }
    },
    methods: {
        ...mapMutations([
            'openTopic',
            'searchTopicKeyword'
        ]),
        formatDate(date) {
            let month = `${date.getMonth() + 1}`;
            let day = `${date.getDate()}`;
            const year = date.getFullYear();
            if (month.length < 2) month = `0${month}`;
            if (day.length < 2) day = `0${day}`;
            return [year, month, day].join('-');
        },
        rowClicked(topic) {
            this.open(topic)
            console.log(topic);
        },
        open(topic) {
            this.popup = true
            this.openTopic(topic)
        },
        saveDates() {
            this.$refs.menu.save(this.dates)
            if (this.dates[0] < this.dates[1]) {
                this.start_date = this.dates[0]
                this.end_date = this.dates[1]
            } else {
                this.start_date = this.dates[1]
                this.end_date = this.dates[0]
            }
            this.dates = [this.start_date, this.end_date]

        },
        searchTopic() {
            if (this.keyword != '') {
                this.search = true
                this.searchTopicKeyword(this.keyword)
            }
        },
        reset() {
            this.end_date = new Date()
            this.start_date = new Date()
            this.start_date.setMonth(this.end_date.getMonth() - 1)

            this.start_date = this.start_date.toISOString().slice(0, 10)                    
            this.end_date = this.end_date.toISOString().slice(0, 10)
            this.dates = [this.start_date, this.end_date]
            this.media = ''
        }
    },
     mounted: function() {
        this.reset()
        console.log("Mounted.")
    },
    computed: {
        todaysDate() {
            const today = new Date();
            return this.formatDate(today);
        },
        dateRange() {
            return this.dates.join(' to ')
        },
    },
}
</script>

<style scoped>
td {
    text-align: center !important;
}

.list-title {
    font-size: 16px !important;
}

.item {
    margin: 5px;
    border-radius: 4px;
}

.item:hover {
    background: ghostwhite;
}
</style>
