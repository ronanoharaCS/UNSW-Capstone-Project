<template>
<div class="trends">
    <template>
        <v-container fluid>

            <v-layout wrap>
                <v-flex xs12 md4>
                    <!-- For now this filters the datatable, really we want it to produce a popup with possible matches on 'enter', and selecting a match will produce the corresponding topic popup. This field ought to be in the same position of the page on both Topics and Trends, to show continuity -->
                    <v-card flat tile width='100%'>
                        <v-list ripple=false expand flat rounded dense>

                            <!-- Search, calendar and media are subgroups in a the group Filters, allowing us to easily modify this entire list as a single element -->
                            <v-list-group value="true" color="none">

                                <template v-slot:activator>
                                    <v-list-item-content>
                                        <v-list-item-title class='font-weight-light list-title'>Filters</v-list-item-title>
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
                            </v-list-group>
                            <!-- Selected, Related and Saved topics are also presented as groups in the List, allowing us to open and close them easily to show their internal components. Selected is set to true so that it is shown automatically, whilst the others are closed by default -->
                            <v-list-group value="true" color="none">
                                <template v-slot:activator>
                                    <v-list-item-content>
                                        <v-list-item-title class='font-weight-light list-title'>Selected Topics</v-list-item-title>
                                    </v-list-item-content>
                                </template>
                                <v-list-item-group value="true" color="none">
                                    <v-list-item class='item' v-for="(item, index) in getSelected" :key="index" >
                                        <v-list-item-title @click='open(item)' v-text="item.name" />
                                        <v-icon v-if='index == 0' color="#FF42DC">mdi-circle</v-icon>
                                        <v-icon v-if='index == 1' color="#0096DB">mdi-circle</v-icon>
                                        <v-icon v-if='index == 2' color="#FF9D00">mdi-circle</v-icon>
                                        <v-icon v-if='index == 3' color='#66DB00'>mdi-circle</v-icon>
                                        <v-icon v-if='index == 4' color="#DB0004">mdi-circle</v-icon>
                                        <v-btn icon @click='removeSelected(item)'>
                                            <v-icon color="grey lighten-1">mdi-minus-circle</v-icon>
                                        </v-btn>
                                    </v-list-item>
                                </v-list-item-group>
                            </v-list-group>
                            <v-list-group color="none">
                                <template v-slot:activator>
                                    <v-list-item-content>
                                        <v-list-item-title class='font-weight-light list-title'>Related Topics</v-list-item-title>
                                    </v-list-item-content>
                                </template>
                                <v-list-item-group color="none">
                                    <v-list-item  class='item' v-for="item in related_topics" :key="item.id">
                                        <v-list-item-title @click='open(item)' v-text="item.name" />
                                        <v-btn icon @click='add(item)'>
                                            <v-icon color="grey lighten-1">mdi-plus-circle</v-icon>
                                        </v-btn>
                                    </v-list-item>
                                </v-list-item-group>
                            </v-list-group>
                            <template v-if="!$auth.loading & $auth.isAuthenticated">
                                <v-list-group color="none">
                                    <template v-slot:activator>
                                        <v-list-item-content>
                                            <v-list-item-title class='font-weight-light list-title'>Saved Trends</v-list-item-title>
                                        </v-list-item-content>
                                    </template>
                                    <v-list-item-group color="none">
                                        <v-list-item class='item' v-for="config in configs" :key="config.id" @click="setSelected(config.topics)">
                                            <v-list-item-title v-text=" config.title" />
                                        </v-list-item>
                                    </v-list-item-group>
                                </v-list-group>
                            </template>
                            <v-list-item>
                                <v-spacer />
                                <SaveTrend v-if="!$auth.loading & $auth.isAuthenticated" v-on:saved="getConfigs()"/>
                                <v-btn rounded depressed @click="reset">
                                    Reset </v-btn>
                                <HelpTrends />
                            </v-list-item>
                        </v-list>
                    </v-card>
                </v-flex>
                <v-spacer />
                <v-flex align-center xs12 md8>
                    <template>
                        <div>
                            <apexchart type="line" :options="options" :series="trends"></apexchart>
                        </div>
                    </template>
                </v-flex>
                <Popup v-model="popup" />
                <Replace v-model="replace" />
                <v-col />
            </v-layout>
        </v-container>
    </template>

</div>
</template>

<script>
import Popup from "../components/common/Popup";
import Replace from "../components/common/Replace";
import SaveTrend from "../components/common/SaveTrend";
import HelpTrends from "../components/common/HelpTrends";
import Search from "../components/common/Search"
import {
    mapGetters,
    mapState,
    mapMutations
} from 'vuex';
import ALL_TOPICS_WITH_FILTER from '../graphql/TopicsAndArticleCount.gql'
import TOPIC_ARTICLES_DATE from '../graphql/TopicArticlesByDate.gql'
import USER_CONFIGS from "../graphql/AllOfAUsersConfigurations.gql"
export default {
    name: "Trends",
    components: {
        Popup,
        SaveTrend,
        HelpTrends,
        Search,
        Replace
    },
    data: () => ({
        search: false,
        popup: false,
        start_date: null,
        end_date: null,
        dates: [],
        keyword: '',
        menu: false,
        related_topics: [],
        configs: [],
        result: null,
        trends: [],
        date: null,
        topic_id: null,
        usr_id: '',
        skipQuery: true,
        replace: false,
        options: {
            stroke: {
                curve: 'smooth',
            },
            colors: [
                '#FF42DC', '#0096DB', '#FF9D00', '#66DB00', '#DB0004', 
            ],
            xaxis: {
                type: 'datetime'
            },
            yaxis: {
                label: {
                    text: 'Number of Articles'
                },
                min: 0,
                forceNiceScale: true
            },
            tooltip: {
                enabled: true,
                followCursor: true,
                shared: true,
            },
            markers: {
                size: 0,
                hover: {
                    sizeOffset: 6
                }
            },
            grid: {
                borderColor: '#f1f1f1',
            },
            legend: {
                horizontalAlign: 'center',
                position: 'bottom',
                onItemHover: {
                    highlightDataSeries: true
                },
            },
            noData: {
                text: 'Select topics to see how they trend over time!',
                align: 'center',
                verticalAlign: 'middle',
                offsetX: 0,
                offsetY: 0,
                style: {
                    color: undefined,
                    fontSize: '14px',
                    fontFamily: undefined
                }
            },
            chart: {
                selection: {
                    enabled: true
                },
                toolbar: {
                    show: true,
                    offsetX: 0,
                    offsetY: 0,
                    tools: {
                        download: true,
                        selection: false,
                        zoom: false,
                        zoomin: true,
                        zoomout: true,
                        pan: true,
                        reset: true,
                        customIcons: []
                    },
                    export: {
                        csv: {
                            filename: undefined,
                            columnDelimiter: ',',
                            headerCategory: 'category',
                            headerValue: 'value',
                            dateFormatter(timestamp) {
                                return new Date(timestamp).toDateString()
                            }
                        }
                    },
                    autoSelected: 'zoom'
                },
            },
        },
    }),
    watch: {
        getSelected: {
            handler: function() {
                this.callTrends()
                if (this.getSelected.length == 0) {
                    this.trends = []
                }
            },
        },
    },
    apollo: {
        related_topics: {
            query: ALL_TOPICS_WITH_FILTER,
            variables() {
                return {
                    limit: 5
                }
            },
            update(data) {
                return data.allTopics.nodes.map(a => ({
                    id: a.id,
                    name: a.name
                }));
            }
        },
        result: {
            query: TOPIC_ARTICLES_DATE,
            variables() {
                return {
                    topicId: this.topic_id,
                    startdate: this.start_date,
                    enddate: this.end_date
                }
            },
            update(data) {
                var result = {
                    name: data.topicById.name, 
                    data: data.aggregatearticlecountbydays.nodes.map(a => ({
                        x: a.x,
                        y: a.y
                    }))}
                let index = this.trends.findIndex(item => item.name == result.name)
                if (index == -1 ) {
                    this.trends.push(result)
                } else {
                    this.trends[index] = result
                }
                this.checkRemove()
            },
            skip() {
                return this.skipQuery
            },
        },
        configs: {
            query: USER_CONFIGS,
            variables() {
                var id
                if (!this.$auth.loading && this.$auth.isAuthenticated) {
                    id = this.$auth.user.sub
                } else {
                    id = ''
                }
                return {
                    usrId: id
                }
            },
            update(data) {
                return data.allUserconfigurations.nodes.map(a => ({
                    id: a.id,
                    title: a.configName,
                    topics: a.topicconfigurationsByUsrConfigId.nodes.map(b => ({
                        id: b.topicId,
                        name: b.topicName
                    }))
                }))
            },
            skip() {
                return this.skipQuery
            },
        }
    },
    methods: {
        checkRemove() {
            if (this.getSelected.length != this.trends.length){
                var i
                for (i = 0; i < this.trends.length; i++) {
                    let index = this.getSelected.findIndex(item => item.name == this.trends[i].name)
                    if (index == -1) {
                        this.trends.splice(index, 1)
                    }
                }
            }
        },
        async callTrends() {
            console.log("Fetching trend data for", this.dateRange)
            var i
            for (i = 0; i < this.getSelected.length; i++) {
                this.topic_id =  this.getSelected[i].id
                this.$apollo.queries.result.skip = false
                await this.$apollo.queries.result.refetch()
            }
            // This line is not redundant. It refreshes the value, particularly useful for automatically updating the graph when dates are changed.
            this.trends = this.trends.map(a => a)
            console.log('Trend data fetched.')
        },
        formatDate(date) {
            let month = `${date.getMonth() + 1}`;
            let day = `${date.getDate()}`;
            const year = date.getFullYear();
            if (month.length < 2) month = `0${month}`;
            if (day.length < 2) day = `0${day}`;
            return [year, month, day].join('-');
        },
        ...mapMutations([
            'addSelected',
            'removeSelected',
            'openTopic',
            'setSelected',
            'emptySelected',
            'searchTopicKeyword'
        ]),
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
            this.callTrends()
        },
        searchTopic() {
            if (this.keyword != '') {
                this.search = true
                this.searchTopicKeyword(this.keyword)
            }
        },
        reset() {
            this.dates = []
            this.end_date = new Date()
            this.start_date = new Date()
            this.start_date.setMonth(this.end_date.getMonth() - 1)
            this.start_date = this.start_date.toISOString().slice(0, 10)                    
            this.end_date = this.end_date.toISOString().slice(0, 10)
            this.dates = [this.start_date, this.end_date]
            this.emptySelected()
        },
        add(topic) {
            if (this.numSelected == 5) {
                this.replace = true
            } else {
                this.addSelected(topic)
            }
        },
        async getConfigs() {
            this.$apollo.queries.configs.skip = false
            await this.$apollo.queries.configs.refetch()
            console.log("Configurations fetched.")
        },
    },
    mounted: function() {
        if (this.start_date == null) {
            this.end_date = new Date()
            this.start_date = new Date()
            this.start_date.setMonth(this.end_date.getMonth() - 1)
            this.start_date = this.start_date.toISOString().slice(0, 10)                    
            this.end_date = this.end_date.toISOString().slice(0, 10)
        }
        this.dates = [this.start_date, this.end_date]
        if (!this.$auth.loading && this.$auth.isAuthenticated) {
            this.usr_id = this.$auth.user.sub
        }
        this.callTrends()
        this.getConfigs()
        console.log("Mounted")
    },
    computed: {
        ...mapState(['selected', 'related']),
        ...mapGetters(['numSelected', 'getSelected', 'getRelated']),
        todaysDate() {
            const today = new Date();
            return this.formatDate(today);
        },
        dateRange() {
            return this.dates.join(' to ')
        },
    }
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
    background: [];
}
.item:hover {
    background: ghostwhite;
}
</style>